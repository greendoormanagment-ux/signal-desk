"""Gate 3 pre-check: does EODHD actually list the stocks our free data is missing — BEFORE paying for it.

Runs on EODHD's free tier (20 calls/day + one-time 500 bonus, 1 year of price history). It spends at most
~17 calls: 2 ticker lists (active + delisted US) and up to 15 one-year price samples of recently delisted names.

What it can prove for free:  whether each missing S&P 500 name appears in EODHD's US ticker lists, how many
                             delisted US common stocks EODHD lists, and that recently delisted names return prices.
What it can NOT prove free:  the full 2016+ price depth of names delisted more than a year ago (free tier = 1 year).
                             That needs one paid month ($19.99) and a second run of this script; cancel if it fails.

The key comes ONLY from the EODHD_KEY environment variable (a GitHub Actions secret). It is never printed or written.

Usage: EODHD_KEY=... python eodhd_coverage.py backtest/audit/sp500_coverage.csv OUT_DIR [--depth]
       --depth (paid month only): also fetch 2016+ history for every missing name and report first/last dates.
"""
import csv, datetime as dt, json, os, sys, time, urllib.error, urllib.request

KEY = os.environ.get("EODHD_KEY", "").strip()
BASE = "https://eodhd.com/api"


def call(path, **q):
    q.update(api_token=KEY, fmt="json")
    url = f"{BASE}/{path}?" + "&".join(f"{k}={v}" for k, v in q.items())
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:          # report the status only — never the URL (it holds the key)
        return {"error": f"HTTP {e.code}"}
    except Exception as e:
        return {"error": type(e).__name__}


def main(cov_csv, out, depth=False):
    if not KEY:
        sys.exit("EODHD_KEY is not set (add it as a repository secret).")
    os.makedirs(out, exist_ok=True)
    rows = list(csv.DictReader(open(cov_csv)))
    missing = {}
    latest = set((rows[-1].get("missing_tickers") or "").split()) | set((rows[-2].get("missing_tickers") or "").split())
    for r in rows:
        for t in (r.get("missing_tickers") or "").split():
            missing.setdefault(t, r["year"])                     # first year the name is missing
    active, delisted = call("exchange-symbol-list/US"), call("exchange-symbol-list/US", delisted=1)
    for name, lst in (("active", active), ("delisted", delisted)):
        if isinstance(lst, dict):
            sys.exit(f"Could not read the {name} ticker list: {lst.get('error')}")
    norm = lambda c: c.upper().replace(".", "-")
    idx = {}
    for status, lst in (("active", active), ("delisted", delisted)):
        for s in lst:
            idx.setdefault(norm(s.get("Code", "")), []).append({"status": status, "name": s.get("Name"), "type": s.get("Type"),
                                                                "exchange": s.get("Exchange"), "isin": s.get("Isin")})
    found = []
    for t in sorted(missing):
        hits = idx.get(t, [])
        found.append({"ticker": t, "first_missing_year": missing[t], "listed": bool(hits),
                      "status": "/".join(sorted({h["status"] for h in hits})), "eodhd_name": "; ".join(sorted({str(h["name"]) for h in hits}))[:120]})
    dl_common = [s for s in delisted if s.get("Type") == "Common Stock"]
    # Price samples: names that left the index most recently (inside the free tier's 1-year window), max 15 calls.
    recent = [f for f in found if f["listed"] and f["ticker"] in latest][:15] if not depth else [f for f in found if f["listed"]]
    frm = "2016-01-01" if depth else (dt.date.today() - dt.timedelta(days=365)).isoformat()
    for f in recent:
        p = call(f"eod/{f['ticker']}.US", **{"from": frm})
        if isinstance(p, list) and p:
            f.update(sample_rows=len(p), sample_first=p[0]["date"], sample_last=p[-1]["date"])
        else:
            f.update(sample_rows=0, sample_note=(p or {}).get("error", "no rows") if isinstance(p, dict) else "no rows")
        time.sleep(3.2)                                           # free tier: 20 requests/minute
    n = len(found); listed = sum(f["listed"] for f in found)
    summ = {"asOf": dt.date.today().isoformat(), "mode": "depth (paid)" if depth else "free tier",
            "missing_sp500_names": n, "listed_in_eodhd": listed, "listed_pct": round(100 * listed / max(n, 1), 1),
            "eodhd_us_delisted_total": len(delisted), "eodhd_us_delisted_common_stocks": len(dl_common),
            "price_samples": len(recent), "price_samples_with_rows": sum(1 for f in recent if f.get("sample_rows"))}
    json.dump({"summary": summ, "names": found}, open(os.path.join(out, "eodhd-coverage.json"), "w"), indent=1)
    L = [f"# EODHD coverage check ({summ['asOf']}, {summ['mode']})", "",
         f"- S&P 500 names our free data is missing: **{n}**; listed by EODHD: **{listed} ({summ['listed_pct']}%)**",
         f"- Delisted US tickers EODHD lists: {len(delisted):,} (common stocks: {len(dl_common):,})",
         f"- Price samples returning data: {summ['price_samples_with_rows']} of {summ['price_samples']}"
         + ("" if depth else " (free tier = last 12 months only, so only recently delisted names can return rows)"), "",
         "Decision rule: subscribe for ONE month only if ≥90% of the missing names are listed. Then rerun with `--depth` and "
         "cancel unless ≥90% of them return history back to the year they went missing.", "",
         "| Ticker | Missing from | Listed | Status | EODHD name | Price rows | First | Last |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for f in found:
        L.append(f"| {f['ticker']} | {f['first_missing_year']} | {'yes' if f['listed'] else 'no'} | {f['status']} | {f['eodhd_name']} | "
                 f"{f.get('sample_rows', '')} | {f.get('sample_first', '')} | {f.get('sample_last', '')} |")
    open(os.path.join(out, "eodhd-coverage.md"), "w").write("\n".join(L) + "\n")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--depth"]
    main(a[0], a[1], depth="--depth" in sys.argv)
