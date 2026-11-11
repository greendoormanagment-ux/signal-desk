"""Exit ACTION rules test — pre-registered in backtest/action-rules-preregistration.md (locked 2026-11-11).

Re-simulates the exits of the SAME breakout trades under: V0 hold full · V1 warning trim (sell half the first day the app's
sellSignals() points reach >= 4) · V2 warning stop-raise (points >= 2 → stop to just under the 5-session low) · V3 earnings
trim (app's earningsCheck(): within 7 days of an SEC 8-K Item 2.02 date, gain < 0 or < expected move → sell half at the
close of the trading day before) · V4 = V1+V2+V3. Bases: A2 trail (live, primary) and original stop (secondary).

Usage: python run_round8d.py UNIVERSE_PKL MEMBERS_CSV EARN_JSON OUT_DIR
"""
import datetime as dt, json, math, os, pickle, sys, time, bisect
import numpy as np, pandas as pd
import engine as E
from run_systems import load_members, is_member
from run_round8a import COST, TUNE, JUDGE, extra_cost, eq_stats
from run_round8b import ols_cluster, holm

BASES = {"A2 trail (live)": "A2", "original stop": "fixed"}
VARIANTS = {"V0 hold full": (0, 0, 0), "V1 warning trim": (1, 0, 0), "V2 warning stop-raise": (0, 1, 0),
            "V3 earnings trim": (0, 0, 1), "V4 full ACTION box": (1, 1, 1)}
MKT_W = {"PRESSURE": 1, "CORRECTION": 2}


def warning_points(o, h, l, c, v, s50, s150, s200, avgv, mkt, ep, e_i, j):
    """index.html sellSignals() at the close of day j for a position bought at ep on bar e_i. Returns points (or None)."""
    n = j + 1
    if n < 160:
        return None
    av = avgv[j] if avgv[j] == avgv[j] else 0.0
    p = c[j]; since = n - e_i; run_start = e_i if e_i >= 1 else max(1, n - 60)
    pts = 0
    if since <= 20 and p < ep * 0.98:                                                   # failed breakout (2)
        pts += 2
    hit = False                                                                         # 50-day break on volume (2)
    for i in range(n - 3, n):
        if s50[i] == s50[i] and s50[i - 1] == s50[i - 1] and c[i] < s50[i] and c[i - 1] >= s50[i - 1] and av and v[i] > av:
            hit = True
    if hit and s50[j] == s50[j] and p < s50[j]:
        pts += 2
    run = (p / ep - 1) * 100                                                            # climax run (1)
    lo = max(run_start + 5, n - 60)
    if run >= 20 and lo < n:
        g = c[lo:n] / c[lo - 5:n - 5] - 1
        k = int(np.argmax(g)); fastest = (lo + k) >= n - 3 and g[k] * 100 >= 12
        ups = int(np.sum(c[n - 9:n] > c[n - 10:n - 1]))
        gap = any(o[i] >= h[i - 1] * 1.03 and av and v[i] >= av * 2 for i in range(n - 3, n))
        ext = s200[j] == s200[j] and (p / s200[j] - 1) * 100 >= 70
        if fastest or ups >= 7 or gap or ext:
            pts += 1
    if run_start < n:                                                                   # worst day of the move (1)
        r = c[run_start:n] / c[run_start - 1:n - 1] - 1
        k = int(np.argmin(r))
        if r[k] < 0 and (run_start + k) >= n - 3 and r[k] * 100 <= -3 and av and v[run_start + k] > av:
            pts += 1
    if av and int(np.sum((c[n - 10:n] <= c[n - 11:n - 1] * 0.998) & (v[n - 10:n] > av))) >= 3:   # distribution cluster (1)
        pts += 1
    if s150[j] == s150[j] and s150[j - 10] == s150[j - 10]:                            # stage change (2)
        if p < s150[j] and (s150[j] / s150[j - 10] - 1) * 100 <= 0.2:
            pts += 2
    pts += MKT_W.get(mkt.get(dates_g[j]), 0)                                            # market (1 / 2)
    return pts


