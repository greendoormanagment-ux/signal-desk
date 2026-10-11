"""Signal Desk backtest engine.

Replays the app's ENTRY SCAN rules (index.html v2.9.7, runRuleEngine "entry" mode) on every stock,
every trading day, using only data that was public on that day:
  * prices: daily bars (split-adjusted), scan assumed after the 4pm close
  * market gate: SPY + QQQ 50-day trend and distribution days (idxStatus / marketFromIndexes)
  * fundamentals: SEC EPS as filed by that date (same math as build_eps.py, 135-day staleness)
  * earnings block: next 8-K Item 2.02 (earnings release) date, 14 days
Then it buys BUY signals at the next day's open and manages them with stop rule A2 ("earn the trail")
and the Position Review sell rules. Rule VARIANTS change one thing at a time so they can be compared.

Known limits (also printed in the report):
  * survivorship bias: universe = stocks listed today (Fix List #69)
  * daily bars only: no intraday entries; stops fill at the stop or the open if it gaps through
  * SEC GAAP EPS includes one-time items (the app has the same limit)
"""
import bisect, datetime as dt, gzip, json, math, os
import numpy as np, pandas as pd
np.seterr(all="ignore")

W = dict(market=20, trend=15, entry=20, momentum=10, volume=10, rs=10, fundamentals=15)
BASE = dict(name="base (live rules v2.9.7)", vol_need=1.4, pb_lo=-3.0, pb_hi=3.0, pb_need_rising=False,
            pb_need_low_vol=False, block_pressure=False, need_rs=False, eps_min=25.0, rev_min=None,
            earn_days=14, stop="A2", atr_mult=3.0, stage4_exit=True, breakout_only=False, pullback_only=False,
            max_ext=5.0, min_rsrank=None, trend_template=False, mkt_mode="live")


# ───────────────────────── data ─────────────────────────
def load_prices(cache):
    out = {}
    for f in os.listdir(cache):
        if not f.endswith(".csv.gz"):
            continue
        df = pd.read_csv(os.path.join(cache, f), compression="gzip")
        df = df[(df.c > 0) & (df.h >= df.l)].drop_duplicates("date").sort_values("date")
        if len(df) >= 300:
            out[f[:-7]] = df.reset_index(drop=True)
    return out


def _days(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def _calc(facts, asof):
    """build_eps.py calc() using only facts filed on or before `asof`."""
    q, y, n9 = {}, {}, {}
    for s, e, v, f in facts:
        if f > asof:
            continue
        d = _days(s, e)
        t = q if 80 <= d <= 100 else y if 350 <= d <= 380 else n9 if 260 <= d <= 285 else None
        if t is None:
            continue
        if e not in t or f > t[e][3]:
            t[e] = (s, e, v, f)
    q = {e: (r[2], r[3], False) for e, r in q.items()}
    for e, r in y.items():
        if e in q:
            continue
        nine = next((g for g in n9.values() if g[0] == r[0]), None)
        if nine:
            q[e] = (round(r[2] - nine[2], 4), r[3], True)
    if not q:
        return None
    ends = sorted(q)
    le = ends[-1]
    pe = next((e for e in ends if abs(_days(e, le) - 365) <= 20), None)
    if pe is None:
        return None
    return (le, q[le][0], q[pe][0])


def fundamentals_timeline(rec, key, tags_order):
    """List of (filed_date, qEnd, latest, yearAgo) — the SEC reading as it changed over time."""
    facts = rec.get(key) or {}
    dates = sorted({f[3] for tag in facts for f in facts[tag]})
    tl = []
    for F in dates:
        best = None
        for tag in tags_order:
            if tag in facts:
                r = _calc(facts[tag], F)
                if r and (best is None or r[0] > best[0]):
                    best = r
        if best and (not tl or tl[-1][1:] != best):
            tl.append((F,) + best)
    return tl


EPS_TAGS = ["EarningsPerShareDiluted", "EarningsPerShareBasicAndDiluted", "EarningsPerShareBasic"]
REV_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet",
            "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet"]


