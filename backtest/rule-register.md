# Signal Desk — Rule Evidence Register

**Policy (Tony, 11/11/2026):** every instruction the app gives must have a pre-registered test behind it, or be shown as untested. New instructions are added here before they ship. Each test is locked on GitHub before it runs; results update this table.

**Review checklist:** every session and review (Nov 16, 23, 30 · Dec 1 · Jan 29) starts by opening this table. Any ⬜ row without a date gets one; nothing stays unscheduled. New fixes from reviews are added here the same day.

Status: ✅ supported by a test · ❌ test says it hurts (removed or to remove) · 🟡 tested, not proven · ⬜ untested · ℹ️ information only (no instruction)

## Buy side
| Rule (live v2.16.3) | Status | Evidence / next test |
| --- | --- | --- |
| Breakouts only (close above the 52-week pivot) | 🟡 | Round 8 s1: better in S&P, slightly worse outside; intervals overlap |
| Breakout volume ≥ 1.4× average | ✅ | `round8f-latest.md` (11/16): 1.2 / 1.4 / 1.6 / 2.0× tested — no challenger beats 1.4× in both periods; stays |
| Max 5% above the pivot | ✅ | `round8f-latest.md` (11/16): 3 / 5 / 8% tested — no challenger beats 5% in both periods; stays |
| Market gate: no buys in CORRECTION | 🟡 | used in every backtest as the base; stricter gates not confirmed (Round 8 s1) |
| Market gate DEFINITION (SPY + QQQ vs their 50-day lines, 5+ distribution days in 25 sessions, 5% expiry, both indexes must agree) | ⬜ | inherited from O’Neil, never varied → **Nov 30**: compare with slower/faster versions (e.g. 200-day based, 3 vs 5 distribution days, SPY only) |
| Real money only in UPTREND (PRESSURE = paper only) | 🟡 | `round8e-latest.md` (11/11): UPTREND-only had the higher return in all 4 comparisons (+0.7 to +4.1 pts/yr); drawdowns mixed → inconclusive by the pre-registered bar; rule stays |
| EPS growth ≥ 25% (hard block) | 🟡 | `round8f-latest.md` (11/16): pass and fail trades earn the same R (no harm shown; sales and operating income no better) → next version: information only, or a ranking input (**Nov 23** ranking test) |
| No buys within 14 days of earnings | 🟡 | `round8f-latest.md` (11/16): no difference inside vs outside the window (7 / 14 / 21 days) → next version: candidate for information only |
| 24-hour rule (rescan tomorrow, then buy) | 🟡 / ❌ | `round8f-latest.md` (11/16): same R per trade, lower portfolio return in all 4 comparisons; HURTS with the original stop → next version: optional, drop if the original stop is adopted |
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

