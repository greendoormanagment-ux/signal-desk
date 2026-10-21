"""Candidate growth systems for Signal Desk (research only — the live app is untouched).

Four systems, each = an entry rule + a stop + an exit plan:
  1. LEADER BREAKOUT   – strong RS leader, growing EPS + sales, tight base, breakout on volume
  2. EARNINGS GAP      – big gap up on earnings day on heavy volume (post-earnings drift)
  3. LEADER PULLBACK   – top-RS stock pulls back to its 21-day EMA on light volume, then turns up
  4. MOMENTUM ROTATION – control: monthly top-10 by 12-month momentum (see momentum_rotation)

Exits are shared and configurable: initial stop, take a part at +kR, a time stop, and a
"runner" exit for the rest (close under the 50-day / 21-day EMA, or an ATR trail).
All data is point-in-time (prices to that close; SEC numbers as filed by that date).
"""
import bisect, random
import numpy as np, pandas as pd
import engine as E

DEFAULT_EXIT = dict(partial_R=2.0, partial_frac=1 / 3, be_after_partial=False, time_days=10, time_R=0.5,
                    runner="sma50", atr_mult=3.0, max_risk=0.10)


# ───────────── extra point-in-time fundamentals: EPS growth for the last TWO quarters (acceleration)
def _qmap(facts, asof):
    q, y, n9 = {}, {}, {}
    for s, e, v, f in facts:
        if f > asof:
            continue
        d = E._days(s, e)
        t = q if 80 <= d <= 100 else y if 350 <= d <= 380 else n9 if 260 <= d <= 285 else None
        if t is not None and (e not in t or f > t[e][3]):
            t[e] = (s, e, v, f)
    out = {e: r[2] for e, r in q.items()}
    for e, r in y.items():
        if e not in out:
            nine = next((g for g in n9.values() if g[0] == r[0]), None)
            if nine:
                out[e] = r[2] - nine[2]
    return out


def _growth(qm, end):
    pe = next((e for e in sorted(qm) if abs(E._days(e, end) - 365) <= 20), None)
    if pe is None or qm[pe] <= 0:
        return None
    return (qm[end] - qm[pe]) / qm[pe] * 100


def eps_accel_timeline(rec):
    facts = (rec.get("eps") or {})
    tag = next((t for t in E.EPS_TAGS if t in facts), None)
    if not tag:
        return []
    tl = []
    for F in sorted({f[3] for f in facts[tag]}):
        qm = _qmap(facts[tag], F)
        if len(qm) < 2:
            continue
        ends = sorted(qm)
        g1, g0 = _growth(qm, ends[-1]), _growth(qm, ends[-2])
        if g1 is not None and g0 is not None:
            tl.append((F, ends[-1], g1, g0))
    return tl


