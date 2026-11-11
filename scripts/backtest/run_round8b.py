"""Round 8 · session 2 — the six institutional footprints, judged by the LOCKED rules in backtest/footprint-test-rules.md.

Question: among trades the existing rules already take, do trades WITH a footprint beat trades WITHOUT it?
Existing rules (primary) = live v2.16: breakouts only + A2 trail + live market gate, all US stocks pooled,
point-in-time eligibility (>= $5, >= $20M/day, 1 year of history), costs 0.07%/side + liquidity slippage — exactly as in
Round 8 session 1. Secondary (report only, not used for pass/fail): the same with the original stop.

Footprints are computed on the signal day from completed daily bars, replicating index.html footprints() at commit 9cd4d99;
"with" = the app's ✓ reading (thresholds in the rules file).

Operational choices fixed BEFORE any result was run (the rules file leaves them open):
 - Primary statistic: difference in mean R (with − without), OLS with an indicator, two-way clustered by stock and entry
   month (Cameron-Gelbach-Miller). Two-sided p-values, Holm across the six footprints, family-wise alpha = 1%.
 - Pass/fail decisions use the development period 2005–16; 2017–25 validation must show a positive estimate.
 - Consistency (S&P / non-S&P / four regimes) uses all years 2005–25 pooled, for sample size.
 - Portfolio rule: footprint-only portfolio vs the rules-only portfolio in the development period (median of 3 random
   same-day orders): return vs SPY must be higher and max drawdown no more than 3 pp deeper. Validation reported.
 - Outcome: PASS = every rule met. FAIL = the 99% Bonferroni interval's upper end is below +0.15R (a meaningful effect
   is ruled out), or rules 1–2 are met but a later rule is clearly not met. INCONCLUSIVE = fewer than 300 trades on
   either side, or the interval still includes +0.15R without meeting rules 1–2.

Usage: python run_round8b.py UNIVERSE_PKL MEMBERS_CSV OUT_DIR
"""
import datetime as dt, json, math, os, pickle, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S
from run_systems import load_members, is_member
from run_round8a import COST, TUNE, JUDGE, extra_cost, regimes, eq_stats

FP = ["up/down volume", "accumulation/distribution", "closing strength", "pocket pivot", "volume dry-up", "biggest-volume day"]
MIN_EFFECT, ALPHA, MIN_N, DD_TOL, NEG_REGIME = 0.15, 0.01, 300, 3.0, -0.10
EXITS = {"A2 trail (live)": {}, "original stop": dict(stop="fixed")}
PRIMARY = "A2 trail (live)"


def footprints_at(o, h, l, c, v, k):
    """index.html footprints() on bars[0..k] (completed bars up to and including the signal day). Returns 6 booleans or None."""
    lo = max(0, k - 120)
    m = (v[lo:k + 1] > 0) & (c[lo:k + 1] > 0)
    H, L, C, V = h[lo:k + 1][m], l[lo:k + 1][m], c[lo:k + 1][m], v[lo:k + 1][m]
    n = len(C)
    if n < 60:
        return None
    # up/down volume, 50 sessions (each compared with the bar before it)
    w = slice(n - 50, n); cw, pw, vw = C[w], C[n - 51:n - 1], V[w]
    upV, dnV = vw[cw > pw].sum(), vw[cw < pw].sum()
    ud = upV / dnV if dnV else None
    av50 = vw.mean()
    # accumulation vs distribution days, 25 sessions
    acc = dist = 0
    for i in range(n - 25, n):
        if C[i] >= C[i - 1] * 1.002 and V[i] > av50: acc += 1
        elif C[i] <= C[i - 1] * 0.998 and V[i] > av50: dist += 1
    # pocket pivot on the most recent up day within the last 3 sessions
    pp = False
    for i in range(n - 1, n - 4, -1):
        if not C[i] > C[i - 1]:
            continue
        downs = [V[j] for j in range(i - 10, i) if C[j] < C[j - 1]]
        ma10 = C[i - 9:i + 1].mean()
        pp = bool(downs and V[i] > max(downs) and C[i] >= ma10 * 0.99)
        break
    # closing strength, 10 sessions
    hl = (H[n - 10:] > L[n - 10:]) & (L[n - 10:] > 0)
    clv = float(((C[n - 10:] - L[n - 10:]) / np.where(hl, H[n - 10:] - L[n - 10:], 1))[hl].mean()) if hl.any() else float("nan")
    dry = V[n - 10:].mean() / av50 if av50 else None
    bi = int(np.argmax(vw)); bdir_up = vw[bi] and C[n - 50 + bi] >= C[n - 51 + bi]
    bmult = vw[bi] / av50 if av50 else 0
    return [ud is not None and ud >= 1.1, acc > dist, clv == clv and clv >= 0.6, pp,
            dry is not None and dry < 0.75, bool(bdir_up and bmult >= 2)]


