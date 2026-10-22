"""Planted test cases with answers worked out by hand. Run from scripts/backtest:
    python tests/test_backtest.py
Each case builds a tiny synthetic stock where the right answer is known in advance, then checks the
engine reproduces it exactly. These test the code against arithmetic — not against another copy of itself.
"""
import math, os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import engine as E, systems as S, audit as A

PASS = []


def check(name, cond, detail=""):
    if not cond:
        raise AssertionError(f"FAIL {name}: {detail}")
    PASS.append(name)


def dates(n, start="2020-01-01"):
    return [d.date().isoformat() for d in pd.bdate_range(start, periods=n)]


def bars(o, h, l, c, v=None):
    n = len(c)
    return pd.DataFrame({"date": dates(n), "o": o, "h": h, "l": l, "c": c, "v": v or [1e6] * n})


def flat_ind(n, atr=2.0):
    return {"sma50": np.full(n, 50.0), "sma200": np.full(n, 50.0), "atr": np.full(n, atr)}


def sig(n, buy_at=0, stop=90.0):
    r = ["DONT_BUY"] * n; r[buy_at] = "BUY"
    return pd.DataFrame({"rating": r, "stop": [stop] * n, "setup": ["BREAKOUT"] * n, "score": [50] * n, "market": ["UPTREND"] * n})


# ── 1. Live-rule trades (engine.simulate_trades, stop rule A2)
# Signal day 0 → buy day 1 at the OPEN (100). Stop 90 → R = 10. Levels: +1R = 110, +2R = 120.
o = [99, 100, 104, 108, 101]; h = [99, 105, 111, 109, 102]; l = [98, 99, 103, 104, 99.5]; c = [99, 104, 110, 105, 100]
t = E.simulate_trades("T1", bars(o, h, l, c), flat_ind(5), sig(5), dict(E.BASE), "2000-01-01", "2100-01-01")
# day 2 high 111 ≥ 110 → from day 3 the stop is breakeven (100); day 4 low 99.5 ≤ 100 → out at 100 → R = 0
check("A2 breakeven after +1R", len(t) == 1 and t[0]["entry"] == 100 and t[0]["exit"] == 100 and abs(t[0]["R"]) < 1e-12
      and t[0]["why"] == "stop", t)

o = [99, 100, 95, 85]; h = [99, 101, 96, 86]; l = [98, 96, 93, 84]; c = [99, 97, 94, 85]
t = E.simulate_trades("T2", bars(o, h, l, c), flat_ind(4), sig(4), dict(E.BASE), "2000-01-01", "2100-01-01")
# day 3 OPENS at 85, under the 90 stop → filled at the open (85), not at 90 → R = -1.5
check("gap through stop fills at the open", t[0]["exit"] == 85 and abs(t[0]["R"] + 1.5) < 1e-12 and t[0]["why"] == "stop (gap)", t)

o = [99, 100, 110, 124, 120]; h = [99, 108, 121, 125, 121]; l = [98, 99, 109, 120, 118]; c = [99, 107, 120, 123, 119]
t = E.simulate_trades("T3", bars(o, h, l, c), flat_ind(5, atr=2.0), sig(5), dict(E.BASE), "2000-01-01", "2100-01-01")
# high since entry reaches 125 (≥ +2R) → trail = max(100, 125 - 3×2) = 119 for day 4; day 4 low 118 → out at 119 → R = 1.9
check("A2 trail after +2R (high − 3×ATR)", t[0]["exit"] == 119 and abs(t[0]["R"] - 1.9) < 1e-12, t)

o = [99, 100, 95, 91]; h = [99, 101, 96, 92]; l = [98, 95, 91, 90.5]; c = [99, 96, 92, 91]
t = E.simulate_trades("T4", bars(o, h, l, c), flat_ind(4), sig(4), dict(E.BASE), "2000-01-01", "2100-01-01")
# day 2 closes at 92 ≤ 92.5 (−7.5%) while the stop (90) is not touched → sold at the next open (91)
check("7.5% loss rule sells next open", t[0]["exit"] == 91 and t[0]["why"] == "7.5% loss rule", t)

