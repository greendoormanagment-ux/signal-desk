"""Round 8 · session 1 — do the three fixes hold beyond the S&P 500?

Universe: every US common stock in the private EODHD download that was ever tradable (>= $5, >= $20M/day average dollar
volume, 300+ bars), delisted and acquired companies included, repaired by data_clean. A stock can be bought on a day only
if it was eligible ON THAT DAY (point in time: price, 50-day dollar volume, one year of history). Price rules only:
there is no SEC file for most of these stocks, so fundamentals are judged in a later session (nosec_pass, as in Round 6).

Three universes from the same trades: ALL US · S&P 500 members on the signal date · NON-S&P (everything else).
Grid (12): setup {breakouts + pullbacks (v2.15), breakouts only (v2.16)} × exit {A2 trail (live), original stop}
         × market {live gate, half size when the gate isn't UPTREND, only buy when SPY is above its 200-day}.
Baseline = v2.16 live rules: breakouts only + A2 trail + live gate.

Costs: 0.07% per side for every trade, plus slippage that grows as liquidity shrinks (+0.15%/side under $50M/day,
+0.05%/side $50–100M/day). Idle money sits in SPY (as in Rounds 5–6). Benchmarks: SPY and RSP (equal-weight S&P).

Statistics (colleague review): portfolio CAGR / excess vs SPY and RSP / max drawdown / Sharpe / Sortino / Calmar,
median of random same-day orders, block bootstrap of judge excess; trade level: mean and median R after costs, win rate,
95% confidence interval of the mean R with two-way clustering (by stock and by entry month) next to the naive one,
and every result split by market regime: bull, bear, sideways, high volatility.
Protocol: choose nothing on the judge years — every cell is reported, the judge period is only for checking.

Usage: python run_round8a.py UNIVERSE_PKL MEMBERS_CSV OUT_DIR
"""
import datetime as dt, json, math, os, pickle, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S
from run_systems import load_members, is_member

COST = 0.0007
TUNE, JUDGE, Y26 = ("2005-01-01", "2016-12-31"), ("2017-01-01", "2025-12-31"), ("2026-01-01", "2026-12-31")
SETUP = {"breakouts + pullbacks": {}, "breakouts only": dict(breakout_only=True)}
EXIT = {"A2 trail": {}, "original stop": dict(stop="fixed")}
MARKET = {"live gate": ({}, False), "half size if not UPTREND": ({}, True), "SPY above 200-day": (dict(mkt_mode="spy200"), False)}
BASELINE = ("breakouts only", "A2 trail", "live gate")
UNIVERSES = ("all US", "S&P 500", "non-S&P")


def extra_cost(dv):
    return 0.0015 if dv < 50 else 0.0005 if dv < 100 else 0.0


def regimes(spy):
    c = spy.c.to_numpy(float); s200 = spy.c.rolling(200).mean().to_numpy(); s200p = pd.Series(s200).shift(20).to_numpy()
    vol = pd.Series(np.log(c)).diff().rolling(20).std().to_numpy() * math.sqrt(252)
    out = {}
    for d, x, m, mp, v in zip(spy.date, c, s200, s200p, vol):
        if m != m or mp != mp:
            continue
        base = "bull" if (x > m and m > mp) else "bear" if (x < m and m < mp) else "sideways"
        out[d] = (base, bool(v == v and v > 0.25))
    return out


def clustered_ci(r, g1, g2):
    """95% CI of the mean with two-way cluster-robust SE (Cameron-Gelbach-Miller): V = V1 + V2 - V12."""
    r = np.asarray(r, float); n = len(r)
    if n < 10:
        return None
    e = r - r.mean()
    def v(groups):
        s = pd.Series(e).groupby(np.asarray(groups)).sum().to_numpy()
        return float((s ** 2).sum()) / n ** 2
    var = v(g1) + v(g2) - v([f"{a}|{b}" for a, b in zip(g1, g2)])
    var = max(var, v(g1), v(g2), 1e-12)                     # never smaller than either one-way variance
    se_naive = float(r.std(ddof=1) / math.sqrt(n))
    se = math.sqrt(var)
    return {"mean": round(float(r.mean()), 3), "lo": round(float(r.mean() - 1.96 * se), 3), "hi": round(float(r.mean() + 1.96 * se), 3),
            "lo_naive": round(float(r.mean() - 1.96 * se_naive), 3), "hi_naive": round(float(r.mean() + 1.96 * se_naive), 3),
            "se_ratio": round(se / se_naive, 2) if se_naive > 0 else None}


