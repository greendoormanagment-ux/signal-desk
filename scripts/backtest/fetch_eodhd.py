"""Gate 3 data: daily bars for EVERY company that was in the S&P 500 since 2004 — including the ones that later
failed, were bought out or were delisted — from EODHD (paid "EOD Historical Data" plan, one month is enough).

Usage: EODHD_KEY=... python fetch_eodhd.py MEMBERS_CSV OUT_DIR [FROM_DATE]
  MEMBERS_CSV = sp500_ticker_start_end.csv (github.com/fja05680/sp500)
Writes OUT_DIR/<TICKER>.csv.gz (date,o,h,l,c,v — same format as fetch_prices.py), OUT_DIR/universe.json
(symbols + company names, used by fetch_sec.py to find SEC filings of delisted companies) and
OUT_DIR/coverage.json / coverage.md (how much of each company's S&P 500 membership has price data).

Adjustment: EODHD gives raw OHLC + an adjusted close (splits AND dividends). Bars are scaled by
adjusted_close / close, so prices are split- and dividend-adjusted; volume is divided by the same factor.
Re-used tickers: when a ticker's history does not cover its membership (an old company used the same
symbol), the delisted list is searched for a code like "<TICKER>_old"-style variants; the best-covering one wins.

The key comes ONLY from the EODHD_KEY environment variable (a GitHub Actions secret) and is never printed.
EODHD's data licence does not allow republishing it: the files stay in the private Actions cache and are
never committed to the public repo.
"""
import concurrent.futures as cf, csv, datetime as dt, gzip, json, os, re, sys, time, urllib.error, urllib.request

KEY = os.environ.get("EODHD_KEY", "").strip()
BASE = "https://eodhd.com/api"
INDEXES = ["SPY", "QQQ", "RSP"]


def call(path, **q):
    q.update(api_token=KEY, fmt="json")
    url = f"{BASE}/{path}?" + "&".join(f"{k}={v}" for k, v in q.items())
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:                  # never echo the URL (it holds the key)
            if e.code in (404, 422):
                return None
            if e.code in (401, 402, 403):
                sys.exit(f"EODHD refused the key (HTTP {e.code}) — is the paid plan active?")
            time.sleep(3 + 5 * a)
        except Exception:
            time.sleep(3 + 5 * a)
    return None


def bars(code, frm):
    j = call(f"eod/{code}.US", **{"from": frm})
    if not isinstance(j, list):
        return []
    out = []
    for r in j:
        try:
            c, ac = float(r["close"]), float(r.get("adjusted_close") or r["close"])
            if c <= 0:
                continue
            f = ac / c
            out.append((r["date"], round(float(r["open"]) * f, 4), round(float(r["high"]) * f, 4), round(float(r["low"]) * f, 4),
                        round(ac, 4), int(float(r.get("volume") or 0) / f) if f > 0 else 0))
        except (KeyError, TypeError, ValueError):
            continue
    return out


def covered(rows, spans, frm):
    """Share of membership weekdays (from FROM_DATE on) that have a bar within 5 days."""
    if not rows:
        return 0.0
    have = [r[0] for r in rows]
    tot = hit = 0
    import bisect
    for a, b in spans:
        a = max(a, frm); b = min(b, dt.date.today().isoformat())
        if a > b:
            continue
        d = dt.date.fromisoformat(a)
        while d.isoformat() <= b:
            if d.weekday() < 5:
                tot += 1
                k = bisect.bisect_left(have, d.isoformat())
                if k < len(have) and (dt.date.fromisoformat(have[k]) - d).days <= 5:
                    hit += 1
            d += dt.timedelta(days=7)                         # weekly sampling is plenty for a coverage %
    return hit / tot if tot else 1.0


