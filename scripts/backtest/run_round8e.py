"""Market gate test — pre-registered in backtest/market-gate-preregistration.md (locked 2026-11-11).
G0 = buys allowed in UPTREND or PRESSURE (backtest default) · G1 = UPTREND only (live app rule, engine block_pressure=True).
Usage: python run_round8e.py UNIVERSE_PKL MEMBERS_CSV OUT_DIR
"""
import datetime as dt, json, math, os, pickle, sys, time
import numpy as np, pandas as pd
import engine as E
from run_round8a import COST, TUNE, JUDGE, extra_cost, eq_stats
from run_round8b import ols_cluster

GATES = {"G0 UPTREND or PRESSURE": False, "G1 UPTREND only": True}
STOPS = {"A2 trail (live)": "A2", "original stop": "fixed"}


def main(pkl, members_csv, out):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    U = pickle.load(open(pkl, "rb")); prices, etf = U["prices"], U["etf"]
    spy, qqq = etf["SPY"], etf["QQQ"]; cal = list(spy.date)
    spy_c = spy.set_index("date").c; rsp_c = etf["RSP"].set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    mkt = E.market_status(spy, qqq); spy_close = dict(zip(spy.date, spy.c))
    TR = {(g, s): [] for g in GATES for s in STOPS}
    for n_s, (sym, df) in enumerate(prices.items()):
        ind = E.indicators(df)
        dv = (df.v.rolling(50, min_periods=50).mean().shift(1) * df.c / 1e6).to_numpy()
        elig = (df.c.to_numpy() >= 5) & (np.nan_to_num(dv) >= 20) & (np.arange(len(df)) >= 252)
        dates = df.date.to_numpy()
        for g, block in GATES.items():
            P0 = dict(E.BASE); P0.update(nosec_pass=True, breakout_only=True, mkt_mode="live", block_pressure=block)
            sig = E.evaluate(sym, df, ind, None, mkt, spy_close, P0)[["rating", "stop", "setup", "score", "market"]]
            for sn, sc in STOPS.items():
                P = dict(P0); P.update(stop=sc)
                for t in E.simulate_trades(sym, df, ind, sig, P, TUNE[0], JUDGE[1]):
                    k = int(np.searchsorted(dates, t["signal"]))
                    if not elig[k]:
                        continue
                    x = extra_cost(float(np.nan_to_num(dv[k])))
                    t["entry"] *= (1 + x); t["exit"] *= (1 - x); per = t["entry"] - t["stop"]
                    if per <= 0:
                        continue
                    t["Rn"] = ((t["exit"] * (1 - COST)) - t["entry"] * (1 + COST)) / per
                    TR[(g, sn)].append(t)
        E._PIT.pop(sym, None)
        if n_s % 1000 == 0:
            print(f"  {n_s} stocks ({time.time()-t0:.0f}s)", flush=True)
    closes = {s: prices[s].set_index("date").c for s in prices}
    live = mkt["live"]
    share_p = {pn: round(100 * float(np.mean([live.get(d) == "PRESSURE" for d in cal if a <= d <= b])), 1) for pn, (a, b) in (("dev", TUNE), ("val", JUDGE))}

    def pstats(tr, a, b):
        runs = [eq_stats(E.portfolio([t for t in tr if a <= t["entry_date"] <= b], closes, cal, a, b, cost=COST, seed=k, idle=idle)[0], spy_c, rsp_c) for k in range(10)]
        return {k: round(float(np.median([r[k] for r in runs if r.get(k) is not None])), 2) for k in ("cagr", "vs_spy", "max_dd", "sharpe")}

    def mean_ci(tr):
        if len(tr) < 30:
            return {"n": len(tr)}
        R = np.array([t["Rn"] for t in tr])
        b, se, _ = ols_cluster(R, np.ones((len(R), 1)), [t["sym"] for t in tr], [t["entry_date"][:7] for t in tr])
        return {"n": len(R), "mean_R": round(float(b[0]), 3), "lo": round(float(b[0] - 1.96 * se[0]), 3), "hi": round(float(b[0] + 1.96 * se[0]), 3)}

    res = {"asOf": dt.date.today().isoformat(), "prereg": "backtest/market-gate-preregistration.md", "pressure_day_share_%": share_p, "stops": {}}
    for sn in STOPS:
        r = {}
        for pn, (a, b) in (("dev", TUNE), ("val", JUDGE)):
            g0 = [t for t in TR[("G0 UPTREND or PRESSURE", sn)] if a <= t["entry_date"] <= b]
            g1 = [t for t in TR[("G1 UPTREND only", sn)] if a <= t["entry_date"] <= b]
            r[pn] = {"G0": pstats(g0, a, b), "G1": pstats(g1, a, b), "n_G0": len(g0), "n_G1": len(g1),
                     "pressure_entries": mean_ci([t for t in g0 if t.get("market") == "PRESSURE"]),
                     "uptrend_entries": mean_ci([t for t in g0 if t.get("market") == "UPTREND"])}
        d, v = r["dev"], r["val"]
        dc = [d["G0"]["cagr"] - d["G1"]["cagr"], v["G0"]["cagr"] - v["G1"]["cagr"]]
        if dc[0] >= 1.0 and dc[1] >= 1.0 and d["pressure_entries"].get("lo", -1) > 0 and v["pressure_entries"].get("mean_R", -1) > 0:
            verdict = "ALLOW PRESSURE (G0)"
        elif dc[0] <= 0.5 and dc[1] <= 0.5 and d["G1"]["max_dd"] >= d["G0"]["max_dd"] + 2 and v["G1"]["max_dd"] >= v["G0"]["max_dd"] + 2:
            verdict = "KEEP UPTREND-ONLY (G1)"
        else:
            verdict = "INCONCLUSIVE"
        r["cagr_G0_minus_G1"] = [round(x, 2) for x in dc]; r["verdict"] = verdict
        res["stops"][sn] = r
        print(f"\n== {sn}: {verdict} · CAGR G0−G1 dev {dc[0]:+.2f} val {dc[1]:+.2f}")
        for pn in ("dev", "val"):
            print(f"  {pn}: G0 {r[pn]['G0']} n={r[pn]['n_G0']} | G1 {r[pn]['G1']} n={r[pn]['n_G1']}")
            print(f"       PRESSURE entries {r[pn]['pressure_entries']} | UPTREND entries {r[pn]['uptrend_entries']}")
    print("PRESSURE share of days", share_p)
    json.dump(res, open(os.path.join(out, f"round8e-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
