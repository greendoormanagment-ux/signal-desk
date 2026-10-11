"""Point-in-time SEC data for the backtest universe.

For each ticker: every quarterly / nine-month / annual EPS and revenue fact WITH its filing date
(so the backtest only uses numbers that were public on each day), plus the dates of every
8-K "Item 2.02" (earnings release) filing = the historical earnings calendar.
Usage: python fetch_sec.py PRICE_CACHE_DIR SEC_CACHE_DIR
"""
import concurrent.futures as cf, gzip, json, os, sys, threading, time, urllib.request

UA = {"User-Agent": "GreenDoor SignalDesk greendoorhomesct@gmail.com"}
EPS_TAGS = ["EarningsPerShareDiluted", "EarningsPerShareBasicAndDiluted", "EarningsPerShareBasic"]
REV_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet",
            "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet"]
_lock = threading.Lock(); _last = [0.0]


def get(url):
    for a in range(4):
        with _lock:  # SEC allows 10 requests/second; stay under it
            wait = _last[0] + 0.12 - time.time()
            if wait > 0:
                time.sleep(wait)
            _last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(3 + 5 * a)
        except Exception:
            time.sleep(3 + 5 * a)
    return None


def facts(gaap, tags, unit):
    out = {}
    for tag in tags:
        for f in ((gaap.get(tag) or {}).get("units") or {}).get(unit, []):
            if f.get("start") and f.get("end") and f.get("filed"):
                out.setdefault(tag, []).append([f["start"], f["end"], f["val"], f["filed"]])
    return out


def one(sym, cik, out_dir):
    path = os.path.join(out_dir, f"{sym}.json.gz")
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < 7 * 86400:
        return "cached"
    c10 = f"{cik:010d}"
    cf_ = get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{c10}.json") or {}
    gaap = (cf_.get("facts") or {}).get("us-gaap") or {}
    sub = get(f"https://data.sec.gov/submissions/CIK{c10}.json") or {}
    er = []
    pages = [(sub.get("filings") or {}).get("recent") or {}]
    for extra in (sub.get("filings") or {}).get("files") or []:
        if extra.get("filingTo", "9999") >= "2015-01-01":
            pages.append(get(f"https://data.sec.gov/submissions/{extra['name']}") or {})
    for p in pages:
        for form, date, items in zip(p.get("form", []), p.get("filingDate", []), p.get("items", [])):
            if form in ("8-K", "8-K/A", "6-K") and "2.02" in (items or ""):
                er.append(date)
    rec = {"sym": sym, "cik": cik, "eps": facts(gaap, EPS_TAGS, "USD/shares"), "rev": facts(gaap, REV_TAGS, "USD"),
           "earn": sorted(set(er))}
    with gzip.open(path, "wt") as f:
        json.dump(rec, f, separators=(",", ":"))
    return "ok" if rec["eps"] else "no-eps"


if __name__ == "__main__":
    prices, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    syms = json.load(open(os.path.join(prices, "universe.json")))["symbols"]
    m = {}
    for v in get("https://www.sec.gov/files/company_tickers.json").values():
        m.setdefault(v["ticker"].upper().replace("-", "."), int(v["cik_str"]))
    todo = [(s, m[s]) for s in syms if s in m]
    print(f"{len(todo)} of {len(syms)} symbols have an SEC CIK", flush=True)
    stats = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for n, r in enumerate(ex.map(lambda t: one(t[0], t[1], out_dir), todo), 1):
            stats[r] = stats.get(r, 0) + 1
            if n % 200 == 0:
                print(n, stats, flush=True)
    print("done", stats)
