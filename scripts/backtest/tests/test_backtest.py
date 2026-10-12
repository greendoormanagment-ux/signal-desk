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

print(f"all {len(PASS)} planted tests passed")