def exp_move(o, c, j):
    """earningsCheck(): average of the 4 largest absolute opening gaps in the past 252 bars (%)."""
    a = max(1, j - 251)
    g = np.abs(o[a:j + 1] / c[a - 1:j] - 1) * 100
    if len(g) < 4:
        return None
    return float(np.mean(np.sort(g)[-4:]))


def simulate(arr, ep, orig, e_i, base, x0, pts, earn_j, trim_w, raise_w, trim_e, atr_mult=3.0):
    """Returns list of (fraction, price, bar) pieces. Replicates engine.simulate_trades exits (A2/fixed, 7.5% rule, stage 4)."""
    o, h, l, c, s50, s200, atr = arr
    n = len(c); R = ep - orig; stp = orig; hi = h[e_i]; f = 1.0; pieces = []; trimmed_w = False; extra = 0.0
    j = e_i
    while j < n:
        if j > e_i:
            lv1, lv2 = ep + R, ep + 2 * R
            if base == "A2":
                new = max(ep, hi - atr_mult * atr[j - 1]) if hi >= lv2 else (max(orig, ep) if hi >= lv1 else orig)
            else:
                new = orig
            stp = max(stp, new, extra)
            if o[j] <= stp:
                pieces.append((f, o[j], j)); return pieces
        if l[j] <= stp:
            pieces.append((f, stp, j)); return pieces
        hi = max(hi, h[j])
        if j + 1 < n:
            if c[j] <= ep * 0.925:
                pieces.append((f, o[j + 1], j + 1)); return pieces
            if c[j] < s200[j] and s50[j] < s200[j]:
                pieces.append((f, o[j + 1], j + 1)); return pieces
            p = pts.get(j)
            if trim_e and j in earn_j:                                      # earnings trim at today's close
                gain = (c[j] / ep - 1) * 100; em = exp_move(o, c, j)
                if gain < 0 or (em is not None and gain < em):
                    pieces.append((f / 2, c[j], j)); f /= 2
            if raise_w and p is not None and p >= 2:                        # warning stop-raise (effective tomorrow)
                low5 = float(np.min(l[j - 4:j + 1])); lvl = math.floor((low5 - 0.01) * 100) / 100
                if lvl < c[j] * 0.995:
                    extra = max(extra, lvl)
            if trim_w and not trimmed_w and p is not None and p >= 4:       # warning trim at tomorrow's open
                pieces.append((f / 2, o[j + 1], j + 1)); f /= 2; trimmed_w = True
        if j >= x0 and not (trim_w or raise_w or trim_e):
            break
        j += 1
    pieces.append((f, c[n - 1], n - 1))
    return pieces