def ols_cluster(y, X, g1, g2):
    """OLS coefficients with two-way cluster-robust covariance (CGM), never below either one-way variance."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    XtX_inv = np.linalg.pinv(X.T @ X); b = XtX_inv @ X.T @ y; e = y - X @ b
    def meat(groups):
        s = pd.DataFrame(X * e[:, None]).groupby(np.asarray(groups)).sum().to_numpy()
        return XtX_inv @ (s.T @ s) @ XtX_inv
    V1, V2 = meat(g1), meat(g2); V12 = meat([f"{a}|{c}" for a, c in zip(g1, g2)])
    V = V1 + V2 - V12
    d = np.maximum(np.diag(V), np.maximum(np.diag(V1), np.diag(V2)))
    naive = np.diag(XtX_inv) * (e @ e) / max(len(y) - X.shape[1], 1)
    return b, np.sqrt(d), np.sqrt(naive)


def diff(tr, k):
    """with − without (footprint k) in mean R, clustered."""
    if not tr:
        return {"n_with": 0, "n_without": 0}
    R = np.array([t["Rn"] for t in tr]); D = np.array([1.0 if t["fp"][k] else 0.0 for t in tr])
    nw, nwo = int(D.sum()), int(len(D) - D.sum())
    out = {"n_with": nw, "n_without": nwo, "mean_with": round(float(R[D == 1].mean()), 3) if nw else None,
           "mean_without": round(float(R[D == 0].mean()), 3) if nwo else None}
    if nw < 30 or nwo < 30:
        return out
    b, se, se_n = ols_cluster(R, np.c_[np.ones(len(R)), D], [t["sym"] for t in tr], [t["entry_date"][:7] for t in tr])
    sd = math.sqrt(((nw - 1) * R[D == 1].var(ddof=1) + (nwo - 1) * R[D == 0].var(ddof=1)) / (nw + nwo - 2))
    z = b[1] / se[1] if se[1] > 0 else 0.0
    out.update(est=round(float(b[1]), 3), se=round(float(se[1]), 4), se_naive=round(float(se_n[1]), 4),
               p=float(math.erfc(abs(z) / math.sqrt(2))), d=round(float(b[1] / sd), 3) if sd else None)
    return out


def interaction(tr, k):
    """Direct test: is the footprint's effect different in S&P vs non-S&P stocks? (coefficient on with × S&P)"""
    R = np.array([t["Rn"] for t in tr]); D = np.array([1.0 if t["fp"][k] else 0.0 for t in tr])
    Sx = np.array([1.0 if t["sp"] else 0.0 for t in tr])
    if min(D.sum(), (1 - D).sum(), Sx.sum(), (1 - Sx).sum()) < 30:
        return None
    b, se, _ = ols_cluster(R, np.c_[np.ones(len(R)), D, Sx, D * Sx], [t["sym"] for t in tr], [t["entry_date"][:7] for t in tr])
    z = b[3] / se[3] if se[3] > 0 else 0.0
    return {"sp_minus_nonsp": round(float(b[3]), 3), "se": round(float(se[3]), 4), "p": float(math.erfc(abs(z) / math.sqrt(2)))}


