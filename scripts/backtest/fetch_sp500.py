"""Point-in-time S&P 500 membership (github.com/fja05680/sp500) + prices/SEC data for past members
that are not in the main price cache. Usage: python fetch_sp500.py MAIN_PRICES EXTRA_PRICES SEC_DIR WORK_DIR"""
import concurrent.futures as cf, csv, json, os, subprocess, sys
import fetch_prices as fp

main_dir, extra, sec_dir, work = sys.argv[1:5]
repo = os.path.join(work, "sp500")
if not os.path.exists(repo):
    subprocess.run(["git", "clone", "-q", "--depth", "1", "https://github.com/fja05680/sp500.git", repo], check=True)
rows = list(csv.DictReader(open(os.path.join(repo, "sp500_ticker_start_end.csv"))))
need = {r["ticker"].replace(".", "-") for r in rows if not r["end_date"] or r["end_date"] >= "2016-06-01"}
have = {f[:-7] for f in os.listdir(main_dir) if f.endswith(".csv.gz")}
os.makedirs(extra, exist_ok=True)
miss = sorted(need - have)
with cf.ThreadPoolExecutor(8) as ex:
    got = [s for s, how in ex.map(lambda s: fp.fetch(s, extra), miss) if how != "failed"]
json.dump({"symbols": got, "meta": {}}, open(os.path.join(extra, "universe.json"), "w"))
print(f"{len(need)} members since mid-2016 · {len(miss)} not in main cache · prices found for {len(got)} (the rest were bought out / delisted)")
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "fetch_sec.py"), extra, sec_dir], check=True)
