"""Round 7 · which thinkorswim studies (and Fibonacci retracements) actually help pick stocks?

Data: EODHD daily bars for every S&P 500 member since 2004, including companies that later failed (point-in-time
membership, $5+, $20M+/day). TUNE 2005-2016 chooses; JUDGE 2017-2025 is only for checking what was already chosen.

Stage 1 — screen every study on its own (thinkorswim default settings, no tuning), with and without a trend filter
  (close > 200-day and 50-day > 200-day). Each signal = buy at the next open. Measure the return over the next 20 and
  60 sessions MINUS what a random eligible stock returned from the same day (the "edge"). Random-entry is the bar, not
  SPY: a study is only useful if it beats picking any stock that day (for filtered studies: any uptrend stock).
  t-statistics use Newey-West errors (overlapping windows) on the per-day averages.
  A study SURVIVES if, in TUNE: 200+ signals, 20- and 60-day edge both > 0, 60-day t-stat >= 2.5 (raised for ~80 tries),
  and the 60-day edge is positive in BOTH halves (2005-10 and 2011-16).
Stage 2 — pairs of survivors (B fired within 5 sessions of A), same screen.
Stage 3 — the 5 best (by tune t-stat) go into a full portfolio (10 slots, 1% risk, idle money in SPY, costs), with
  Round 6's best exit (original stop only) and a 50-day exit, with and without the S&P-above-200-day gate. Each is
  compared with RANDOM entries under the same rules. Best by tune excess vs SPY is then judged once on 2017-2025.
Fibonacci: the same retracement rules at made-up levels (30/44/56/70%) are the control.

Data repair (data_clean.py) runs first: unadjusted splits rescaled, bad one-day prints dropped, spliced tickers cut;
files still broken after that are left out and listed in the report.

Usage: python run_round7.py PRICE_DIR MEMBERS_CSV OUT_DIR
"""
import datetime as dt, itertools, json, os, sys, time
import numpy as np, pandas as pd
import engine as E, systems as S, studies as T, data_clean as DC
from run_systems import load_members, is_member

TUNE, JUDGE, Y26 = ("2005-01-01", "2016-12-31"), ("2017-01-01", "2025-12-31"), ("2026-01-01", "2026-12-31")
HALVES = (("2005-01-01", "2010-12-31"), ("2011-01-01", "2016-12-31"))
HZ = (20, 60)
COST = 0.0007
T_MIN, N_MIN, PAIR_WIN = float(os.environ.get("R7_TMIN", 2.5)), 200, 5      # R7_TMIN only for smoke tests


def nw_t(y, lag):
    y = np.asarray(y, float); n = len(y)
    if n < 30:
        return 0.0
    e = y - y.mean(); v = e @ e / n
    for k in range(1, min(lag, n - 1) + 1):
        v += 2 * (1 - k / (lag + 1)) * (e[k:] @ e[:-k]) / n
    return float(y.mean() / np.sqrt(v / n)) if v > 0 else 0.0


