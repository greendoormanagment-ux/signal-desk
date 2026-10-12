"""Round 3 · Gate 1 data audit. Never edits the price cache; it writes evidence + a corrections overlay.

Usage: python audit.py PRICE_DIR [EXTRA_PRICE_DIR] SP500_START_END_CSV OUT_DIR

Writes to OUT_DIR:
  data-manifest.json     sha256 of every cached file (the exact data snapshot the results came from)
  extreme_moves.csv      every close-to-close move over 60%, with evidence and a classification
  corrections.json       the overlay the engine applies at load time (originals stay untouched)
  corrections_log.csv    one line per correction: what changed and why
  data_gaps.csv          per-stock coverage: first/last date, missing sessions, zero-volume days, bad rows
  sp500_coverage.csv     per year: S&P 500 members, members with price data, members missing
  audit-summary.json     the counts the report quotes
Classification of an extreme move (|close/prev close - 1| > 60%):
  data error: split not adjusted  – a split record within 2 sessions and the move matches the split ratio
  genuine                         – an independent source (Nasdaq) shows the same move within 5% (log terms)
  data error: one-day bad bar     – the other source disagrees AND the move reverses the next day
  unresolved                      – anything else (kept as is, listed, and tested for sensitivity in Gate 2)
"""
import csv, gzip, hashlib, json, math, os, sys
import datetime as dt
import numpy as np, pandas as pd
import fetch_prices as fp

THRESH = 0.60


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def raw(path):
    return pd.read_csv(path, compression="gzip")


def yahoo_splits(sym):
    try:
        j = fp.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=10y&interval=1d&events=split")
        ev = (j["chart"]["result"][0].get("events") or {}).get("splits") or {}
        return [(dt.datetime.utcfromtimestamp(v["date"]).date().isoformat(), v["numerator"] / v["denominator"]) for v in ev.values()]
    except Exception:
        return None


def nasdaq_closes(sym):
    try:
        return {d: c for d, o, h, l, c, v in fp.nasdaq(sym)}
    except Exception:
        return None


SEC_DIR = os.environ.get("SEC_DIR", "")


def sec_earn(sym):
    p = os.path.join(SEC_DIR, f"{sym}.json.gz")
    if SEC_DIR and os.path.exists(p):
        return json.load(gzip.open(p, "rt")).get("earn") or []
    return []


def classify(df, t, splits, nq):
    d, c = df.date.to_numpy(), df.c.to_numpy(float)
    r = c[t] / c[t - 1]
    ev = {"ratio": round(r, 4)}
    near = [f for sd, f in (splits or []) if abs(int(np.searchsorted(d, sd)) - t) <= 2]
    ev["split_records_near"] = ";".join(f"{f:g}" for f in near)
    for f in near:
        if abs(math.log(r) + math.log(f)) < 0.15:
            return "data error: split not adjusted", dict(ev, split_factor=f)
    rev = None
    if t + 1 < len(c):
        rev = abs(math.log(c[t + 1] / c[t - 1])) < 0.2 * abs(math.log(r))
    ev["reverses_next_day"] = rev
    if nq is not None and d[t] in nq and d[t - 1] in nq and nq[d[t - 1]] > 0:
        rn = nq[d[t]] / nq[d[t - 1]]
        ev["nasdaq_ratio"] = round(rn, 4)
        if abs(math.log(r) - math.log(rn)) < 0.05:
            return "genuine", ev
        if rev:
            return "data error: one-day bad bar", ev
        return "unresolved", ev
    ev["nasdaq_ratio"] = None
    return "unresolved", ev