# ───────────── per-stock feature table (computed once, shared by all systems)
def features(sym, df, ind, sec, rec, mkt, meta):
    n = len(df); dates = df.date.to_numpy()
    o, h, l, c, v = (df[k].to_numpy(float) for k in ("o", "h", "l", "c", "v"))
    f = {"dates": dates, "o": o, "h": h, "l": l, "c": c, "v": v}
    f.update({k: ind[k] for k in ("sma50", "sma150", "sma200", "sma200_20", "sma50_10", "atr", "avgv", "rsrank",
                                  "hi52", "lo52", "volratio")})
    f["ema21"] = pd.Series(c).ewm(span=21, adjust=False).mean().to_numpy()
    f["ema10"] = pd.Series(c).ewm(span=10, adjust=False).mean().to_numpy()
    f["sma5"] = pd.Series(c).rolling(5).mean().to_numpy()
    d1 = np.diff(c, prepend=c[0])
    up2 = pd.Series(np.maximum(d1, 0)).ewm(alpha=1 / 2, adjust=False).mean()
    dn2 = pd.Series(np.maximum(-d1, 0)).ewm(alpha=1 / 2, adjust=False).mean()
    f["rsi2"] = (100 - 100 / (1 + up2 / dn2.replace(0, np.nan))).fillna(100).to_numpy()   # 2-day RSI (Wilder)
    dn = (d1 < 0).astype(int)
    f["down_days"] = pd.Series(dn).groupby((dn == 0).cumsum()).cumsum().to_numpy()      # consecutive down closes
    f["dollar_vol"] = ind["avgv"] * c / 1e6                                # $M per day, point in time
    f["hh50"] = pd.Series(h).rolling(50).max().shift(1).to_numpy()        # highest high of the prior 50 days
    rng10 = (pd.Series(h).rolling(10).max() - pd.Series(l).rolling(10).min()) / pd.Series(c)
    f["range10"] = rng10.shift(1).to_numpy() * 100                        # tightness of the 10 days before today
    pit = E.point_in_time(sym, dates, sec)
    f["eps_g"], f["rev_g"] = pit["g"], pit["rev"]
    acc = np.full(n, np.nan); acc_prev = np.full(n, np.nan)
    tl = eps_accel_timeline(rec) if rec else []
    if tl:
        fd = [r[0] for r in tl]
        for i, d in enumerate(dates):
            j = bisect.bisect_right(fd, d) - 1
            if j >= 0 and E._days(tl[j][1], d) <= 135:
                acc[i], acc_prev[i] = tl[j][2], tl[j][3]
    f["g_last"], f["g_prev"] = acc, acc_prev
    # earnings-release days (8-K Item 2.02): mark the day itself and the next session (after-close reports gap next day)
    er = np.zeros(n, bool)
    for d in (sec or {}).get("earn", []):
        j = bisect.bisect_left(list(dates), d)
        if j < n:
            er[j] = True
            if j + 1 < n:
                er[j + 1] = True
    f["earn_window"] = er
    mk = mkt["live"]
    f["mkt"] = np.array([mk.get(d, "UNKNOWN") for d in dates])
    f["spy_above200"] = np.array([mkt["spy200"].get(d) == "UPTREND" for d in dates])
    f["sector"] = (meta or {}).get("sector", "")
    return f


# ───────────── entry rules → list of (i, stop, score)
def leader_breakout(f, P):
    c, h, l, atr = f["c"], f["h"], f["l"], f["atr"]
    trend = (c > f["sma50"]) & (f["sma50"] > f["sma150"]) & (f["sma150"] > f["sma200"]) & (f["sma200"] > f["sma200_20"])
    rs = np.nan_to_num(f["rsrank"]) >= P.get("min_rs", 85)
    fund = (np.nan_to_num(f["eps_g"], nan=-1) >= P.get("eps_min", 25)) & (np.nan_to_num(f["rev_g"], nan=-1) >= P.get("rev_min", 20))
    if P.get("need_accel"):
        fund &= np.nan_to_num(f["g_last"], nan=-1) > np.nan_to_num(f["g_prev"], nan=1e9)
    tight = np.nan_to_num(f["range10"], nan=99) <= P.get("max_range10", 12)
    piv = f["hh50"]
    brk = (c > piv) & (c <= piv * 1.05) & (np.nan_to_num(f["volratio"]) >= P.get("vol_need", 1.5))
    liq = np.nan_to_num(f["dollar_vol"]) >= P.get("min_dollar_vol", 20)
    mkt = f["mkt"] != "CORRECTION" if P.get("mkt_gate", True) else np.ones(len(c), bool)
    sig = trend & rs & fund & tight & brk & liq & mkt
    stop = np.maximum(piv - atr, c * 0.93)
    return [(i, stop[i], f["rsrank"][i]) for i in np.flatnonzero(sig)]


def earnings_gap(f, P):
    o, c, h, l = f["o"], f["c"], f["h"], f["l"]
    pc = np.r_[np.nan, c[:-1]]
    gap = (o / pc - 1) * 100 >= P.get("min_gap", 4)
    up = (c / pc - 1) * 100 >= P.get("min_up", 5)
    vol = np.nan_to_num(f["volratio"]) >= P.get("vol_need", 3)
    upper = (c - l) >= 0.5 * (h - l)
    trend = c > f["sma200"] if P.get("need_trend", True) else np.ones(len(c), bool)
    rs = np.nan_to_num(f["rsrank"]) >= P.get("min_rs", 0)
    liq = np.nan_to_num(f["dollar_vol"]) >= P.get("min_dollar_vol", 20)
    mkt = f["mkt"] != "CORRECTION" if P.get("mkt_gate", True) else np.ones(len(c), bool)
    sig = f["earn_window"] & gap & up & vol & upper & trend & rs & liq & mkt
    stop = l                                                              # under the gap day's low
    score = (c / pc - 1) * 100 + np.nan_to_num(f["rsrank"]) / 10
    return [(i, stop[i], score[i]) for i in np.flatnonzero(sig)]


