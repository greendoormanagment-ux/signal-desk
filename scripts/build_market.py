"""Signal Desk nightly job: builds market.json — daily market-risk readings from the Federal Reserve's
free FRED database (no key needed). LOGGING ONLY: no rule uses these yet. The November backtest will
test whether adding them to the market gate would have avoided losses.

  BAMLH0A0HYM2  high-yield (junk) bond spread over Treasuries, %   — widening = credit stress
  VIXCLS        VIX, the market's expected volatility ("fear gauge")
  T10Y3M        10-year minus 3-month Treasury yield, %             — below 0 = inverted curve
  T10Y2Y        10-year minus 2-year Treasury yield, %
Keeps about 2 years of daily history in the file. If FRED is down, yesterday's file is kept.
"""
import csv, datetime as dt, io, json, os, sys, urllib.request

SERIES = {"hySpread": "BAMLH0A0HYM2", "vix": "VIXCLS", "curve10y3m": "T10Y3M", "curve10y2y": "T10Y2Y"}
TODAY = dt.date.today()
START = (TODAY - dt.timedelta(days=730)).isoformat()


def fetch(sid):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={START}"
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "SignalDesk/1.0 (+greendoorhomesct@gmail.com)"}), timeout=30).read().decode()
    out = {}
    for row in csv.reader(io.StringIO(raw)):
        if len(row) == 2 and row[0][:2] == "20" and row[1] not in ("", "."):
            out[row[0]] = float(row[1])
    return out


def main(out_path):
    data, latest = {}, {}
    for key, sid in SERIES.items():
        try:
            s = fetch(sid)
        except Exception as e:
            print(f"{sid}: download failed ({e})")
            continue
        if not s:
            continue
        data[key] = s
        d = max(s)
        latest[key] = {"date": d, "value": s[d]}
        print(f"{sid}: {len(s)} days, latest {d} = {s[d]}")
    if len(data) < 3:
        sys.exit("Too few series downloaded — keeping yesterday's market.json")
    days = sorted({d for s in data.values() for d in s})
    rows = [[d] + [data[k].get(d) for k in SERIES] for d in days]
    out = {"asOf": TODAY.isoformat(), "source": "FRED (St. Louis Fed)", "fields": ["date"] + list(SERIES),
           "latest": latest, "rows": rows}
    with open(out_path, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"market.json: {len(rows)} days, {os.path.getsize(out_path)//1024} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "market.json")