def main(price_dir, extra_dir, members_csv, out):
    os.makedirs(out, exist_ok=True)
    dirs = [x for x in (price_dir, extra_dir) if x and os.path.isdir(x)]
    files = {f[:-7]: os.path.join(dd, f) for dd in dirs for f in sorted(os.listdir(dd)) if f.endswith(".csv.gz")}
    # 1) snapshot
    man = {s: sha(p) for s, p in sorted(files.items())}
    combo = hashlib.sha256("".join(f"{k}:{v}" for k, v in man.items()).encode()).hexdigest()
    json.dump({"created": dt.date.today().isoformat(), "files": len(man), "combined_sha256": combo, "sha256": man},
              open(os.path.join(out, "data-manifest.json"), "w"), indent=0)
    spy = raw(files["SPY"]).drop_duplicates("date").sort_values("date")
    cal = list(spy.date)
    # 2) gaps + extreme moves
    gaps, events = [], []
    for s, p in files.items():
        df0 = raw(p)
        dup = int(df0.date.duplicated().sum())
        bad = int(((df0.c <= 0) | (df0.h < df0.l)).sum())
        df = df0[(df0.c > 0) & (df0.h >= df0.l)].drop_duplicates("date").sort_values("date").reset_index(drop=True)
        if len(df) < 2:
            continue
        a, b = df.date.iat[0], df.date.iat[-1]
        exp = [x for x in cal if a <= x <= b]
        have = set(df.date)
        miss = [x for x in exp if x not in have]
        longest, run = 0, 0
        for x in exp:
            run = run + 1 if x not in have else 0
            longest = max(longest, run)
        gaps.append({"sym": s, "first": a, "last": b, "bars": len(df), "expected_sessions": len(exp), "missing_sessions": len(miss),
                     "longest_missing_run": longest, "zero_volume_days": int((df.v == 0).sum()), "duplicate_rows": dup,
                     "bad_rows_dropped": bad, "starts_after_2016": a > "2016-12-31", "ends_before_2026_09": b < "2026-09-01"})
        r = df.c / df.c.shift(1) - 1
        for t in np.flatnonzero(r.abs().to_numpy() > THRESH):
            events.append((s, int(t), df))
    print(f"{len(files)} files · {len(events)} extreme moves in {len({e[0] for e in events})} stocks", flush=True)
    # 3) classify each extreme move with outside evidence
    rows, overlay, log = [], [], []
    cache_s, cache_n = {}, {}
    for s, t, df in events:
        if s not in cache_s:
            cache_s[s] = yahoo_splits(s); cache_n[s] = nasdaq_closes(s)
        cls, ev = classify(df, t, cache_s[s], cache_n[s])
        avgv = df.v.iloc[max(0, t - 50):t].mean()
        row = {"sym": s, "date": df.date.iat[t], "prev_close": df.c.iat[t - 1], "close": df.c.iat[t],
               "next_close": df.c.iat[t + 1] if t + 1 < len(df) else None,
               "volume_x_avg": round(df.v.iat[t] / avgv, 1) if avgv else None, "classification": cls}
        er = (sec_earn(s) or [])
        row["earnings_8k_within_1_day"] = any(abs(int(np.searchsorted(df.date.to_numpy(), x)) - t) <= 1 for x in er)
        row.update(ev); rows.append(row)
        if cls == "data error: split not adjusted":
            f = ev["split_factor"]
            overlay.append({"sym": s, "op": "scale_before", "date": row["date"], "price_factor": 1 / f, "volume_factor": f})
            log.append({"sym": s, "date": row["date"], "action": f"prices before {row['date']} divided by {f:g}, volume x{f:g}",
                        "reason": f"split record {f:g}:1 matches the {ev['ratio']} move"})
        elif cls == "data error: one-day bad bar":
            overlay.append({"sym": s, "op": "drop_bar", "date": row["date"]})
            log.append({"sym": s, "date": row["date"], "action": "bar excluded",
                        "reason": f"Nasdaq shows {ev.get('nasdaq_ratio')} vs {ev['ratio']} and the move reverses next day"})
    pd.DataFrame(rows).to_csv(os.path.join(out, "extreme_moves.csv"), index=False)
    json.dump({"created": dt.date.today().isoformat(), "note": "applied at load time; cache files are never modified",
               "corrections": overlay}, open(os.path.join(out, "corrections.json"), "w"), indent=1)
    pd.DataFrame(log, columns=["sym", "date", "action", "reason"]).to_csv(os.path.join(out, "corrections_log.csv"), index=False)
    g = pd.DataFrame(gaps); g.to_csv(os.path.join(out, "data_gaps.csv"), index=False)
    # 4) S&P 500 point-in-time coverage
    from run_systems import load_members          # applies the reviewed ticker renames (ticker_aliases.csv)
    mem = load_members(members_csv)
    cal = sorted({d for f in ("SPY",) for d in pd.read_csv(os.path.join(price_dir, "SPY.csv.gz")).date})
    cov = []
    for y in range(2017, 2027):
        a, b = f"{y}-01-01", f"{y}-12-31"
        m = [k for k, iv in mem.items() if any(s0 <= b and e0 >= a for s0, e0 in iv)]
        have = [k for k in m if k in files]
        days = [d for d in cal if a <= d <= b]
        md = sum(1 for k in m for d in days if any(s0 <= d <= e0 for s0, e0 in mem[k]))
        mh = sum(1 for k in have for d in days if any(s0 <= d <= e0 for s0, e0 in mem[k]))
        cov.append({"year": y, "members_during_year": len(m), "with_price_data": len(have), "missing": len(m) - len(have),
                    "member_days_covered_pct": round(100 * mh / md, 1) if md else None,
                    "missing_pct": round(100 * (len(m) - len(have)) / len(m), 1), "missing_tickers": " ".join(sorted(set(m) - set(have)))})
    pd.DataFrame(cov).to_csv(os.path.join(out, "sp500_coverage.csv"), index=False)
    cls_counts = pd.Series([r["classification"] for r in rows]).value_counts().to_dict()
    summ = {"files": len(files), "combined_sha256": combo, "extreme_moves": len(rows), "stocks_with_extreme_moves": len({r['sym'] for r in rows}),
            "classification": cls_counts, "corrections": len(overlay),
            "stocks_with_unresolved": sorted({r["sym"] for r in rows if r["classification"] == "unresolved"}),
            "stocks_with_missing_sessions": int((g.missing_sessions > 0).sum()), "total_missing_sessions": int(g.missing_sessions.sum()),
            "stocks_with_zero_volume_days": int((g.zero_volume_days > 0).sum()), "bad_rows_dropped": int(g.bad_rows_dropped.sum()),
            "duplicate_rows": int(g.duplicate_rows.sum()), "stocks_starting_after_2016": int(g.starts_after_2016.sum()),
            "sp500_coverage": [{k: v for k, v in c.items() if k != "missing_tickers"} for c in cov]}
    json.dump(summ, open(os.path.join(out, "audit-summary.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k not in ("sp500_coverage",)}, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3:
        a = [a[0], None, a[1], a[2]]
    main(*a)
