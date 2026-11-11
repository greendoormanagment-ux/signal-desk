# Signal Desk — Rule Evidence Register

**Policy (Tony, 11/11/2026):** every instruction the app gives must have a pre-registered test behind it, or be shown as untested. New instructions are added here before they ship. Each test is locked on GitHub before it runs; results update this table.

**Review checklist:** every session and review (Nov 16, 23, 30 · Dec 1 · Jan 29) starts by opening this table. Any ⬜ row without a date gets one; nothing stays unscheduled. New fixes from reviews are added here the same day.

Status: ✅ supported by a test · ❌ test says it hurts (removed or to remove) · 🟡 tested, not proven · ⬜ untested · ℹ️ information only (no instruction)

## Buy side
| Rule (live v2.16.3) | Status | Evidence / next test |
| --- | --- | --- |
| Breakouts only (close above the 52-week pivot) | 🟡 | Round 8 s1: better in S&P, slightly worse outside; intervals overlap |
| Breakout volume ≥ 1.4× average | ⬜ | never varied (Fix #35) → **Nov 16** |
| Max 5% above the pivot | ⬜ | never varied → **Nov 16** |
| Market gate: no buys in CORRECTION | 🟡 | used in every backtest as the base; stricter gates not confirmed (Round 8 s1) |
| Real money only in UPTREND (PRESSURE = paper only) | 🟡 | `round8e-latest.md` (11/11): UPTREND-only had the higher return in all 4 comparisons (+0.7 to +4.1 pts/yr); drawdowns mixed → inconclusive by the pre-registered bar; rule stays |
| EPS growth ≥ 25% (hard block) | ⬜ | Round 8 ran without it → **Nov 16** |
| No buys within 14 days of earnings | ⬜ | never tested alone → **Nov 16** (SEC earnings dates downloaded) |
| 24-hour rule (rescan tomorrow, then buy) | ⬜ | backtests buy the next open → **Nov 16** |
| Sector / theme crowding ("consider skipping") | ⬜ | → **Nov 23** |
| 100-point score | ❌ | no predictive power (day-30 corr 0.06) → replaced by the ranking test |
| Footprints, trend filters (21-day, momentum, drift) | ℹ️ | Round 8 s2/2b: none adds value — information only |

## Sell side
| Rule | Status | Evidence / next test |
| --- | --- | --- |
| Stop rule A2 (trail) | ❌ vs original | Round 8 s1: the original stop beats A2 in every universe, period and regime → next version |
| Sell half on warning signs · warning stop-raise · sell half before earnings | ❌ | round8d: all lower R per trade → info only since v2.16.3 |
| SELL ALL when the stop is hit | ✅ | core of every backtest |
| 7.5% loss rule | ⬜ | inside every backtest, never tested alone → **Nov 23** |
| Stage 4 exit (price < 200-day and 50-day < 200-day) | ⬜ | inside every backtest, never tested alone → **Nov 23** |
| Take some profit at +20% (optional) | ⬜ | → **Nov 23** |
| Holdings tab: Stage 4 → cut half or more (core holdings) | ⬜ | → **Nov 23** |

## Portfolio
| Rule | Status | Evidence / next test |
| --- | --- | --- |
| 10 positions, 1% risk each, max 20% per position | ⬜ | portfolio capacity 10 / 15 / 20 → **Nov 30** |
| Which signals get the slots (current: score order) | ⬜ | ranking test, locked 11/11 → **Nov 23** |

## Whole-system challengers (same data, same bar)
| Challenger | Status | When |
| --- | --- | --- |
| SPY buy-and-hold (the bar to beat) | in every report | S&P version ≈ SPY; all-US trails it (Round 8 s1) |
| Pure momentum ranking (strongest stocks, rebalanced monthly) | ⬜ | → **Nov 30** |
| Core SPY + Signal Desk satellite | ⬜ | → **Nov 30** |
| Next-version package re-tested as one system | ⬜ | before it goes live; final check on held-back 2026 data |

## App fixes (not rules — next version)
| Fix | Found | Status |
| --- | --- | --- |
| Watchlist results board (all scanned stocks in one table, best on top) | 11/09 | next version |
| Tap to reopen any scan without rescanning | 11/09 | next version |
| Don't repeat SELL HALF after a partial sale is logged | 11/09 | moot since v2.16.3 (no SELL HALF instruction) |
| Refresh row numbers after I SOLD SOME splits a row | 11/09 | next version |
| Top verdict vs ACTION box wording conflict (HOLD vs action) | 11/07 | next version |
| "Check operating EPS" warning when official EPS fails | 11/07 | after the Nov 16 EPS test |
| Watchlist PAUSE / auto-pause | 11/10 | ✅ done (v2.16.1) |
| One-tap + WATCHLIST | 11/10 | ✅ done (v2.16.2) |
| WHAT TO DO NOW says "take partial profits" without "optional" (ACTION box says optional) — make them match | 11/11 | next version |
| App doesn’t know a position was already trimmed (SCALE_OUT keeps prompting) — fix: sheet script returns any closed row with the same ticker + account + entry date (date, shares, reason); app shows “already took profit on [date], the rest rides with the stop” | 11/11 | next version (display only) |