def holm(ps):
    order = np.argsort(ps); m = len(ps); adj = [0.0] * m; run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * ps[i])); adj[i] = run
    return adj


def main(pkl, members_csv, out):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    U = pickle.load(open(pkl, "rb")); prices, etf = U["prices"], U["etf"]
    members = load_members(members_csv)
    spy, qqq = etf["SPY"], etf["QQQ"]
    cal = list(spy.date); spy_c = spy.set_index("date").c; rsp_c = etf["RSP"].set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    mkt = E.market_status(spy, qqq); spy_close = dict(zip(spy.date, spy.c)); reg = regimes(spy)
    TR = {ex: [] for ex in EXITS}; missing = 0
    for n_s, (s, df) in enumerate(prices.items()):
        ind = E.indicators(df)
        dv = (df.v.rolling(50, min_periods=50).mean().shift(1) * df.c / 1e6).to_numpy()
        elig = (df.c.to_numpy() >= 5) & (np.nan_to_num(dv) >= 20) & (np.arange(len(df)) >= 252)
        dates = df.date.to_numpy(); O, H, L, C, V = (df[k].to_numpy(float) for k in "ohlcv")
        P0 = dict(E.BASE); P0.update(nosec_pass=True, breakout_only=True, mkt_mode="live")
        sig = E.evaluate(s, df, ind, None, mkt, spy_close, P0)[["rating", "stop", "setup", "score", "market"]]
        for ex, chg in EXITS.items():
            P = dict(P0); P.update(chg)
            for t in E.simulate_trades(s, df, ind, sig, P, TUNE[0], JUDGE[1]):
                k = int(np.searchsorted(dates, t["signal"]))
                if not elig[k]:
                    continue
                x = extra_cost(float(np.nan_to_num(dv[k])))
                entry, exitp = t["entry"] * (1 + x), t["exit"] * (1 - x); per = entry - t["stop"]
                if per <= 0:
                    continue
                fp = footprints_at(O, H, L, C, V, k)
                if fp is None:
                    missing += 1; continue
                rg = reg.get(t["signal"])
                TR[ex].append({"sym": s, "signal": t["signal"], "entry_date": t["entry_date"], "exit_date": t.get("exit_date"),
                               "entry": entry, "exit": exitp, "stop": t["stop"], "score": t.get("score", 0), "shares_hint": t.get("shares_hint"),
                               "Rn": ((exitp * (1 - COST)) - entry * (1 + COST)) / per, "fp": fp,
                               "sp": bool(is_member(members, s, t["signal"])), "regime": rg[0] if rg else None, "hv": bool(rg and rg[1]),
                               **{kk: vv for kk, vv in t.items() if kk not in ("entry", "exit", "stop", "Rn")}})
        E._PIT.pop(s, None)
        if n_s % 1000 == 0:
            print(f"  {n_s} stocks ({time.time()-t0:.0f}s)", flush=True)
    closes = {s: prices[s].set_index("date").c for s in prices}
    print(f"trades: {{{', '.join(f'{k}: {len(v)}' for k, v in TR.items())}}} · no footprint (short history) {missing} · {time.time()-t0:.0f}s", flush=True)

    def port(tr, a, b, seed):
        return E.portfolio([t for t in tr if a <= t["entry_date"] <= b], closes, cal, a, b, cost=COST, seed=seed, idle=idle)[0]

    def pstats(tr, a, b):
        runs = [eq_stats(port(tr, a, b, k), spy_c, rsp_c) for k in range(3)]
        return {k: round(float(np.median([r[k] for r in runs if r.get(k) is not None])), 2) for k in ("cagr", "vs_spy", "vs_rsp", "max_dd", "sharpe")}

    res = {"asOf": dt.date.today().isoformat(), "rules": "backtest/footprint-test-rules.md (locked 2026-11-06)", "primary": PRIMARY,
           "tune": TUNE, "judge": JUDGE, "footprints": FP, "exits": {}}
    for ex, tr in TR.items():
        dev = [t for t in tr if TUNE[0] <= t["entry_date"] <= TUNE[1]]
        val = [t for t in tr if JUDGE[0] <= t["entry_date"] <= JUDGE[1]]
        base_dev, base_val = (pstats(dev, *TUNE), pstats(val, *JUDGE)) if ex == PRIMARY else (None, None)
        rows = []
        for k, name in enumerate(FP):
            r = {"footprint": name, "share_with_%": round(100 * float(np.mean([t["fp"][k] for t in tr])), 1),
                 "dev": diff(dev, k), "val": diff(val, k)}
            r["sp"] = diff([t for t in tr if t["sp"]], k); r["nonsp"] = diff([t for t in tr if not t["sp"]], k)
            r["interaction"] = interaction(tr, k)
            r["regimes"] = {g: diff([t for t in tr if (t["regime"] == g if g != "high volatility" else t["hv"])], k)
                            for g in ("bull", "bear", "sideways", "high volatility")}
            if ex == PRIMARY:
                r["portfolio"] = {"dev_with": pstats([t for t in dev if t["fp"][k]], *TUNE), "dev_rules_only": base_dev,
                                  "val_with": pstats([t for t in val if t["fp"][k]], *JUDGE), "val_rules_only": base_val}
            rows.append(r)
        ps = [r["dev"].get("p", 1.0) for r in rows]
        for r, a in zip(rows, holm(ps)):
            r["dev"]["p_holm"] = a
        zb = 3.144  # two-sided 99% Bonferroni over 6 tests (alpha 0.01/6)
        for r in rows:
            d0 = r["dev"]; reasons = []
            if d0.get("n_with", 0) < MIN_N or d0.get("n_without", 0) < MIN_N or "est" not in d0:
                r["verdict"], r["why"] = "INCONCLUSIVE", "fewer than 300 trades on one side"; continue
            d0["ci99_bonf"] = [round(d0["est"] - zb * d0["se"], 3), round(d0["est"] + zb * d0["se"], 3)]
            stat_ok = d0["est"] >= MIN_EFFECT and d0["p_holm"] < ALPHA and d0["est"] > 0
            if not stat_ok:
                if d0["ci99_bonf"][1] < MIN_EFFECT:
                    r["verdict"], r["why"] = "FAIL", f"a +{MIN_EFFECT}R effect is ruled out (99% upper end {d0['ci99_bonf'][1]:+.3f}R)"
                else:
                    r["verdict"], r["why"] = "INCONCLUSIVE", "interval still includes +0.15R but the effect is not established"
                continue
            if not (r["val"].get("est", -1) > 0): reasons.append("validation effect not positive")
            if not (r["sp"].get("est", -1) > 0 and r["nonsp"].get("est", -1) > 0): reasons.append("not positive in both S&P and non-S&P")
            rg = [x.get("est") for x in r["regimes"].values() if x.get("est") is not None]
            if sum(e > 0 for e in rg) < 3 or any(e < NEG_REGIME for e in rg): reasons.append("regime consistency")
            if "portfolio" in r:
                pw, pb = r["portfolio"]["dev_with"], r["portfolio"]["dev_rules_only"]
                if not (pw["vs_spy"] > pb["vs_spy"] and pw["max_dd"] >= pb["max_dd"] - DD_TOL): reasons.append("portfolio vs SPY / drawdown")
            r["verdict"], r["why"] = ("PASS", "every rule met") if not reasons else ("FAIL", "; ".join(reasons))
        res["exits"][ex] = {"n_dev": len(dev), "n_val": len(val), "rules_only_dev": base_dev, "rules_only_val": base_val, "rows": rows}
        print(f"\n== {ex} · dev n={len(dev)} · val n={len(val)}", flush=True)
        for r in rows:
            d0, v0 = r["dev"], r["val"]
            print(f"{r['footprint']:26s} {r.get('verdict','-'):12s} dev {d0.get('est')} (p_holm {d0.get('p_holm', float('nan')):.3g}, "
                  f"n {d0.get('n_with')}/{d0.get('n_without')}) · val {v0.get('est')} · {r.get('why')}", flush=True)
    json.dump(res, open(os.path.join(out, f"round8b-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