def leader_pullback(f, P):
    c, h, l = f["c"], f["h"], f["l"]
    ema = f["ema21"]
    trend = (c > f["sma200"]) & (f["sma50"] > f["sma200"]) & (f["sma50"] > f["sma50_10"])
    rs = np.nan_to_num(f["rsrank"]) >= P.get("min_rs", 90)
    fund = np.nan_to_num(f["eps_g"], nan=-1) >= P.get("eps_min", 25) if P.get("need_eps", True) else np.ones(len(c), bool)
    lo3 = pd.Series(l).rolling(3).min().shift(1).to_numpy()
    touched = lo3 <= np.r_[np.nan, ema[:-1]] * 1.01                       # one of the last 3 lows tagged the 21-day EMA
    quiet = pd.Series(f["volratio"]).rolling(3).mean().shift(1).to_numpy() < P.get("quiet_vol", 1.0)
    turn = (c > np.r_[np.nan, h[:-1]]) & (c > ema)                         # closes above yesterday's high
    liq = np.nan_to_num(f["dollar_vol"]) >= P.get("min_dollar_vol", 20)
    mkt = f["mkt"] != "CORRECTION" if P.get("mkt_gate", True) else np.ones(len(c), bool)
    sig = trend & rs & fund & touched & np.nan_to_num(quiet).astype(bool) & turn & liq & mkt
    stop = pd.Series(l).rolling(5).min().to_numpy() * 0.995                # under the pullback low
    return [(i, stop[i], f["rsrank"][i]) for i in np.flatnonzero(sig)]


def mean_reversion(f, P):
    """Short-term pullback in an uptrend (Connors-style): buy a sharp 2-3 day dip in a stock above its
    200-day, sell on the bounce. High win rate, small gains. Disaster stop only (default 10% under entry)."""
    c = f["c"]
    trend = c > f["sma200"]
    dip = f["rsi2"] < P.get("rsi_max", 10)
    if P.get("min_down_days"):
        dip &= f["down_days"] >= P["min_down_days"]
    liq = np.nan_to_num(f["dollar_vol"]) >= P.get("min_dollar_vol", 20)
    mkt = (f["spy_above200"] if P.get("spy_filter") else np.ones(len(c), bool))
    sig = trend & dip & liq & mkt
    stop = c * (1 - P.get("disaster_stop", 0.10))
    score = -f["rsi2"] if P.get("rank", "rsi") == "rsi" else np.nan_to_num(f["rsrank"])   # most oversold, or strongest RS, first
    return [(i, stop[i], score[i]) for i in np.flatnonzero(sig)]


def combined(f, P):
    """All three entry rules feeding one portfolio (raises time invested). Ranked by RS rank."""
    seen = {}
    for fn, kw in ((leader_breakout, {}), (earnings_gap, {}), (leader_pullback, dict(need_eps=False))):
        for i, stop, _ in fn(f, kw):
            seen.setdefault(i, (i, stop, f["rsrank"][i]))
    return [seen[i] for i in sorted(seen)]


SYSTEMS = {"leader_breakout": leader_breakout, "earnings_gap": earnings_gap, "leader_pullback": leader_pullback,
           "combined": combined, "mean_reversion": mean_reversion}


