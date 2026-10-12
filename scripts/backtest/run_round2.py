"""Round 2: (a) short-term pullback / mean-reversion system, (b) stress test of momentum rotation.

Usage: python run_round2.py PRICE_CACHE SEC_CACHE OUT_DIR EXTRA_PRICE_DIR SP500_START_END_CSV
Main universe = point-in-time S&P 500 members (fairer). The broad (today's $2B+) universe is shown for
reference only, because it is survivorship-biased.
"""
import datetime as dt, gzip, json, os, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S
from fetch_prices import WATCH
from run_systems import load_members, is_member, tstats, yearly

FULL, IS, OOS = ("2017-10-15", "2026-12-31"), ("2017-10-15", "2021-12-31"), ("2022-01-01", "2026-12-31")
EX26, OOS_EX26, Y26 = ("2017-10-15", "2025-12-31"), ("2022-01-01", "2025-12-31"), ("2026-01-01", "2026-12-31")
PER = {"full": FULL, "2017-21": IS, "2022-26": OOS, "2017-25 (no 2026)": EX26, "2022-25": OOS_EX26, "2026 so far": Y26}
MC = 10
MR_X = dict(S.DEFAULT_EXIT, partial_R=0, time_days=0, runner="none", bounce="sma5", max_days=10, max_risk=0.6)

MR_RUNS = [  # (label, entry params, exit overrides, portfolio overrides)
    ("base: above 200-day, RSI(2) < 10; buy next open; sell on close > 5-day avg (max 10 days); 10% disaster stop; 10 slots x 10%", {}, {}, {}),
    ("deeper dip: RSI(2) < 5", dict(rsi_max=5), {}, {}),
    ("dip + 2 or more down days", dict(min_down_days=2), {}, {}),
    ("exit when RSI(2) > 70", {}, dict(bounce="rsi70"), {}),
    ("exit on first up close", {}, dict(bounce="first_up"), {}),
    ("max hold 5 days", {}, dict(max_days=5), {}),
    ("only when SPY is above its 200-day", dict(spy_filter=True), {}, {}),
    ("no disaster stop", dict(disaster_stop=0.5), {}, dict(risk=0.05)),
    ("20 slots x 5%", {}, {}, dict(max_pos=20, risk=0.005, sector_cap=4)),
    ("buy at the signal-day close (market-on-close order)", {}, dict(entry="close"), {}),
    ("buy with a limit 2% under the signal close (next day only)", {}, dict(entry="limit", limit_pct=0.02), {}),
    ("buy at close + rank by RS instead of deepest dip", dict(rank="rs"), dict(entry="close"), {}),
    ("buy at close + lower trading cost (0.05% a side)", {}, dict(entry="close"), dict(cost=0.0005)),
    ("buy at close + RSI(2) < 5 + low cost", dict(rsi_max=5), dict(entry="close"), dict(cost=0.0005)),
]

MOM_RUNS = [  # (label, kwargs)
    ("base: top 10 by 12-1 month return, above 200-day, monthly", {}),
    ("top 5", dict(top=5)),
    ("top 20", dict(top=20)),
    ("6-month momentum (6-1)", dict(lookback=126)),
    ("3-month momentum, no skip", dict(lookback=63, skip=0)),
    ("12-month, no skip", dict(skip=0)),
    ("weight by low volatility", dict(weighting="invvol")),
    ("cash when SPY < 200-day (checked monthly)", dict(regime=True)),
    ("cash when SPY < 200-day (checked daily)", dict(regime_daily=True)),
    ("no 200-day filter on the stocks", dict(trend_filter=False)),
    ("max 3 per sector", dict(sector_cap=3)),
] + [(f"rebalance on trading day {k + 1} of the month", dict(offset=k)) for k in range(1, 5)]


def slice_stats(eq, a, b):
    x = eq[(eq.index >= a) & (eq.index <= b)]
    return E.stats_equity(x) if len(x) > 20 else {}


def rolling_beat(eq, bench, months=36):
    """Share of 3-year windows (monthly steps) where the strategy beat the benchmark."""
    m = eq.groupby(eq.index.str[:7]).last(); bm = bench.groupby(bench.index.str[:7]).last()
    m, bm = m.align(bm, join="inner")
    w = [(m.iloc[i + months] / m.iloc[i]) > (bm.iloc[i + months] / bm.iloc[i]) for i in range(len(m) - months)]
    return round(100 * float(np.mean(w)), 0) if w else None


