"""Round 4 · fix the weaknesses: better SELLING, v3 leadership gates, regime sizing — judged on unseen years.

Usage: python run_round4.py PRICE_DIR SEC_DIR OUT_DIR MEMBERS_CSV [EXTRA_PRICE_DIR] [AUDIT_DIR]

Universe and execution follow Round 3 (backtest/round3-latest.md):
  * S&P 500 members ON THE DATE (point in time), $5+, $20M+/day, 1 year of history
  * signals at the close, filled at the next open; gaps through a stop fill at the open; 0.07% cost per side
  * a stock with NO SEC file (usually a company that later failed or was bought) is judged on its price rules
    instead of being parked as CHECK_FIRST — otherwise delisted companies could never be bought (nosec_pass)
Periods (chosen from the data, never by result):
  * long data (EODHD, starts <= 2004): TUNE 2005-2016 · JUDGE 2017-2025 · 2026 shown alone
  * free data (Yahoo, ~2016+):          TUNE 2017-2021 · JUDGE 2022-2025 · 2026 shown alone
Pass bar (Playbook §4): higher average result per trade AFTER costs than the live rules in BOTH periods,
drawdown no worse (2-point tolerance), and the change must make sense. Beating SPY is not required.
"""
import datetime as dt, json, os, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S
from run_systems import load_members, is_member

COST = 0.0007
MC = 10
EXITS = dict(exit_ma50vol=True, exit_climax=True, exit_failbo=True, hold8w=True)
VARIANTS = [
    ("base: live rules (v2.9.7 entries, stop A2)", {}, False),
    # ── selling (weakness #5) — same entries, different exits
    ("exit: original stop only (no trail)", dict(stop="fixed"), False),
    ("exit: close 2% under 50-day", dict(stop="ma50"), False),
    ("exit: 50-day break on volume", dict(exit_ma50vol=True), False),
    ("exit: sell into a climax run", dict(exit_climax=True), False),
    ("exit: cut failed breakouts (-2% within 20 days)", dict(exit_failbo=True), False),
    ("exit: O'Neil 8-week hold after +20% in 3 weeks", dict(hold8w=True), False),
    ("exit: full sell playbook (all four)", dict(EXITS), False),
    ("exit: sell playbook + no trail", dict(EXITS, stop="fixed"), False),
    # ── buying (weaknesses #3, #8)
    ("entry: breakouts only", dict(breakout_only=True), False),
    ("entry: pullback needs a RISING 50-day (#31)", dict(pb_lo=0.0, pb_need_rising=True), False),
    ("entry: leaders only (RS top 20% + within 15% of high)", dict(min_rsrank=80, near_high=15), False),
    ("entry: Minervini trend template", dict(trend_template=True), False),
    ("entry: EPS >= 25% AND sales >= 15%", dict(rev_min=15.0), False),
    # ── market (weakness #4)
    ("market: block new buys in PRESSURE", dict(block_pressure=True), False),
    ("market: v3 regime sizing (full / half / none)", {}, True),
    # ── v3 candidate = the layers together
    ("v3 candidate: leaders + EPS&sales + sell playbook + regime", dict(EXITS, min_rsrank=80, near_high=15, rev_min=15.0), True),
    ("v3 candidate, breakouts only", dict(EXITS, min_rsrank=80, near_high=15, rev_min=15.0, breakout_only=True), True),
]
ENTRY_KEYS = ("vol_need", "pb_lo", "pb_hi", "pb_need_rising", "pb_need_low_vol", "block_pressure", "need_rs", "eps_min", "rev_min",
              "earn_days", "breakout_only", "pullback_only", "max_ext", "min_rsrank", "trend_template", "mkt_mode", "near_high", "nosec_pass")


def tstats(tr, cost):
    if not tr:
        return {"trades": 0}
    R = np.array([t["R"] - 2 * cost * t["entry"] / (t["entry"] - t["stop"]) for t in tr])   # R after costs
    r = np.array([t["ret"] for t in tr]) - 200 * cost
    w = r > 0
    gb = [t["mfe_R"] - t["R"] for t in tr if t["mfe_R"] >= 1]                                  # gave back, on trades that reached +1R
    return {"trades": len(tr), "win_%": round(float(w.mean()) * 100, 1), "avg_R_net": round(float(R.mean()), 3),
            "avg_ret_net_%": round(float(r.mean()), 2), "avg_win_%": round(float(r[w].mean()), 1) if w.any() else 0,
            "avg_loss_%": round(float(r[~w].mean()), 1) if (~w).any() else 0,
            "profit_factor": round(float(r[w].sum() / -r[~w].sum()), 2) if (~w).any() and r[~w].sum() < 0 else None,
            "avg_days": round(float(np.mean([t["days"] for t in tr])), 1), "big_3R_%": round(float((R >= 3).mean()) * 100, 1),
            "gave_back_R_after_+1R": round(float(np.mean(gb)), 2) if gb else None}


