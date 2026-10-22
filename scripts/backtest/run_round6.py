"""Round 6 · find the best SMALL combination of rules (not the most rules) — without fooling ourselves.

Five building blocks, 2-4 choices each → 288 combinations of 2-5 rules:
  entry filter : live rules · trend template · leaders (RS top 20% + within 15% of high) · EPS & sales
  setup        : breakouts + pullbacks · breakouts only
  exit         : A2 trail · original stop only · 50-day exit · original stop + climax sell
  market       : live gate · half size when the gate isn't UPTREND · only buy when the S&P is above its 200-day
  re-entry     : off · buy back on a close above the high since the sale · EARLY: buy back on a 50-day reclaim that tops
                 the prior 10-day high (catches the turn below the sale price; added after the first run)
Idle money sits in SPY in every combination (Round 5: small help, never hurt).

Protocol (set BEFORE the run, to avoid finding a lucky combination):
  1. Every combination is scored on the TUNE years only (median of 3 random-order runs, excess CAGR vs SPY).
     The JUDGE years stay sealed while choosing.
  2. Eligible: tune max drawdown no worse than SPY's + 5 pts. Ties (within 0.5 pt): fewer rules, then steadier
     sub-period results.
  3. Only the TOP 3 are opened on the JUDGE years (10 random-order runs + block bootstrap).
  4. Pass bar is raised for having searched 288 combinations: beat SPY in tune AND judge, ≥ 80% of judge bootstrap
     resamples above zero, judge drawdown no worse than SPY's + 5 pts.

Usage: python run_round6.py PRICE_DIR SEC_DIR OUT_DIR MEMBERS_CSV [EXTRA_PRICE_DIR] [AUDIT_DIR]
"""
import datetime as dt, itertools, json, os, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S
from run_systems import load_members, is_member

COST = 0.0007
ENTRY = {"live rules": {}, "trend template": dict(trend_template=True),
         "leaders": dict(min_rsrank=80, near_high=15), "EPS & sales": dict(rev_min=15.0)}
SETUP = {"breakouts + pullbacks": {}, "breakouts only": dict(breakout_only=True)}
EXIT = {"A2 trail": {}, "original stop": dict(stop="fixed"), "50-day exit": dict(stop="ma50"),
        "original stop + climax sell": dict(stop="fixed", exit_climax=True)}
MARKET = {"live gate": ({}, False), "half size if not UPTREND": ({}, True), "S&P above 200-day": (dict(mkt_mode="spy200"), False)}
REENTRY = {"no re-entry": {}, "re-entry": dict(reentry=True), "early re-entry": dict(reentry="early")}
NC = 4 * 2 * 4 * 3 * 3
DEFAULTS = ("live rules", "breakouts + pullbacks", "A2 trail", "live gate", "no re-entry")
ENTRY_KEYS = ("vol_need", "pb_lo", "pb_hi", "pb_need_rising", "pb_need_low_vol", "block_pressure", "need_rs", "eps_min", "rev_min",
              "earn_days", "breakout_only", "pullback_only", "max_ext", "min_rsrank", "trend_template", "mkt_mode", "near_high", "nosec_pass")


def blocks_of(span):
    a, b = int(span[0][:4]), int(span[1][:4])
    step = 4 if b - a >= 8 else 2
    out, y = [], a
    while y <= b:
        z = min(y + step - 1, b)
        out.append((f"{y}-01-01" if y > a else span[0], f"{z}-12-31" if z < b else span[1]))
        y = z + 1
    return out


