"""Round 8 · session 3 — the live BUY rules, pre-registered in backtest/buy-rules-preregistration.md (locked 2026-11-16).
T1 fundamentals block (EPS / sales / operating income) · T2 14-day earnings block · T3 breakout definition grid ·
T4 24-hour rule · T5 earnings gap as its own entry setup.
Base: breakouts only + live gate, all US, point-in-time eligibility, Round 8 costs. A2 trail = primary, original stop = secondary.
SEC_DIR holds one {sym}.json.gz per stock (EPS / revenue / operating income facts with filing dates + 8-K 2.02 dates).

Usage: python run_round8f.py UNIVERSE_PKL SEC_DIR OUT_DIR
"""
import bisect, datetime as dt, gzip, json, math, os, pickle, sys, time
import numpy as np, pandas as pd
import engine as E
from run_round8a import COST, TUNE, JUDGE, extra_cost, eq_stats
from run_round8b import ols_cluster, holm

STOPS = {"A2 trail (live)": "A2", "original stop": "fixed"}
PRIMARY = "A2 trail (live)"
VOLS, EXTS, CHAMP = (1.2, 1.4, 1.6, 2.0), (3.0, 5.0, 8.0), (1.4, 5.0)
PERIODS = (("dev", TUNE), ("val", JUDGE))
MIN_N = 300


def load_sec(sec_dir, sym):
    p = os.path.join(sec_dir, f"{sym}.json.gz")
    if not os.path.exists(p):
        return None
    rec = json.load(gzip.open(p, "rt"))
    return {"eps": E.fundamentals_timeline(rec, "eps", E.EPS_TAGS), "rev": E.fundamentals_timeline(rec, "rev", E.REV_TAGS),
            "op": E.fundamentals_timeline(rec, "opinc", ["OperatingIncomeLoss"]), "earn": rec.get("earn") or []}


def growth_at(tl, fd, d, profit_rule):
    """Reading as filed by day d (engine.point_in_time math). nan = no usable reading (none, or quarter older than 135 days)."""
    j = bisect.bisect_right(fd, d) - 1
    if j < 0:
        return float("nan")
    _, qe, a, b = tl[j]
    if E._days(qe, d) > 135:
        return float("nan")
    if profit_rule:
        return -np.inf if a <= 0 else 999.0 if b <= 0 else (a - b) / b * 100
    return (a - b) / b * 100 if b and b > 0 else float("nan")


def edays_at(er, d):
    j = bisect.bisect_left(er, d)
    if j < len(er):
        k = E._days(d, er[j])
        return k if k <= 100 else None
    return None


def mean_ci(tr):
    if len(tr) < 30:
        return {"n": len(tr)}
    R = np.array([t["Rn"] for t in tr])
    b, se, _ = ols_cluster(R, np.ones((len(R), 1)), [t["sym"] for t in tr], [t["entry_date"][:7] for t in tr])
    return {"n": len(R), "mean_R": round(float(b[0]), 3), "lo": round(float(b[0] - 1.96 * se[0]), 3), "hi": round(float(b[0] + 1.96 * se[0]), 3),
            "win_%": round(100 * float((R > 0).mean()), 1)}


def diff_flag(tr, flag):
    """mean R of flag=True minus flag=False, two-way clustered."""
    R = np.array([t["Rn"] for t in tr]); D = np.array([1.0 if f else 0.0 for f in flag])
    n1, n0 = int(D.sum()), int(len(D) - D.sum())
    out = {"n_yes": n1, "n_no": n0, "mean_yes": round(float(R[D == 1].mean()), 3) if n1 else None,
           "mean_no": round(float(R[D == 0].mean()), 3) if n0 else None}
    if n1 < 30 or n0 < 30:
        return out
    b, se, _ = ols_cluster(R, np.c_[np.ones(len(R)), D], [t["sym"] for t in tr], [t["entry_date"][:7] for t in tr])
    z = b[1] / se[1] if se[1] > 0 else 0.0
    out.update(est=round(float(b[1]), 3), se=round(float(se[1]), 4), lo=round(float(b[1] - 1.96 * se[1]), 3),
               hi=round(float(b[1] + 1.96 * se[1]), 3), p=float(math.erfc(abs(z) / math.sqrt(2))))
    return out


