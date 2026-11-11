# Signal Desk — Rule Evidence Register

**Policy (Tony, 11/11/2026):** every instruction the app gives must have a pre-registered test behind it, or be shown as untested. New instructions are added here before they ship. Each test is locked on GitHub before it runs; results update this table.

Status: ✅ supported by a test · ❌ test says it hurts (removed or to remove) · 🟡 tested, not proven · ⬜ untested · ℹ️ information only (no instruction)

## Buy side
| Rule (live v2.16.3) | Status | Evidence / next test |
| --- | --- | --- |
| Breakouts only (close above the 52-week pivot) | 🟡 | Round 8 s1: better in S&P, slightly worse outside; intervals overlap |
| Breakout volume ≥ 1.4× average | ⬜ | never varied (Fix #35) — buy-filter track |
| Max 5% above the pivot | ⬜ | never varied — buy-filter track |
| Market gate: no buys in CORRECTION | 🟡 | used in every backtest as the base; stricter gates not confirmed (Round 8 s1) |
| Real money only in UPTREND (PRESSURE = paper only) | 🟡 | `round8e-latest.md` (11/11): UPTREND-only had the higher return in all 4 comparisons (+0.7 to +4.1 pts/yr); drawdowns mixed → inconclusive by the pre-registered bar; rule stays |
| EPS growth ≥ 25% (hard block) | ⬜ | Round 8 ran without it → Round 8 session 3 |
| No buys within 14 days of earnings | ⬜ | never tested alone → session 3 (SEC earnings dates now available) |
| 24-hour rule (rescan tomorrow, then buy) | ⬜ | backtests buy the next open → to test |
| Sector / theme crowding ("consider skipping") | ⬜ | to test |
| 100-point score | ❌ | no predictive power (day-30 corr 0.06) → replaced by the ranking test |
| Footprints, trend filters (21-day, momentum, drift) | ℹ️ | Round 8 s2/2b: none adds value — information only |

## Sell side
| Rule | Status | Evidence / next test |
| --- | --- | --- |
| Stop rule A2 (trail) | ❌ vs original | Round 8 s1: the original stop beats A2 in every universe, period and regime → next version |
| Sell half on warning signs · warning stop-raise · sell half before earnings | ❌ | round8d: all lower R per trade → info only since v2.16.3 |
| SELL ALL when the stop is hit | ✅ | core of every backtest |
| 7.5% loss rule | ⬜ | inside every backtest, never tested alone → exit track |
| Stage 4 exit (price < 200-day and 50-day < 200-day) | ⬜ | inside every backtest, never tested alone → exit track |
| Take some profit at +20% (optional) | ⬜ | exit track |
| Holdings tab: Stage 4 → cut half or more (core holdings) | ⬜ | exit track |

## Portfolio
| Rule | Status | Evidence / next test |
| --- | --- | --- |
| 10 positions, 1% risk each, max 20% per position | ⬜ | portfolio-capacity track (10 / 15 / 20) |
| Which signals get the slots (current: score order) | ⬜ | ranking test, locked 11/11, runs after session 3 |
