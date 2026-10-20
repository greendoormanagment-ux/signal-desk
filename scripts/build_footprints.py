"""Nightly 'outside' institutional footprints for Signal Desk (v2.12). INFO / LOGGING ONLY — no rule reads this.

Writes footprints.json:
  si   short interest (FINRA, all US stocks, twice a month): shares short, days to cover, % change vs prior report
  ins  insider open-market trades (SEC Form 4, last 90 days) for the watchlist: buys, buyers, $ bought, sells, $ sold
  rev  analyst EPS-estimate revision for the next report, from our own nightly earnings.json snapshots in history/

Why: big holders and insiders leave tracks. Insider *buying* (especially several insiders) and rising estimates are
among the better-documented footprints (Lakonishok & Lee 2001; Cohen, Malloy & Pomorski 2012; Chan, Jegadeesh &
Lakonishok 1996). Heavy short interest marks stocks the pros are betting against (Asquith, Pathak & Ritter 2005).

Usage: python scripts/build_footprints.py footprints.json
"""
import datetime as dt, glob, gzip, json, os, re, sys, time, urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "GreenDoor SignalDesk greendoorhomesct@gmail.com"}
TODAY = dt.date.today()


def get(url, data=None, headers=None, tries=3):
    h = dict(UA); h.update(headers or {})
    for a in range(tries):
        try:
            time.sleep(0.13)
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(2 + 3 * a)
    print("  fetch failed:", url[:90], type(last).__name__)
    return None


def watchlist():
    """The app's default watchlist (index.html) + any tickers in scripts/footprint_extra.txt."""
    here = os.path.dirname(os.path.abspath(__file__))
    html = open(os.path.join(here, "..", "index.html"), encoding="utf-8").read()
    m = re.search(r'const WATCH_DEFAULT = "([^"]+)"', html)
    syms = set(m.group(1).split()) if m else set()
    extra = os.path.join(here, "footprint_extra.txt")
    if os.path.exists(extra):
        syms |= {s.strip().upper() for s in open(extra).read().split() if s.strip() and not s.startswith("#")}
    return sorted(syms)


# ---------- short interest (FINRA, free API, no key) ----------
def short_interest():
    url = "https://api.finra.org/data/group/otcMarket/name/consolidatedShortInterest"
    hdr = {"Content-Type": "application/json", "Accept": "application/json"}
    start = (TODAY - dt.timedelta(days=40)).isoformat()
    rows, offset = [], 0
    while True:
        body = json.dumps({"limit": 5000, "offset": offset,
                           "dateRangeFilters": [{"fieldName": "settlementDate", "startDate": start, "endDate": TODAY.isoformat()}],
                           "fields": ["symbolCode", "settlementDate", "currentShortPositionQuantity",
                                      "daysToCoverQuantity", "changePercent", "averageDailyVolumeQuantity"]}).encode()
        raw = get(url, data=body, headers=hdr)
        if not raw:
            break
        page = json.loads(raw)
        if not isinstance(page, list) or not page:
            break
        rows += page; offset += len(page)
        if len(page) < 5000 or offset > 60000:
            break
    latest = {}
    for r in rows:
        s = r.get("symbolCode"); d = r.get("settlementDate", "")
        if s and (s not in latest or d > latest[s]["date"]):
            latest[s] = {"date": d, "short": r.get("currentShortPositionQuantity"), "dtc": r.get("daysToCoverQuantity"),
                         "chg": r.get("changePercent")}
    print(f"short interest: {len(rows)} rows → {len(latest)} symbols")
    return latest