# ── 2. Partial exits (systems.simulate)
n = 8
o = [100, 100, 104, 109, 111, 108, 103, 102]; h = [100, 103, 108, 111, 112, 109, 104, 103]
l = [99, 98, 103, 108, 107, 103, 101, 100]; c = [100, 102, 107, 110, 108, 104, 102, 101]
f = {"dates": np.array(dates(n)), "o": np.array(o, float), "h": np.array(h, float), "l": np.array(l, float), "c": np.array(c, float),
     "atr": np.full(n, 2.0), "sma50": np.array([0, 0, 0, 0, 0, 105, 105, 105], float), "ema21": np.zeros(n), "ema10": np.zeros(n),
     "sector": ""}
X = dict(S.DEFAULT_EXIT, time_days=0)
t = S.simulate("P1", f, [(0, 95.0, 1.0)], X, "2000-01-01", "2100-01-01")
# entry day 1 open 100, stop 95 → R = 5; +2R = 110 hit on day 3 (high 111, open 109 < 110) → sell 1/3 at 110.
# day 5 closes 104 < 50-day (105) → rest (2/3) sold day 6 open 103.  R = (1/3·10 + 2/3·3) / 5 = 1.0667
exp = (10 / 3 + 2 * 3 / 3) / 5
check("partial 1/3 at +2R then runner exit", abs(t[0]["R"] - exp) < 1e-9 and len(t[0]["fills"]) == 2, (t[0]["R"], exp, t[0]["fills"]))

# ── 3. Portfolio cash and costs
tr = [{"sym": "X", "entry_date": "2020-01-02", "entry": 100.0, "stop": 90.0, "exit_date": "2020-01-06", "score": 1, "sector": "",
       "fills": [("2020-01-06", 1.0, 120.0, "exit")]}]
cal = dates(5)
eq, taken = S.portfolio(tr, {"X": {d: 110.0 for d in cal}}, cal, cal[0], cal[-1], max_pos=8, risk=0.01, cost=0.001)
# size = 1% of $100k / $10 risk = 100 shares; buy 100×100×1.001 = 10,010; sell 100×120×0.999 = 11,988 → 101,978
check("portfolio sizing + costs", abs(eq.iloc[-1] - 101_978.0) < 1e-6, eq.iloc[-1])

# ── 4. Momentum executes at the NEXT open, sold stocks keep the overnight move
n = 300
dts = dates(n)
def mk(gday, gap_day=None, gap=1.0):
    c = [10.0 * gday ** i for i in range(n)]
    o = [c[0]] + c[:-1]                                 # open = previous close (no gaps) ...
    if gap_day is not None:
        o[gap_day] = c[gap_day - 1] * gap; c = c[:gap_day] + [x * gap for x in c[gap_day:]]
    return pd.DataFrame({"date": dts, "o": o, "h": c, "l": c, "c": c, "v": [5e6] * n})
P = {"A": mk(1.002), "B": mk(1.001), "C": mk(0.999)}
cal = dts
start = cal[260]
eq, det = S.momentum_open(P, cal, start, cal[-1], top=1, cost=0.001, min_dollar_vol=0)
first_rebal = det["picks"][0][0]; k = cal.index(first_rebal)
# A is the strongest; bought at the open the day after the rebalance → from then on it compounds 0.2% a day,
# minus one buy cost (0.1% of 100% traded). Value at the end = 100,000 × 0.999 × 1.002^(days held)
held = len(cal) - 1 - k
check("momentum: next-open entry + cost", abs(eq.iloc[-1] - 100_000 * 0.999 * 1.002 ** held) < 1e-6, (eq.iloc[-1], held))
check("momentum: no return before the first trade", abs(eq.loc[first_rebal] - 100_000) < 1e-9)

# ── 5. Point-in-time EPS: a quarter is invisible until its filing date
facts = {"EarningsPerShareDiluted": [["2024-01-01", "2024-03-31", 1.0, "2024-05-01"], ["2025-01-01", "2025-03-31", 1.5, "2025-05-01"],
                                     ["2024-10-01", "2024-12-31", 0.9, "2025-02-10"], ["2023-10-01", "2023-12-31", 0.8, "2024-02-10"],
                                     ["2024-01-01", "2024-03-31", 0.5, "2025-06-01"]]}   # a later restatement of Q1-24
