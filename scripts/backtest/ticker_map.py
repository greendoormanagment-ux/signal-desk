"""Find S&P 500 members whose ticker CHANGED (e.g. ANTM -> ELV, BLL -> BALL), so their history is not lost.

The membership file uses the ticker of the day; the price data uses today's ticker. A former ticker is
treated as a rename only when BOTH hold:
  1. SEC full-text search shows the old ticker mostly in 10-K/10-Q filings of the SAME company (same SEC CIK)
     that owns today's ticker, and
  2. the new ticker's S&P 500 membership starts within 3 days of the old ticker's membership ending.
Rule 2 rejects look-alikes (e.g. "IPG" text inside IPG Photonics filings); rule 1 rejects index replacements
(one company removed, another added the same day).

This script only PROPOSES renames. The table the backtests use is ticker_aliases.csv, where every row was
checked by hand against the SEC record of the new ticker (same CIK, and the old company name in SEC
"formerNames" or an unchanged name with a ticker change). Renames that leave the index before the new ticker
joins (e.g. FleetCor -> Corpay) fail rule 2 here and were added from that SEC check. Rejected on review:
CHK -> EXE (post-bankruptcy shares, price history starts 2021), CBS/VIAC -> PARA (ticker now belongs to another
company), and the look-alikes AABA, BXLT, FRC, IPG, SCG, WCG.

Usage: python ticker_map.py SP500_START_END_CSV PRICE_DIR [EXTRA_PRICE_DIR] OUT_JSON
"""
import collections, csv, datetime as dt, json, os, sys, time, urllib.parse, urllib.request

UA = {"User-Agent": "GreenDoor SignalDesk greendoorhomesct@gmail.com"}


def get(url):
    for a in range(4):
        try:
            time.sleep(0.15)
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.loads(r.read())
        except Exception:
            time.sleep(2 + 3 * a)
    return None


def top_cik(ticker):
    """Most frequent filer among 10-K/10-Q documents that mention the ticker in quotes."""
    q = urllib.parse.quote(f'"{ticker}"')
    j = get(f"https://efts.sec.gov/LATEST/search-index?q={q}&forms=10-K,10-Q")
    hits = ((j or {}).get("hits") or {}).get("hits") or []
    c = collections.Counter(int(h["_source"]["ciks"][0]) for h in hits if h.get("_source", {}).get("ciks"))
    if not c:
        return None, 0, 0
    cik, n = c.most_common(1)[0]
    return cik, n, len(hits)


def main(members_csv, price_dir, extra_dir, out):
    dirs = [d for d in (price_dir, extra_dir) if d and os.path.isdir(d)]
    have = {f[:-7] for d in dirs for f in os.listdir(d) if f.endswith(".csv.gz")}
    tick = get("https://www.sec.gov/files/company_tickers.json") or {}
    cik_to_ticker = {}
    for v in tick.values():
        t = v["ticker"].upper().replace(".", "-")
        if t in have:
            cik_to_ticker.setdefault(int(v["cik_str"]), t)
    rows = list(csv.DictReader(open(members_csv)))
    missing = sorted({r["ticker"].replace(".", "-") for r in rows
                      if r["ticker"].replace(".", "-") not in have and (not r["end_date"] or r["end_date"] >= "2016-06-01")})
    ends = {}; starts = collections.defaultdict(list)
    for r in rows:
        t = r["ticker"].replace(".", "-")
        if r["end_date"]:
            ends[t] = max(ends.get(t, ""), r["end_date"])
        starts[t].append(r["start_date"])
    near = lambda a, b: abs((dt.date.fromisoformat(a) - dt.date.fromisoformat(b)).days) <= 3
    aliases, evidence = {}, []
    for t in missing:
        cik, n, tot = top_cik(t)
        new = cik_to_ticker.get(cik)
        same_co = bool(new) and n >= 3 and n >= 0.3 * max(tot, 1)
        handover = bool(new) and t in ends and any(near(s0, ends[t]) for s0 in starts.get(new, []))
        ok = same_co and handover
        evidence.append({"old": t, "sec_cik": cik, "hits_for_cik": n, "hits_total": tot, "current_ticker": new,
                         "same_company": same_co, "membership_handover": handover, "rename": ok})
        if ok:
            aliases[t] = new
    json.dump({"aliases": aliases, "checked": len(missing), "evidence": evidence}, open(out, "w"), indent=1)
    print(f"{len(missing)} membership tickers without price files · {len(aliases)} confirmed renames")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3:
        a = [a[0], a[1], None, a[2]]
    main(*a)
