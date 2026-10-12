"""Round 1 of candidate growth systems vs SPY.

Usage: python run_systems.py PRICE_CACHE SEC_CACHE OUT_DIR [EXTRA_PRICE_DIR SP500_START_END_CSV]
Runs every system on two universes:
  * broad  = US stocks >= $2B market cap TODAY (survivorship-biased: today's winners are in it)
  * sp500  = stocks only while they were actually in the S&P 500 (point-in-time membership,
             github.com/fja05680/sp500). Members that were later bought out or delisted have no free
             price history, so ~19% of past members are still missing — less biased, not bias-free.
"""
import datetime as dt, gzip, json, os, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S
from fetch_prices import WATCH

FULL, IS, OOS = ("2017-10-15", "2026-12-31"), ("2017-10-15", "2021-12-31"), ("2022-01-01", "2026-12-31")
PER = {"full": FULL, "in-sample 2017-21": IS, "out-of-sample 2022-26": OOS}
MC = 10

RUNS = [  # (system, label, entry params, exit overrides, portfolio overrides)
    ("leader_breakout", "base: RS85, EPS25+sales20, tight 10-day range, 1.5x vol; 1/3 at +2R, rest on 50-day", {}, {}, {}),
    ("leader_breakout", "no partial (all on 50-day exit)", {}, dict(partial_R=0), {}),
    ("leader_breakout", "sell 1/2 at +2R", {}, dict(partial_frac=0.5), {}),
    ("leader_breakout", "partial at +3R", {}, dict(partial_R=3.0), {}),
    ("leader_breakout", "no time stop", {}, dict(time_days=0), {}),
    ("leader_breakout", "stop to breakeven after partial", {}, dict(be_after_partial=True), {}),
    ("leader_breakout", "runner on 21-day EMA", {}, dict(runner="ema21"), {}),
    ("leader_breakout", "runner on 3x ATR trail", {}, dict(runner="atr"), {}),
    ("leader_breakout", "needs EPS acceleration", dict(need_accel=True), {}, {}),
    ("leader_breakout", "RS >= 70", dict(min_rs=70), {}, {}),
    ("leader_breakout", "EPS only (no sales filter)", dict(rev_min=-999), {}, {}),
    ("leader_breakout", "looser base (10-day range <= 20%)", dict(max_range10=20), {}, {}),
    ("leader_breakout", "no market gate", dict(mkt_gate=False), {}, {}),
    ("leader_breakout", "5 positions max", {}, {}, dict(max_pos=5)),
    ("earnings_gap", "base: gap 4%+, up 5%+, 3x vol, upper half, above 200-day; stop gap low; 1/3 at +2R, rest on 21-day EMA", {}, dict(runner="ema21"), {}),
    ("earnings_gap", "runner on 50-day", {}, dict(runner="sma50"), {}),
    ("earnings_gap", "no partial", {}, dict(runner="ema21", partial_R=0), {}),
    ("earnings_gap", "no time stop", {}, dict(runner="ema21", time_days=0), {}),
    ("earnings_gap", "RS >= 70", dict(min_rs=70), dict(runner="ema21"), {}),
    ("earnings_gap", "volume 2x", dict(vol_need=2), dict(runner="ema21"), {}),
    ("earnings_gap", "no 200-day filter", dict(need_trend=False), dict(runner="ema21"), {}),
    ("leader_pullback", "base: RS90, EPS25, tag 21-EMA on light volume, close > prior high; stop pullback low; 1/3 at +2R, rest on 21-EMA", {}, dict(runner="ema21"), {}),
    ("leader_pullback", "runner on 50-day", {}, dict(runner="sma50"), {}),
    ("leader_pullback", "no partial", {}, dict(runner="ema21", partial_R=0), {}),
    ("leader_pullback", "RS >= 80", dict(min_rs=80), dict(runner="ema21"), {}),
    ("leader_pullback", "no EPS filter", dict(need_eps=False), dict(runner="ema21"), {}),
    ("combined", "base: breakout + earnings gap + pullback in one 8-slot portfolio; all exits on the 50-day", {},
     dict(runner="sma50", partial_R=0, time_days=0), {}),
    ("combined", "12 slots", {}, dict(runner="sma50", partial_R=0, time_days=0), dict(max_pos=12)),
]


def yearly(eq):
    y = eq.groupby(eq.index.str[:4]).last()
    return {k: round(float(v) * 100, 1) for k, v in (y / y.shift(1, fill_value=eq.iloc[0]) - 1).items()}


def tstats(tr):
    if not tr:
        return {"trades": 0}
    R = np.array([t["R"] for t in tr]); w = R > 0
    return {"trades": len(tr), "win_%": round(w.mean() * 100, 1), "avg_R": round(R.mean(), 2),
            "avg_win_R": round(R[w].mean(), 2) if w.any() else 0, "avg_loss_R": round(R[~w].mean(), 2) if (~w).any() else 0,
            "profit_factor": round(R[w].sum() / -R[~w].sum(), 2) if (~w).any() and R[~w].sum() < 0 else None,
            "avg_days": round(np.mean([t["days"] for t in tr]), 1), "big_3R_%": round((R >= 3).mean() * 100, 1)}


def load_members(path):
    import csv
    m = {}
    for r in csv.DictReader(open(path)):
        m.setdefault(r["ticker"].replace(".", "-"), []).append((r["start_date"], r["end_date"] or "9999"))
    if "META" in m and "FB" in m:
        m["META"] += m["FB"]
    # Reviewed ticker renames (ticker_aliases.csv): membership under the old ticker is credited to today's ticker,
    # whose price history covers the old period. Rejected look-alikes are documented in ticker_map.py output.
    ap = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticker_aliases.csv")
    if os.path.exists(ap):
        for r in csv.DictReader(open(ap)):
            if r["old"] in m:
                m.setdefault(r["new"], []).extend(m.pop(r["old"]))
    return m