tl = E.fundamentals_timeline({"eps": facts}, "eps", E.EPS_TAGS)
pit = E.point_in_time("PIT", np.array(["2025-04-30", "2025-05-02", "2025-06-02"]), {"eps": tl, "rev": [], "earn": []})
# 4/30: newest filed quarter = Q4-24 (0.9 vs 0.8) → +12.5%. 5/02: Q1-25 now public (1.5 vs 1.0) → +50%.
# 6/02: the Q1-24 restatement (0.5) became public on 6/01 → (1.5−0.5)/0.5 = +200%. It must NOT leak into 5/02.
g = pit["g"]
check("point-in-time EPS", abs(g[0] - 12.5) < 1e-9 and abs(g[1] - 50) < 1e-9 and abs(g[2] - 200) < 1e-9, g)

# ── 6. Point-in-time RS: ineligible stocks get no rank
n = 300; dts2 = dates(n)
def series(p0, g, start_at=0, vol=5e6):
    c = [np.nan] * start_at + [p0 * g ** i for i in range(n - start_at)]
    return pd.DataFrame({"date": dts2, "o": c, "h": c, "l": c, "c": c, "v": [vol] * n}).dropna()
P = {"BIG": series(50, 1.002), "PENNY": series(2, 1.001), "IPO": series(50, 1.003, start_at=200), "OK": series(50, 1.001)}
el = E.eligibility(P, dts2)
rk = E.rs_rank(P, dts2, eligible=el)
d = dts2[-1]
check("RS: price under $5 not ranked", np.isnan(rk["PENNY"][d]))
check("RS: IPO with < 252 sessions not ranked", np.isnan(rk["IPO"][d]))
check("RS: eligible stocks ranked against each other only", rk["BIG"][d] > rk["OK"][d] and not np.isnan(rk["OK"][d]))

# ── 7. Extreme-move classifier
df = pd.DataFrame({"date": ["2021-01-04", "2021-01-05", "2021-01-06", "2021-01-07"], "c": [100.0, 100.0, 50.0, 51.0]})
cls, _ = A.classify(df, 2, [("2021-01-06", 2.0)], None)
check("classifier: unadjusted 2:1 split", cls == "data error: split not adjusted", cls)
df = pd.DataFrame({"date": ["2021-01-04", "2021-01-05", "2021-01-06", "2021-01-07"], "c": [100.0, 100.0, 300.0, 101.0]})
cls, _ = A.classify(df, 2, [], {"2021-01-05": 100.0, "2021-01-06": 100.5, "2021-01-07": 101.0})
check("classifier: one-day bad bar", cls == "data error: one-day bad bar", cls)
df = pd.DataFrame({"date": ["2021-01-04", "2021-01-05", "2021-01-06", "2021-01-07"], "c": [10.0, 10.0, 20.0, 21.0]})
cls, _ = A.classify(df, 2, [], {"2021-01-05": 10.0, "2021-01-06": 20.1, "2021-01-07": 21.0})
check("classifier: genuine (second source agrees)", cls == "genuine", cls)

# ── 8. Round 4 sell signals (engine.simulate_trades). Buy = day 1 open 100, stop 90 (R = 10).
def ind4(n, s50=50.0, avgv=1e6):
    return {"sma50": np.full(n, s50), "sma200": np.full(n, 50.0), "atr": np.full(n, 2.0), "avgv": np.full(n, avgv)}
P4 = dict(E.BASE, exit_failbo=True)
o = [99, 100, 99, 97, 96]; h = [99, 101, 100, 98, 97]; l = [98, 99, 97, 96, 95]; c = [99, 100, 97.5, 97, 96]
t = E.simulate_trades("R1", bars(o, h, l, c), ind4(5), sig(5), P4, "2000-01-01", "2100-01-01")
# day 2 closes 97.5 < 98 (2% under the buy) within 20 sessions → sold at day 3 open (97)
check("R4 failed breakout sells next open", t[0]["exit"] == 97 and t[0]["why"] == "failed breakout", t)

