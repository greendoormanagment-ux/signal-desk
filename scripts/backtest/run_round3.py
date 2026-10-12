"""Round 3 · Gate 2: momentum and short-term pullback re-tested with realistic execution.

Usage: python run_round3.py PRICE_CACHE SEC_CACHE OUT_DIR EXTRA_PRICE_DIR SP500_START_END_CSV AUDIT_DIR

Rules applied everywhere (see backtest/round3-latest.md):
  * universe = S&P 500 members ON THE DATE (point in time), $5+, $20M+/day average, 1 year of history
  * the Gate 1 corrections overlay is applied in memory (cache files untouched)
  * a signal computed from a close trades no earlier than the next session (next open, or a next-day limit order)
  * a stop crossed by an opening gap fills at the open; costs charged on every buy and sell
  * the main evaluation window ENDS 2025-12-31; 2026 is shown separately
"""
import datetime as dt, json, os, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S
from run_systems import load_members, is_member

EVAL = ("2017-10-15", "2025-12-31")
Y26 = ("2026-01-01", "2026-12-31")
BLOCKS = [("2018-01-01", "2019-12-31"), ("2020-01-01", "2021-12-31"), ("2022-01-01", "2023-12-31"), ("2024-01-01", "2025-12-31")]
BOOT = ("2017-12-01", "2025-12-31")
COST = 0.0007          # per side: $0 commission + ~5 bp slippage + ~2 bp half-spread for liquid S&P 500 stocks
COST_STRESS = 0.0015   # per side, pessimistic
MC = 10


def block_table(eq, spy_c):
    out = []
    for a, b in BLOCKS:
        m = S.perf_metrics(eq[(eq.index >= a) & (eq.index <= b)], spy_c)
        out.append({"period": f"{a[:4]}-{b[:4]}", "cagr_%": m.get("cagr_%"), "spy_cagr_%": m.get("bench_cagr_%"),
                    "excess_%": m.get("excess_cagr_%"), "max_dd_%": m.get("max_dd_%")})
    return out