def main(members_csv, out, frm="2003-01-01"):
    if not KEY:
        sys.exit("EODHD_KEY is not set (add it as a repository secret).")
    os.makedirs(out, exist_ok=True)
    spans = {}
    for r in csv.DictReader(open(members_csv)):
        end = r["end_date"] or "9999-12-31"
        if end >= "2004-01-01":
            spans.setdefault(r["ticker"].replace(".", "-"), []).append((r["start_date"], end))
    lists = {}
    for st, extra in (("active", {}), ("delisted", {"delisted": 1})):
        lst = call("exchange-symbol-list/US", **extra)
        if not isinstance(lst, list):
            sys.exit(f"Could not read the {st} ticker list.")
        lists[st] = lst
    names, codes = {}, {}
    for st in ("active", "delisted"):
        for s in lists[st]:
            c = str(s.get("Code", "")).upper()
            if s.get("Type") in ("Common Stock", "ETF", "FUND", None):
                codes.setdefault(re.sub(r"[^A-Z]", "", c.split("_")[0].split(".")[0]), []).append(c)
                names.setdefault(c, s.get("Name") or "")
    print(f"{len(spans)} S&P 500 members since 2004 · EODHD lists {len(lists['active']):,} active / {len(lists['delisted']):,} delisted US codes", flush=True)

    def one(sym):
        path = os.path.join(out, f"{sym}.csv.gz")
        if os.path.exists(path) and time.time() - os.path.getmtime(path) < 3 * 86400:
            return sym, "cached", None, 1.0
        cands = [sym] + [c for c in codes.get(re.sub(r"[^A-Z]", "", sym), []) if c != sym]
        best = (None, [], -1.0)
        for c in cands[:6]:
            rows = bars(c, frm)
            cov = covered(rows, spans.get(sym, [("1900-01-01", "9999-12-31")]), frm)
            if cov > best[2]:
                best = (c, rows, cov)
            if cov >= 0.98:
                break
        code, rows, cov = best
        if len(rows) < 260:
            return sym, "missing", code, max(cov, 0.0)
        with gzip.open(path, "wt") as f:
            w = csv.writer(f); w.writerow(["date", "o", "h", "l", "c", "v"]); w.writerows(rows)
        return sym, "ok", code, cov

    syms = INDEXES + sorted(spans)
    got, rep = [], []
    with cf.ThreadPoolExecutor(8) as ex:
        for n, (s, how, code, cov) in enumerate(ex.map(one, syms), 1):
            if how != "missing":
                got.append(s)
            rep.append({"ticker": s, "status": how, "eodhd_code": code, "membership_covered": round(cov, 3)})
            if n % 100 == 0:
                print(n, sum(1 for r in rep if r["status"] != "missing"), "with data", flush=True)
    json.dump({"asOf": dt.date.today().isoformat(), "source": "EODHD", "from": frm, "symbols": got, "meta": {},
               "names": {r["ticker"]: names.get(r["eodhd_code"] or r["ticker"], "") for r in rep if r["status"] != "missing"}},
              open(os.path.join(out, "universe.json"), "w"))
    mem = [r for r in rep if r["ticker"] not in INDEXES]
    full = sum(1 for r in mem if r["membership_covered"] >= 0.95)
    summ = {"asOf": dt.date.today().isoformat(), "members_since_2004": len(mem), "with_prices": sum(1 for r in mem if r["status"] != "missing"),
            "membership_95pct_covered": full, "membership_95pct_covered_%": round(100 * full / max(len(mem), 1), 1)}
    json.dump({"summary": summ, "tickers": rep}, open(os.path.join(out, "coverage.json"), "w"), indent=1)
    L = [f"# EODHD price coverage of S&P 500 members since 2004 ({summ['asOf']})", "",
         f"- Members: **{summ['members_since_2004']}** · with price data: **{summ['with_prices']}** · "
         f"≥95% of their membership covered: **{full} ({summ['membership_95pct_covered_%']}%)**", "",
         "Gate 3 pass mark: ≥ 90% of members covered. Below that, the Round 4 results still carry survivorship bias.", "",
         "| Ticker | Status | EODHD code | Membership covered |", "| --- | --- | --- | --- |"]
    L += [f"| {r['ticker']} | {r['status']} | {r['eodhd_code'] or ''} | {round(100*r['membership_covered'])}% |"
          for r in sorted(mem, key=lambda r: r["membership_covered"]) if r["membership_covered"] < 0.95]
    open(os.path.join(out, "coverage.md"), "w").write("\n".join(L) + "\n")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
