"""Signal Desk nightly job: builds eps.json from the SEC's free company-facts bulk file.

For every US-listed company it finds the latest quarterly diluted EPS and the same
quarter one year earlier (fiscal Q4 is derived as full year minus nine months),
then writes a small lookup file the app reads instantly. Runs on GitHub Actions.
"""
import datetime as dt, json, os, sys, time, urllib.request, zipfile

UA = {"User-Agent": "GreenDoor SignalDesk greendoorhomesct@gmail.com"}
TAGS = ["EarningsPerShareDiluted", "EarningsPerShareBasicAndDiluted", "EarningsPerShareBasic"]
TODAY = dt.date.today()


def get(url, path=None):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r:
        if path is None:
            return r.read()
        with open(path, "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
        return path


def days(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def calc(units):
    facts = (units or {}).get("USD/shares", [])
    if isinstance(facts, dict):
        facts = list(facts.values())
    q, y, n9 = {}, {}, {}
    for f in facts:
        if not f.get("start") or not f.get("end"):
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
            q[e] = {"end": e, "val": round(f["val"] - nine["val"], 4), "filed": f.get("filed", ""), "derived": True}
    if not q:
        return None
    ends = sorted(q)
    last = q[ends[-1]]
    prev = next((q[e] for e in ends if abs(days(e, last["end"]) - 365) <= 20), None)
    if not prev:
        return None
    g = round((last["val"] - prev["val"]) / prev["val"] * 100, 1) if prev["val"] > 0 else None
    return [last["end"], last["val"], prev["val"], g, last.get("filed", ""), 1 if last.get("derived") else 0]


def main(out_path, zip_path):
    tickers = json.loads(get("https://www.sec.gov/files/company_tickers.json"))
    by_cik = {}
    for v in tickers.values():
        by_cik.setdefault(int(v["cik_str"]), []).append(v["ticker"].upper())
    if not (os.path.exists(zip_path) and zipfile.is_zipfile(zip_path)):
        for attempt in range(1, 4):  # big file: retry if the download is cut short
            try:
                get("https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip", zip_path)
                if zipfile.is_zipfile(zip_path):
                    break
            except Exception as e:
                print(f"download attempt {attempt} failed: {e}")
            time.sleep(30)
        else:
            sys.exit("Could not download the SEC file — keeping yesterday's eps.json")
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
            if b"EarningsPerShare" not in raw:
                continue
            seen += 1
            gaap = (json.loads(raw).get("facts") or {}).get("us-gaap") or {}
            best = None
            for tag in TAGS:
                if tag in gaap:
                    r = calc(gaap[tag].get("units"))
                    if r and (best is None or r[0] > best[0]):
                        best = r
            if best and days(best[0], TODAY.isoformat()) <= 400:
                for t in by_cik[cik]:
                    data[t.replace("-", ".")] = best
                    data[t] = best
    out = {"asOf": TODAY.isoformat(), "source": "SEC EDGAR company facts (GAAP, includes one-time items)",
           "fields": ["qEnd", "eps", "prevEps", "growthPct", "filed", "q4Derived"], "data": data}
    with open(out_path, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"companies scanned: {seen}, tickers written: {len(data)}, size: {os.path.getsize(out_path)//1024} KB")
    if len(data) < 1000:
        sys.exit("Too few results — not publishing")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "eps.json", sys.argv[2] if len(sys.argv) > 2 else "/tmp/companyfacts.zip")