def main(pc, sc, out, extra, members_csv, audit_dir):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    prices = E.load_prices(pc)
    for k, v in E.load_prices(extra).items():
        prices.setdefault(k, v)
    prices = E.apply_corrections(prices, os.path.join(audit_dir, "corrections.json"))
    audit = json.load(open(os.path.join(audit_dir, "audit-summary.json")))
    unresolved = set(audit.get("stocks_with_unresolved", []))
    uni = json.load(open(os.path.join(pc, "universe.json")))
    members = load_members(members_csv)
    spy, qqq = prices.pop("SPY"), prices.pop("QQQ"); prices.pop("RSP", None)
    prices = {k: v for k, v in prices.items() if k in members}
    cal = list(spy.date); spy_c = spy.set_index("date").c
    try:                                                     # SPY with dividends reinvested (price-only results ignore ~1.5%/yr of dividends)
        import fetch_prices as fp
        spy_tr = pd.Series(fp.yahoo_total_return("SPY")).sort_index()
    except Exception:
        spy_tr = None
    mem_fn = lambda s, d: is_member(members, s, d)
    el = E.eligibility(prices, cal, member=mem_fn)
    rk = E.rs_rank(prices, cal, eligible=el)
    mkt = E.market_status(spy, qqq)
    F = {}
    for s in sorted(prices):
        ind = E.indicators(prices[s]); ind["rsrank"] = rk[s].reindex(prices[s].date).to_numpy()
        F[s] = S.features(s, prices[s], ind, E.load_sec(sc, s), None, mkt, uni["meta"].get(s))
    closes = {s: dict(zip(prices[s].date, prices[s].c)) for s in prices}
    elig = {s: dict(zip(cal, el[s].to_numpy())) for s in el.columns}
    print(f"{len(F)} S&P members with data · corrections applied · {time.time()-t0:.0f}s", flush=True)
    res = {"asOf": dt.date.today().isoformat(), "eval_window": EVAL, "costs_per_side": {"base": COST, "stress": COST_STRESS},
           "spy_total_return": S.perf_metrics(spy_tr[(spy_tr.index >= EVAL[0]) & (spy_tr.index <= EVAL[1])]) if spy_tr is not None else None,
           "spy": {"eval": S.perf_metrics(spy_c[(spy_c.index >= EVAL[0]) & (spy_c.index <= EVAL[1])]),
                   "2026": S.perf_metrics(spy_c[spy_c.index >= Y26[0]]), "blocks": block_table(spy_c, spy_c)},
           "data": {k: audit[k] for k in ("combined_sha256", "extreme_moves", "classification", "corrections")},
           "momentum": [], "pullback": []}

    # ── momentum (next-open execution)
    group_ind = {s: (uni["meta"].get(s) or {}).get("industry") for s in prices}
    group_sec = {s: (uni["meta"].get(s) or {}).get("sector") for s in prices}
    runs = [("base: top 10, 12-1 month, monthly, next-open, 0.07%/side", {}, None),
            ("cost stress: 0.15%/side", dict(cost=COST_STRESS), None),
            ("top 20", dict(top=20), None),
            ("theme cap: max 2 per industry", dict(group=group_ind, group_cap=2), None),
            ("sector cap: max 3 per sector", dict(group=group_sec, group_cap=3), None),
            ("without stocks that have unresolved data moves", {}, "drop_unresolved")]
    runs += [(f"rebalance on trading day {k + 1}", dict(offset=k), None) for k in range(1, 5)]
    for label, kw, mode in runs:
        sub = {s: p for s, p in prices.items() if not (mode == "drop_unresolved" and s in unresolved)}
        kw2 = dict(cost=COST); kw2.update(kw)
        eq, det = S.momentum_open(sub, cal, EVAL[0], "2026-12-31", member=mem_fn, **kw2)
        ev = eq[eq.index <= EVAL[1]]
        r = {"label": label, "eval": S.perf_metrics(ev, spy_c), "2026": S.perf_metrics(eq[eq.index >= Y26[0]], spy_c),
             "turnover_per_year": det["turnover_per_year"], "blocks": block_table(ev, spy_c),
             "bootstrap": S.block_bootstrap_excess(ev, spy_c, *BOOT) if label.startswith("base") or "theme" in label else {}}
        if label.startswith("base"):
            r["recent_picks"] = det["picks"][-4:]
        res["momentum"].append(r)
        print(f"MOM {label[:45]} | {r['eval']} | turnover {r['turnover_per_year']} | {r['bootstrap']} ({time.time()-t0:.0f}s)", flush=True)

    # ── short-term pullback (control): only executions that are possible after the close
    MR_X = dict(S.DEFAULT_EXIT, partial_R=0, time_days=0, runner="none", bounce="sma5", max_days=10, max_risk=0.6)
    pruns = [("next-open entry, RSI(2) < 10, 0.07%/side", {}, dict(entry="open"), COST),
             ("next-open entry, RSI(2) < 5", dict(rsi_max=5), dict(entry="open"), COST),
             ("limit 2% under signal close (next day), RSI(2) < 10", {}, dict(entry="limit", limit_pct=0.02), COST),
             ("limit 2% under signal close, RSI(2) < 5", dict(rsi_max=5), dict(entry="limit", limit_pct=0.02), COST),
             ("limit 2%, RSI(2) < 10, cost stress 0.15%/side", {}, dict(entry="limit", limit_pct=0.02), COST_STRESS)]
    for label, ep, xo, cost in pruns:
        X = dict(MR_X); X.update(xo)
        tr = []
        for s, f in F.items():
            ent = [e for e in S.mean_reversion(f, ep) if elig.get(s, {}).get(f["dates"][e[0]], False)]
            tr += S.simulate(s, f, ent, X, *EVAL)
        tr26 = []
        for s, f in F.items():
            ent = [e for e in S.mean_reversion(f, ep) if elig.get(s, {}).get(f["dates"][e[0]], False)]
            tr26 += S.simulate(s, f, ent, X, *Y26)
        eq, taken = S.portfolio(tr, closes, cal, *EVAL, max_pos=10, sector_cap=3, cost=cost)
        mcs = [S.perf_metrics(S.portfolio(tr, closes, cal, *EVAL, max_pos=10, sector_cap=3, cost=cost, seed=k)[0]) for k in range(MC)]
        rets = np.array([t["ret"] for t in taken]) / 100 - 2 * cost       # per-trade result AFTER costs
        yrs = (pd.Timestamp(EVAL[1]) - pd.Timestamp(EVAL[0])).days / 365.25
        eq26, _ = S.portfolio(tr26, closes, cal, *Y26, max_pos=10, sector_cap=3, cost=cost)
        r = {"label": label, "signals": len(tr), "trades_taken": len(taken), "trades_per_year": round(len(taken) / yrs, 0),
             "win_after_costs_%": round(float((rets > 0).mean() * 100), 1), "expectancy_after_costs_%": round(float(rets.mean() * 100), 3),
             "avg_win_%": round(float(rets[rets > 0].mean() * 100), 2), "avg_loss_%": round(float(rets[rets <= 0].mean() * 100), 2),
             "avg_days": round(float(np.mean([t["days"] for t in taken])), 1),
             "capital_turnover_per_year": round(len(taken) * 0.10 * 2 / yrs, 1),
             "eval": S.perf_metrics(eq, spy_c), "mc_cagr_range": [min(m["cagr_%"] for m in mcs), max(m["cagr_%"] for m in mcs)],
             "2026": S.perf_metrics(eq26, spy_c), "blocks": block_table(eq, spy_c), "bootstrap": S.block_bootstrap_excess(eq, spy_c, *BOOT)}
        res["pullback"].append(r)
        print(f"PB {label[:45]} | trades {len(taken)} win {r['win_after_costs_%']} exp {r['expectancy_after_costs_%']}% | {r['eval']} ({time.time()-t0:.0f}s)", flush=True)
    json.dump(res, open(os.path.join(out, f"round3-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:7])