# ───────────── trade simulation with partial exits
def simulate(sym, f, entries, X, start, end):
    o, h, l, c, atr = f["o"], f["h"], f["l"], f["c"], f["atr"]
    dates = f["dates"]; n = len(c)
    runner = {"sma50": f["sma50"], "ema21": f["ema21"], "ema10": f["ema10"]}.get(X["runner"])
    trades, busy_until = [], -1
    dl = list(dates)
    for i, stop, score in entries:
        if i <= busy_until or i + 1 >= n or not (start <= dates[i] <= end):
            continue
        mode = X.get("entry", "open")
        if mode == "close":                                                # market-on-close order on the signal day
            e = i; ep = c[i]; j0 = i + 1
        elif mode == "limit":                                              # limit order k% under the signal close, next day only
            e = i + 1; lim = c[i] * (1 - X.get("limit_pct", 0.02))
            if l[e] > lim:
                continue
            ep = min(o[e], lim); j0 = e
        else:
            e = i + 1; ep = o[e]; j0 = e
        if not (ep > stop > 0) or (ep - stop) / ep > X["max_risk"]:
            continue
        R = ep - stop; stp = stop; rem = 1.0; fills = []; hi = h[e] if j0 == e else ep; mfe = 0.0; took = False
        j = j0; exit_next = None
        while j < n:
            if exit_next is not None:
                fills.append((dates[j], rem, o[j], exit_next)); rem = 0; break
            if j > e and o[j] <= stp:
                fills.append((dates[j], rem, o[j], "stop (gap)")); rem = 0; break
            if l[j] <= stp:
                fills.append((dates[j], rem, stp, "stop" if not took else "stop after partial")); rem = 0; break
            if not took and X["partial_R"] and h[j] >= ep + X["partial_R"] * R:
                px = max(o[j], ep + X["partial_R"] * R) if j > e else ep + X["partial_R"] * R
                fills.append((dates[j], X["partial_frac"], px, f"+{X['partial_R']:g}R partial")); rem -= X["partial_frac"]; took = True
                if X["be_after_partial"]:
                    stp = max(stp, ep)
            hi = max(hi, h[j]); mfe = max(mfe, (hi - ep) / R)
            # end-of-day decisions (executed next open)
            if X.get("bounce") == "sma5" and c[j] > f["sma5"][j]:
                exit_next = "bounce: close > 5-day avg"
            elif X.get("bounce") == "rsi70" and f["rsi2"][j] > 70:
                exit_next = "bounce: RSI(2) > 70"
            elif X.get("bounce") == "first_up" and j > e and c[j] > c[j - 1]:
                exit_next = "bounce: first up close"
            elif X.get("max_days") and j - e + 1 >= X["max_days"]:
                exit_next = "max hold"
            elif X["time_days"] and j - e == X["time_days"] and hi < ep + X["time_R"] * R:
                exit_next = "time stop"
            elif X["runner"] in ("sma50", "ema21", "ema10") and c[j] < runner[j] and (took or X.get("runner_before_partial", True)):
                exit_next = f"close < {X['runner']}"
            elif X["runner"] == "atr":
                stp = max(stp, hi - X["atr_mult"] * atr[j])
            j += 1
        if rem > 0:
            fills.append((dates[n - 1], rem, c[n - 1], "open at end"))
        Rm = sum(fr * (px - ep) for _, fr, px, _ in fills) / R
        ret = sum(fr * (px / ep - 1) for _, fr, px, _ in fills) * 100
        last = fills[-1]
        busy_until = bisect.bisect_left(dl, last[0])
        trades.append({"sym": sym, "signal": dates[i], "entry_date": dates[e], "entry": ep, "stop": stop,
                       "exit_date": last[0], "fills": fills, "why": last[3], "R": Rm, "ret": ret,
                       "mfe_R": mfe, "score": float(np.nan_to_num(score)), "sector": f["sector"],
                       "days": busy_until - e})
    return trades