def main(pc, sc, out, members_csv, extra=None, audit_dir=None):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    prices = E.load_prices(pc)
    if extra and os.path.isdir(extra):
        for k, v in E.load_prices(extra).items():
            prices.setdefault(k, v)
    if audit_dir:
        prices = E.apply_corrections(prices, os.path.join(audit_dir, "corrections.json"))
    members = load_members(members_csv)
    if os.environ.get("R6_CLEAN"):                       # Round 7 data repair (splits, bad prints, spliced tickers)
        import data_clean as DC
        prices = DC.clean_all(prices, members)[0]
    spy, qqq = prices.pop("SPY"), prices.pop("QQQ"); prices.pop("RSP", None)
    long_data = spy.date.iat[0] <= "2004-06-30"
    TUNE, JUDGE = (("2005-01-01", "2016-12-31"), ("2017-01-01", "2025-12-31")) if long_data else \
                  (("2017-10-15", "2021-12-31"), ("2022-01-01", "2025-12-31"))
    Y26 = ("2026-01-01", "2026-12-31")
    prices = {k: v for k, v in prices.items() if k in members}
    cal = list(spy.date); spy_c = spy.set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    el = E.eligibility(prices, cal, member=lambda s, d: is_member(members, s, d))
    rk = E.rs_rank(prices, cal, eligible=el)
    elig = {s: dict(zip(cal, el[s].to_numpy())) for s in el.columns}
    mkt = E.market_status(spy, qqq)
    live = mkt["live"]
    half = lambda d: 1.0 if live.get(d) == "UPTREND" else 0.5
    spy_close = dict(zip(spy.date, spy.c))
    IND, SEC = {}, {}
    for s in sorted(prices):
        IND[s] = E.indicators(prices[s]); IND[s]["rsrank"] = rk[s].reindex(prices[s].date).to_numpy()
        SEC[s] = E.load_sec(sc, s)
    del rk
    closes = {s: prices[s].set_index("date").c for s in prices}
    spy_m = lambda a, b: S.perf_metrics(spy_c[(spy_c.index >= a) & (spy_c.index <= b)])
    SUB = blocks_of(TUNE)
    res = {"asOf": dt.date.today().isoformat(), "mode": "long (EODHD)" if long_data else "free (Yahoo, survivorship-limited)",
           "tune": TUNE, "judge": JUDGE, "sub_periods": SUB, "stocks": len(prices), "cost_per_side": COST,
           "spy": {"tune": spy_m(*TUNE), "judge": spy_m(*JUDGE), "2026": spy_m(*Y26)}, "combos": []}
    print(f"{len(prices)} S&P members · {'LONG' if long_data else 'FREE'} · tune {TUNE} judge {JUDGE} · {time.time()-t0:.0f}s", flush=True)

    def port(tr, a, b, regime, seed=None, stats=None):
        return E.portfolio([t for t in tr if a <= t["entry_date"] <= b], closes, cal, a, b, cost=COST, seed=seed,
                           idle=idle, risk_fn=half if regime else None, stats=stats)

    TRADES = {}
    n = 0
    for en, se, mk_name in itertools.product(ENTRY, SETUP, MARKET):
        mchange, _ = MARKET[mk_name]
        P0 = dict(E.BASE); P0.update(nosec_pass=True); P0.update(ENTRY[en]); P0.update(SETUP[se]); P0.update(mchange)
        if mk_name == "half size if not UPTREND":
            pass                                              # same signals as "live gate"; reuse its trades below
        else:
            sigs = {s: E.evaluate(s, prices[s], IND[s], SEC[s], mkt, spy_close, P0) for s in prices}
        for ex, re_ in itertools.product(EXIT, REENTRY):
            P = dict(P0); P.update(EXIT[ex]); P.update(REENTRY[re_])
            key = (en, se, "live gate" if mk_name == "half size if not UPTREND" else mk_name, ex, re_)
            if key not in TRADES:
                tr = []
                for s in prices:
                    tr += [t for t in E.simulate_trades(s, prices[s], IND[s], sigs[s], P, TUNE[0], Y26[1]) if elig.get(s, {}).get(t["signal"], False)]
                TRADES[key] = tr
            tr = TRADES[key]
            regime = mk_name == "half size if not UPTREND"
            names = (en, se, ex, mk_name, re_)
            nrules = sum(1 for x, d in zip(names, ("live rules", "breakouts + pullbacks", "A2 trail", "live gate", "no re-entry")) if x != d)
            st = {}
            eq, taken = port(tr, *TUNE, regime, None, st)
            ex_runs = [S.perf_metrics(port(tr, *TUNE, regime, seed=k)[0], spy_c).get("excess_cagr_%", -99) for k in range(3)]
            subs = [S.perf_metrics(eq[(eq.index >= a) & (eq.index <= b)], spy_c).get("excess_cagr_%", -99) for a, b in SUB]
            m = S.perf_metrics(eq, spy_c)
            res["combos"].append({"entry": en, "setup": se, "exit": ex, "market": mk_name, "reentry": re_, "changes_vs_live": nrules,
                                  "tune": {"excess_median": round(float(np.median(ex_runs)), 2), "cagr": m.get("cagr_%"),
                                           "max_dd": m.get("max_dd_%"), "sub_excess": subs, "trades": len(taken),
                                           "in_stocks_%": st.get("avg_in_stocks_%"),
                                           "reentries": sum(1 for t in taken if t.get("setup") == "REENTRY")}})
            n += 1
            if n % 12 == 0:
                print(f"{n}/{NC} combos scored on tune ({time.time()-t0:.0f}s)", flush=True)
        if mk_name != "half size if not UPTREND":
            del sigs
        # drop trades no longer needed (keyed by entry/setup/market); keep memory flat
        for k in [k for k in TRADES if k[:3] != (en, se, "live gate")]:
            if k[:2] != (en, se):
                TRADES.pop(k, None)
    # choose on TUNE only
    spy_dd_t = res["spy"]["tune"].get("max_dd_%") or -100
    ok = [c for c in res["combos"] if (c["tune"]["max_dd"] or -100) >= spy_dd_t - 5]
    ok.sort(key=lambda c: (-round(c["tune"]["excess_median"] * 2) / 2, c["changes_vs_live"], -min(c["tune"]["sub_excess"])))
    res["beat_spy_in_tune"] = sum(1 for c in res["combos"] if c["tune"]["excess_median"] > 0)
    top = ok[:3]
    base = next(c for c in res["combos"] if (c["entry"], c["setup"], c["exit"], c["market"], c["reentry"]) == DEFAULTS)
    print(f"tune done: {res['beat_spy_in_tune']}/{NC} beat SPY in tune · opening the judge period for the top 3 + the live baseline", flush=True)
    # open the JUDGE period: top 3 + the live baseline (for reference only)
    spy_dd_j = res["spy"]["judge"].get("max_dd_%") or -100
    for c in top + [base]:
        en, se, ex, mk_name, re_ = c["entry"], c["setup"], c["exit"], c["market"], c["reentry"]
        mchange, regime = MARKET[mk_name]
        P = dict(E.BASE); P.update(nosec_pass=True)
        for d in (ENTRY[en], SETUP[se], mchange, EXIT[ex], REENTRY[re_]):
            P.update(d)
        tr = []
        for s in prices:
            sg = E.evaluate(s, prices[s], IND[s], SEC[s], mkt, spy_close, P)
            tr += [t for t in E.simulate_trades(s, prices[s], IND[s], sg, P, TUNE[0], Y26[1]) if elig.get(s, {}).get(t["signal"], False)]
        out_j = {}
        for pn, span in (("judge", JUDGE), ("2026", Y26)):
            st = {}
            eq, taken = port(tr, *span, regime, None, st)
            runs = [S.perf_metrics(port(tr, *span, regime, seed=k)[0], spy_c) for k in range(10)]
            exs = [r.get("excess_cagr_%", -99) for r in runs]; cg = [r.get("cagr_%", 0) for r in runs]
            out_j[pn] = {"cagr_median": round(float(np.median(cg)), 1), "excess_median": round(float(np.median(exs)), 1),
                         "cagr_low": min(cg), "cagr_high": max(cg), "max_dd": S.perf_metrics(eq).get("max_dd_%"),
                         "trades": len(taken), "in_stocks_%": st.get("avg_in_stocks_%")}
            if pn == "judge":
                out_j[pn]["bootstrap"] = S.block_bootstrap_excess(eq, spy_c, *span)
        c["judge"], c["2026"] = out_j["judge"], out_j["2026"]
        j = c["judge"]
        c["passes_bar"] = bool(c["tune"]["excess_median"] > 0 and j["excess_median"] > 0
                               and (j.get("bootstrap") or {}).get("share_above_zero_%", 0) >= 80
                               and (j["max_dd"] or -100) >= spy_dd_j - 5)
        print(f"JUDGE {en} | {se} | {ex} | {mk_name} | {re_}: tune excess {c['tune']['excess_median']} · judge excess {j['excess_median']} "
              f"(CAGR {j['cagr_median']}) · bootstrap {(j.get('bootstrap') or {}).get('share_above_zero_%')}% · DD {j['max_dd']}", flush=True)
    res["top3"] = [{k: c[k] for k in ("entry", "setup", "exit", "market", "reentry", "changes_vs_live", "tune", "judge", "2026", "passes_bar")} for c in top]
    res["live_baseline"] = {k: base.get(k) for k in ("entry", "setup", "exit", "market", "reentry", "tune", "judge", "2026")}
    json.dump(res, open(os.path.join(out, f"round6-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:7])
