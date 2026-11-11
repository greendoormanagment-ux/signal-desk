# Round 8 · session 2b — pre-registration (LOCKED 2026-11-11, before any result was run)

Same standard as `footprint-test-rules.md` (all eight rules, the same thresholds and the same operational choices written in `scripts/backtest/run_round8b.py`): +0.15R minimum, 99% family-wise with Holm, two-way clustering by stock and entry month, development 2005–16 decides, validation 2017–25 checks, 300+ trades on each side, consistency in S&P / non-S&P and 3 of 4 regimes, portfolio vs SPY with no more than 3 pp deeper drawdown, PASS / FAIL / INCONCLUSIVE. Base = live v2.16 rules (breakouts only + A2 trail + live gate), all US pooled.

## The family (3 primary tests, own Holm correction)

| # | Test | "With" means (read on the signal day, completed bars) |
| --- | --- | --- |
| 1 | 21-day moving average | close above its 21-day simple average **and** that average higher than 5 sessions earlier |
| 2 | 12-1 momentum | return from 252 to 21 sessions ago in the **top 30%** of all eligible US stocks that day |
| 3 | Earnings-gap drift | the app's `driftSetup()` (v2.16): an opening gap up of **≥ 4%** on **≥ 2×** the 50-day average volume (excluding that day) in the last 3 sessions |

**Dropped from this family, with reason:** "52-week vs latest-base pivot". The engine's pivot is already the prior-year high, so every breakout is a 52-week-high breakout; a "latest-base" pivot would be a different entry rule (it needs a base-detection definition) and is listed as a future hypothesis, not tested here.

## Descriptive questions from the colleague (no pass/fail)

For the best version from session 1 (breakouts only + original stop + live gate), development and validation separately:
- Trade profile: number of trades, win rate, average win / loss in R, largest win, longest losing streak, profit factor, share of total R from the top 5% of trades.
- Concentration: share of total R from the top 10 stocks, and the mean R with them removed.
- S&P vs non-S&P: the difference in mean R tested directly (clustered); and why the portfolio gap is larger than the per-trade gap (trades per year, holding days, average stop distance, how often all 10 slots are full).
- Year by year: S&P-only portfolio vs SPY and RSP.
