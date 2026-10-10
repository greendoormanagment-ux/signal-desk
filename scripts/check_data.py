"""Signal Desk nightly sanity check (Fix List #46). Runs AFTER the data is saved.
It never changes any data — it only looks for obvious problems. If it finds one, this step fails,
so GitHub emails you "Run failed". The log for this step says exactly what looked wrong."""
import datetime as dt, json, sys

today = dt.date.today()
problems, notes = [], []
WATCH = ["AAPL", "MSFT", "NVDA", "AMZN", "LLY", "XOM", "FCX", "KNSA", "PLTR", "TGT"]

def load(name):
    try:
        with open(name) as f:
            return json.load(f)
    except Exception as e:
        problems.append(f"{name}: could not read ({e})")
        return None

def age(asof):
    try:
        return (today - dt.date.fromisoformat(asof)).days
    except Exception:
        return 999

eps = load("eps.json")
if eps:
    d = eps.get("data", {})
    a = age(eps.get("asOf", ""))
    if a > 3: problems.append(f"eps.json is {a} days old (asOf {eps.get('asOf')}) - SEC download may be failing")
    if len(d) < 4000: problems.append(f"eps.json has only {len(d)} companies (normally ~5,800)")
    for t in WATCH:
        r = d.get(t)
        if not r: problems.append(f"eps.json: {t} missing")
        elif age(r[0]) > 200: problems.append(f"eps.json: {t} latest quarter ended {r[0]} - looks stale")
    big = sum(1 for r in d.values() if isinstance(r[3], (int, float)) and r[3] > 500)
    notes.append(f"eps.json: {len(d)} companies, asOf {eps.get('asOf')}, {big} with EPS growth >500% (info only)")

cal = load("earnings.json")
if cal:
    d = cal.get("data", {})
    a = age(cal.get("asOf", ""))
    if a > 3: problems.append(f"earnings.json is {a} days old (asOf {cal.get('asOf')}) - Alpha Vantage may be failing")
    if len(d) < 2000: problems.append(f"earnings.json has only {len(d)} companies (normally ~4,500)")
    past = [s for s, r in d.items() if r[0] < cal.get("asOf", "")]
    if len(past) > max(20, len(d) // 100): problems.append(f"earnings.json: {len(past)} dates already in the past, e.g. {past[:5]}")
    notes.append(f"earnings.json: {len(d)} companies, asOf {cal.get('asOf')}, {len(past)} past dates")

for n in notes: print("OK  ", n)
for p in problems: print("PROBLEM", p)
if problems:
    print(f"\n{len(problems)} problem(s) found - check before trusting today's scans.")
    sys.exit(1)
print("All data checks passed.")