def load_sec(sec_dir, sym):
    p = os.path.join(sec_dir, f"{sym}.json.gz")
    if not os.path.exists(p):
        return None
    rec = json.load(gzip.open(p, "rt"))
    return {"eps": fundamentals_timeline(rec, "eps", EPS_TAGS), "rev": fundamentals_timeline(rec, "rev", REV_TAGS),
            "earn": rec.get("earn") or []}


# ───────────────────────── indicators ─────────────────────────
def wilder(x, n=14):
    out = np.full(len(x), np.nan)
    if len(x) <= n:
        return out
    a = np.nanmean(x[1:n + 1])
    out[n] = a
    for i in range(n + 1, len(x)):
        a = (a * (n - 1) + x[i]) / n
        out[i] = a
    return out


def indicators(df):
    c, h, l, v = (df[k].to_numpy(float) for k in ("c", "h", "l", "v"))
    s = pd.Series(c)
    o = {}
    o["sma50"] = s.rolling(50).mean().to_numpy()
    o["sma200"] = s.rolling(200).mean().to_numpy()
    o["sma50_10"] = pd.Series(o["sma50"]).shift(10).to_numpy()
    o["sma150"] = s.rolling(150).mean().to_numpy()
    o["sma200_20"] = pd.Series(o["sma200"]).shift(20).to_numpy()
    o["hi52"] = pd.Series(h).rolling(252).max().to_numpy()
    o["lo52"] = pd.Series(l).rolling(252).min().to_numpy()
    o["avgv"] = pd.Series(v).rolling(50).mean().shift(1).to_numpy()          # 50-day avg volume, excluding today
    d = np.diff(c, prepend=c[0])
    g, ls = wilder(np.maximum(d, 0)), wilder(np.maximum(-d, 0))
    with np.errstate(divide="ignore", invalid="ignore"):
        o["rsi"] = np.where(ls == 0, 100, 100 - 100 / (1 + g / ls))
    pc = np.roll(c, 1); pc[0] = c[0]
    tr = np.maximum.reduce([h - l, np.abs(h - pc), np.abs(l - pc)])
    o["atr"] = wilder(tr)
    o["pivot"] = pd.Series(h).rolling(252).max().shift(5).to_numpy()          # prior-year high, excl. last 5 sessions
    piv = o["pivot"]
    found = np.zeros(len(c), bool); vr = np.full(len(c), np.nan); ago = np.full(len(c), np.nan)
    ratio = v / o["avgv"]
    for k in (4, 3, 2, 1, 0):                                                   # earliest close above the pivot wins
        ck = pd.Series(c).shift(k).to_numpy(); rk = pd.Series(ratio).shift(k).to_numpy()
        hit = (ck > piv) & ~found
        vr[hit] = rk[hit]; ago[hit] = k; found |= hit
    o["bo_found"], o["bo_vr"], o["bo_ago"] = found, vr, ago
    o["volratio"] = ratio
    return o


def market_status(spy, qqq):
    def idx(df):
        c, v = df.c.to_numpy(float), df.v.to_numpy(float)
        st = {}
        for t in range(60, len(c)):
            ma = c[t - 49:t + 1].mean(); mp = c[t - 54:t - 4].mean(); last = c[t]; rising = ma > mp
            dd = 0
            for i in range(max(1, t - 24), t + 1):
                if c[i] <= c[i - 1] * 0.998 and v[i] > v[i - 1] and last < c[i] * 1.05:
                    dd += 1
            s = "CORRECTION" if (last < ma and not rising) else "PRESSURE" if (last < ma or dd >= 5) else "UPTREND"
            st[df.date.iat[t]] = (s, dd, (last / ma - 1) * 100)
        return st
    a, b = idx(spy), idx(qqq)
    s200 = spy.c.rolling(200).mean()
    simple = {d: ("UPTREND" if c > m else "CORRECTION") for d, c, m in zip(spy.date, spy.c, s200) if m == m}
    out = {}
    for d in a:
        if d in b:
            x, y = a[d][0], b[d][0]
            out[d] = "CORRECTION" if (x == "CORRECTION" and y == "CORRECTION") else \
                     "PRESSURE" if (x != "UPTREND" or y != "UPTREND") else "UPTREND"
    return {"live": out, "spy200": simple}