def inp(t, ab):
    return ab[0] <= t["entry_date"] <= ab[1]


def main(pkl, sec_dir, out):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    U = pickle.load(open(pkl, "rb")); prices, etf = U["prices"], U["etf"]
    spy, qqq = etf["SPY"], etf["QQQ"]; cal = list(spy.date)
    spy_c = spy.set_index("date").c; rsp_c = etf["RSP"].set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    mkt = E.market_status(spy, qqq); live = mkt["live"]; spy_close = dict(zip(spy.date, spy.c))
    GRID = {(v, x, s): [] for v in VOLS for x in EXTS for s in STOPS}       # T3 (champion cell = the base for T1, T2, T4)
    W1 = {s: [] for s in STOPS}                                               # T4
    GAP = {s: [] for s in STOPS}; POOL = {s: [] for s in STOPS}               # T5
    n_sec = 0
    for n_s, (sym, df) in enumerate(prices.items()):
        ind = E.indicators(df)
        o, h, l, c, v = (df[k].to_numpy(float) for k in ("o", "h", "l", "c", "v"))
        dv = (df.v.rolling(50, min_periods=50).mean().shift(1) * df.c / 1e6).to_numpy()
        elig = (c >= 5) & (np.nan_to_num(dv) >= 20) & (np.arange(len(df)) >= 252)
        dates = df.date.to_numpy(); n = len(df)
        sec = load_sec(sec_dir, sym); n_sec += bool(sec)
        fd = {k: [r[0] for r in sec[k]] for k in ("eps", "rev", "op")} if sec else None

        def finish(t, extra=None):
            k = int(np.searchsorted(dates, t["signal"]))
            if not elig[k]:
                return None
            x = extra_cost(float(np.nan_to_num(dv[k])))
            t["entry"] *= (1 + x); t["exit"] *= (1 - x); per = t["entry"] - t["stop"]
            if per <= 0:
                return None
            t["Rn"] = ((t["exit"] * (1 - COST)) - t["entry"] * (1 + COST)) / per
            t["k"] = k
            if extra:
                extra(t, k)
            return t

        sigs = {}
        for vn in VOLS:
            for xe in EXTS:
                P0 = dict(E.BASE); P0.update(nosec_pass=True, breakout_only=True, mkt_mode="live", vol_need=vn, max_ext=xe)
                sig = E.evaluate(sym, df, ind, None, mkt, spy_close, P0)[["rating", "stop", "setup", "score", "market", "bo_vr", "ext"]]
                sigs[(vn, xe)] = sig
                bo_vr, ext = sig.bo_vr.to_numpy(), sig.ext.to_numpy(); rating = sig.rating.to_numpy()

                def tag(t, k, champ=(vn, xe) == CHAMP):
                    t["bo_vr"] = float(bo_vr[k]); t["ext"] = float(ext[k])
                    if champ:
                        t["conf"] = bool(k + 1 < n and rating[k + 1] == "BUY")
                        if sec:
                            d = t["signal"]
                            t["g_eps"] = growth_at(sec["eps"], fd["eps"], d, True)
                            t["g_rev"] = growth_at(sec["rev"], fd["rev"], d, False)
                            t["g_op"] = growth_at(sec["op"], fd["op"], d, True)
                            t["edays"] = edays_at(sec["earn"], d)
                            t["has_earn"] = bool(sec["earn"])
                for sn, sc in STOPS.items():
                    P = dict(P0); P.update(stop=sc)
                    for t in E.simulate_trades(sym, df, ind, sig, P, TUNE[0], JUDGE[1]):
                        t = finish(t, tag)
                        if t:
                            GRID[(vn, xe, sn)].append(t)
        base = sigs[CHAMP]; P0 = dict(E.BASE); P0.update(nosec_pass=True, breakout_only=True, mkt_mode="live")
        r0 = base.rating.to_numpy()
        # T4: BUY only when yesterday's close was also a BUY (signal, rescan, then buy the following open)
        s1 = base.copy(); r1 = r0.copy()
        prev_buy = np.r_[False, r0[:-1] == "BUY"]
        r1[(r0 == "BUY") & ~prev_buy] = "CHECK_FIRST"; s1["rating"] = r1
        for sn, sc in STOPS.items():
            P = dict(P0); P.update(stop=sc)
            for t in E.simulate_trades(sym, df, ind, s1, P, TUNE[0], JUDGE[1]):
                t = finish(t)
                if t:
                    W1[sn].append(t)
        # T5: earnings gap as its own entry setup (only stocks with SEC earnings dates)
        if sec and sec["earn"]:
            er = set(sec["earn"]); isE = np.array([d in er for d in dates]); near = isE | np.r_[False, isE[:-1]]
            pc = np.r_[np.nan, c[:-1]]; avgv = ind["avgv"]; rng = h - l
            mk = np.array([live.get(d, "UNKNOWN") for d in dates])
            gap = (near & (o >= pc * 1.04) & (v >= 2 * np.nan_to_num(avgv, nan=np.inf)) & (rng > 0) & ((c - l) >= 0.5 * rng)
                   & (c > ind["sma50"]) & (c > ind["sma200"]) & (mk != "CORRECTION") & (mk != "UNKNOWN") & ~np.isnan(ind["atr"]))
            gstop = np.maximum(l, c * 0.92)
            sg = base.copy(); rg = np.where(gap, "BUY", "DONT_BUY").astype(object); rg[r0 == "SELL"] = "SELL"; rg[r0 == "NA"] = "NA"
            sg["rating"] = rg; sg["stop"] = np.where(gap, gstop, np.nan); sg["setup"] = np.where(gap, "EGAP", "NONE")
            sp = base.copy(); rp = r0.copy(); only = gap & (r0 != "BUY") & (r0 != "SELL") & (r0 != "NA")
            rp[only] = "BUY"; sp["rating"] = rp; sp["stop"] = np.where(only, gstop, base.stop.to_numpy())
            sp["setup"] = np.where(only, "EGAP", base.setup.to_numpy())
            for sn, sc in STOPS.items():
                P = dict(P0); P.update(stop=sc)
                for t in E.simulate_trades(sym, df, ind, sg, P, TUNE[0], JUDGE[1]):
                    t = finish(t, lambda t, k: t.update(also_bo=bool(r0[k] == "BUY")))
                    if t:
                        GAP[sn].append(t)
                for t in E.simulate_trades(sym, df, ind, sp, P, TUNE[0], JUDGE[1]):
                    t = finish(t)
                    if t:
                        POOL[sn].append(t)
        E._PIT.pop(sym, None)
        if n_s % 500 == 0:
            print(f"  {n_s} stocks ({time.time()-t0:.0f}s)", flush=True)
    closes = {s: prices[s].set_index("date").c for s in prices}
    print(f"trades built · {n_sec} stocks with an SEC file · {time.time()-t0:.0f}s", flush=True)

    def pstats(tr, ab, seeds=10):
        a, b = ab
        runs = [eq_stats(E.portfolio([t for t in tr if a <= t["entry_date"] <= b], closes, cal, a, b, cost=COST, seed=k, idle=idle)[0], spy_c, rsp_c)
                for k in range(seeds)]
        return {k: round(float(np.median([r[k] for r in runs if r.get(k) is not None])), 2) for k in ("cagr", "vs_spy", "max_dd", "sharpe")}

    res = {"asOf": dt.date.today().isoformat(), "prereg": "backtest/buy-rules-preregistration.md", "stocks": len(prices), "stocks_with_sec": n_sec}

    # ───── T1 + T2 (with-vs-without on the base trades) ─────
    def fam(sn):
        tr = GRID[CHAMP + (sn,)]
        tests = {
            "E1 official EPS growth >= 25%": ("g_eps", lambda t: t["g_eps"] >= 25),
            "E2 sales growth >= 25%": ("g_rev", lambda t: t["g_rev"] >= 25),
            "E3 operating income growth >= 25%": ("g_op", lambda t: t["g_op"] >= 25),
            "T2 outside the 14-day earnings window": ("edays", lambda t: t["edays"] > 14),
        }
        outp = {"base_trades": {pn: len([t for t in tr if inp(t, ab)]) for pn, ab in PERIODS}, "tests": {}}
        for name, (key, fn) in tests.items():
            cov = [t for t in tr if t.get(key) is not None and t[key] == t[key]]
            r = {"covered": {pn: len([t for t in cov if inp(t, ab)]) for pn, ab in PERIODS}}
            for pn, ab in PERIODS:
                x = [t for t in cov if inp(t, ab)]
                r[pn] = diff_flag(x, [fn(t) for t in x]) if x else {"n_yes": 0, "n_no": 0}
                r[pn + "_portfolio"] = {"with_rule": pstats([t for t in x if fn(t)], ab), "without_rule": pstats(x, ab)}
            outp["tests"][name] = r
        for (name, r), a in zip(outp["tests"].items(), holm([r["dev"].get("p", 1.0) for r in outp["tests"].values()])):
            d, v = r["dev"], r["val"]; d["p_holm"] = a
            enough = min(d["n_yes"], d["n_no"], v["n_yes"], v["n_no"]) >= MIN_N
            if enough and d.get("est", 0) > 0 and a < 0.05 and v.get("est", 0) > 0:
                r["verdict"] = "EARNS ITS PLACE"
            elif d.get("est", 0) < 0 and d.get("hi", 1) < 0 and v.get("est", 0) < 0:
                r["verdict"] = "HURTS"
            else:
                r["verdict"] = "INCONCLUSIVE"
        # reported: EPS buckets, official-fails-but-operating-passes, earnings windows
        def bucket(g):
            return ("unprofitable" if g == -np.inf else "loss to profit" if g == 999 else "below 0" if g < 0 else "0-25" if g < 25
                    else "25-50" if g < 50 else "50-100" if g < 100 else "over 100")
        outp["eps_buckets"] = {}; outp["earn_buckets"] = {}; outp["berkshire"] = {}; outp["earn_windows"] = {}
        for pn, ab in PERIODS:
            x = [t for t in tr if inp(t, ab) and t.get("g_eps") is not None and t["g_eps"] == t["g_eps"]]
            by = {}
            for t in x:
                by.setdefault(bucket(t["g_eps"]), []).append(t)
            outp["eps_buckets"][pn] = {k: mean_ci(v) for k, v in by.items()}
            both = [t for t in x if t["g_op"] == t["g_op"]]
            outp["berkshire"][pn] = {"EPS fails, operating passes": mean_ci([t for t in both if t["g_eps"] < 25 and t["g_op"] >= 25]),
                                     "both fail": mean_ci([t for t in both if t["g_eps"] < 25 and t["g_op"] < 25]),
                                     "both pass": mean_ci([t for t in both if t["g_eps"] >= 25 and t["g_op"] >= 25]),
                                     "EPS passes, operating fails": mean_ci([t for t in both if t["g_eps"] >= 25 and t["g_op"] < 25])}
            x = [t for t in tr if inp(t, ab) and t.get("edays") is not None]
            eb = lambda k: "0-3" if k <= 3 else "4-7" if k <= 7 else "8-14" if k <= 14 else "15-30" if k <= 30 else "31+"
            by = {}
            for t in x:
                by.setdefault(eb(t["edays"]), []).append(t)
            outp["earn_buckets"][pn] = {k: mean_ci(v) for k, v in by.items()}
            outp["earn_windows"][pn] = {f"outside {w} days": diff_flag(x, [t["edays"] > w for t in x]) for w in (7, 21)}
        return outp

    res["T1_T2"] = {sn: fam(sn) for sn in STOPS}
    for sn in STOPS:
        print(f"\n== T1/T2 · {sn}")
        for name, r in res["T1_T2"][sn]["tests"].items():
            d, v = r["dev"], r["val"]
            print(f"  {name:40s} {r['verdict']:16s} dev {d.get('est')} [{d.get('lo')},{d.get('hi')}] p_holm {d.get('p_holm'):.4f} n {d['n_yes']}/{d['n_no']}"
                  f" · val {v.get('est')} [{v.get('lo')},{v.get('hi')}] n {v['n_yes']}/{v['n_no']}")
            print(f"      portfolio dev with {r['dev_portfolio']['with_rule']} without {r['dev_portfolio']['without_rule']}")
            print(f"      portfolio val with {r['val_portfolio']['with_rule']} without {r['val_portfolio']['without_rule']}")
    print(f"T1/T2 done {time.time()-t0:.0f}s", flush=True)

    # ───── T3 breakout definition grid ─────
    res["T3"] = {}
    for sn in STOPS:
        cells = {}
        for vn in VOLS:
            for xe in EXTS:
                tr = GRID[(vn, xe, sn)]
                cells[f"{vn}x / {xe:.0f}%"] = {pn: dict(pstats([t for t in tr if inp(t, ab)], ab), **{"trades": mean_ci([t for t in tr if inp(t, ab)])})
                                               for pn, ab in PERIODS}
        ck = f"{CHAMP[0]}x / {CHAMP[1]:.0f}%"; ch = cells[ck]; qual = []
        for k, cl in cells.items():
            if k == ck:
                continue
            ok = all(cl[p]["cagr"] >= ch[p]["cagr"] + 1.0 and cl[p]["max_dd"] >= ch[p]["max_dd"] - 2.0
                     and cl[p]["trades"].get("mean_R", -9) >= ch[p]["trades"].get("mean_R", 9) for p in ("dev", "val"))
            cl["qualifies"] = ok
            if ok:
                qual.append(k)
        winner = max(qual, key=lambda k: cells[k]["dev"]["cagr"]) if qual else None
        loose = GRID[(1.2, 8.0, sn)]; bk = {}
        for pn, ab in PERIODS:
            x = [t for t in loose if inp(t, ab)]
            vb = lambda r: "1.2-1.4x" if r < 1.4 else "1.4-1.6x" if r < 1.6 else "1.6-2.0x" if r < 2.0 else "2.0-3.0x" if r < 3.0 else "3.0x+"
            xb = lambda e: "0-1%" if e < 1 else "1-3%" if e < 3 else "3-5%" if e < 5 else "5-8%"
            b1, b2 = {}, {}
            for t in x:
                b1.setdefault(vb(t["bo_vr"]), []).append(t); b2.setdefault(xb(t["ext"]), []).append(t)
            bk[pn] = {"by_volume": {k: mean_ci(v) for k, v in sorted(b1.items())}, "by_extension": {k: mean_ci(v) for k, v in sorted(b2.items())}}
        res["T3"][sn] = {"cells": cells, "champion": ck, "qualifiers": qual, "verdict": f"REPLACE with {winner}" if winner else "CHAMPION STAYS",
                         "buckets_in_loosest_cell": bk}
        print(f"\n== T3 · {sn}: {res['T3'][sn]['verdict']} (qualifiers {qual})")
        for k, cl in cells.items():
            print(f"  {k:12s} dev cagr {cl['dev']['cagr']} dd {cl['dev']['max_dd']} R {cl['dev']['trades'].get('mean_R')} n {cl['dev']['trades']['n']}"
                  f" | val cagr {cl['val']['cagr']} dd {cl['val']['max_dd']} R {cl['val']['trades'].get('mean_R')} n {cl['val']['trades']['n']}")
        print(f"  T3 {sn} done {time.time()-t0:.0f}s", flush=True)

    # ───── T4 24-hour rule ─────
    res["T4"] = {}
    for sn in STOPS:
        w0, w1 = GRID[CHAMP + (sn,)], W1[sn]; r = {}
        for pn, ab in PERIODS:
            a = [t for t in w0 if inp(t, ab)]; b = [t for t in w1 if inp(t, ab)]
            r[pn] = {"diff_W1_minus_W0": diff_flag(b + a, [True] * len(b) + [False] * len(a)), "W0": pstats(a, ab), "W1": pstats(b, ab),
                     "share_still_BUY_next_day_%": round(100 * float(np.mean([t["conf"] for t in a])), 1) if a else None,
                     "W0_trades_not_confirmed": mean_ci([t for t in a if not t["conf"]]), "W0_trades_confirmed": mean_ci([t for t in a if t["conf"]])}
        d, v = r["dev"]["diff_W1_minus_W0"], r["val"]["diff_W1_minus_W0"]
        dc = [r[p]["W1"]["cagr"] - r[p]["W0"]["cagr"] for p in ("dev", "val")]
        if d.get("est", 0) > 0 and d.get("lo", -1) > 0 and v.get("est", 0) > 0 and min(dc) >= -0.5:
            verdict = "EARNS ITS PLACE"
        elif (d.get("est", 0) < 0 and d.get("hi", 1) < 0 and v.get("est", 0) < 0) or max(dc) <= -1.0:
            verdict = "HURTS"
        else:
            verdict = "INCONCLUSIVE"
        r["cagr_W1_minus_W0"] = [round(x, 2) for x in dc]; r["verdict"] = verdict; res["T4"][sn] = r
        print(f"\n== T4 · {sn}: {verdict} · R diff dev {d.get('est')} [{d.get('lo')},{d.get('hi')}] val {v.get('est')} · CAGR W1−W0 {r['cagr_W1_minus_W0']}")
        for pn in ("dev", "val"):
            print(f"  {pn}: W0 {r[pn]['W0']} | W1 {r[pn]['W1']} | still BUY next day {r[pn]['share_still_BUY_next_day_%']}% | skipped {r[pn]['W0_trades_not_confirmed']}")
    print(f"T4 done {time.time()-t0:.0f}s", flush=True)

    # ───── T5 earnings gap as its own setup ─────
    res["T5"] = {}
    for sn in STOPS:
        base_cov = [t for t in GRID[CHAMP + (sn,)] if t.get("has_earn")]; r = {}
        for pn, ab in PERIODS:
            g = [t for t in GAP[sn] if inp(t, ab)]; b = [t for t in base_cov if inp(t, ab)]; p = [t for t in POOL[sn] if inp(t, ab)]
            r[pn] = {"gap_trades": mean_ci(g), "base_breakouts_same_stocks": mean_ci(b),
                     "gap_also_breakout_%": round(100 * float(np.mean([t["also_bo"] for t in g])), 1) if g else None,
                     "gap_not_breakout": mean_ci([t for t in g if not t["also_bo"]]),
                     "portfolio_breakouts": pstats(b, ab), "portfolio_breakouts_plus_gaps": pstats(p, ab), "portfolio_gaps_only": pstats(g, ab)}
        d, v = r["dev"], r["val"]
        dc = [r[p]["portfolio_breakouts_plus_gaps"]["cagr"] - r[p]["portfolio_breakouts"]["cagr"] for p in ("dev", "val")]
        dd = [r[p]["portfolio_breakouts_plus_gaps"]["max_dd"] - r[p]["portfolio_breakouts"]["max_dd"] for p in ("dev", "val")]
        gd, gv = d["gap_trades"], v["gap_trades"]
        if (min(gd["n"], gv["n"]) >= MIN_N and gd.get("lo", -1) > 0 and gv.get("mean_R", -1) > 0 and min(dc) >= 1.0 and min(dd) >= -2.0):
            verdict = "CANDIDATE SETUP"
        elif gd.get("mean_R", 1) <= 0 or max(dc) <= -1.0:
            verdict = "NO"
        else:
            verdict = "INCONCLUSIVE"
        r["cagr_pool_minus_breakouts"] = [round(x, 2) for x in dc]; r["dd_pool_minus_breakouts"] = [round(x, 2) for x in dd]; r["verdict"] = verdict
        res["T5"][sn] = r
        print(f"\n== T5 · {sn}: {verdict} · CAGR pool−breakouts {r['cagr_pool_minus_breakouts']} DD {r['dd_pool_minus_breakouts']}")
        for pn in ("dev", "val"):
            print(f"  {pn}: gaps {r[pn]['gap_trades']} | breakouts {r[pn]['base_breakouts_same_stocks']} | also breakout {r[pn]['gap_also_breakout_%']}%")
            print(f"       port breakouts {r[pn]['portfolio_breakouts']} | +gaps {r[pn]['portfolio_breakouts_plus_gaps']} | gaps only {r[pn]['portfolio_gaps_only']}")
    json.dump(res, open(os.path.join(out, f"round8f-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
