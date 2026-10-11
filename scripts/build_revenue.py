"""Signal Desk nightly job: builds revenue.json from the SEC company-facts bulk file
(the same file build_eps.py downloads). For every US-listed company: the latest quarter's
revenue vs the same quarter a year earlier, plus the quarter before that — so the app can
check sales growth and "two quarters of shrinking revenue" from official filings, not AI search.
Fiscal Q4 is derived as full year minus nine months. Never touches eps.json.
"""
import datetime as dt, json, os, sys, urllib.request, zipfile

TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
        "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet", "SalesRevenueGoodsNet"]
TODAY = dt.date.today()


def days(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def quarters(units):
    facts = (units or {}).get("USD", [])
    q, y, n9 = {}, {}, {}
    for f in facts:
        if not f.get("start") or not f.get("end") or f.get("val") is None:
            continue
        d = days(f["start"], f["end"])
        t = q if 80 <= d <= 100 else y if 350 <= d <= 380 else n9 if 260 <= d <= 285 else None
        if t is None:
            continue
        if f["end"] not in t or f.get("filed", "") > t[f["end"]].get("filed", ""):
            t[f["end"]] = f
    for e, f in y.items():  # fiscal Q4 = full year minus first nine months
        if e in q:
            continue
        nine = next((g for g in n9.values() if g["start"] == f["start"]), None)
        if nine:
            q[e] = {"end": e, "val": f["val"] - nine["val"], "filed": f.get("filed", ""), "derived": True}
    return q


def yoy(q, end):
    """growth % of quarter `end` vs the quarter ~1 year earlier (None if missing or base <= 0)"""
    prev = next((q[e] for e in sorted(q) if abs(days(e, end) - 365) <= 20), None)
    if not prev or prev["val"] <= 0:
        return None, None
    return round((q[end]["val"] - prev["val"]) / prev["val"] * 100, 1), prev["val"]


def calc(units):
    q = quarters(units)
    if not q:
        return None
    ends = sorted(q)
    last = ends[-1]
    g1, base = yoy(q, last)
    if g1 is None:
        return None
    before = [e for e in ends if 60 <= days(e, last) <= 120]  # the quarter before the latest one
    p_end = before[-1] if before else ""
    g2 = yoy(q, p_end)[0] if p_end else None
    return [last, round(q[last]["val"]), round(base), g1, p_end, g2, q[last].get("filed", ""), 1 if q[last].get("derived") else 0]


def best_for(gaap):
    best = None
    for tag in TAGS:  # pick the tag with the most recent quarter (ties: earlier tag in the list wins)
        if tag in gaap:
            r = calc(gaap[tag].get("units"))
            if r and (best is None or r[0] > best[0]):
                best = r
    return best


def main(out_path, zip_path, tickers_path):
    if not (os.path.exists(zip_path) and zipfile.is_zipfile(zip_path)):
        sys.exit("No SEC zip (build_eps.py downloads it) — keeping yesterday's revenue.json")
    if os.path.exists(tickers_path):
        tickers = json.load(open(tickers_path))
    else:
        req = urllib.request.Request("https://www.sec.gov/files/company_tickers.json",
                                     headers={"User-Agent": "GreenDoor SignalDesk greendoorhomesct@gmail.com"})
        tickers = json.loads(urllib.request.urlopen(req, timeout=120).read())
    by_cik = {}
    for v in tickers.values():
        by_cik.setdefault(int(v["cik_str"]), []).append(v["ticker"].upper())
    data, seen = {}, 0
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            try:
                cik = int(name.replace("CIK", "").replace(".json", ""))
            except ValueError:
                continue
            if cik not in by_cik:
                continue
            raw = z.read(name)
            if b"Revenue" not in raw and b"SalesRevenue" not in raw:
                continue
            seen += 1
            best = best_for((json.loads(raw).get("facts") or {}).get("us-gaap") or {})
            if best and days(best[0], TODAY.isoformat()) <= 400:
                for t in by_cik[cik]:
                    data[t.replace("-", ".")] = best
                    data[t] = best
    out = {"asOf": TODAY.isoformat(), "source": "SEC EDGAR company facts (GAAP revenue)",
           "fields": ["qEnd", "revenue", "revenueYearAgo", "growthPct", "priorQEnd", "priorGrowthPct", "filed", "q4Derived"],
           "data": data}
    with open(out_path, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"companies scanned: {seen}, tickers written: {len(data)}, size: {os.path.getsize(out_path)//1024} KB")
    if len(data) < 1000:
        sys.exit("Too few results — not publishing")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "revenue.json",
         sys.argv[2] if len(sys.argv) > 2 else "/tmp/companyfacts.zip",
         sys.argv[3] if len(sys.argv) > 3 else "/tmp/company_tickers.json")