_PIT = {}


def point_in_time(sym, dates, sec):
    """EPS growth, revenue growth and days-to-next-earnings for every day, using only what was filed by then.
    g: nan = no usable SEC reading (missing or quarter older than 135 days) · -inf = not profitable · 999 = turned profitable
    edays: nan = next date unknown (neutral) · -1 = no date on file but last report was recent (counts as pass)"""
    if sym in _PIT:
        return _PIT[sym]
    n = len(dates)
    g, rv, ed = np.full(n, np.nan), np.full(n, np.nan), np.full(n, np.nan)
    if sec:
        fd = [r[0] for r in sec["eps"]]; rd = [r[0] for r in sec["rev"]]; er = sec["earn"]
        for i, d in enumerate(dates):
            j = bisect.bisect_right(fd, d) - 1
            if j >= 0:
                F, qe, eps, prev = sec["eps"][j]
                if _days(qe, d) <= 135:
                    g[i] = -np.inf if eps <= 0 else 999.0 if prev <= 0 else (eps - prev) / prev * 100
            j = bisect.bisect_right(rd, d) - 1
            if j >= 0:
                F, qe, a, b = sec["rev"][j]
                if _days(qe, d) <= 135 and b and b > 0:
                    rv[i] = (a - b) / b * 100
            if er:
                j = bisect.bisect_left(er, d)
                if j < len(er):
                    k = _days(d, er[j])
                    if k <= 100:
                        ed[i] = k
                elif _days(er[-1], d) < 80:
                    ed[i] = -1
    _PIT[sym] = {"g": g, "rev": rv, "edays": ed}
    return _PIT[sym]