# ───────────── portfolio: ranked, max N positions, sector cap, partial fills
def portfolio(trades, closes, cal, start, end, max_pos=8, sector_cap=2, risk=0.01, max_w=0.25, cost=0.001, seed=None,
              idle=None, idle_cost=0.0003, stats=None):
    """idle=(spy_open, spy_close): money not in a stock sits in SPY (Round 5); see engine.portfolio."""
    rnd = random.Random(seed)
    by_day = {}
    for t in trades:
        if start <= t["entry_date"] <= end:
            by_day.setdefault(t["entry_date"], []).append(t)
    for d in by_day:
        if seed is None:
            by_day[d].sort(key=lambda t: -t["score"])
        else:
            rnd.shuffle(by_day[d])
    cash, pos, eq, taken = 100_000.0, {}, [], []
    io, ic = idle if idle else ({}, {})
    xc = idle_cost if idle else 0.0
    prev, inv = None, []

    def settle(p, d):
        nonlocal cash
        while p["next"] < len(p["t"]["fills"]) and p["t"]["fills"][p["next"]][0] <= d:
            _, fr, px, _ = p["t"]["fills"][p["next"]]
            cash += p["sh0"] * fr * px * (1 - cost) * (1 - xc); p["sh"] -= p["sh0"] * fr; p["next"] += 1

    for d in (x for x in cal if start <= x <= end):
        if idle and prev and cash > 0 and ic.get(prev) and io.get(d):
            cash *= io[d] / ic[prev]
        for k in list(pos):
            settle(pos[k], d)
            if pos[k]["next"] >= len(pos[k]["t"]["fills"]):
                del pos[k]
        val = cash + sum(p["sh"] * closes[s].get(d, p["last"]) for s, p in pos.items())
        for t in by_day.get(d, []):
            if len(pos) >= max_pos or t["sym"] in pos:
                continue
            if sector_cap and t["sector"] and sum(1 for p in pos.values() if p["t"]["sector"] == t["sector"]) >= sector_cap:
                continue
            sh = min(val * risk / (t["entry"] - t["stop"]), val * max_w / t["entry"], cash / (t["entry"] * (1 + cost)))
            if sh * t["entry"] < 1000:
                continue
            cash -= sh * t["entry"] * (1 + cost) * (1 + xc); taken.append(t)
            pos[t["sym"]] = {"t": t, "sh": sh, "sh0": sh, "next": 0, "last": t["entry"]}
            settle(pos[t["sym"]], d)
            if pos[t["sym"]]["next"] >= len(t["fills"]):
                del pos[t["sym"]]
        if idle and cash > 0 and io.get(d) and ic.get(d):
            cash *= ic[d] / io[d]
        for s, p in pos.items():
            p["last"] = closes[s].get(d, p["last"])
        held = sum(p["sh"] * p["last"] for p in pos.values()); tot = cash + held
        inv.append(held / tot if tot > 0 else 0); prev = d
        eq.append((d, tot))
    if stats is not None:
        stats["avg_in_stocks_%"] = round(100 * float(np.mean(inv)), 1) if inv else 0
    return pd.Series([x for _, x in eq], index=[d for d, _ in eq]), taken


# ───────────── system 4: momentum rotation (control)
def momentum_rotation(prices, cal, start, end, top=10, spy=None, regime=False, min_dollar_vol=20, cost=0.001, member=None,
                      lookback=252, skip=21, offset=0, weighting="equal", regime_daily=False, trend_filter=True, sector=None,
                      sector_cap=None, return_holdings=False):
    """Monthly rotation into the strongest stocks.
    lookback/skip: momentum = return from `lookback` to `skip` trading days ago (12-1 month by default)
    offset: rebalance on the Nth trading day of each month (tests whether the day matters)
    weighting: "equal" or "invvol" (less money in jumpier stocks)
    regime: hold cash when SPY < its 200-day at the rebalance; regime_daily: check every day, re-enter next day"""
    cl = pd.DataFrame({s: df.set_index("date").c for s, df in prices.items()}).reindex(cal)
    vol = pd.DataFrame({s: df.set_index("date").v for s, df in prices.items()}).reindex(cal)
    dv = (vol.rolling(50).mean().shift(1) * cl) / 1e6
    mom = cl.shift(skip) / cl.shift(lookback) - 1
    above = cl > cl.rolling(200).mean() if trend_filter else cl.notna()
    rv = cl.pct_change(fill_method=None).rolling(63).std()
    sp = spy.set_index("date").c if spy is not None else None
    spy200 = (sp > sp.rolling(200).mean()).reindex(cal) if sp is not None else None
    days = [d for d in cal if start <= d <= end]
    months = {}
    for d in days:
        months.setdefault(d[:7], []).append(d)
    rebal = {v[min(offset, len(v) - 1)] for v in months.values()}
    val, hold, eq, held_rets, log = 100_000.0, {}, [], [], []
    w = {}; prev = None; out = False
    for d in days:
        if regime_daily and spy200 is not None and prev is not None:
            want_out = not bool(spy200.get(prev, True))                      # decided at yesterday's close, acted on today
            if want_out != out:
                val *= 1 - cost; out = want_out
        if prev is not None and hold and not out:
            r = sum(w[s] * ((cl.at[d, s] / cl.at[prev, s] - 1) if not (np.isnan(cl.at[d, s]) or np.isnan(cl.at[prev, s])) else 0) for s in hold)
            val *= 1 + r
            for s in hold:                                                    # drift the weights with prices
                if not (np.isnan(cl.at[d, s]) or np.isnan(cl.at[prev, s])):
                    w[s] *= cl.at[d, s] / cl.at[prev, s]
            tot = sum(w.values()) or 1
            w = {s: x / tot for s, x in w.items()}
        if d in rebal:
            if hold:
                held_rets += [(cl.at[d, s] / hold[s] - 1) * 100 for s in hold if not np.isnan(cl.at[d, s])]
            ok = above.loc[d] & (dv.loc[d] >= min_dollar_vol) & mom.loc[d].notna()
            if member is not None:
                ok &= pd.Series({s: member(s, d) for s in ok.index})
            ranked = list(mom.loc[d][ok].sort_values(ascending=False).index)
            pick = []
            for s in ranked:
                if sector_cap and sector and sum(1 for x in pick if sector.get(x) == sector.get(s) and sector.get(s)) >= sector_cap:
                    continue
                pick.append(s)
                if len(pick) >= top:
                    break
            if regime and spy200 is not None and not spy200.get(d, True):
                pick = []
            turnover = len(set(pick) ^ set(hold)) / max(1, 2 * top)
            val *= 1 - cost * 2 * turnover
            hold = {s: cl.at[d, s] for s in pick}
            if weighting == "invvol" and pick:
                iv = {s: 1 / rv.at[d, s] if rv.at[d, s] and not np.isnan(rv.at[d, s]) else 0 for s in pick}
                tot = sum(iv.values()) or 1
                w = {s: iv[s] / tot for s in pick}
            else:
                w = {s: 1 / len(pick) for s in pick}
            log.append((d, pick))
        eq.append((d, val)); prev = d
    s = pd.Series([v for _, v in eq], index=[d for d, _ in eq])
    r = np.array(held_rets)
    st = {"holdings": len(r), "win_%": round((r > 0).mean() * 100, 1) if len(r) else 0,
          "avg_hold_ret_%": round(r.mean(), 2) if len(r) else 0}
    return (s, st, log) if return_holdings else (s, st)


