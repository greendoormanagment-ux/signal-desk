"""Round 5 · can Signal Desk beat SPY? Test the gaps Round 4 exposed:
  1. CASH DRAG — a stock-picking portfolio sits in cash between setups while SPY is always invested.
     Fix tested: money not in a stock stays in SPY ("core + satellite" inside one account).
  2. CUTTING WINNERS SHORT — the A2 trailing stop exits early; Round 4 showed the original stop alone earned far more per trade.
  3. THE BEST EARLIER RESULT — Round 1's combined system (breakout + earnings gap + pullback, all exits on the 50-day)
     was only ever run on a survivorship-biased universe.

Usage: python run_round5.py PRICE_DIR SEC_DIR OUT_DIR MEMBERS_CSV [EXTRA_PRICE_DIR] [AUDIT_DIR]
Universe/execution as Round 3-4: point-in-time S&P 500, $5+, $20M+/day, next-open fills, 0.07%/side + 0.03% per SPY switch.
Periods: long data → TUNE 2005-2016 / JUDGE 2017-2025; free data → TUNE 2017-2021 / JUDGE 2022-2025; 2026 alone.
Pass bar (set BEFORE the run): beat SPY (price, same costs basis) in BOTH tune and judge, with ≥ 70% of judge-period
bootstrap resamples above zero, and a max drawdown no worse than SPY's + 5 points.
"""
import datetime as dt, json, os, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S
from run_systems import load_members, is_member

COST = 0.0007
MC = 10
# (label, engine overrides, idle in SPY?, system)  system: "live" = engine rules · "combined" = systems.combined
VARIANTS = [
    ("control: live rules, cash idle (= Round 4 base)", {}, False, "live"),
    ("live rules + idle cash in SPY", {}, True, "live"),
    ("live rules + original stop only + idle SPY", dict(stop="fixed"), True, "live"),
    ("live rules + exit on close 2% under 50-day + idle SPY", dict(stop="ma50"), True, "live"),
    ("trend template + idle SPY", dict(trend_template=True), True, "live"),
    ("trend template + 50-day exit + idle SPY", dict(trend_template=True, stop="ma50"), True, "live"),
    ("trend template + original stop only + idle SPY", dict(trend_template=True, stop="fixed"), True, "live"),
    ("EPS & sales + 50-day exit + idle SPY", dict(rev_min=15.0, stop="ma50"), True, "live"),
    ("breakouts only + 50-day exit + idle SPY", dict(breakout_only=True, stop="ma50"), True, "live"),
    ("control: combined system, cash idle", {}, False, "combined"),
    ("combined system (breakout + earnings gap + pullback, 50-day exit) + idle SPY", {}, True, "combined"),
    ("combined system, 12 slots + idle SPY", dict(max_pos=12), True, "combined"),
]
ENTRY_KEYS = ("vol_need", "pb_lo", "pb_hi", "pb_need_rising", "pb_need_low_vol", "block_pressure", "need_rs", "eps_min", "rev_min",
              "earn_days", "breakout_only", "pullback_only", "max_ext", "min_rsrank", "trend_template", "mkt_mode", "near_high", "nosec_pass")
COMBINED_X = dict(S.DEFAULT_EXIT, runner="sma50", partial_R=0, time_days=0)