P4 = dict(E.BASE, exit_ma50vol=True)
o = [99, 100, 101, 99, 94, 93]; h = [99, 101, 102, 100, 95, 94]; l = [98, 99, 100, 94.5, 93.5, 92]; c = [99, 100, 101, 95, 94, 93]
v = [1e6, 1e6, 1e6, 3e6, 1e6, 1e6]
t = E.simulate_trades("R2", bars(o, h, l, c, v), ind4(6, s50=96.0), sig(6), P4, "2000-01-01", "2100-01-01")
# day 3 closes 95 < 50-day 96 (day 2 was above) on 3× volume → sold at day 4 open (94). The 7.5% rule (92.5) never fires.
check("R4 50-day break on volume", t[0]["exit"] == 94 and t[0]["why"] == "50-day break on volume", t)
v2 = [1e6] * 6
t = E.simulate_trades("R2b", bars(o, h, l, c, v2), ind4(6, s50=96.0), sig(6), P4, "2000-01-01", "2100-01-01")
check("R4 50-day break on LIGHT volume does not sell", t[0]["why"] != "50-day break on volume", t)

P4 = dict(E.BASE, exit_climax=True, stop="fixed")
c = [99, 100, 102, 104, 106, 108, 110, 114, 120, 126, 127, 128]
o = [99, 100] + c[1:-1]; h = [x + 0.5 for x in c]; l = [x - 0.5 for x in c]; l[1] = 99
t = E.simulate_trades("R3", bars(o, h, l, c), ind4(12), sig(12), P4, "2000-01-01", "2100-01-01")
# day 9 closes 126 (+26% from 100); 5-day gain 126/108 = +16.7% = fastest week so far → sold at day 10 open (126)
check("R4 climax run takes profit", t[0]["why"] == "climax run" and t[0]["exit"] == 126, t)

P4 = dict(E.BASE, hold8w=True, stop="ma50")
n = 50
c = [99, 100, 110, 121] + [118 - 0.5 * k for k in range(n - 4)]
o = [99, 100] + c[1:-1]; h = [x + 0.5 for x in c]; l = [x - 0.5 for x in c]; l[1] = 99
ind = ind4(n); ind["sma50"] = np.array([95.0] * 4 + [119.0] * (n - 4))   # 50-day jumps above price after the run-up
t = E.simulate_trades("R4", bars(o, h, l, c), ind, sig(n), P4, "2000-01-01", "2100-01-01")
# +20% reached on day 3 (high 121.5) → 8-week hold: the "below 50-day" sell is ignored until 40 sessions after the buy
check("R4 8-week hold ignores the 50-day sell", t[0]["days"] >= 40 or t[0]["why"].startswith("stop"), t)
t2 = E.simulate_trades("R4b", bars(o, h, l, c), ind, sig(n), dict(E.BASE, stop="ma50"), "2000-01-01", "2100-01-01")
check("R4 without the hold the 50-day sell fires early", t2[0]["why"] == "below 50-day" and t2[0]["days"] < 10, t2)

# ── 9. Regime sizing: half risk = half the shares; zero risk = no trade
tr = [{"sym": "X", "signal": "2020-01-01", "entry_date": "2020-01-02", "entry": 100.0, "stop": 90.0, "exit_date": "2020-01-06",
       "exit": 120.0, "score": 1}]
cal = dates(5)
eq, tk = E.portfolio(tr, {"X": {d: 110.0 for d in cal}}, cal, cal[0], cal[-1], risk=0.01, cost=0.0, risk_fn=lambda d: 0.5)
# 0.5% of $100k / $10 = 50 shares → +$20 × 50 = +$1,000
check("R4 regime half size", abs(eq.iloc[-1] - 101_000.0) < 1e-6 and len(tk) == 1, eq.iloc[-1])
eq, tk = E.portfolio(tr, {"X": {d: 110.0 for d in cal}}, cal, cal[0], cal[-1], risk=0.01, cost=0.0, risk_fn=lambda d: 0.0)
check("R4 regime defense = no new buys", abs(eq.iloc[-1] - 100_000.0) < 1e-6 and len(tk) == 0, eq.iloc[-1])