def main(pc, members_csv, out):
    t0 = time.time(); os.makedirs(out, exist_ok=True)
    prices = E.load_prices(pc)
    members = load_members(members_csv)
    prices, clean_notes, dropped = DC.clean_all(prices, members)         # unadjusted splits, bad prints, spliced tickers
    spy = prices.pop("SPY"); prices.pop("QQQ", None); prices.pop("RSP", None)
    prices = {k: v for k, v in prices.items() if k in members}
    syms = sorted(prices); cal = list(spy.date); D = {d: i for i, d in enumerate(cal)}; nd, ns = len(cal), len(syms)
    el = E.eligibility(prices, cal, member=lambda s, d: is_member(members, s, d))
    ELIG = el.reindex(columns=syms).fillna(False).to_numpy(bool)
    so, sc = spy.o.to_numpy(float), spy.c.to_numpy(float)
    X = {H: np.full((nd, ns), np.nan, np.float32) for H in HZ}
    UP = np.zeros((nd, ns), bool); MOM = np.full((nd, ns), np.nan, np.float32)
    SIG = {}                                    # study -> list of global keys (stock*nd + day)
    STOPS = {}                                  # (study, key) not stored; recomputed in stage 3
    print(f"{ns} S&P members since 2004 · {nd} days · {time.time()-t0:.0f}s", flush=True)
    for si, s in enumerate(syms):
        df = prices[s]; di = np.array([D.get(d, -1) for d in df.date]); okd = di >= 0
        df, di = df[okd].reset_index(drop=True), di[okd]
        o, c = df.o.to_numpy(float), df.c.to_numpy(float)
        for H in HZ:
            f = np.full(len(c), np.nan)
            if len(c) > H + 1:
                f[:len(c) - H] = c[H:] / o[1:len(c) - H + 1] - 1      # buy next open, sell at the close H sessions after the signal
            # SPY over the same calendar window (entry at the next open, exit at the close H sessions after the signal)
            j0 = np.minimum(di + 1, nd - 1); j1 = np.minimum(di + H, nd - 1)
            fs = sc[j1] / so[j0] - 1
            ok = (di + H < nd)
            g = np.clip(np.where(ok, f - fs, np.nan), -1.0, 3.0)          # last-resort guard against any bad bar left
            X[H][di, si] = g
        UP[di, si] = T.uptrend(df)
        MOM[di, si] = pd.Series(c).pct_change(126).to_numpy()
        for name, (sig, _) in T.signals(df).items():
            k = si * nd + di[sig]
            SIG.setdefault(name, []).append(k)
        if si % 100 == 0:
            print(f"  studies computed for {si}/{ns} stocks ({time.time()-t0:.0f}s)", flush=True)
    SIG = {k: np.sort(np.concatenate(v)) for k, v in SIG.items()}
    dates = np.array(cal)
    base = {}
    for H in HZ:
        xa = np.where(ELIG, X[H], np.nan); xu = np.where(ELIG & UP, X[H], np.nan)
        with np.errstate(all="ignore"):
            base[(H, False)] = np.nanmean(xa, axis=1); base[(H, True)] = np.nanmean(xu, axis=1)
    print(f"stage 1 ready · {len(SIG)} studies · {time.time()-t0:.0f}s", flush=True)

    def screen(keys, filt, span):
        si_, di_ = keys // nd, keys % nd
        m = ELIG[di_, si_] & (dates[di_] >= span[0]) & (dates[di_] <= span[1])
        if filt:
            m &= UP[di_, si_]
        si_, di_ = si_[m], di_[m]
        r = {"signals": int(len(di_))}
        for H in HZ:
            x = X[H][di_, si_].astype(float); ok = ~np.isnan(x)
            if ok.sum() < 30:
                r[f"edge{H}"] = None; r[f"t{H}"] = 0.0; continue
            dd = di_[ok]; xx = x[ok]
            sm = np.bincount(dd, xx, nd); cn = np.bincount(dd, minlength=nd)
            days = np.where(cn > 0)[0]
            diff = sm[days] / cn[days] - base[(H, filt)][days]
            diff = diff[~np.isnan(diff)]
            r[f"edge{H}"] = round(float(diff.mean()) * 100, 2); r[f"t{H}"] = round(nw_t(diff, H), 2)
            r[f"vsSPY{H}"] = round(float(xx.mean()) * 100, 2); r[f"hit{H}"] = round(float((xx > 0).mean()) * 100, 1)
        return r

    rows = []
    for name, keys in SIG.items():
        for filt in (False, True):
            r = {"study": name, "trend_filter": filt, "tune": screen(keys, filt, TUNE),
                 "halves": [screen(keys, filt, hv).get("edge60") for hv in HALVES]}
            tu = r["tune"]
            r["survives"] = bool(tu["signals"] >= N_MIN and (tu.get("edge20") or -1) > 0 and (tu.get("edge60") or -1) > 0
                                 and tu.get("t60", 0) >= T_MIN and all((x or -1) > 0 for x in r["halves"]))
            rows.append(r)
    surv = sorted([r for r in rows if r["survives"]], key=lambda r: -r["tune"]["t60"])
    print(f"stage 1: {len(surv)} of {len(rows)} study/filter versions survive", flush=True)

    # stage 2: pairs of survivors (same filter setting), B within PAIR_WIN sessions of A (either order)
    def near(a, b):
        j = np.searchsorted(b, a - PAIR_WIN)
        hit = (j < len(b)) & (b[np.minimum(j, len(b) - 1)] <= a) & ((b[np.minimum(j, len(b) - 1)] // nd) == (a // nd))
        return a[hit]
    pairs = []
    top = [r for r in surv][:10]
    for ra, rb in itertools.combinations(top, 2):
        if ra["trend_filter"] != rb["trend_filter"] or ra["study"] == rb["study"]:
            continue
        a, b = SIG[ra["study"]], SIG[rb["study"]]
        keys = np.unique(np.concatenate([near(a, b), near(b, a)]))
        name = f"{ra['study']} + {rb['study']}"
        SIG[name] = keys
        r = {"study": name, "trend_filter": ra["trend_filter"], "tune": screen(keys, ra["trend_filter"], TUNE),
             "halves": [screen(keys, ra["trend_filter"], hv).get("edge60") for hv in HALVES], "pair": [ra["study"], rb["study"]]}
        tu = r["tune"]
        r["survives"] = bool(tu["signals"] >= N_MIN and (tu.get("edge20") or -1) > 0 and (tu.get("edge60") or -1) > 0
                             and tu.get("t60", 0) >= T_MIN and all((x or -1) > 0 for x in r["halves"]))
        pairs.append(r)
    print(f"stage 2: {sum(p['survives'] for p in pairs)} of {len(pairs)} pairs survive", flush=True)

    # judge columns are filled AFTER every choice above is frozen (information only)
    for r in rows + pairs:
        r["judge"] = screen(SIG[r["study"]], r["trend_filter"], JUDGE)

    # stage 3: portfolio for the 5 best survivors (singles or pairs) + random entries
    cand = sorted([r for r in rows + pairs if r["survives"]], key=lambda r: -r["tune"]["t60"])[:5]
    s200 = pd.Series(sc).rolling(200).mean().to_numpy()
    spy_up = dict(zip(cal, sc > s200))
    closes = {s: prices[s].set_index("date").c for s in syms}
    spy_c = spy.set_index("date").c
    idle = (dict(zip(spy.date, spy.o)), dict(zip(spy.date, spy.c)))
    IND = {s: E.indicators(prices[s]) for s in syms}
    need = sorted({p for r in cand for p in (r.get("pair") or [r["study"]])})
    ARR = {}                                    # stock -> {study: (sig, stop)} for the candidates only
    for s in syms:
        a = T.signals(prices[s]); ARR[s] = {k: a[k] for k in need}
    print(f"stage 3: candidate signals rebuilt ({time.time()-t0:.0f}s)", flush=True)

    def trades_for(spec, exit_kind, gate):
        P = dict(E.BASE); P.update(nosec_pass=True, stop="fixed" if exit_kind == "original stop" else "ma50")
        tr = []; rng = np.random.default_rng(7)
        for si, s in enumerate(syms):
            df = prices[s]; n = len(df)
            di = np.array([D.get(d, -1) for d in df.date])
            if spec["study"] == "RANDOM":
                sig = (rng.random(n) < 0.004)
                stop = df.c.to_numpy(float) * 0.92
            else:
                arr = ARR[s]
                parts = spec.get("pair") or [spec["study"]]
                if len(parts) == 1:
                    sig, stop = arr[parts[0]]
                else:
                    keyset = SIG[spec["study"]]
                    k = si * nd + np.where(di >= 0, di, 0)
                    sig = np.isin(k, keyset) & (di >= 0)
                    st_a, st_b = arr[parts[0]][1], arr[parts[1]][1]
                    stop = np.fmax(np.nan_to_num(st_a, nan=-1), np.nan_to_num(st_b, nan=-1))
                    stop = np.where(stop > 0, stop, df.c.to_numpy(float) * 0.92)
            ok = sig & (di >= 0)
            ok[ok] &= ELIG[di[ok], si]
            if spec.get("trend_filter"):
                ok[ok] &= UP[di[ok], si]
            if gate:
                ok &= np.array([bool(spy_up.get(d, False)) for d in df.date])
            if not ok.any():
                continue
            sg = pd.DataFrame({"rating": np.where(ok, "BUY", "DONT_BUY"), "stop": np.where(ok, stop, np.nan),
                               "setup": spec["study"][:40], "score": np.nan_to_num(MOM[np.maximum(di, 0), si]) * 100,
                               "market": "UPTREND"})
            tr += E.simulate_trades(s, df, IND[s], sg, P, TUNE[0], Y26[1])
        return tr

    def port(tr, span, seed=None):
        return E.portfolio([t for t in tr if span[0] <= t["entry_date"] <= span[1]], closes, cal, span[0], span[1],
                           cost=COST, seed=seed, idle=idle)

    spy_m = lambda a, b: S.perf_metrics(spy_c[(spy_c.index >= a) & (spy_c.index <= b)])
    res3 = []
    specs = cand + [{"study": "RANDOM", "trend_filter": True}]
    for spec in specs:
        for exit_kind, gate in itertools.product(("original stop", "50-day exit"), (False, True)):
            tr = trades_for(spec, exit_kind, gate)
            runs = [S.perf_metrics(port(tr, TUNE, seed=k)[0], spy_c) for k in range(3)]
            eq, taken = port(tr, TUNE)
            m = S.perf_metrics(eq, spy_c)
            res3.append({"study": spec["study"], "trend_filter": spec.get("trend_filter"), "exit": exit_kind,
                         "spy200_gate": gate, "tune": {"excess_median": round(float(np.median([r.get('excess_cagr_%', -99) for r in runs])), 1),
                                                       "cagr": m.get("cagr_%"), "max_dd": m.get("max_dd_%"), "trades": len(taken)},
                         "_trades": tr})
            print(f"stage 3 tune: {spec['study'][:50]:50} | {exit_kind:13} | gate {gate}: excess {res3[-1]['tune']['excess_median']} "
                  f"({time.time()-t0:.0f}s)", flush=True)
    real = [r for r in res3 if r["study"] != "RANDOM"]
    spy_dd_t = spy_m(*TUNE).get("max_dd_%") or -100
    best = sorted([r for r in real if (r["tune"]["max_dd"] or -100) >= spy_dd_t - 5] or real,
                  key=lambda r: -r["tune"]["excess_median"])[:3]
    rand = [r for r in res3 if r["study"] == "RANDOM"]
    spy_dd_j = spy_m(*JUDGE).get("max_dd_%") or -100
    for r in best + rand:
        out_j = {}
        for pn, span in (("judge", JUDGE), ("2026", Y26)):
            runs = [S.perf_metrics(port(r["_trades"], span, seed=k)[0], spy_c) for k in range(10)]
            eq, taken = port(r["_trades"], span)
            out_j[pn] = {"cagr_median": round(float(np.median([x.get("cagr_%", 0) for x in runs])), 1),
                         "excess_median": round(float(np.median([x.get("excess_cagr_%", -99) for x in runs])), 1),
                         "max_dd": S.perf_metrics(eq).get("max_dd_%"), "trades": len(taken)}
            if pn == "judge":
                out_j[pn]["bootstrap"] = S.block_bootstrap_excess(eq, spy_c, *span)
        r["judge"], r["2026"] = out_j["judge"], out_j["2026"]
        j = r["judge"]
        r["passes_bar"] = bool(r["tune"]["excess_median"] > 0 and j["excess_median"] > 0
                               and (j.get("bootstrap") or {}).get("share_above_zero_%", 0) >= 80 and (j["max_dd"] or -100) >= spy_dd_j - 5)
        print(f"JUDGE {r['study'][:50]} | {r['exit']} | gate {r['spy200_gate']}: excess {j['excess_median']} (CAGR {j['cagr_median']}) "
              f"bootstrap {(j.get('bootstrap') or {}).get('share_above_zero_%')}% DD {j['max_dd']}", flush=True)
    for r in res3:
        r.pop("_trades", None)
    res = {"asOf": dt.date.today().isoformat(), "stocks": ns, "data_repairs": len(clean_notes), "dropped_files": dropped, "tune": TUNE, "judge": JUDGE, "halves": HALVES,
           "rules": {"t_min": T_MIN, "n_min": N_MIN, "pair_window": PAIR_WIN, "horizons": HZ, "cost_per_side": COST},
           "spy": {"tune": spy_m(*TUNE), "judge": spy_m(*JUDGE), "2026": spy_m(*Y26)},
           "studies": rows, "pairs": pairs, "portfolio": res3, "best": [r["study"] + " | " + r["exit"] + " | gate " + str(r["spy200_gate"]) for r in best]}
    json.dump(res, open(os.path.join(out, f"round7-{res['asOf']}.json"), "w"), indent=1, default=str)
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
