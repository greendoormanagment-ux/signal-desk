# Round 6 — best small combination of rules (2026-10-22)

> **Re-run on REPAIRED data (Round 7 `data_clean.py`: 157 files fixed, 29 dropped), run locally without SEC files** — so the EPS/sales checks inside 'live rules' and 'EPS & sales' are switched off (price rules only). Compare with `round6-latest.md` (raw EODHD files, SEC data on).

**Data:** long (EODHD) · 923 S&P 500 members (point in time) · cost 0.07% per side · idle money in SPY · signals at the close, filled next open.
**Periods:** TUNE 2005-01-01 → 2016-12-31 (used to choose) · JUDGE 2017-01-01 → 2025-12-31 (opened only for the top 3) · 2026 shown alone.

**Search:** 4 entry filters × 2 setup choices × 4 exits × 3 market rules × re-entry (off / standard / early) = 288 combinations. *Re-entry* = after any sale, buy back within 40 sessions if the stock closes above its high since the sale, above the 50-day, on 1.2× volume, not rated SELL, market not in CORRECTION (max 2 buy-backs in a row). *Early re-entry* = same, but the trigger is a close back above the 50-day that also tops the prior 10-day high (3+ sessions after the sale), so it can buy back below the sale price.

**Pass bar (raised because 288 combinations were tried):** beat SPY in tune AND judge, ≥ 80% of judge bootstrap resamples above zero, judge drawdown no worse than SPY's + 5 points.

**43 of 288 combinations beat SPY in the tune years.**

| SPY | CAGR | max drawdown |
| --- | --- | --- |
| tune | 7.5% | -55.2% |
| judge | 14.9% | -33.7% |
| 2026 | 16.1% | -8.9% |

## Top 3 (chosen on tune only) + the live system

| Combination | Rule changes | Tune vs SPY | Judge CAGR (vs SPY) | Judge range | Judge max DD | Bootstrap % | 2026 vs SPY | Passes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trend template · breakouts only · 50-day exit · S&P above 200-day · early re-entry | 5 | 3.1 | **11.9% (-3.0)** | 9.0 to 13.8 | -27.1% | 4.0 | -19.9 | ✗ |
| trend template · breakouts only · original stop · half size if not UPTREND · no re-entry | 4 | 2.3 | **12.4% (-2.5)** | 10.8 to 15.5 | -32.5% | 47.0 | -3.1 | ✗ |
| live rules · breakouts only · original stop · half size if not UPTREND · re-entry | 4 | 2.4 | **17.4% (2.5)** | 11.2 to 22.8 | -31.9% | 92.0 | -10.6 | ✅ |
| live rules · breakouts + pullbacks · A2 trail · live gate · no re-entry **(live today)** | 0 | -8.2 | **7.0% (-7.9)** | 2.2 to 14.3 | -31.4% | 7.0 | -11.2 | – |

## Which single choices helped most (tune years, averaged over every combination that used them)

**Entry filter:** trend template -1.8 (14/72 beat SPY) · live rules -2.7 (10/72 beat SPY) · EPS & sales -2.7 (10/72 beat SPY) · leaders -2.8 (9/72 beat SPY)

**Setups:** breakouts only -1.3 (37/144 beat SPY) · breakouts + pullbacks -3.7 (6/144 beat SPY)

**Exit:** original stop -0.7 (27/72 beat SPY) · 50-day exit -2.2 (10/72 beat SPY) · original stop + climax sell -2.4 (5/72 beat SPY) · A2 trail -4.8 (1/72 beat SPY)

**Market rule:** S&P above 200-day -1.6 (23/96 beat SPY) · half size if not UPTREND -2.5 (13/96 beat SPY) · live gate -3.4 (7/96 beat SPY)

**Re-entry:** no re-entry -2.1 (18/96 beat SPY) · re-entry -2.7 (11/96 beat SPY) · early re-entry -2.8 (14/96 beat SPY)