# ── 10. Round 5: idle cash sits in SPY
cal = dates(5)
spy_o = {d: 100.0 + 2 * k for k, d in enumerate(cal)}; spy_c = {d: 101.0 + 2 * k for k, d in enumerate(cal)}
st = {}
eq, tk = E.portfolio([], {}, cal, cal[0], cal[-1], idle=(spy_o, spy_c), stats=st)
# all cash in SPY from the first close (101) to the last close (109) → 100,000 × 109/101 (day 0 earns open→close too: ×101/100)
check("R5 idle cash earns SPY", abs(eq.iloc[-1] - 100_000 * 101 / 100 * 109 / 101) < 1e-6 and st["avg_in_stocks_%"] == 0, (eq.iloc[-1], st))
flat = {d: 100.0 for d in cal}
tr = [{"sym": "X", "signal": "2020-01-01", "entry_date": cal[1], "entry": 100.0, "stop": 90.0, "exit_date": cal[3], "exit": 120.0, "score": 1}]
eq, tk = E.portfolio(tr, {"X": {d: 110.0 for d in cal}}, cal, cal[0], cal[-1], cost=0.001, idle=(flat, flat), idle_cost=0.0003)
exp = 100_000 - 100 * 100 * 1.001 * 1.0003 + 100 * 120 * 0.999 * 0.9997
check("R5 idle switch costs charged both ways", abs(eq.iloc[-1] - exp) < 1e-6, (eq.iloc[-1], exp))

# ── 11. Round 6: buy back after a sale when the stock breaks above its high since the sale
n = 12
o = [99, 100, 101, 93, 92, 93, 95, 97, 99, 104, 106, 107]
h = [99, 102, 102, 94, 93, 95, 96, 98, 100, 105, 107, 108]
l = [98, 99, 92, 91, 91, 92, 94, 96, 98, 103, 105, 106]
c = [99, 101, 92.4, 92, 92.5, 94, 95.5, 97.5, 99.5, 104.5, 106.5, 107.5]
v = [1e6] * 9 + [2e6, 1e6, 1e6]
ind = ind4(n, s50=90.0)
P6 = dict(E.BASE, stop="fixed", reentry=True)
t = E.simulate_trades("R6", bars(o, h, l, c, v), ind, sig(n), P6, "2000-01-01", "2100-01-01")
# trade 1: buy day 1 open 100, stop 90; day 2 closes 92.4 (−7.6%) → 7.5% rule sells day 3 open (93).
# high since the sale (days 3–8) = 100; day 9 closes 104.5 > 100 on 2× volume, above the 50-day → re-buy day 10 open (106)
# stop = max(lowest low since the sale 91 × 0.995, 104.5 × 0.92) = 96.14
check("R6 re-entry after a recovery breakout", len(t) == 2 and t[1]["setup"] == "REENTRY" and t[1]["entry"] == 106
      and abs(t[1]["stop"] - 104.5 * 0.92) < 1e-9, t)
t = E.simulate_trades("R6b", bars(o, h, l, c, v), ind, sig(n), dict(P6, reentry=False), "2000-01-01", "2100-01-01")
check("R6 no re-entry when the option is off", len(t) == 1, t)

# ── 12. Round 6b: EARLY buy-back — the TSLA case: sold, kept sliding, then turned up well below the sale price
n = 20
o = [99, 100, 101, 93] + [92 - k for k in range(11)] + [83, 86, 89, 90, 91]
h = [99, 102, 102, 94] + [93 - k for k in range(11)] + [84, 87, 91, 91, 92]
l = [98, 99, 92, 91] + [90 - k for k in range(11)] + [80, 85, 88, 89, 90]
c = [99, 101, 92.4, 92] + [91 - k for k in range(11)] + [82, 86.5, 90.5, 90.5, 91.5]
v = [1e6] * 17 + [2e6, 1e6, 1e6]
ind = ind4(n, s50=85.0)
t = E.simulate_trades("R6c", bars(o, h, l, c, v), ind, sig(n), dict(E.BASE, stop="fixed", reentry="early"), "2000-01-01", "2100-01-01")
# sold day 3 open (93); slide to a low of 80 (day 15). Day 17 closes 90.5: above the 50-day (85), above the highest high of
# days 7-16 (90 on day 7), 2x volume → early buy-back at day 18 open (90), below the sale-day high (94)
check("R6b early buy-back below the sale price", len(t) == 2 and t[1]["setup"] == "REENTRY" and t[1]["entry"] == 90, t)
t = E.simulate_trades("R6d", bars(o, h, l, c, v), ind, sig(n), dict(E.BASE, stop="fixed", reentry=True), "2000-01-01", "2100-01-01")
check("R6b standard buy-back waits for the sale-day high", len(t) == 1, t)

print(f"all {len(PASS)} planted tests passed")