def main(pc, sc, out, extra, members_csv):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    prices = E.load_prices(pc); uni = json.load(open(os.path.join(pc, "universe.json")))
    for k, v in E.load_prices(extra).items():
        prices.setdefault(k, v)
    members = load_members(members_csv)
    spy, qqq, rsp = prices.pop("SPY"), prices.pop("QQQ"), prices.pop("RSP")
    for k in [k for k in prices if k not in uni["meta"] and k not in WATCH and k not in members]:
        prices.pop(k)
    mkt = E.market_status(spy, qqq); cal = list(spy.date)
    rk = E.rs_rank(prices, cal)
    F = {}
    for s in sorted(prices):
        ind = E.indicators(prices[s]); ind["rsrank"] = rk[s].reindex(prices[s].date).to_numpy()
        F[s] = S.features(s, prices[s], ind, E.load_sec(sc, s), None, mkt, uni["meta"].get(s))
    del rk
    closes = {s: dict(zip(prices[s].date, prices[s].c)) for s in prices}
    spy_c = spy.set_index("date").c; rsp_c = rsp.set_index("date").c
    print(f"features {len(F)} stocks {time.time()-t0:.0f}s", flush=True)
    res = {"asOf": dt.date.today().isoformat(), "benchmarks": {}, "mean_reversion": [], "momentum": []}
    for pn, (a, b) in PER.items():
        res["benchmarks"][pn] = {"SPY": slice_stats(spy_c, a, b), "RSP (equal-weight S&P)": slice_stats(rsp_c, a, b)}
    res["spy_yearly"] = yearly(spy_c[spy_c.index >= FULL[0]]); res["rsp_yearly"] = yearly(rsp_c[rsp_c.index >= FULL[0]])

    # ── (a) mean reversion
    for uname, mem in (("sp500", members), ("broad", None)):
        syms = [s for s in F if (mem is None and (s in uni["meta"] or s in WATCH)) or (mem is not None and s in mem)]
        runs = MR_RUNS if uname == "sp500" else MR_RUNS[:1]
        for label, ep, xo, po in runs:
            X = dict(MR_X); X.update(xo)
            tr = []
            for s in syms:
                ent = [e for e in S.mean_reversion(F[s], ep) if mem is None or is_member(mem, s, F[s]["dates"][e[0]])]
                tr += S.simulate(s, F[s], ent, X, *FULL)
            po2 = dict(max_pos=10, sector_cap=3); po2.update(po)
            eq, taken = S.portfolio(tr, closes, cal, *FULL, **po2)
            mc = [S.portfolio(tr, closes, cal, *FULL, seed=k, **po2)[0] for k in range(MC)]
            r = {"universe": uname, "label": label, "periods": {}, "yearly": yearly(eq)}
            for pn, (a, b) in PER.items():
                t = [x for x in tr if a <= x["entry_date"] <= b]
                rets = np.array([x["ret"] for x in t]) if t else np.array([0.0])
                cg = [slice_stats(m, a, b).get("cagr_%", 0) for m in mc]; dd = [slice_stats(m, a, b).get("max_dd_%", 0) for m in mc]
                r["periods"][pn] = {"trades": len(t), "win_%": round(float((rets > 0).mean() * 100), 1),
                                    "avg_ret_%": round(float(rets.mean()), 2),
                                    "avg_win_%": round(float(rets[rets > 0].mean()), 2) if (rets > 0).any() else 0,
                                    "avg_loss_%": round(float(rets[rets <= 0].mean()), 2) if (rets <= 0).any() else 0,
                                    "avg_days": round(float(np.mean([x["days"] for x in t])), 1) if t else 0,
                                    "mc_cagr": [round(float(np.median(cg)), 1), round(min(cg), 1), round(max(cg), 1)],
                                    "mc_dd_median": round(float(np.median(dd)), 1)}
            res["mean_reversion"].append(r)
            f_ = r["periods"]["full"]
            print(f"MR {uname} | {label[:40]} | n={f_['trades']} win={f_['win_%']} avg={f_['avg_ret_%']}% | CAGR {f_['mc_cagr']} dd {f_['mc_dd_median']} ({time.time()-t0:.0f}s)", flush=True)
            if label.startswith("base") and uname == "sp500":
                pd.DataFrame([{k: x[k] for k in x if k != "fills"} for x in tr]).to_csv(os.path.join(out, f"trades-sp500-mean_reversion-{res['asOf']}.csv.gz"), index=False)

    # ── (b) momentum stress test (S&P 500 point-in-time only)
    syms = [s for s in F if s in members]
    sub = {s: prices[s] for s in syms}
    sector = {s: uni["meta"].get(s, {}).get("sector") for s in syms}
    mem_fn = lambda s, d: is_member(members, s, d)
    for label, kw in MOM_RUNS:
        eq, st, log = S.momentum_rotation(sub, cal, *FULL, spy=spy, member=mem_fn, sector=sector, return_holdings=True, **kw)
        r = {"label": label, "periods": {pn: slice_stats(eq, a, b) for pn, (a, b) in PER.items()}, "yearly": yearly(eq),
             "holdings": st, "beat_spy_3y_windows_%": rolling_beat(eq, spy_c), "beat_rsp_3y_windows_%": rolling_beat(eq, rsp_c)}
        if label.startswith("base"):
            r["recent_picks"] = [(d, p) for d, p in log[-6:]]
        res["momentum"].append(r)
        print(f"MOM | {label[:45]} | full {r['periods']['full'].get('cagr_%')} dd {r['periods']['full'].get('max_dd_%')} | "
              f"ex2026 {r['periods']['2017-25 (no 2026)'].get('cagr_%')} | beatSPY3y {r['beat_spy_3y_windows_%']}% ({time.time()-t0:.0f}s)", flush=True)
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(os.path.join(out, f"round2-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:6])