**Re-entry effect by exit** (tune, minus no re-entry): A2 trail -0.1 · original stop -0.5 · 50-day exit -1.2 · original stop + climax sell -0.4

**Early re-entry effect by exit** (tune, minus no re-entry): A2 trail +0.2 · original stop -0.8 · 50-day exit -1.4 · original stop + climax sell -0.7

## Top 40 of 288 on tune (best first)

| # | Combination | Tune vs SPY | Tune CAGR | Tune DD | Sub-periods vs SPY | Trades | Buy-backs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | trend template · breakouts only · 50-day exit · S&P above 200-day · early re-entry | 3.1 | 8.6% | -51.8% | 4.7 / -0.8 / -1.2 | 417 | 119 |
| 2 | trend template · breakouts only · 50-day exit · S&P above 200-day · re-entry | 2.7 | 8.1% | -51.6% | 1.6 / -0.8 / 1.1 | 431 | 126 |
| 3 | live rules · breakouts only · original stop · half size if not UPTREND · re-entry | 2.4 | 8.9% | -49.8% | 1.5 / 3.9 / -1.2 | 174 | 53 |
| 4 | EPS & sales · breakouts only · original stop · half size if not UPTREND · re-entry | 2.4 | 8.9% | -49.8% | 1.5 / 3.9 / -1.2 | 174 | 53 |
| 5 | trend template · breakouts only · original stop · half size if not UPTREND · no re-entry | 2.3 | 8.7% | -55.7% | -0.2 / 4.2 / 0.1 | 172 | 0 |
| 6 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | 2.0 | 7.6% | -52.6% | 4.4 / -5.0 / 0.4 | 710 | 95 |
| 7 | leaders · breakouts only · original stop · S&P above 200-day · no re-entry | 1.6 | 9.8% | -56.6% | 1.3 / 4.8 / 1.5 | 153 | 0 |
| 8 | trend template · breakouts only · 50-day exit · S&P above 200-day · no re-entry | 1.5 | 8.6% | -51.2% | 4.3 / -2.2 / 0.9 | 384 | 0 |
| 9 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | 1.5 | 6.4% | -51.4% | 0.2 / -3.7 / 0.2 | 252 | 0 |
| 10 | trend template · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | 1.4 | 7.2% | -53.8% | 1.6 / -5.5 / 3.0 | 465 | 0 |
| 11 | leaders · breakouts only · original stop · half size if not UPTREND · no re-entry | 1.4 | 8.9% | -55.2% | 2.0 / 2.4 / -0.2 | 183 | 0 |
| 12 | leaders · breakouts only · 50-day exit · S&P above 200-day · no re-entry | 1.4 | 8.6% | -51.1% | 3.7 / -4.5 / 4.0 | 408 | 0 |
| 13 | leaders · breakouts only · original stop · half size if not UPTREND · re-entry | 1.2 | 8.4% | -56.3% | 1.2 / 1.1 / 0.6 | 198 | 46 |
| 14 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | 1.1 | 8.3% | -53.1% | 1.3 / -0.2 / 1.4 | 229 | 0 |
| 15 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | 1.1 | 8.3% | -53.1% | 1.3 / -0.2 / 1.4 | 229 | 0 |
| 16 | live rules · breakouts only · original stop · S&P above 200-day · early re-entry | 0.9 | 8.0% | -52.9% | 0.9 / 3.8 / -2.7 | 149 | 40 |
| 17 | EPS & sales · breakouts only · original stop · S&P above 200-day · early re-entry | 0.9 | 8.0% | -52.9% | 0.9 / 3.8 / -2.7 | 149 | 40 |
| 18 | live rules · breakouts only · original stop · live gate · re-entry | 0.8 | 7.1% | -47.0% | 4.6 / -0.5 / -5.8 | 156 | 38 |
| 19 | live rules · breakouts only · original stop · half size if not UPTREND · no re-entry | 0.8 | 8.1% | -51.4% | 1.4 / 3.4 / -2.8 | 177 | 0 |
| 20 | EPS & sales · breakouts only · original stop · live gate · re-entry | 0.8 | 7.1% | -47.0% | 4.6 / -0.5 / -5.8 | 156 | 38 |
| 21 | EPS & sales · breakouts only · original stop · half size if not UPTREND · no re-entry | 0.8 | 8.1% | -51.4% | 1.4 / 3.4 / -2.8 | 177 | 0 |
| 22 | leaders · breakouts only · original stop · live gate · re-entry | 0.6 | 6.5% | -54.0% | 0.7 / -0.5 / -3.0 | 177 | 44 |
| 23 | live rules · breakouts only · original stop · S&P above 200-day · no re-entry | 0.5 | 6.1% | -57.7% | -1.8 / 3.3 / -5.3 | 145 | 0 |
| 24 | leaders · breakouts only · original stop · S&P above 200-day · early re-entry | 0.5 | 7.2% | -56.2% | 2.2 / 4.7 / -7.4 | 173 | 39 |
| 25 | EPS & sales · breakouts only · original stop · S&P above 200-day · no re-entry | 0.5 | 6.1% | -57.7% | -1.8 / 3.3 / -5.3 | 145 | 0 |
| 26 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | 0.4 | 8.4% | -54.2% | -0.6 / -3.4 / 7.3 | 252 | 23 |
| 27 | live rules · breakouts only · 50-day exit · S&P above 200-day · early re-entry | 0.4 | 8.3% | -51.3% | 4.3 / -2.7 / 0.4 | 416 | 113 |
| 28 | trend template · breakouts only · 50-day exit · live gate · no re-entry | 0.4 | 7.2% | -53.2% | -0.3 / -5.9 / 5.7 | 409 | 0 |
| 29 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | 0.4 | 6.9% | -55.1% | -0.4 / -2.4 / 1.3 | 303 | 0 |
| 30 | leaders · breakouts only · original stop · half size if not UPTREND · early re-entry | 0.4 | 8.0% | -55.9% | 1.0 / 1.3 / -0.6 | 197 | 46 |
| 31 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | 0.4 | 8.4% | -54.2% | -0.6 / -3.4 / 7.3 | 252 | 23 |
| 32 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · early re-entry | 0.4 | 8.3% | -51.3% | 4.3 / -2.7 / 0.4 | 416 | 113 |
| 33 | trend template · breakouts only · original stop · half size if not UPTREND · re-entry | 0.3 | 8.9% | -54.4% | 1.0 / 3.2 / 0.4 | 186 | 67 |
| 34 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | 0.3 | 9.5% | -52.1% | 5.8 / -2.3 / 2.1 | 293 | 0 |
| 35 | trend template · breakouts only · A2 trail · S&P above 200-day · re-entry | 0.2 | 9.9% | -55.1% | 1.1 / 2.9 / 3.6 | 411 | 111 |
| 36 | trend template · breakouts only · original stop · S&P above 200-day · no re-entry | 0.2 | 7.6% | -53.5% | -2.2 / 4.0 / -0.7 | 132 | 0 |
| 37 | live rules · breakouts only · original stop · live gate · early re-entry | 0.1 | 4.8% | -46.4% | 1.9 / -2.2 / -8.3 | 172 | 48 |
| 38 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | 0.1 | 4.7% | -56.3% | 0.2 / -2.1 / -6.7 | 264 | 49 |
| 39 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | 0.1 | 7.2% | -51.0% | 5.5 / -6.7 / -0.0 | 863 | 99 |
| 40 | trend template · breakouts only · original stop · S&P above 200-day · early re-entry | 0.1 | 8.2% | -54.2% | -0.3 / 4.2 / -1.2 | 154 | 55 |

_Full table: re-run locally with `R6_CLEAN=1`. Generated by scripts/backtest/run_round6.py._
