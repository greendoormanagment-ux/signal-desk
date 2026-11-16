"""Signal Desk nightly job: builds sectors.json — sector and industry for every US-listed stock, from Nasdaq's free
stock screener (one request, no key). DISPLAY ONLY: shown under the company name when the AI check didn't run.
Nasdaq's sector names are mapped to the app's 11; its industry text is kept as is.
If Nasdaq can't be reached, yesterday's file is kept (the step never blocks the job).
Usage: python scripts/build_sectors.py sectors.json
"""
import datetime as dt, json, sys, urllib.request

URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&download=true"
MAP = {"Finance": "Financial", "Health Care": "Healthcare", "Consumer Discretionary": "Consumer Cyclical",
       "Consumer Staples": "Consumer Defensive", "Telecommunications": "Communication Services",
       "Technology": "Technology", "Industrials": "Industrials", "Real Estate": "Real Estate", "Energy": "Energy",
       "Utilities": "Utilities", "Basic Materials": "Basic Materials"}


def main(out_path):
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh) SignalDesk/1.0", "Accept": "application/json"})
    rows = json.load(urllib.request.urlopen(req, timeout=60))["data"]["rows"]
    data = {}
    for r in rows:
        sym = (r.get("symbol") or "").strip().upper().replace("/", ".").replace("-", ".")
        sec, ind = MAP.get((r.get("sector") or "").strip(), ""), (r.get("industry") or "").strip()
        if sym and (sec or ind):
            data[sym] = [sec, ind]
    if len(data) < 3000:
        raise SystemExit(f"only {len(data)} stocks with a sector — keeping yesterday's file")
    json.dump({"asOf": dt.date.today().isoformat(), "source": "Nasdaq stock screener", "data": data},
              open(out_path, "w"), separators=(",", ":"))
    print(f"sectors.json: {len(data)} stocks")


if __name__ == "__main__":
    main(sys.argv[1])
