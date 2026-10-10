"""Signal Desk nightly job: builds earnings.json — every US company's next earnings date (next 3 months).

Source: Alpha Vantage EARNINGS_CALENDAR (free key, one request). The key is stored as the
GitHub secret ALPHAVANTAGE_KEY. If anything goes wrong, yesterday's earnings.json is kept.
"""
import csv, datetime as dt, io, json, os, sys, urllib.request

key = os.environ.get("AV_KEY", "").strip()
if not key:
    print("No ALPHAVANTAGE_KEY secret set - skipping earnings calendar")
    sys.exit(0)
url = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={key}"
try:
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "SignalDesk"}), timeout=120).read().decode("utf-8", "replace")
except Exception as e:
    print(f"Download failed ({e}) - keeping yesterday's earnings.json")
    sys.exit(0)
if not raw.startswith("symbol"):
    print("Unexpected reply - keeping yesterday's earnings.json:", raw[:200])
    sys.exit(0)
data = {}
for r in csv.DictReader(io.StringIO(raw)):
    s, d = (r.get("symbol") or "").upper().strip(), (r.get("reportDate") or "").strip()
    if not s or not d:
        continue
    try:
        est = float(r["estimate"]) if r.get("estimate") else None
    except ValueError:
        est = None
    if s not in data or d < data[s][0]:  # keep the soonest report
        data[s] = [d, r.get("fiscalDateEnding", ""), est, r.get("timeOfTheDay", "")]
if len(data) < 500:
    print(f"Only {len(data)} companies - keeping yesterday's earnings.json")
    sys.exit(0)
out = {"asOf": dt.date.today().isoformat(), "source": "Alpha Vantage earnings calendar (next 3 months)",
       "fields": ["reportDate", "fiscalDateEnding", "epsEstimate", "timeOfDay"], "data": data}
with open("earnings.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
print(f"earnings.json: {len(data)} companies, {os.path.getsize('earnings.json')//1024} KB")