def trade_stats(tr, reg):
    if not tr:
        return {"n": 0}
    R = np.array([t["Rn"] for t in tr]); stock = [t["sym"] for t in tr]; month = [t["entry_date"][:7] for t in tr]
    out = {"n": len(tr), "stocks": len(set(stock)), "mean_R": round(float(R.mean()), 3), "median_R": round(float(np.median(R)), 3),
           "win_%": round(float((R > 0).mean() * 100), 1), "avg_win_R": round(float(R[R > 0].mean()), 2) if (R > 0).any() else None,
           "avg_loss_R": round(float(R[R <= 0].mean()), 2) if (R <= 0).any() else None, "ci": clustered_ci(R, stock, month)}
    by = {}
    for t in tr:
        rg = reg.get(t["signal"])
        if not rg:
            continue
        by.setdefault(rg[0], []).append(t["Rn"])
        if rg[1]:
            by.setdefault("high volatility", []).append(t["Rn"])
    out["regimes"] = {k: {"n": len(v), "mean_R": round(float(np.mean(v)), 3), "median_R": round(float(np.median(v)), 3),
                          "win_%": round(float(np.mean(np.array(v) > 0) * 100), 1)} for k, v in by.items()}
    return out


def eq_stats(eq, spy_c, rsp_c):
    m = S.perf_metrics(eq, spy_c); mr = S.perf_metrics(eq, rsp_c)
    r = eq.pct_change().dropna(); dn = r[r < 0]
    sortino = float(r.mean() / dn.std() * math.sqrt(252)) if len(dn) > 2 and dn.std() > 0 else None
    calmar = (m.get("cagr_%", 0) / abs(m["max_dd_%"])) if m.get("max_dd_%") else None
    return {"cagr": m.get("cagr_%"), "vs_spy": m.get("excess_cagr_%"), "vs_rsp": mr.get("excess_cagr_%"), "max_dd": m.get("max_dd_%"),
            "sharpe": m.get("sharpe"), "sortino": round(sortino, 2) if sortino is not None else None,
            "calmar": round(calmar, 2) if calmar is not None else None}