# ───────────────────────── rule engine (vectorized per stock) ─────────────────────────
def evaluate(sym, df, ind, sec, mkt, spy_close, P):
    n = len(df)
    dates = df.date.to_numpy()
    c = df.c.to_numpy(float)
    s50, s200, piv = ind["sma50"], ind["sma200"], ind["pivot"]
    ok = ~np.isnan(s200) & ~np.isnan(piv) & ~np.isnan(ind["atr"])
    # market
    mk = mkt[P["mkt_mode"]] if "live" in mkt else mkt
    m = np.array([mk.get(d, "UNKNOWN") for d in dates])
    m_fail = (m == "CORRECTION") | (m == "UNKNOWN")
    if P["block_pressure"]:
        m_fail |= (m == "PRESSURE")
    # trend
    abv50, abv200 = c > s50, c > s200
    t_pass = abv50 & abv200 & (s50 > s200)
    t_fail = ~abv200
    # entry
    pct = (c - piv) / piv * 100
    from50 = (c - s50) / s50 * 100
    brk_zone = (c > piv) & (pct <= P["max_ext"])
    vr = ind["bo_vr"]
    breakout = brk_zone & ind["bo_found"] & (np.nan_to_num(vr) >= P["vol_need"])
    weak = brk_zone & ~breakout
    nearpb = (from50 >= P["pb_lo"]) & (from50 <= P["pb_hi"]) & ~brk_zone
    if P["pb_need_rising"]:
        nearpb &= s50 > ind["sma50_10"]
    if P["pb_need_low_vol"]:
        nearpb &= np.nan_to_num(ind["volratio"], nan=9) < 1.0
    pb_base = (from50 >= -3) & (from50 <= 3) & ~brk_zone          # the live rule's zone (for setup labels)
    extended = ~brk_zone & ~pb_base & (pct > P["max_ext"])
    watch = ~brk_zone & ~pb_base & ~extended & (pct >= -5) & abv50
    if P["breakout_only"]:
        nearpb = np.zeros(n, bool)
    if P["pullback_only"]:
        breakout = np.zeros(n, bool)
    e_pass = breakout | nearpb
    watch_flag = watch                                               # weak breakout = fail, not watch (as in app)
    setup = np.where(breakout, "BREAKOUT", np.where(nearpb, "PULLBACK", np.where(weak, "WEAK_BREAKOUT",
             np.where(pb_base, "PULLBACK_FILTERED", np.where(extended, "EXTENDED", np.where(watch, "WATCH", "NONE"))))))
    # fundamentals + earnings dates (point in time; computed once per stock, reused by every variant)
    pit = point_in_time(sym, dates, sec)
    g_arr = pit["g"]
    f_stat = np.where(np.isnan(g_arr), "neutral", np.where(g_arr >= P["eps_min"], "pass", "fail")).astype(object)
    if P["rev_min"] is not None:
        f_stat = np.where((f_stat == "pass") & ~(np.nan_to_num(pit["rev"], nan=-999) >= P["rev_min"]), "fail", f_stat)
    edays = pit["edays"]
    e_stat = np.where(np.isnan(edays), "neutral", np.where((edays >= 0) & (edays <= P["earn_days"]), "fail", "pass")).astype(object)
    # relative strength (score only in the live rules)
    sc = np.array([spy_close.get(d, np.nan) for d in dates])
    ratio = pd.Series(c / sc)
    mans = (ratio / ratio.rolling(252, min_periods=130).mean() - 1).to_numpy() * 100
    rel3 = (ratio / ratio.shift(63) - 1).to_numpy() * 100
    rs = np.where((mans > 0) & (rel3 > 0), "pass", np.where((mans < 0) & (rel3 < 0), "fail", "neutral"))
    # rating — same order as runRuleEngine
    rating = np.full(n, "BUY", dtype=object)
    entry_fail = ~e_pass
    rating[entry_fail] = np.where(watch_flag[entry_fail], "WATCH", "DONT_BUY")
    rating[(f_stat == "fail") & ~entry_fail] = "DONT_BUY"
    rating[(e_stat == "fail") & ~entry_fail & (f_stat != "fail")] = "DONT_BUY"
    rating[t_fail] = "DONT_BUY"
    rating[m_fail] = "DONT_BUY"
    unv = (f_stat == "neutral") | (e_stat == "neutral")
    rating[(rating == "BUY") & unv] = "CHECK_FIRST"
    if P["need_rs"]:
        rating[(rating == "BUY") & (rs != "pass")] = "DONT_BUY"
    if P["min_rsrank"] is not None:                                  # IBD-style RS rank vs the whole universe (0-99)
        rating[(rating == "BUY") & ~(np.nan_to_num(ind.get("rsrank", np.full(n, np.nan)), nan=-1) >= P["min_rsrank"])] = "DONT_BUY"
    if P["trend_template"]:                                          # Minervini trend template
        tt = (c > ind["sma150"]) & (c > s200) & (s50 > ind["sma150"]) & (ind["sma150"] > s200) & (s200 > ind["sma200_20"]) \
             & (c >= ind["lo52"] * 1.3) & (c >= ind["hi52"] * 0.75)
        rating[(rating == "BUY") & ~tt] = "DONT_BUY"
    rating[(rating == "WATCH") & ((f_stat == "fail") | (e_stat == "fail") | (m == "CORRECTION"))] = "DONT_BUY"
    rating[(c < s200) & (s50 < s200)] = "SELL"
    rating[~ok] = "NA"
    # stop at the signal (breakout: pivot −7%, pullback: 50-day −7%, never more than 8% under the buy zone)
    stop = np.where(breakout, piv * 0.93, np.where(nearpb, s50 * 0.93, np.nan))
    zlo = np.where(breakout, piv, s50 * 0.97); zhi = np.where(breakout, piv * 1.05, s50 * 1.03)
    ref = np.minimum(np.maximum(c, zlo), zhi)
    stop = np.maximum(stop, ref * 0.92)
    # score (used to rank same-day buys in the portfolio)
    rsi = ind["rsi"]
    score = (np.where(m == "UPTREND", 20, np.where(m == "PRESSURE", 8, 0)) + np.where(t_pass, 15, np.where(abv200, 6, 0))
             + np.where(e_pass, 20, np.where(watch, 10, np.where(weak, 5, 0)))
             + np.where((rsi >= 40) & (rsi <= 75), 10, np.where((rsi > 75) & (rsi <= 80), 5, 0))
             + np.where(rs == "pass", 10, np.where(rs == "neutral", 5, 0))
             + np.where(f_stat == "pass", 15, np.where(f_stat == "neutral", 8, 0)) + 10)
    rsr = ind.get("rsrank", np.full(n, np.nan))
    return pd.DataFrame({"sym": sym, "date": dates, "rsrank": rsr, "close": c, "rating": rating, "setup": setup, "market": m,
                         "fund": f_stat, "eps_g": g_arr, "earn": e_stat, "earn_days": edays, "rs": rs, "mans": mans,
                         "rel3": rel3, "stop": stop, "score": score, "ext": pct, "from50": from50,
                         "volratio": ind["volratio"], "bo_vr": vr})