# ---------- insider trades (SEC Form 4) ----------
def insiders(syms):
    tick = json.loads(get("https://www.sec.gov/files/company_tickers.json") or b"{}")
    cik_of = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in tick.values()}
    since = (TODAY - dt.timedelta(days=90)).isoformat()
    out = {}
    for s in syms:
        cik = cik_of.get(s)
        if not cik:
            continue
        sub = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
        if not sub:
            continue
        r = json.loads(sub)["filings"]["recent"]
        forms = [(a, d, doc) for f, a, d, doc in zip(r["form"], r["accessionNumber"], r["filingDate"], r["primaryDocument"])
                 if f == "4" and d >= since]
        buys = sells = 0; buy_usd = sell_usd = 0.0; buyers = set(); last_buy = ""
        for acc, fdate, doc in forms[:40]:
            xml_name = re.sub(r"^xsl[^/]*/", "", doc)  # primaryDocument may point at the styled HTML view
            raw = get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{xml_name}")
            if not raw:
                continue
            try:
                root = ET.fromstring(raw)
            except ET.ParseError:
                continue
            owner = (root.findtext(".//reportingOwnerId/rptOwnerName") or "").strip()
            for t in root.findall(".//nonDerivativeTransaction"):
                code = (t.findtext(".//transactionCoding/transactionCode") or "").strip()
                try:
                    sh = float(t.findtext(".//transactionAmounts/transactionShares/value") or 0)
                    px = float(t.findtext(".//transactionAmounts/transactionPricePerShare/value") or 0)
                except ValueError:
                    sh = px = 0.0
                if code == "P":            # open-market purchase — the footprint that matters
                    buys += 1; buy_usd += sh * px; buyers.add(owner); last_buy = max(last_buy, fdate)
                elif code == "S":          # open-market sale (often routine / planned)
                    sells += 1; sell_usd += sh * px
        out[s] = {"buys": buys, "buyers": len(buyers), "buyUSD": round(buy_usd), "sells": sells, "sellUSD": round(sell_usd),
                  "lastBuy": last_buy, "forms": len(forms)}
    print(f"insiders: {len(out)} watchlist stocks checked")
    return out


# ---------- estimate revisions (our own nightly snapshots) ----------
def revisions(hist_dir="history"):
    files = sorted(glob.glob(os.path.join(hist_dir, "*-earnings.json.gz")))
    if len(files) < 2:
        return {}
    now = json.load(gzip.open(files[-1], "rt"))["data"]
    target = (TODAY - dt.timedelta(days=30)).isoformat()
    old_f = next((f for f in files if os.path.basename(f)[:10] >= target), files[0])
    old = json.load(gzip.open(old_f, "rt"))["data"]
    out = {}
    for s, r in now.items():
        o = old.get(s)
        try:
            e1, e0 = float(r[2]), float(o[2])
        except (TypeError, ValueError, IndexError):
            continue
        if o and r[1] == o[1] and e0 != 0:   # same fiscal quarter, so the change is a real revision
            chg = round((e1 / e0 - 1) * 100, 1)
            row = {"est": e1, "was": e0, "since": os.path.basename(old_f)[:10], "chg": chg}
            if abs(chg) > 40: row["suspect"] = 1   # huge one-step moves are usually a data-source change, not analysts
            out[s] = row
    print(f"revisions: {len(out)} stocks vs snapshot {os.path.basename(old_f)[:10]}")
    return out


def main(out_path):
    si = short_interest()
    ins = insiders(watchlist())
    rev = revisions()
    # keep the file small for phones: only stocks the app can rate (in eps.json) + the watchlist
    try:
        keep = set(json.load(open("eps.json"))["data"]) | set(ins)
    except Exception:
        keep = set(si) | set(ins) | set(rev)
    data = {}
    for s in (set(si) | set(ins) | set(rev)) & keep:
        row = {}
        if s in si: row["si"] = si[s]
        if s in ins: row["ins"] = ins[s]
        if s in rev: row["rev"] = rev[s]
        data[s] = row
    json.dump({"asOf": TODAY.isoformat(), "note": "info/logging only — no Signal Desk rule reads this", "data": data},
              open(out_path, "w"), separators=(",", ":"))
    print(f"wrote {out_path}: {len(data)} symbols")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "footprints.json")
