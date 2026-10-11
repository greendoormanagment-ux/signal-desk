"""Download ~10 years of daily bars (split-adjusted OHLC + volume) for the backtest universe.

Source: Yahoo chart API (free, no key), Nasdaq historical API as a fallback.
Writes one gzipped CSV per ticker into the cache folder. Re-runs skip files fresher than 1 day.
Usage: python fetch_prices.py CACHE_DIR [min_market_cap_billions]
"""
import concurrent.futures as cf, csv, gzip, io, json, os, sys, time, urllib.request, datetime as dt

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9"}
INDEXES = ["SPY", "QQQ", "RSP"]
WATCH = ("MU NVDA AVGO AMD PLTR APP DELL ANET MRVL LRCX AMAT ARM ORCL GOOGL AMZN MSFT SHOP DDOG HOOD IBKR APO BX "
         "FIX PWR VRT GEV EME HWM CAT LLY ISRG MEDP SCCO KNSA XOM BP TGT ETON FCX TSLA META NFLX JPM HD NKE").split()


def get(url, tries=3):
    hdr = {"User-Agent": "Mozilla/5.0"} if "yahoo.com" in url else UA  # Yahoo stalls on full browser headers
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=30) as r:
                return json.loads(r.read())
        except Exception as e:
            err = e
            time.sleep(2 + 3 * a)
    raise err


def universe(min_cap):
    f = os.environ.get("SCREENER_JSON")  # optional saved copy of the Nasdaq screener download
    j = json.load(open(f)) if f else get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&download=true")
    rows = j["data"]["rows"]
    out = []
    for r in rows:
        s = r["symbol"].strip().upper()
        if not s.isalpha():           # skip preferreds, units, warrants (e.g. ABC^A, ABC/U)
            continue
        try:
            cap = float(r.get("marketCap") or 0); px = float(r["lastsale"].replace("$", "") or 0)
        except ValueError:
            continue
        if cap >= min_cap * 1e9 and px >= 5:
            out.append((s, r.get("sector") or "", r.get("industry") or "", cap))
    return out


def yahoo(sym):
    j = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=10y&interval=1d&events=split")
    res = j["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    rows = []
    for i, t in enumerate(res.get("timestamp") or []):
        o, h, l, c, v = (q[k][i] for k in ("open", "high", "low", "close", "volume"))
        if None in (o, h, l, c) or not c:
            continue
        d = dt.datetime.utcfromtimestamp(t + res["meta"].get("gmtoffset", -14400)).date().isoformat()
        rows.append((d, round(o, 4), round(h, 4), round(l, 4), round(c, 4), int(v or 0)))
    return rows


def nasdaq(sym):
    asset = "etf" if sym in INDEXES else "stocks"
    to = dt.date.today().isoformat(); fr = (dt.date.today() - dt.timedelta(days=3660)).isoformat()
    j = get(f"https://api.nasdaq.com/api/quote/{sym}/historical?assetclass={asset}&fromdate={fr}&limit=9999&todate={to}")
    num = lambda s: float(str(s).replace("$", "").replace(",", "") or 0)
    rows = []
    for r in j["data"]["tradesTable"]["rows"]:
        m, d, y = r["date"].split("/")
        rows.append((f"{y}-{m}-{d}", num(r["open"]), num(r["high"]), num(r["low"]), num(r["close"]), int(num(r["volume"]))))
    return sorted(rows)


def fetch(sym, cache):
    path = os.path.join(cache, f"{sym}.csv.gz")
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < 86400:
        return sym, "cached"
    for src in (yahoo, nasdaq):
        try:
            rows = src(sym)
            if len(rows) >= 260:
                with gzip.open(path, "wt") as f:
                    w = csv.writer(f); w.writerow(["date", "o", "h", "l", "c", "v"]); w.writerows(rows)
                return sym, src.__name__
        except Exception as e:
            last = e
    return sym, "failed"


if __name__ == "__main__":
    cache = sys.argv[1]; min_cap = float(sys.argv[2]) if len(sys.argv) > 2 else 2
    os.makedirs(cache, exist_ok=True)
    uni = universe(min_cap)
    have = {u[0] for u in uni}
    meta = {u[0]: {"sector": u[1], "industry": u[2], "cap": u[3]} for u in uni}
    syms = INDEXES + [s for s in WATCH if s not in have] + [u[0] for u in uni]
    json.dump({"asOf": dt.date.today().isoformat(), "minCapB": min_cap, "meta": meta, "symbols": syms},
              open(os.path.join(cache, "universe.json"), "w"))
    stats = {}
    with cf.ThreadPoolExecutor(6) as ex:
        for n, (s, how) in enumerate(ex.map(lambda s: fetch(s, cache), syms), 1):
            stats[how] = stats.get(how, 0) + 1
            if n % 200 == 0:
                print(n, stats, flush=True)
    print("done", len(syms), stats)