## New ideas to test (added 11/14 — each locked before it runs)
| Idea | Status | When |
| --- | --- | --- |
| Position size by volatility (calmer stocks get more, wild ones less) vs equal dollar risk | ⬜ | → **Nov 30**, with the portfolio test |
| Add to winners (a second piece once a trade is up 1R or 2R) vs one entry | ⬜ | → **Nov 30**, with the portfolio test |
| Re-entry after a stop-out (buy back on a new high) on all-US data | ⬜ | → **Nov 23**, with the exit rules (Round 6 tested S&P only) |
| Sector strength as a ranking input (breakouts in leading sectors first) | ⬜ | → **Nov 23**: written amendment to the ranking pre-registration before it runs, if sector data is available for the universe |
| Earnings gap as its own entry setup (not a filter on breakouts) | ❌ live stop · 🟡 original stop | `round8f-latest.md` (11/16): about 0R with the A2 trail; +1.2R per trade with the original stop but mixed portfolio → re-test with the next-version package |
| Stricter pullback entry (50-day rising + the pullback has stopped, e.g. a close back above the prior day's high on lighter selling) vs breakouts only | ⬜ | → **Nov 30**: pullbacks are paused, not banned — the loose version (within 3% of the 50-day) was not proven in Round 8 s1; this stricter one never had a fair test (Fix List #31) |
| More chart indicators layered on breakouts | ❌ stop | nine failed for the same reason (Round 8 s2/2b) |
| **Stale watchlist** (found 11/18): the scan list only changes when Tony adds or removes a name, so it ages — new leaders never come in, faded ones never leave. Challenger: a list refreshed by rules (in: Stage 2 above a rising 200-day + RS top 20% + within 25% of the 52-week high + EPS ≥ 25%; out: two weekly closes failing, kept on a "Dropped" list and still tracked) vs today's fixed list. Same as the v3 "leader shortlist". Not changed during the live test (it would change what the test scans) | ⬜ | → **Jan 29** review: backtest the in/out rules on the EODHD data first |
| **Outside sources: IBD 50 and Finviz presets** (Tony, 11/18: "not sure their suggestions have merit"). Does a stock from IBD 50 or a Finviz preset do better than our watchlist and SPY? Finviz presets are rules → can be backtested on 2003–2026 data; IBD 50 has no history → forward-test only (record the list each week, track 5/10/20-day returns vs SPY) | ⬜ | Finviz → backtest with the **Jan 29** list work · IBD 50 → only if Tony starts recording it |

## App fixes (not rules — next version)
| Fix | Found | Status |
| --- | --- | --- |
| Watchlist results board (all scanned stocks in one table, best on top) | 11/09 | next version |
| Tap to reopen any scan without rescanning | 11/09 | next version |
| Don't repeat SELL HALF after a partial sale is logged | 11/09 | moot since v2.16.3 (no SELL HALF instruction) |
| Refresh row numbers after I SOLD SOME splits a row | 11/09 | ✅ done (v2.16.5) |
| Top verdict vs ACTION box wording conflict (HOLD vs action) | 11/07 | next version |
| "Check operating EPS" warning when official EPS fails | 11/07 | dropped — operating income separates trades no better than official EPS (`round8f-latest.md`) |
| Watchlist PAUSE / auto-pause | 11/10 | ✅ done (v2.16.1) |
| One-tap + WATCHLIST | 11/10 | ✅ done (v2.16.2) |
| WHAT TO DO NOW says "take partial profits" without "optional" (ACTION box says optional) — make them match | 11/11 | ✅ done (v2.16.5) |
| App doesn’t know a position was already trimmed (SCALE_OUT keeps prompting) — fix: sheet script returns any closed row with the same ticker + account + entry date (date, shares, reason); app shows “already took profit on [date], the rest rides with the stop” | 11/11 | next version (display only) |
| Earnings dates not yet announced show as unknown (Alpha Vantage lists only announced dates; ~850 companies between seasons) — fill the gap with an estimate from SEC history (last year’s same-quarter 8-K date), labeled “estimated” | 11/14 | next version |
| Nightly data check failed 9 nights (11/6–11/14) on a seasonal earnings-count threshold — data was saved every night | 11/14 | ✅ fixed (threshold 300) |
| App vs backtest parity check (`scripts/backtest/tests/parity_app_vs_engine.py`, results in `app-audit.md`) | 11/14 | ✅ done — price rules and market gate identical on 4,429 stock-days |
| Row numbers refresh after I SOLD SOME · +20% prompt says "optional" everywhere | 11/14 | ✅ done (v2.16.5) |
| Position sizing: fixed $ risk, no per-position cap, no position-count limit (backtest: 1% of account, 20% cap, 10 positions) | 11/14 | next version, after the Nov 30 portfolio test |
| Eligibility check in the app (≥ $5 and ≥ $20M/day, as in the backtests) | 11/14 | next version |
| AI adjusted EPS overrides official SEC EPS in the 25% rule (backtests used SEC only) | 11/14 | cannot be backtested (no history) — moot if the EPS rule becomes information only |