# ───────────── Round 3: momentum with realistic execution
def momentum_open(prices, cal, start, end, top=10, lookback=252, skip=21, offset=0, cost=0.0007, member=None,
                  min_dollar_vol=20, trend_filter=True, group=None, group_cap=None):
    """Monthly momentum rotation, executed realistically:
      * the ranking uses data up to the CLOSE of the rebalance day; trades happen at the NEXT day's OPEN
      * stocks sold carry their overnight move (close -> open); stocks bought start at the open (gaps included)
      * cost is charged on the fraction of the portfolio actually traded (per side: commission + slippage + half-spread)
      * group_cap: at most N holdings per group (industry/theme, current classification)
    Returns (daily equity, details) — details holds turnover and the monthly picks."""
    cl = pd.DataFrame({s: df.set_index("date").c for s, df in prices.items()}).reindex(cal)
    op = pd.DataFrame({s: df.set_index("date").o for s, df in prices.items()}).reindex(cal)
    vol = pd.DataFrame({s: df.set_index("date").v for s, df in prices.items()}).reindex(cal)
    dv = (vol.rolling(50, min_periods=50).mean().shift(1) * cl) / 1e6
    mom = cl.shift(skip) / cl.shift(lookback) - 1
    above = cl > cl.rolling(200, min_periods=200).mean() if trend_filter else cl.notna()
    days = [d for d in cal if start <= d <= end]
    months = {}
    for d in days:
        months.setdefault(d[:7], []).append(d)
    rebal = {v[min(offset, len(v) - 1)] for v in months.values()}
    C, O = cl.to_dict("index"), op.to_dict("index")
    val, w, pending, eq, picks, traded_total = 100_000.0, {}, None, [], [], 0.0
    prev = None
    for d in days:
        cd, od = C[d], O[d]
        if prev is not None and w:
            cp = C[prev]
            if pending is not None:
                # overnight: held stocks move from yesterday's close to today's open
                g = {s: (od[s] / cp[s] if (od.get(s) == od.get(s) and cp.get(s) == cp.get(s) and cp[s]) else 1.0) for s in w}
                r1 = sum(w[s] * (g[s] - 1) for s in w); val *= 1 + r1
                w = {s: w[s] * g[s] / (1 + r1) for s in w}
        elif prev is not None:
            cp = C[prev]
        if pending is not None and prev is not None:
            traded = sum(abs(pending.get(s, 0) - w.get(s, 0)) for s in set(pending) | set(w))
            val *= 1 - cost * traded; traded_total += traded / 2
            w = dict(pending); pending = None
            g = {s: (cd[s] / od[s] if (cd.get(s) == cd.get(s) and od.get(s) == od.get(s) and od[s]) else 1.0) for s in w}
            r2 = sum(w[s] * (g[s] - 1) for s in w); val *= 1 + r2
            w = {s: w[s] * g[s] / (1 + r2) for s in w} if (1 + r2) else w
        elif prev is not None and w:
            g = {s: (cd[s] / cp[s] if (cd.get(s) == cd.get(s) and cp.get(s) == cp.get(s) and cp[s]) else 1.0) for s in w}
            r = sum(w[s] * (g[s] - 1) for s in w); val *= 1 + r
            w = {s: w[s] * g[s] / (1 + r) for s in w}
        if d in rebal:
            ok = above.loc[d] & (dv.loc[d] >= min_dollar_vol) & mom.loc[d].notna()
            if member is not None:
                ok &= pd.Series({s: member(s, d) for s in ok.index})
            pick = []
            for s in mom.loc[d][ok].sort_values(ascending=False).index:
                if group_cap and group and group.get(s) and sum(1 for x in pick if group.get(x) == group.get(s)) >= group_cap:
                    continue
                pick.append(s)
                if len(pick) >= top:
                    break
            pending = {s: 1 / len(pick) for s in pick} if pick else {}
            picks.append((d, pick))
        eq.append((d, val)); prev = d
    s = pd.Series([v for _, v in eq], index=[d for d, _ in eq])
    yrs = max((pd.Timestamp(days[-1]) - pd.Timestamp(days[0])).days / 365.25, 1e-9)
    return s, {"turnover_per_year": round(traded_total / yrs, 2), "picks": picks}