# ───────────────────────── trades ─────────────────────────
def simulate_trades(sym, df, ind, sig, P, start, end):
    o, h, l, c = (df[k].to_numpy(float) for k in ("o", "h", "l", "c"))
    dates = df.date.to_numpy(); s50, s200, atr = ind["sma50"], ind["sma200"], ind["atr"]
    rating, stop0, setup = sig.rating.to_numpy(), sig.stop.to_numpy(), sig.setup.to_numpy()
    score = sig.score.to_numpy()
    trades, i, n = [], 0, len(df)
    while i < n - 1:
        if not (start <= dates[i] <= end and rating[i] == "BUY"):
            i += 1; continue
        e_i = i + 1; ep = o[e_i]; orig = stop0[i]
        if not (ep > orig > 0):
            i += 1; continue
        R = ep - orig; stp = orig; hi = h[e_i]; mae = mfe = 0.0
        x_i, xp, why = None, None, None
        j = e_i
        while j < n:
            if j > e_i:
                # stop for today was set after yesterday's close
                lv1, lv2 = ep + R, ep + 2 * R
                if P["stop"] == "A2":
                    new = max(ep, hi - P["atr_mult"] * atr[j - 1]) if hi >= lv2 else (max(orig, ep) if hi >= lv1 else orig)
                elif P["stop"] == "chand":
                    new = max(orig, hi - P["atr_mult"] * atr[j - 1])
                elif P["stop"] == "be1R":
                    new = max(orig, ep) if hi >= lv1 else orig
                else:
                    new = orig
                stp = max(stp, new)                                        # never lower a stop
                if o[j] <= stp:
                    x_i, xp, why = j, o[j], "stop (gap)"; break
            if l[j] <= stp:
                x_i, xp, why = j, stp, "stop"; break
            mae = min(mae, (l[j] - ep) / R); mfe = max(mfe, (h[j] - ep) / R)
            hi = max(hi, h[j])
            # Position Review sells, judged at the close, sold next open
            if j + 1 < n:
                if c[j] <= ep * 0.925:
                    x_i, xp, why = j + 1, o[j + 1], "7.5% loss rule"; break
                if P["stage4_exit"] and c[j] < s200[j] and s50[j] < s200[j]:
                    x_i, xp, why = j + 1, o[j + 1], "stage 4"; break
                if P["stop"] == "ma50" and c[j] < s50[j] * 0.98:
                    x_i, xp, why = j + 1, o[j + 1], "below 50-day"; break
            j += 1
        if x_i is None:
            x_i, xp, why = n - 1, c[n - 1], "open at end"
        trades.append({"sym": sym, "signal": dates[i], "entry_date": dates[e_i], "entry": ep, "stop": orig,
                       "exit_date": dates[x_i], "exit": xp, "why": why, "ret": (xp / ep - 1) * 100,
                       "R": (xp - ep) / R, "days": x_i - e_i, "mae_R": mae, "mfe_R": mfe, "setup": setup[i],
                       "score": score[i], "market": sig.market.iat[i]})
        i = x_i + 1
    return trades


# ───────────────────────── portfolio ─────────────────────────
def rs_rank(prices, cal):
    """IBD-style relative strength: weighted 3/6/9/12-month return, ranked 0-99 across the universe each day."""
    cl = pd.DataFrame({s: df.set_index("date").c for s, df in prices.items()}).reindex(cal)
    perf = 0.4 * cl.pct_change(63, fill_method=None) + 0.2 * cl.pct_change(126, fill_method=None) \
         + 0.2 * cl.pct_change(189, fill_method=None) + 0.2 * cl.pct_change(252, fill_method=None)
    rk = perf.rank(axis=1, pct=True) * 99
    return {s: rk[s] for s in rk.columns}