def main(pkl, members_csv, earn_json, out):
    global dates_g
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    U = pickle.load(open(pkl, "rb")); prices, etf = U["prices"], U["etf"]
    members = load_members(members_csv); earn = json.load(open(earn_json))
    spy, qqq = etf["SPY"], etf["QQQ"]; cal = list(spy.date)
    spy_c = spy.set_index("date").c; rsp_c = etf["RSP"].set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    mkt = E.market_status(spy, qqq); live = mkt["live"]; spy_close = dict(zip(spy.date, spy.c))
    RES = {b: [] for b in BASES}; mism = 0; checked = 0
    for n_s, (s, df) in enumerate(prices.items()):
        ind = E.indicators(df)
        dv = (df.v.rolling(50, min_periods=50).mean().shift(1) * df.c / 1e6).to_numpy()
        elig = (df.c.to_numpy() >= 5) & (np.nan_to_num(dv) >= 20) & (np.arange(len(df)) >= 252)
        dates_g = df.date.to_numpy(); o, h, l, c, v = (df[k].to_numpy(float) for k in "ohlcv")
        s50, s200, s150, atr, avgv = ind["sma50"], ind["sma200"], ind["sma150"], ind["atr"], ind["avgv"]
        ed = earn.get(s) or []
        covered_span = (ed[0], ed[-1]) if ed else None
        earn_idx = set()
        for r in ed:                                                     # trading day before each report date
            k = int(np.searchsorted(dates_g, r)) - 1
            if k >= 0:
                earn_idx.add(k)
        P0 = dict(E.BASE); P0.update(nosec_pass=True, breakout_only=True, mkt_mode="live")
        sig = E.evaluate(s, df, ind, None, mkt, spy_close, P0)[["rating", "stop", "setup", "score", "market"]]
        for bname, bcode in BASES.items():
            P = dict(P0); P.update(stop=bcode)
            for t in E.simulate_trades(s, df, ind, sig, P, TUNE[0], JUDGE[1]):
                k = int(np.searchsorted(dates_g, t["signal"]))
                if not elig[k]:
                    continue
                e_i = int(np.searchsorted(dates_g, t["entry_date"])); x0 = int(np.searchsorted(dates_g, t["exit_date"]))
                ep, orig = t["entry"], t["stop"]
                pts = {j: warning_points(o, h, l, c, v, s50, s150, s200, avgv, live, ep, e_i, j) for j in range(e_i, min(x0 + 1, len(c)))}
                arr = (o, h, l, c, s50, s200, atr)
                x = extra_cost(float(np.nan_to_num(dv[k]))); entry = ep * (1 + x); per = entry - orig
                if per <= 0:
                    continue
                cov = bool(covered_span and covered_span[0] <= t["entry_date"] and covered_span[1] >= str(pd.Timestamp(t["exit_date"]) - pd.Timedelta(days=120))[:10])
                rec = {"sym": s, "entry_date": t["entry_date"], "exit_date": t["exit_date"], "entry": entry, "stop": orig,
                       "score": t.get("score", 0), "sp": bool(is_member(members, s, t["signal"])), "earn_cov": cov, "v": {}}
                for vn, (tw, rw, te) in VARIANTS.items():
                    pcs = simulate(arr, ep, orig, e_i, bcode, x0, pts, earn_idx if cov else set(), tw, rw, te)
                    Rv = sum(fr * (px * (1 - x) * (1 - COST) - entry * (1 + COST)) for fr, px, _ in pcs) / per
                    pxe = sum(fr * px * (1 - x) for fr, px, _ in pcs)
                    rec["v"][vn] = {"R": Rv, "exit": pxe, "exit_date": dates_g[max(b for _, _, b in pcs)], "n_pieces": len(pcs)}
                checked += 1
                if rec["v"]["V0 hold full"]["exit_date"] != t["exit_date"] or abs(rec["v"]["V0 hold full"]["exit"] / (1 - x) - t["exit"]) > 1e-6 * max(1, t["exit"]):
                    mism += 1
                RES[bname].append(rec)
        E._PIT.pop(s, None)
        if n_s % 1000 == 0:
            print(f"  {n_s} stocks ({time.time()-t0:.0f}s)", flush=True)
    print(f"V0 replication: {checked - mism}/{checked} trades identical to the engine ({mism} differ)", flush=True)
    closes = {s: prices[s].set_index("date").c for s in prices}

    def paired(recs, vn, only_cov=False):
        rs = [r for r in recs if (r["earn_cov"] or not only_cov)]
        if len(rs) < 30:
            return {"n": len(rs)}
        d = np.array([r["v"][vn]["R"] - r["v"]["V0 hold full"]["R"] for r in rs])
        b, se, _ = ols_cluster(d, np.ones((len(d), 1)), [r["sym"] for r in rs], [r["entry_date"][:7] for r in rs])
        z = b[0] / se[0] if se[0] > 0 else 0
        R0 = np.array([r["v"]["V0 hold full"]["R"] for r in rs]); Rv = np.array([r["v"][vn]["R"] for r in rs])
        top = np.argsort(R0)[-max(1, int(round(0.05 * len(R0)))):]
        return {"n": len(rs), "changed": int(np.sum(np.abs(d) > 1e-9)), "est": round(float(b[0]), 4), "se": round(float(se[0]), 4),
                "p": float(math.erfc(abs(z) / math.sqrt(2))), "mean_R_hold": round(float(R0.mean()), 3), "mean_R_variant": round(float(Rv.mean()), 3),
                "top5_kept_%": round(100 * float(Rv[top].sum() / R0[top].sum()), 1), "win_hold_%": round(100 * float((R0 > 0).mean()), 1),
                "win_variant_%": round(100 * float((Rv > 0).mean()), 1)}

    def port(recs, vn, a, b):
        tr = [{"sym": r["sym"], "entry_date": r["entry_date"], "entry": r["entry"], "stop": r["stop"], "score": r["score"],
               "exit": r["v"][vn]["exit"], "exit_date": r["v"][vn]["exit_date"]} for r in recs if a <= r["entry_date"] <= b]
        eq, _ = E.portfolio(tr, closes, cal, a, b, cost=COST, idle=idle)
        m = eq_stats(eq, spy_c, rsp_c)
        return {k: m.get(k) for k in ("cagr", "vs_spy", "max_dd", "sharpe")}

    res = {"asOf": dt.date.today().isoformat(), "prereg": "backtest/action-rules-preregistration.md",
           "earn_symbols": sum(1 for x in earn.values() if x), "replication_mismatch": mism, "bases": {}}
    for bname, recs in RES.items():
        dev = [r for r in recs if TUNE[0] <= r["entry_date"] <= TUNE[1]]; val = [r for r in recs if JUDGE[0] <= r["entry_date"] <= JUDGE[1]]
        rows = {}
        for vn in VARIANTS:
            if vn.startswith("V0"):
                continue
            oc = vn.startswith("V3")
            rows[vn] = {"dev": paired(dev, vn, oc), "val": paired(val, vn, oc)}
            rows[vn]["portfolio"] = {"dev": port(dev, vn, *TUNE), "val": port(val, vn, *JUDGE)}
        base_port = {"dev": port(dev, "V0 hold full", *TUNE), "val": port(val, "V0 hold full", *JUDGE)}
        fam = ["V1 warning trim", "V2 warning stop-raise", "V3 earnings trim"]
        for vn, a in zip(fam, holm([rows[v]["dev"].get("p", 1.0) for v in fam])):
            rows[vn]["dev"]["p_holm"] = a
        for vn in fam:
            d0, v0 = rows[vn]["dev"], rows[vn]["val"]
            if "est" not in d0 or "est" not in v0:
                rows[vn]["verdict"] = "INCONCLUSIVE"; continue
            if d0["est"] > 0 and d0["p_holm"] < 0.05 and v0["est"] > 0 and d0["top5_kept_%"] >= 90 and v0["top5_kept_%"] >= 90:
                rows[vn]["verdict"] = "KEEP"
            elif d0["est"] < 0 and d0["est"] + 1.96 * d0["se"] < 0 and v0["est"] < 0:
                rows[vn]["verdict"] = "REMOVE"
            else:
                rows[vn]["verdict"] = "INCONCLUSIVE"
        res["bases"][bname] = {"n_dev": len(dev), "n_val": len(val), "earn_covered_dev": sum(r["earn_cov"] for r in dev),
                               "earn_covered_val": sum(r["earn_cov"] for r in val), "hold_portfolio": base_port, "rows": rows}
        print(f"\n== {bname} · dev {len(dev)} · val {len(val)} · earnings-covered {res['bases'][bname]['earn_covered_dev']}/{res['bases'][bname]['earn_covered_val']}")
        print("hold full portfolio", base_port)
        for vn, r in rows.items():
            print(f"{vn:24s} {r.get('verdict','(reported)'):12s} dev {r['dev'].get('est')} ±{r['dev'].get('se')} p_holm {r['dev'].get('p_holm','-')} "
                  f"top5 kept {r['dev'].get('top5_kept_%')}% · val {r['val'].get('est')} ±{r['val'].get('se')} top5 {r['val'].get('top5_kept_%')}% "
                  f"· port dev {r['portfolio']['dev']} val {r['portfolio']['val']}", flush=True)
    json.dump(res, open(os.path.join(out, f"round8d-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


dates_g = None
if __name__ == "__main__":
    main(*sys.argv[1:5])
