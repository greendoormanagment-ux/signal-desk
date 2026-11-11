"""Round 8 · session 2b — three trend filters + the colleague's descriptive questions.
Pre-registered in backtest/round8c-preregistration.md (locked 2026-11-11 before any result was run).
Same standard and same operational choices as run_round8b.py; base = live v2.16 rules, all US pooled.

Usage: python run_round8c.py UNIVERSE_PKL MEMBERS_CSV OUT_DIR
"""
import datetime as dt, json, math, os, pickle, sys, time
import numpy as np, pandas as pd
import engine as E
from run_systems import load_members, is_member
from run_round8a import COST, TUNE, JUDGE, extra_cost, regimes, eq_stats
from run_round8b import diff, interaction, holm, ols_cluster, MIN_EFFECT, ALPHA, MIN_N, DD_TOL, NEG_REGIME

TESTS = ["21-day moving average", "12-1 momentum (top 30%)", "earnings-gap drift"]
EXITS = {"A2 trail (live)": {}, "original stop": dict(stop="fixed")}
PRIMARY, BEST = "A2 trail (live)", "original stop"


def drift_at(o, c, v, k):
    """index.html driftSetup(): gap up >= 4% on >= 2x the 50-day average volume (excluding today) in the last 3 sessions."""
    if k < 52:
        return False
    av = v[k - 50:k].mean()
    if not av:
        return False
    return any(o[i] / c[i - 1] - 1 >= 0.04 and v[i] >= 2 * av for i in (k, k - 1, k - 2))


def profile(tr):
    if not tr:
        return {}
    tr = sorted(tr, key=lambda t: t["entry_date"]); R = np.array([t["Rn"] for t in tr])
    streak = best = 0
    for x in R:
        streak = streak + 1 if x <= 0 else 0; best = max(best, streak)
    k = max(1, int(round(0.05 * len(R)))); tot = R.sum()
    by = pd.Series(R).groupby([t["sym"] for t in tr]).sum().sort_values(ascending=False)
    top10 = set(by.index[:10]); rest = np.array([t["Rn"] for t in tr if t["sym"] not in top10])
    return {"n": len(R), "win_%": round(100 * float((R > 0).mean()), 1), "avg_win_R": round(float(R[R > 0].mean()), 2),
            "avg_loss_R": round(float(R[R <= 0].mean()), 2), "largest_win_R": round(float(R.max()), 1),
            "longest_losing_streak": int(best), "profit_factor": round(float(R[R > 0].sum() / -R[R <= 0].sum()), 2),
            "mean_R": round(float(R.mean()), 3), "top5pct_share_of_total_R_%": round(100 * float(np.sort(R)[-k:].sum() / tot), 1) if tot else None,
            "mean_R_without_top5pct": round(float(np.sort(R)[:-k].mean()), 3),
            "top10_stocks": list(by.index[:10]), "top10_stocks_share_of_total_R_%": round(100 * float(by.iloc[:10].sum() / tot), 1) if tot else None,
            "mean_R_without_top10_stocks": round(float(rest.mean()), 3) if len(rest) else None}