def portfolio(trades, closes, cal, start, end, cash0=100_000.0, risk=0.01, max_pos=10, max_w=0.20, cost=0.001, seed=None):
    """Takes trades while there is room (10 positions, 1% risk each); marks to market daily.
    seed=None: best score first on the same day · seed=k: random same-day order (for Monte Carlo)."""
    import random
    rnd = random.Random(seed)
    by_day = {}
    for t in trades:
        by_day.setdefault(t["entry_date"], []).append(t)
    for d in by_day:
        if seed is None:
            by_day[d].sort(key=lambda t: -t["score"])
        else:
            rnd.shuffle(by_day[d])
    cash, pos, eq, taken = cash0, {}, [], []
    days = [d for d in cal if start <= d <= end]
    for d in days:
        for k in [k for k, p in pos.items() if p["t"]["exit_date"] <= d]:
            p = pos.pop(k); cash += p["sh"] * p["t"]["exit"] * (1 - cost)
        val = cash + sum(p["sh"] * closes[p["t"]["sym"]].get(d, p["last"]) for p in pos.values())
        for t in by_day.get(d, []):
            if len(pos) >= max_pos or t["sym"] in pos:
                continue
            per = t["entry"] - t["stop"]
            sh = min(val * risk / per, val * max_w / t["entry"], cash / (t["entry"] * (1 + cost)))
            if sh * t["entry"] < 1000:
                continue
            cash -= sh * t["entry"] * (1 + cost); taken.append(t)
            if t["exit_date"] <= d:                                      # stopped out the same day
                cash += sh * t["exit"] * (1 - cost)
            else:
                pos[t["sym"]] = {"t": t, "sh": sh, "last": t["entry"]}
        for p in pos.values():
            p["last"] = closes[p["t"]["sym"]].get(d, p["last"])
        eq.append((d, cash + sum(p["sh"] * p["last"] for p in pos.values())))
    return pd.Series([v for _, v in eq], index=[d for d, _ in eq]), taken


def stats_equity(s):
    if len(s) < 2:
        return {}
    yrs = (pd.Timestamp(s.index[-1]) - pd.Timestamp(s.index[0])).days / 365.25
    cagr = (s.iloc[-1] / s.iloc[0]) ** (1 / yrs) - 1 if yrs > 0 else 0
    dd = (s / s.cummax() - 1).min()
    r = s.pct_change().dropna()
    sharpe = r.mean() / r.std() * math.sqrt(252) if r.std() > 0 else 0
    return {"total_%": round((s.iloc[-1] / s.iloc[0] - 1) * 100, 1), "cagr_%": round(cagr * 100, 1),
            "max_dd_%": round(dd * 100, 1), "sharpe": round(sharpe, 2)}


def spy_benchmarks(spy, start, end):
    d = spy[(spy.date >= start) & (spy.date <= end)].reset_index(drop=True)
    full = spy.copy(); full["s200"] = full.c.rolling(200).mean()
    bh = pd.Series(d.c.to_numpy() / d.c.iat[0] * 100_000, index=d.date)
    f = full[(full.date >= start) & (full.date <= end)].reset_index(drop=True)
    o, c, want = f.o.to_numpy(), f.c.to_numpy(), (f.c > f.s200).to_numpy()
    v, eq = 100_000.0, [100_000.0]
    for i in range(1, len(f)):
        was, now = want[i - 1] if i > 1 else False, want[i - 1]   # held today = decided at yesterday's close
        held_before = want[i - 2] if i > 1 else False
        if held_before and now:
            v *= c[i] / c[i - 1]
        elif held_before and not now:
            v *= o[i] / c[i - 1]
        elif not held_before and now:
            v *= c[i] / o[i]
        eq.append(v)
    return stats_equity(bh), stats_equity(pd.Series(eq, index=f.date))