def is_member(m, sym, d):
    return any(a <= d <= b for a, b in m.get(sym, []))


def main(pc, sc, out, extra=None, members_csv=None):
    t0 = time.time()
    prices = E.load_prices(pc); uni = json.load(open(os.path.join(pc, "universe.json")))
    members = load_members(members_csv) if members_csv else None
    if extra:
        for k, v in E.load_prices(extra).items():
            prices.setdefault(k, v)
    spy, qqq = prices.pop("SPY"), prices.pop("QQQ"); prices.pop("RSP", None)
    for k in [k for k in prices if k not in uni["meta"] and k not in WATCH and not (members and k in members)]:
        prices.pop(k)
    mkt = E.market_status(spy, qqq); cal = list(spy.date)
    rk = E.rs_rank(prices, cal)
    F = {}
    for s in sorted(prices):
        ind = E.indicators(prices[s]); ind["rsrank"] = rk[s].reindex(prices[s].date).to_numpy()
        p = os.path.join(sc, f"{s}.json.gz")
        rec = json.load(gzip.open(p, "rt")) if os.path.exists(p) else None
        sec = E.load_sec(sc, s)
        F[s] = S.features(s, prices[s], ind, sec, rec, mkt, uni["meta"].get(s))
    del rk
    closes = {s: dict(zip(prices[s].date, prices[s].c)) for s in prices}
    print(f"features for {len(F)} stocks in {time.time()-t0:.0f}s", flush=True)
    res = {"asOf": dt.date.today().isoformat(), "stocks": len(F), "runs": [],
           "benchmarks": {k: dict(zip(["SPY buy-and-hold", "SPY 200-day rule"], E.spy_benchmarks(spy, *v))) for k, v in PER.items()},
           "spy_yearly": yearly(spy.set_index("date").c[lambda x: x.index >= FULL[0]])}
    all_trades = {}
    universes = [("broad", None)] + ([("sp500", members)] if members else [])
    for uname, mem in universes:
        keep = (lambda s_, d_: True) if mem is None else (lambda s_, d_, m_=mem: is_member(m_, s_, d_))
        syms = [s_ for s_ in F if mem is None and s_ in uni["meta"] or mem is None and s_ in WATCH or mem is not None and s_ in mem]
        for sysname, label, ep, xo, po in RUNS:
            X = dict(S.DEFAULT_EXIT); X.update(xo)
            trades = []
            for s_ in syms:
                ent = [e for e in S.SYSTEMS[sysname](F[s_], ep) if keep(s_, F[s_]["dates"][e[0]])]
                trades += S.simulate(s_, F[s_], ent, X, *FULL)
            r = {"universe": uname, "system": sysname, "label": label, "periods": {}}
            for pn, (a, b) in PER.items():
                tr = [t for t in trades if a <= t["entry_date"] <= b]
                eq, taken = S.portfolio(tr, closes, cal, a, b, **po)
                mc = [E.stats_equity(S.portfolio(tr, closes, cal, a, b, seed=k, **po)[0]) for k in range(MC)]
                cg = [m.get("cagr_%", 0) for m in mc]; dd = [m.get("max_dd_%", 0) for m in mc]
                r["periods"][pn] = {"signals": tstats(tr), "portfolio": E.stats_equity(eq), "portfolio_trades": tstats(taken),
                                    "mc_cagr": [round(float(np.median(cg)), 1), round(min(cg), 1), round(max(cg), 1)],
                                    "mc_dd_median": round(float(np.median(dd)), 1)}
                if pn == "full":
                    r["periods"][pn]["yearly"] = yearly(eq)
            res["runs"].append(r)
            if label.startswith("base"):
                all_trades[f"{uname}-{sysname}"] = trades
            f_ = r["periods"]["full"]["signals"]; o_ = r["periods"]["out-of-sample 2022-26"]
            print(f"{uname} | {sysname} | {label[:38]} | n={f_.get('trades')} win={f_.get('win_%')} avgR={f_.get('avg_R')} | "
                  f"MC {r['periods']['full']['mc_cagr']} dd {r['periods']['full']['mc_dd_median']} | OOS avgR {o_['signals'].get('avg_R')} MC {o_['mc_cagr']} ({time.time()-t0:.0f}s)", flush=True)
        for lab, kw in [("momentum top 10", {}), ("momentum top 10 + SPY 200-day regime", dict(regime=True)), ("momentum top 20", dict(top=20))]:
            r = {"universe": uname, "system": "momentum_rotation", "label": lab, "periods": {}}
            sub = {s_: prices[s_] for s_ in syms}
            for pn, (a, b) in PER.items():
                eq, st = S.momentum_rotation(sub, cal, a, b, spy=spy, member=None if mem is None else (lambda s_, d_, m_=mem: is_member(m_, s_, d_)), **kw)
                r["periods"][pn] = {"portfolio": E.stats_equity(eq), "holdings": st}
                if pn == "full":
                    r["periods"][pn]["yearly"] = yearly(eq)
            res["runs"].append(r)
            print(uname, lab, r["periods"]["full"]["portfolio"], "| OOS", r["periods"]["out-of-sample 2022-26"]["portfolio"], flush=True)
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(os.path.join(out, f"systems-{res['asOf']}.json"), "w"), indent=1, default=str)
    for k, tr in all_trades.items():
        pd.DataFrame([{x: t[x] for x in t if x != "fills"} for t in tr]).to_csv(os.path.join(out, f"trades-{k}-{res['asOf']}.csv.gz"), index=False)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:6])