def main(pkl, members_csv, out):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    U = pickle.load(open(pkl, "rb")); prices, etf = U["prices"], U["etf"]
    members = load_members(members_csv)
    spy, qqq = etf["SPY"], etf["QQQ"]
    cal = list(spy.date); cix = {d: i for i, d in enumerate(cal)}
    spy_c = spy.set_index("date").c; rsp_c = etf["RSP"].set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    mkt = E.market_status(spy, qqq); spy_close = dict(zip(spy.date, spy.c)); reg = regimes(spy)
    MOM = np.full((len(cal), len(prices)), np.nan, dtype=np.float32)
    TR = {ex: [] for ex in EXITS}
    for j, (s, df) in enumerate(prices.items()):
        ind = E.indicators(df)
        dv = (df.v.rolling(50, min_periods=50).mean().shift(1) * df.c / 1e6).to_numpy()
        elig = (df.c.to_numpy() >= 5) & (np.nan_to_num(dv) >= 20) & (np.arange(len(df)) >= 252)
        dates = df.date.to_numpy(); O, C, V = (df[k].to_numpy(float) for k in "ocv")
        cs = pd.Series(C); mom = (cs.shift(21) / cs.shift(252) - 1).to_numpy()
        ma = cs.rolling(21).mean().to_numpy(); ma_up = (C > ma) & (ma > np.r_[np.full(5, np.nan), ma[:-5]])
        rows = [cix.get(d) for d in dates]
        for i, r in enumerate(rows):
            if r is not None and elig[i] and mom[i] == mom[i]:
                MOM[r, j] = mom[i]
        P0 = dict(E.BASE); P0.update(nosec_pass=True, breakout_only=True, mkt_mode="live")
        sig = E.evaluate(s, df, ind, None, mkt, spy_close, P0)[["rating", "stop", "setup", "score", "market"]]
        for ex, chg in EXITS.items():
            P = dict(P0); P.update(chg)
            for t in E.simulate_trades(s, df, ind, sig, P, TUNE[0], JUDGE[1]):
                k = int(np.searchsorted(dates, t["signal"]))
                if not elig[k]:
                    continue
                x = extra_cost(float(np.nan_to_num(dv[k])))
                t["entry"] *= (1 + x); t["exit"] *= (1 - x); per = t["entry"] - t["stop"]
                if per <= 0:
                    continue
                rg = reg.get(t["signal"])
                t.update(Rn=((t["exit"] * (1 - COST)) - t["entry"] * (1 + COST)) / per, sp=bool(is_member(members, s, t["signal"])),
                         regime=rg[0] if rg else None, hv=bool(rg and rg[1]), mom=float(mom[k]) if mom[k] == mom[k] else None,
                         cal_i=cix.get(t["signal"]), f_ma=bool(ma_up[k]), f_drift=drift_at(O, C, V, k),
                         stop_pct=per / t["entry"] * 100,
                         hold_days=(pd.Timestamp(t["exit_date"]) - pd.Timestamp(t["entry_date"])).days)
                TR[ex].append(t)
        E._PIT.pop(s, None)
        if j % 1000 == 0:
            print(f"  {j} stocks ({time.time()-t0:.0f}s)", flush=True)
    p70 = np.nanpercentile(MOM, 70, axis=1); del MOM
    for ex in TR:
        for t in TR[ex]:
            t["fp"] = [t["f_ma"], t["mom"] is not None and t["cal_i"] is not None and t["mom"] >= p70[t["cal_i"]], t["f_drift"]]
    closes = {s: prices[s].set_index("date").c for s in prices}
    print(f"trades {', '.join(f'{k}: {len(v)}' for k, v in TR.items())} · {time.time()-t0:.0f}s", flush=True)

    def port(tr, a, b, seed=None, stats=None):
        return E.portfolio([t for t in tr if a <= t["entry_date"] <= b], closes, cal, a, b, cost=COST, seed=seed, idle=idle, stats=stats)

    def pstats(tr, a, b):
        runs = [eq_stats(port(tr, a, b, k)[0], spy_c, rsp_c) for k in range(3)]
        return {k: round(float(np.median([r[k] for r in runs if r.get(k) is not None])), 2) for k in ("cagr", "vs_spy", "vs_rsp", "max_dd", "sharpe")}

    res = {"asOf": dt.date.today().isoformat(), "prereg": "backtest/round8c-preregistration.md", "tests": TESTS}
    # ---- primary family (live rules)
    tr = TR[PRIMARY]; dev = [t for t in tr if TUNE[0] <= t["entry_date"] <= TUNE[1]]; val = [t for t in tr if JUDGE[0] <= t["entry_date"] <= JUDGE[1]]
    base_dev, base_val = pstats(dev, *TUNE), pstats(val, *JUDGE)
    rows = []
    for k, name in enumerate(TESTS):
        r = {"test": name, "share_with_%": round(100 * float(np.mean([t["fp"][k] for t in tr])), 1), "dev": diff(dev, k), "val": diff(val, k),
             "sp": diff([t for t in tr if t["sp"]], k), "nonsp": diff([t for t in tr if not t["sp"]], k), "interaction": interaction(tr, k),
             "regimes": {g: diff([t for t in tr if (t["regime"] == g if g != "high volatility" else t["hv"])], k) for g in ("bull", "bear", "sideways", "high volatility")},
             "portfolio": {"dev_with": pstats([t for t in dev if t["fp"][k]], *TUNE), "dev_rules_only": base_dev,
                           "val_with": pstats([t for t in val if t["fp"][k]], *JUDGE), "val_rules_only": base_val}}
        rows.append(r)
    for r, a in zip(rows, holm([r["dev"].get("p", 1.0) for r in rows])):
        r["dev"]["p_holm"] = a
    zb = 2.935  # two-sided 99% Bonferroni over 3 tests (alpha 0.01/3)
    for r in rows:
        d0 = r["dev"]; reasons = []
        if d0.get("n_with", 0) < MIN_N or d0.get("n_without", 0) < MIN_N or "est" not in d0:
            r["verdict"], r["why"] = "INCONCLUSIVE", "fewer than 300 trades on one side"; continue
        d0["ci99_bonf"] = [round(d0["est"] - zb * d0["se"], 3), round(d0["est"] + zb * d0["se"], 3)]
        if not (d0["est"] >= MIN_EFFECT and d0["p_holm"] < ALPHA):
            r["verdict"], r["why"] = (("FAIL", f"+{MIN_EFFECT}R ruled out (99% upper end {d0['ci99_bonf'][1]:+.3f}R)") if d0["ci99_bonf"][1] < MIN_EFFECT
                                      else ("INCONCLUSIVE", "interval still includes +0.15R; effect not established"))
            continue
        if not (r["val"].get("est", -1) > 0): reasons.append("validation effect not positive")
        if not (r["sp"].get("est", -1) > 0 and r["nonsp"].get("est", -1) > 0): reasons.append("not positive in both S&P and non-S&P")
        rg = [x.get("est") for x in r["regimes"].values() if x.get("est") is not None]
        if sum(e > 0 for e in rg) < 3 or any(e < NEG_REGIME for e in rg): reasons.append("regime consistency")
        pw, pb = r["portfolio"]["dev_with"], r["portfolio"]["dev_rules_only"]
        if not (pw["vs_spy"] > pb["vs_spy"] and pw["max_dd"] >= pb["max_dd"] - DD_TOL): reasons.append("portfolio vs SPY / drawdown")
        r["verdict"], r["why"] = ("PASS", "every rule met") if not reasons else ("FAIL", "; ".join(reasons))
    res["primary"] = {"n_dev": len(dev), "n_val": len(val), "rules_only_dev": base_dev, "rules_only_val": base_val, "rows": rows}
    for r in rows:
        print(f"{r['test']:26s} {r['verdict']:12s} with {r['share_with_%']}% · dev {r['dev'].get('est')} {r['dev'].get('ci99_bonf')} p_holm {r['dev'].get('p_holm'):.3g} · val {r['val'].get('est')} · {r['why']}", flush=True)
    # secondary: same three tests with the original stop (report only)
    tb = TR[BEST]; devb = [t for t in tb if TUNE[0] <= t["entry_date"] <= TUNE[1]]; valb = [t for t in tb if JUDGE[0] <= t["entry_date"] <= JUDGE[1]]
    res["secondary_original_stop"] = [{"test": n, "dev": diff(devb, k), "val": diff(valb, k)} for k, n in enumerate(TESTS)]

    # ---- descriptive (best version: breakouts + original stop + live gate)
    desc = {}
    for pn, (a, b) in (("dev", TUNE), ("val", JUDGE)):
        tp = [t for t in tb if a <= t["entry_date"] <= b]; yrs = (pd.Timestamp(b) - pd.Timestamp(a)).days / 365.25
        d = {"all US": profile(tp), "S&P 500": profile([t for t in tp if t["sp"]]), "non-S&P": profile([t for t in tp if not t["sp"]])}
        Rr = np.array([t["Rn"] for t in tp]); Sx = np.array([1.0 if t["sp"] else 0.0 for t in tp])
        bb, se, _ = ols_cluster(Rr, np.c_[np.ones(len(Rr)), Sx], [t["sym"] for t in tp], [t["entry_date"][:7] for t in tp])
        d["sp_minus_nonsp_meanR"] = {"est": round(float(bb[1]), 3), "se": round(float(se[1]), 3), "p": float(math.erfc(abs(bb[1] / se[1]) / math.sqrt(2)))}
        gap = {}
        for u, f in (("S&P 500", lambda t: t["sp"]), ("non-S&P", lambda t: not t["sp"])):
            tu = [t for t in tp if f(t)]; st = {}
            eq, taken = port(tu, a, b, stats=st)
            m = eq_stats(eq, spy_c, rsp_c)
            gap[u] = {"signals_per_year": round(len(tu) / yrs, 0), "trades_taken_per_year": round(len(taken) / yrs, 0),
                      "taken_share_%": round(100 * len(taken) / max(len(tu), 1), 1),
                      "mean_R_of_taken": round(float(np.mean([t["Rn"] for t in taken])), 3) if taken else None,
                      "avg_hold_days": round(float(np.mean([t["hold_days"] for t in tu])), 0),
                      "avg_stop_distance_%": round(float(np.mean([t["stop_pct"] for t in tu])), 1),
                      "avg_share_invested_%": st.get("avg_in_stocks_%"),
                      "portfolio": m}
            if pn == "val":
                yr = {}
                ser = eq.copy(); ser.index = pd.to_datetime(ser.index)
                for y, g in ser.groupby(ser.index.year):
                    sp_ = spy_c[(spy_c.index >= f"{y}-01-01") & (spy_c.index <= f"{y}-12-31")]
                    rs_ = rsp_c[(rsp_c.index >= f"{y}-01-01") & (rsp_c.index <= f"{y}-12-31")]
                    yr[int(y)] = {"strategy_%": round(100 * float(g.iloc[-1] / g.iloc[0] - 1), 1),
                                  "SPY_%": round(100 * float(sp_.iloc[-1] / sp_.iloc[0] - 1), 1), "RSP_%": round(100 * float(rs_.iloc[-1] / rs_.iloc[0] - 1), 1)}
                gap[u]["by_year"] = yr
            gap[u]["stats_raw"] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in st.items()}
        d["portfolio_gap"] = gap
        desc[pn] = d
    res["descriptive_best_version"] = desc
    json.dump(res, open(os.path.join(out, f"round8c-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(json.dumps(desc, indent=1, default=str)[:6000])
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