def main(pc, sc, out, members_csv, extra=None, audit_dir=None):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    prices = E.load_prices(pc)
    if extra and os.path.isdir(extra):
        for k, v in E.load_prices(extra).items():
            prices.setdefault(k, v)
    if audit_dir:
        prices = E.apply_corrections(prices, os.path.join(audit_dir, "corrections.json"))
    members = load_members(members_csv)
    spy, qqq = prices.pop("SPY"), prices.pop("QQQ"); prices.pop("RSP", None)
    long_data = spy.date.iat[0] <= "2004-06-30"
    TUNE, JUDGE = (("2005-01-01", "2016-12-31"), ("2017-01-01", "2025-12-31")) if long_data else \
                  (("2017-10-15", "2021-12-31"), ("2022-01-01", "2025-12-31"))
    Y26 = ("2026-01-01", "2026-12-31")
    PER = {"tune": TUNE, "judge": JUDGE, "2026": Y26}
    prices = {k: v for k, v in prices.items() if k in members}
    cal = list(spy.date); spy_c = spy.set_index("date").c
    mem_fn = lambda s, d: is_member(members, s, d)
    el = E.eligibility(prices, cal, member=mem_fn)
    rk = E.rs_rank(prices, cal, eligible=el)
    elig = {s: dict(zip(cal, el[s].to_numpy())) for s in el.columns}
    mkt = E.market_status(spy, qqq)
    live, s200 = mkt["live"], mkt["spy200"]
    regime = lambda d: 0.0 if s200.get(d) == "CORRECTION" else (1.0 if live.get(d) == "UPTREND" else 0.5)
    spy_close = dict(zip(spy.date, spy.c))
    IND, SEC = {}, {}
    for s in sorted(prices):
        IND[s] = E.indicators(prices[s]); IND[s]["rsrank"] = rk[s].reindex(prices[s].date).to_numpy()
        SEC[s] = E.load_sec(sc, s)
    del rk
    closes = {s: prices[s].set_index("date").c for s in prices}
    have_sec = sum(1 for s in prices if SEC[s] and SEC[s]["eps"])
    print(f"{len(prices)} S&P members with prices ({have_sec} with SEC EPS) · data from {spy.date.iat[0]} · "
          f"{'LONG' if long_data else 'FREE'} mode · {time.time()-t0:.0f}s", flush=True)
    res = {"asOf": dt.date.today().isoformat(), "mode": "long (EODHD)" if long_data else "free (Yahoo, survivorship-limited)",
           "periods": PER, "cost_per_side": COST, "stocks": len(prices), "with_sec": have_sec,
           "spy": {k: S.perf_metrics(spy_c[(spy_c.index >= a) & (spy_c.index <= b)]) for k, (a, b) in PER.items()},
           "regime_days_%": {}, "variants": []}
    days = [d for d in cal if JUDGE[0] <= d <= JUDGE[1]]
    res["regime_days_%"] = {k: round(100 * sum(1 for d in days if regime(d) == v) / max(len(days), 1), 1)
                            for k, v in (("full", 1.0), ("half", 0.5), ("none", 0.0))}
    sig_cache = {}
    for vi, (label, change, use_regime) in enumerate(VARIANTS):
        P = dict(E.BASE); P.update(nosec_pass=True); P.update(change)
        key = tuple(P[k] for k in ENTRY_KEYS)
        if key not in sig_cache:
            sig_cache.clear()                                   # keep memory flat: one signal set at a time
            sig_cache[key] = {s: E.evaluate(s, prices[s], IND[s], SEC[s], mkt, spy_close, P) for s in prices}
        sigs = sig_cache[key]
        trades = []
        for s in prices:
            for t in E.simulate_trades(s, prices[s], IND[s], sigs[s], P, TUNE[0], Y26[1]):
                if elig.get(s, {}).get(t["signal"], False):
                    trades.append(t)
        rf = regime if use_regime else None
        r = {"label": label, "change": {k: v for k, v in change.items()}, "regime_sizing": use_regime, "periods": {}}
        for pn, (a, b) in PER.items():
            tr = [t for t in trades if a <= t["entry_date"] <= b]
            eq, taken = E.portfolio(tr, closes, cal, a, b, cost=COST, risk_fn=rf)
            mcs = [S.perf_metrics(E.portfolio(tr, closes, cal, a, b, cost=COST, seed=k, risk_fn=rf)[0], spy_c) for k in range(MC)]
            cg = [m.get("cagr_%", 0) for m in mcs]
            r["periods"][pn] = {"signals": tstats(tr, COST), "portfolio": S.perf_metrics(eq, spy_c), "taken": tstats(taken, COST),
                                "mc_cagr": {"median": round(float(np.median(cg)), 1), "low": min(cg), "high": max(cg)},
                                "exit_reasons": pd.Series([t["why"] for t in tr]).value_counts().to_dict() if tr else {}}
            if pn == "judge":
                r["periods"][pn]["bootstrap_vs_spy"] = S.block_bootstrap_excess(eq, spy_c, a, b)
        res["variants"].append(r)
        j = r["periods"]["judge"]
        print(f"[{vi+1}/{len(VARIANTS)}] {label[:55]:55} | judge avgR {j['signals'].get('avg_R_net')} · CAGR {j['portfolio'].get('cagr_%')} "
              f"(MC {j['mc_cagr']['median']}) · DD {j['portfolio'].get('max_dd_%')} ({time.time()-t0:.0f}s)", flush=True)
        json.dump(res, open(os.path.join(out, "round4-partial.json"), "w"), indent=1, default=str)
    # pass bar vs the live rules
    base = res["variants"][0]["periods"]
    for r in res["variants"][1:]:
        p = r["periods"]
        if r["regime_sizing"] and r["change"] == {}:
            # sizing changes HOW MUCH is bet, not which trades — judge it on risk-adjusted portfolio results instead
            better = all((p[k]["portfolio"].get("sharpe") or -9) > (base[k]["portfolio"].get("sharpe") or -9) for k in ("tune", "judge"))
        else:
            better = all((p[k]["signals"].get("avg_R_net") or -9) > (base[k]["signals"].get("avg_R_net") or -9) for k in ("tune", "judge"))
        dd_ok = (p["judge"]["portfolio"].get("max_dd_%") or -100) >= (base["judge"]["portfolio"].get("max_dd_%") or -100) - 2
        enough = (p["judge"]["signals"].get("trades") or 0) >= 100
        r["passes_bar"] = bool(better and dd_ok and enough)
    json.dump(res, open(os.path.join(out, f"round4-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:7])