def main(pc, sc, out, members_csv, extra=None, audit_dir=None):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    prices = E.load_prices(pc)
    if extra and os.path.isdir(extra):
        for k, v in E.load_prices(extra).items():
            prices.setdefault(k, v)
    if audit_dir:
        prices = E.apply_corrections(prices, os.path.join(audit_dir, "corrections.json"))
    try:
        meta = json.load(open(os.path.join(pc, "universe.json"))).get("meta") or {}
    except Exception:
        meta = {}
    members = load_members(members_csv)
    spy, qqq = prices.pop("SPY"), prices.pop("QQQ"); prices.pop("RSP", None)
    long_data = spy.date.iat[0] <= "2004-06-30"
    TUNE, JUDGE = (("2005-01-01", "2016-12-31"), ("2017-01-01", "2025-12-31")) if long_data else \
                  (("2017-10-15", "2021-12-31"), ("2022-01-01", "2025-12-31"))
    PER = {"tune": TUNE, "judge": JUDGE, "2026": ("2026-01-01", "2026-12-31")}
    prices = {k: v for k, v in prices.items() if k in members}
    cal = list(spy.date); spy_c = spy.set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    mem_fn = lambda s, d: is_member(members, s, d)
    el = E.eligibility(prices, cal, member=mem_fn)
    rk = E.rs_rank(prices, cal, eligible=el)
    elig = {s: dict(zip(cal, el[s].to_numpy())) for s in el.columns}
    mkt = E.market_status(spy, qqq)
    spy_close = dict(zip(spy.date, spy.c))
    IND, SEC = {}, {}
    for s in sorted(prices):
        IND[s] = E.indicators(prices[s]); IND[s]["rsrank"] = rk[s].reindex(prices[s].date).to_numpy()
        SEC[s] = E.load_sec(sc, s)
    del rk
    closes_s = {s: prices[s].set_index("date").c for s in prices}
    closes_d = {s: dict(zip(prices[s].date, prices[s].c)) for s in prices}
    print(f"{len(prices)} S&P members · data from {spy.date.iat[0]} · {'LONG' if long_data else 'FREE'} mode · {time.time()-t0:.0f}s", flush=True)
    res = {"asOf": dt.date.today().isoformat(), "mode": "long (EODHD)" if long_data else "free (Yahoo, survivorship-limited)",
           "periods": PER, "cost_per_side": COST, "idle_switch_cost": 0.0003, "stocks": len(prices),
           "spy": {k: S.perf_metrics(spy_c[(spy_c.index >= a) & (spy_c.index <= b)]) for k, (a, b) in PER.items()}, "variants": []}
    sig_cache, comb_trades = {}, None
    for vi, (label, change, use_idle, system) in enumerate(VARIANTS):
        trades = []
        if system == "live":
            P = dict(E.BASE); P.update(nosec_pass=True); P.update(change)
            key = tuple(P[k] for k in ENTRY_KEYS)
            if key not in sig_cache:
                sig_cache.clear()
                sig_cache[key] = {s: E.evaluate(s, prices[s], IND[s], SEC[s], mkt, spy_close, P) for s in prices}
            for s in prices:
                trades += [t for t in E.simulate_trades(s, prices[s], IND[s], sig_cache[key][s], P, TUNE[0], PER["2026"][1])
                           if elig.get(s, {}).get(t["signal"], False)]
        else:
            if comb_trades is None:
                comb_trades = []
                for s in prices:
                    f = S.features(s, prices[s], IND[s], SEC[s], None, mkt, meta.get(s))
                    ent = [e for e in S.combined(f, {}) if elig.get(s, {}).get(f["dates"][e[0]], False)]
                    comb_trades += S.simulate(s, f, ent, COMBINED_X, TUNE[0], PER["2026"][1])
            trades = comb_trades
        r = {"label": label, "system": system, "idle_in_spy": use_idle, "change": change, "periods": {}}
        for pn, (a, b) in PER.items():
            tr = [t for t in trades if a <= t["entry_date"] <= b]
            st = {}
            if system == "live":
                run = lambda seed=None, stt=None: E.portfolio(tr, closes_s, cal, a, b, cost=COST, seed=seed, idle=idle if use_idle else None, stats=stt)
            else:
                mp = change.get("max_pos", 8)
                run = lambda seed=None, stt=None: S.portfolio(tr, closes_d, cal, a, b, max_pos=mp, sector_cap=2, cost=COST, seed=seed,
                                                             idle=idle if use_idle else None, stats=stt)
            eq, taken = run(None, st)
            mcs = [S.perf_metrics(run(k)[0], spy_c) for k in range(MC)]
            cg = [m.get("cagr_%", 0) for m in mcs]; ex = [m.get("excess_cagr_%", 0) for m in mcs]
            r["periods"][pn] = {"portfolio": S.perf_metrics(eq, spy_c), "trades_taken": len(taken), "signals": len(tr),
                                "avg_in_stocks_%": st.get("avg_in_stocks_%"),
                                "mc": {"cagr_median": round(float(np.median(cg)), 1), "cagr_low": min(cg), "cagr_high": max(cg),
                                       "excess_median": round(float(np.median(ex)), 1)}}
            if pn == "judge":
                r["periods"][pn]["bootstrap_vs_spy"] = S.block_bootstrap_excess(eq, spy_c, a, b)
        p = r["periods"]
        spy_dd = res["spy"]["judge"].get("max_dd_%") or -100
        r["passes_bar"] = bool((p["tune"]["mc"]["excess_median"] > 0) and (p["judge"]["mc"]["excess_median"] > 0)
                               and (p["judge"].get("bootstrap_vs_spy", {}).get("share_above_zero_%", 0) >= 70)
                               and ((p["judge"]["portfolio"].get("max_dd_%") or -100) >= spy_dd - 5))
        res["variants"].append(r)
        j = p["judge"]
        print(f"[{vi+1}/{len(VARIANTS)}] {label[:60]:60} | judge CAGR {j['portfolio'].get('cagr_%')} (MC {j['mc']['cagr_median']}, "
              f"vs SPY {j['mc']['excess_median']}) · in stocks {j['avg_in_stocks_%']}% · DD {j['portfolio'].get('max_dd_%')} ({time.time()-t0:.0f}s)", flush=True)
        json.dump(res, open(os.path.join(out, "round5-partial.json"), "w"), indent=1, default=str)
    json.dump(res, open(os.path.join(out, f"round5-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:7])