def perf_metrics(eq, bench=None):
    """CAGR, max drawdown, annualized volatility, Sharpe (no risk-free), and excess CAGR vs a benchmark."""
    if len(eq) < 20:
        return {}
    yrs = (pd.Timestamp(eq.index[-1]) - pd.Timestamp(eq.index[0])).days / 365.25
    r = eq.pct_change().dropna()
    out = {"cagr_%": round(((eq.iloc[-1] / eq.iloc[0]) ** (1 / yrs) - 1) * 100, 1),
           "max_dd_%": round(float((eq / eq.cummax() - 1).min()) * 100, 1),
           "vol_%": round(float(r.std() * np.sqrt(252)) * 100, 1),
           "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 2) if r.std() > 0 else 0}
    if bench is not None:
        b = bench[(bench.index >= eq.index[0]) & (bench.index <= eq.index[-1])]
        bc = ((b.iloc[-1] / b.iloc[0]) ** (1 / yrs) - 1) * 100
        out["bench_cagr_%"] = round(bc, 1); out["excess_cagr_%"] = round(out["cagr_%"] - bc, 1)
    return out


def block_bootstrap_excess(eq, bench, start, end, block=6, n=5000, seed=1):
    """Resample MONTHLY excess log returns (strategy minus benchmark) in blocks of `block` months
    (keeps short-run streaks together). Returns the 5th/50th/95th percentile of the annualized excess
    return and the share of resamples above zero. Describes uncertainty in the PAST average only —
    it is not a probability of beating SPY in the future."""
    m = eq[(eq.index >= start) & (eq.index <= end)].groupby(lambda x: x[:7]).last()
    bm = bench[(bench.index >= start) & (bench.index <= end)].groupby(lambda x: x[:7]).last()
    m, bm = m.align(bm, join="inner")
    ex = (np.log(m / m.shift(1)) - np.log(bm / bm.shift(1))).dropna().to_numpy()
    if len(ex) < block * 2:
        return {}
    rng = np.random.default_rng(seed); k = len(ex); res = []
    for _ in range(n):
        idx = []
        while len(idx) < k:
            st = rng.integers(0, k - block + 1); idx.extend(range(st, st + block))
        res.append(ex[idx[:k]].mean() * 12)
    res = np.array(res)
    return {"months": k, "block_months": block, "resamples": n,
            "excess_p5_%": round(float(np.percentile(res, 5)) * 100, 1), "excess_median_%": round(float(np.median(res)) * 100, 1),
            "excess_p95_%": round(float(np.percentile(res, 95)) * 100, 1), "share_above_zero_%": round(float((res > 0).mean()) * 100, 0)}