def main(pkl, members_csv, out):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    U = pickle.load(open(pkl, "rb"))
    prices, etf = U["prices"], U["etf"]
    members = load_members(members_csv)
    spy, qqq, rsp = etf["SPY"], etf["QQQ"], etf["RSP"]
    cal = list(spy.date); spy_c = spy.set_index("date").c; rsp_c = rsp.set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    mkt = E.market_status(spy, qqq); live = mkt["live"]
    half = lambda d: 1.0 if live.get(d) == "UPTREND" else 0.5
    spy_close = dict(zip(spy.date, spy.c)); reg = regimes(spy)
    # one stock at a time (memory): indicators → signals for each setup/market mode → trades for each exit; keep only trades
    TR = {}
    for n_s, (s, df) in enumerate(prices.items()):
        ind = E.indicators(df)
        dv = (df.v.rolling(50, min_periods=50).mean().shift(1) * df.c / 1e6).to_numpy()
        elig = (df.c.to_numpy() >= 5) & (np.nan_to_num(dv) >= 20) & (np.arange(len(df)) >= 252)
        dates = df.date.to_numpy()
        for se in SETUP:
            for mode in ("live", "spy200"):
                P0 = dict(E.BASE); P0.update(nosec_pass=True); P0.update(SETUP[se]); P0.update(mkt_mode=mode)
                sig = E.evaluate(s, df, ind, None, mkt, spy_close, P0)[["rating", "stop", "setup", "score", "market"]]
                for ex in EXIT:
                    P = dict(P0); P.update(EXIT[ex])
                    for t in E.simulate_trades(s, df, ind, sig, P, TUNE[0], Y26[1]):
                        k = int(np.searchsorted(dates, t["signal"]))
                        if not elig[k]:
                            continue
                        x = extra_cost(float(np.nan_to_num(dv[k])))
                        t["entry"] *= (1 + x); t["exit"] *= (1 - x)
                        per = t["entry"] - t["stop"]
                        if per <= 0:
                            continue
                        t["Rn"] = ((t["exit"] * (1 - COST)) - t["entry"] * (1 + COST)) / per
                        TR.setdefault((se, mode, ex), []).append(t)
        E._PIT.pop(s, None)
        if n_s % 500 == 0:
            print(f"  trades built for {n_s} stocks ({time.time()-t0:.0f}s)", flush=True)
    closes = {s: prices[s].set_index("date").c for s in prices}
    print(f"{len(prices)} stocks · indicators {time.time()-t0:.0f}s", flush=True)
    res = {"asOf": dt.date.today().isoformat(), "stocks": len(prices), "files": U["n_files"], "ever_tradable": U["n_tradable"],
           "repaired": len(U["notes"]), "dropped_unrepairable": len(U["dropped"]),
           "delisted": sum(1 for s in prices if U["status"].get(s) != "active"), "tune": TUNE, "judge": JUDGE,
           "cost_per_side": COST, "benchmarks": {}, "cells": []}
    for nm, ser in (("SPY", spy_c), ("RSP", rsp_c)):
        res["benchmarks"][nm] = {p: S.perf_metrics(ser[(ser.index >= a) & (ser.index <= b)]) for p, (a, b) in
                                 (("tune", TUNE), ("judge", JUDGE), ("2026", Y26))}

    def uni_ok(u, t):
        if u == "all US":
            return True
        m = is_member(members, t["sym"], t["signal"])
        return m if u == "S&P 500" else not m

    def port(tr, a, b, regime, seed=None):
        return E.portfolio([t for t in tr if a <= t["entry_date"] <= b], closes, cal, a, b, cost=COST, seed=seed, idle=idle,
                           risk_fn=half if regime else None)

    for se in SETUP:
        for mk_name, (mchange, regime) in MARKET.items():
            for ex in EXIT:
                tr = TR[(se, mchange.get("mkt_mode", "live"), ex)]
                for u in UNIVERSES:
                    tu = [t for t in tr if uni_ok(u, t)]
                    cell = {"universe": u, "setup": se, "exit": ex, "market": mk_name,
                            "baseline": (se, ex, mk_name) == BASELINE}
                    for pn, (a, b), nseed in (("tune", TUNE, 3), ("judge", JUDGE, 10), ("2026", Y26, 3)):
                        eq, taken = port(tu, a, b, regime)
                        runs = [eq_stats(port(tu, a, b, regime, seed=k)[0], spy_c, rsp_c) for k in range(nseed)]
                        med = lambda key: (round(float(np.median([r[key] for r in runs if r.get(key) is not None])), 2)
                                           if any(r.get(key) is not None for r in runs) else None)
                        cs = {k: med(k) for k in ("cagr", "vs_spy", "vs_rsp", "max_dd", "sharpe", "sortino", "calmar")}
                        cs["portfolio_trades"] = len(taken)
                        cs["trades"] = trade_stats([t for t in tu if a <= t["entry_date"] <= b], reg)
                        if pn == "judge":
                            cs["bootstrap_vs_spy"] = S.block_bootstrap_excess(eq, spy_c, a, b)
                        cell[pn] = cs
                    res["cells"].append(cell)
                    j, tn = cell["judge"], cell["tune"]
                    print(f"{u:8s} | {se:22s} | {ex:14s} | {mk_name:24s} | tune vs SPY {tn['vs_spy']} | judge vs SPY {j['vs_spy']} "
                          f"vs RSP {j['vs_rsp']} DD {j['max_dd']} | judge mean R {j['trades'].get('mean_R')} n={j['trades'].get('n')} "
                          f"({time.time()-t0:.0f}s)", flush=True)
                    json.dump(res, open(os.path.join(out, "round8a-partial.json"), "w"), default=str)
    json.dump(res, open(os.path.join(out, f"round8a-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
