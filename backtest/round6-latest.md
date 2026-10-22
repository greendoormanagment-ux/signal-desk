# Round 6 — best small combination of rules (2026-10-22)

**Data:** long (EODHD) · 951 S&P 500 members (point in time) · cost 0.07% per side · idle money in SPY · signals at the close, filled next open.
**Periods:** TUNE 2005-01-01 → 2016-12-31 (used to choose) · JUDGE 2017-01-01 → 2025-12-31 (opened only for the top 3) · 2026 shown alone.

**Search:** 4 entry filters × 2 setup choices × 4 exits × 3 market rules × re-entry (off / standard / early) = 288 combinations. *Re-entry* = after any sale, buy back within 40 sessions if the stock closes above its high since the sale, above the 50-day, on 1.2× volume, not rated SELL, market not in CORRECTION (max 2 buy-backs in a row). *Early re-entry* = same, but the trigger is a close back above the 50-day that also tops the prior 10-day high (3+ sessions after the sale), so it can buy back below the sale price.

**Pass bar (raised because 288 combinations were tried):** beat SPY in tune AND judge, ≥ 80% of judge bootstrap resamples above zero, judge drawdown no worse than SPY's + 5 points.

**30 of 288 combinations beat SPY in the tune years.**

| SPY | CAGR | max drawdown |
| --- | --- | --- |
| tune | 7.5% | -55.2% |
| judge | 14.9% | -33.7% |
| 2026 | 16.1% | -8.9% |

## Top 3 (chosen on tune only) + the live system

| Combination | Rule changes | Tune vs SPY | Judge CAGR (vs SPY) | Judge range | Judge max DD | Bootstrap % | 2026 vs SPY | Passes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trend template · breakouts only · original stop · S&P above 200-day · no re-entry | 4 | 6.1 | **14.2% (-0.7)** | 12.4 to 18.5 | -32.1% | 66.0 | 2.8 | ✗ |
| trend template · breakouts only · original stop · half size if not UPTREND · no re-entry | 4 | 3.8 | **12.8% (-2.1)** | 11.9 to 14.1 | -34.1% | 27.0 | 0.1 | ✗ |
| trend template · breakouts only · 50-day exit · S&P above 200-day · no re-entry | 4 | 3.4 | **12.6% (-2.3)** | 11.9 to 14.1 | -33.3% | 37.0 | -20.4 | ✗ |
| live rules · breakouts + pullbacks · A2 trail · live gate · no re-entry **(live today)** | 0 | -6.9 | **10.1% (-4.8)** | 6.9 to 14.5 | -34.7% | 5.0 | -6.4 | – |

## Which single choices helped most (tune years, averaged over every combination that used them)

**Entry filter:** trend template -2.0 (19/72 beat SPY) · live rules -4.4 (7/72 beat SPY) · EPS & sales -4.4 (3/72 beat SPY) · leaders -7.5 (1/72 beat SPY)

**Setups:** breakouts + pullbacks -4.0 (15/144 beat SPY) · breakouts only -5.1 (15/144 beat SPY)

**Exit:** original stop -1.5 (19/72 beat SPY) · original stop + climax sell -4.4 (4/72 beat SPY) · 50-day exit -5.3 (5/72 beat SPY) · A2 trail -7.1 (2/72 beat SPY)

**Market rule:** half size if not UPTREND -3.5 (11/96 beat SPY) · S&P above 200-day -4.5 (14/96 beat SPY) · live gate -5.7 (5/96 beat SPY)

**Re-entry:** no re-entry -3.2 (17/96 beat SPY) · re-entry -5.2 (8/96 beat SPY) · early re-entry -5.3 (5/96 beat SPY)

**Re-entry effect by exit** (tune, minus no re-entry): A2 trail -2.6 · original stop -1.3 · 50-day exit -2.6 · original stop + climax sell -1.8

**Early re-entry effect by exit** (tune, minus no re-entry): A2 trail -2.1 · original stop -1.9 · 50-day exit -3.1 · original stop + climax sell -1.4

## All 288 on tune (best first)

| # | Combination | Tune vs SPY | Tune CAGR | Tune DD | Sub-periods vs SPY | Trades | Buy-backs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | trend template · breakouts only · original stop · S&P above 200-day · no re-entry | 6.1 | 12.3% | -46.2% | -3.3 / 16.0 / 4.5 | 118 | 0 |
| 2 | trend template · breakouts only · original stop · half size if not UPTREND · no re-entry | 3.8 | 11.0% | -50.0% | -3.3 / 14.2 / 1.8 | 150 | 0 |
| 3 | trend template · breakouts only · 50-day exit · S&P above 200-day · no re-entry | 3.4 | 10.6% | -41.1% | 0.9 / 7.3 / 2.3 | 297 | 0 |
| 4 | trend template · breakouts only · original stop · S&P above 200-day · re-entry | 3.3 | 10.9% | -50.3% | -5.6 / 15.2 / 3.6 | 138 | 51 |
| 5 | trend template · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | 3.2 | 6.6% | -51.0% | 0.1 / 2.7 / -5.2 | 195 | 35 |
| 6 | trend template · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | 3.1 | 10.7% | -43.0% | 1.4 / 6.9 / 2.1 | 352 | 0 |
| 7 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | 2.8 | 8.2% | -60.0% | -5.1 / 4.3 / 4.4 | 232 | 41 |
| 8 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | 2.7 | 6.8% | -55.9% | -0.8 / 1.1 / -2.1 | 274 | 0 |
| 9 | trend template · breakouts only · original stop · live gate · no re-entry | 2.3 | 9.9% | -49.3% | -5.6 / 13.7 / 1.7 | 131 | 0 |
| 10 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | 1.6 | 8.2% | -46.6% | -4.4 / 9.6 / -1.5 | 243 | 0 |
| 11 | trend template · breakouts only · 50-day exit · live gate · no re-entry | 1.5 | 9.6% | -40.1% | -0.1 / 3.2 / 4.1 | 308 | 0 |
| 12 | trend template · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | 1.2 | 8.7% | -51.1% | 6.4 / 1.8 / -4.9 | 184 | 0 |
| 13 | trend template · breakouts only · original stop · S&P above 200-day · early re-entry | 1.2 | 10.4% | -52.5% | -6.4 / 12.9 / 5.1 | 130 | 41 |
| 14 | trend template · breakouts + pullbacks · original stop · live gate · re-entry | 1.1 | 8.0% | -50.9% | 1.6 / 3.6 / -3.3 | 190 | 43 |
| 15 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | 1.1 | 7.7% | -46.1% | -2.5 / 6.4 / -2.1 | 212 | 0 |
| 16 | EPS & sales · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | 1.1 | 7.8% | -51.8% | 3.8 / 1.9 / -5.0 | 294 | 0 |
| 17 | trend template · breakouts only · 50-day exit · half size if not UPTREND · early re-entry | 1.0 | 7.5% | -51.0% | -7.1 / 10.2 / -0.7 | 403 | 162 |
| 18 | leaders · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | 0.9 | 8.2% | -51.4% | 1.6 / -3.7 / 4.4 | 133 | 0 |
| 19 | live rules · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | 0.8 | 2.8% | -50.9% | -2.2 / -6.2 / -5.9 | 337 | 0 |
| 20 | trend template · breakouts + pullbacks · original stop · live gate · early re-entry | 0.8 | 6.9% | -50.8% | 1.5 / 4.1 / -7.1 | 192 | 41 |
| 21 | live rules · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | 0.7 | 8.2% | -51.8% | 3.8 / -0.8 / -1.2 | 273 | 0 |
| 22 | live rules · breakouts + pullbacks · original stop · live gate · re-entry | 0.6 | 4.5% | -58.2% | -4.2 / -2.1 / -2.2 | 231 | 34 |
| 23 | live rules · breakouts + pullbacks · original stop · half size if not UPTREND · early re-entry | 0.6 | 5.8% | -52.2% | 0.0 / -1.0 / -4.1 | 274 | 47 |
| 24 | trend template · breakouts only · 50-day exit · half size if not UPTREND · re-entry | 0.6 | 8.6% | -49.3% | -6.3 / 10.1 / 2.1 | 391 | 141 |
| 25 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | 0.5 | 5.7% | -60.0% | -5.1 / -0.7 / 1.5 | 216 | 33 |
| 26 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | 0.4 | 8.2% | -55.9% | -0.8 / -0.5 / 3.9 | 224 | 0 |
| 27 | trend template · breakouts only · A2 trail · half size if not UPTREND · no re-entry | 0.2 | 6.8% | -47.0% | -4.6 / 6.8 / -2.9 | 359 | 0 |
| 28 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | 0.2 | 7.7% | -51.2% | -6.0 / 11.0 / -2.2 | 222 | 80 |
| 29 | live rules · breakouts only · original stop · half size if not UPTREND · no re-entry | 0.1 | 7.3% | -47.0% | 0.2 / -0.4 / -0.1 | 160 | 0 |
| 30 | trend template · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | 0.1 | 5.7% | -43.5% | -2.8 / 4.5 / -6.1 | 549 | 61 |
| 31 | trend template · breakouts + pullbacks · original stop · live gate · no re-entry | 0.0 | 5.9% | -46.6% | 2.3 / -0.3 / -6.8 | 179 | 0 |
| 32 | trend template · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | 0.0 | 5.9% | -51.2% | 0.7 / -0.7 / -4.8 | 218 | 51 |
| 33 | trend template · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | 0.0 | 6.5% | -50.9% | 1.9 / 1.4 / -6.3 | 194 | 38 |
| 34 | trend template · breakouts only · original stop · live gate · re-entry | -0.1 | 7.8% | -58.0% | -9.7 / 14.5 / -0.0 | 153 | 51 |
| 35 | EPS & sales · breakouts + pullbacks · original stop · live gate · no re-entry | -0.1 | 5.8% | -52.6% | 0.0 / 1.4 / -6.6 | 256 | 0 |
| 36 | EPS & sales · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -0.1 | 4.4% | -51.4% | -3.6 / -2.8 / -2.8 | 400 | 66 |
| 37 | live rules · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -0.2 | 6.0% | -47.4% | -0.5 / -1.9 / -1.9 | 385 | 0 |
| 38 | trend template · breakouts only · original stop · half size if not UPTREND · re-entry | -0.2 | 7.4% | -56.2% | -8.9 / 13.1 / -1.2 | 180 | 67 |
| 39 | live rules · breakouts + pullbacks · original stop · live gate · early re-entry | -0.3 | 4.7% | -56.7% | -3.4 / -2.1 / -2.5 | 231 | 35 |
| 40 | EPS & sales · breakouts only · original stop · half size if not UPTREND · no re-entry | -0.3 | 7.7% | -47.0% | 0.2 / 0.7 / -0.0 | 153 | 0 |
| 41 | EPS & sales · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -0.3 | 7.6% | -44.0% | -2.6 / 2.3 / 1.3 | 226 | 0 |
| 42 | live rules · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | -0.4 | 3.9% | -52.2% | -1.1 / -10.2 / 0.9 | 391 | 43 |
| 43 | live rules · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -0.5 | 3.9% | -56.7% | -5.5 / -1.0 / -3.6 | 278 | 46 |
| 44 | trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -0.6 | 1.8% | -58.0% | -5.4 / -7.8 / -3.7 | 313 | 0 |
| 45 | trend template · breakouts only · 50-day exit · S&P above 200-day · early re-entry | -0.6 | 8.4% | -52.7% | -5.3 / 9.4 / 0.7 | 333 | 137 |
| 46 | live rules · breakouts + pullbacks · original stop · live gate · no re-entry | -0.7 | 6.0% | -52.6% | 0.0 / -2.0 / -2.5 | 249 | 0 |
| 47 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | -0.7 | 6.5% | -58.0% | -4.0 / -0.7 / 2.7 | 206 | 38 |
| 48 | trend template · breakouts + pullbacks · original stop · half size if not UPTREND · early re-entry | -0.7 | 4.8% | -51.4% | 0.7 / -1.5 / -7.5 | 233 | 55 |
| 49 | leaders · breakouts only · original stop · half size if not UPTREND · no re-entry | -0.7 | 7.4% | -49.1% | 2.1 / -3.4 / 0.9 | 165 | 0 |
| 50 | EPS & sales · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -0.7 | 5.6% | -50.9% | -2.2 / -0.3 / -2.9 | 394 | 0 |
| 51 | trend template · breakouts only · original stop · half size if not UPTREND · early re-entry | -0.9 | 7.1% | -58.3% | -10.1 / 13.2 / -0.9 | 177 | 64 |
| 52 | trend template · breakouts only · original stop + climax sell · live gate · no re-entry | -1.0 | 5.5% | -56.3% | -8.8 / 6.1 / -1.0 | 230 | 0 |
| 53 | EPS & sales · breakouts + pullbacks · original stop · half size if not UPTREND · early re-entry | -1.0 | 6.3% | -52.2% | 0.0 / 2.9 / -6.4 | 294 | 55 |
| 54 | live rules · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -1.1 | 5.5% | -49.7% | 1.7 / -7.9 / -0.2 | 689 | 71 |
| 55 | trend template · breakouts only · original stop · live gate · early re-entry | -1.1 | 6.4% | -60.7% | -11.1 / 13.1 / -1.7 | 152 | 54 |
| 56 | EPS & sales · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -1.1 | 3.9% | -56.7% | -5.5 / 2.1 / -6.4 | 298 | 54 |
| 57 | EPS & sales · breakouts only · original stop + climax sell · half size if not UPTREND · early re-entry | -1.2 | 6.7% | -50.2% | -5.9 / 3.1 / 1.9 | 279 | 96 |
| 58 | EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | -1.3 | 4.2% | -52.2% | -1.1 / -7.8 / -0.9 | 415 | 62 |
| 59 | leaders · breakouts + pullbacks · original stop · live gate · no re-entry | -1.4 | 6.1% | -47.4% | 5.2 / -5.2 / -4.7 | 171 | 0 |
| 60 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -1.5 | 7.5% | -56.7% | -9.1 / 11.8 / 0.4 | 276 | 102 |
| 61 | trend template · breakouts only · 50-day exit · S&P above 200-day · re-entry | -1.5 | 6.3% | -58.9% | -10.1 / 9.8 / -0.2 | 334 | 132 |
| 62 | live rules · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -1.6 | 5.2% | -44.0% | -2.6 / -0.3 / -3.6 | 235 | 0 |
| 63 | trend template · breakouts only · original stop + climax sell · live gate · re-entry | -1.6 | 7.0% | -60.7% | -11.1 / 15.3 / -1.6 | 250 | 87 |
| 64 | trend template · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -1.7 | 5.9% | -47.7% | 2.6 / -2.3 / -5.5 | 215 | 0 |
| 65 | EPS & sales · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -1.7 | 4.1% | -49.7% | 1.7 / -7.4 / -5.3 | 764 | 99 |
| 66 | live rules · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -1.8 | 8.7% | -44.3% | -2.7 / 4.1 / 3.5 | 353 | 0 |
| 67 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · early re-entry | -1.8 | 5.9% | -54.8% | -7.7 / 9.3 / -4.2 | 236 | 85 |
| 68 | leaders · breakouts + pullbacks · original stop · live gate · early re-entry | -1.8 | 5.4% | -55.7% | -2.3 / 0.7 / -4.3 | 172 | 35 |
| 69 | EPS & sales · breakouts + pullbacks · original stop · live gate · early re-entry | -1.8 | 5.9% | -56.7% | -3.4 / 2.0 / -2.9 | 230 | 37 |
| 70 | EPS & sales · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -1.8 | 8.0% | -44.3% | -2.7 / 3.1 / 2.2 | 334 | 0 |
| 71 | trend template · breakouts + pullbacks · A2 trail · half size if not UPTREND · early re-entry | -1.9 | 4.8% | -43.8% | -2.9 / 2.6 / -7.0 | 559 | 70 |
| 72 | EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -1.9 | 2.9% | -52.9% | -3.3 / -8.0 / -2.4 | 421 | 57 |
| 73 | leaders · breakouts only · original stop · S&P above 200-day · no re-entry | -2.0 | 6.3% | -45.2% | -3.2 / -2.7 / 3.0 | 118 | 0 |
| 74 | EPS & sales · breakouts + pullbacks · original stop · live gate · re-entry | -2.0 | 5.6% | -58.2% | -4.2 / 2.1 / -2.9 | 233 | 35 |
| 75 | EPS & sales · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | -2.1 | 3.5% | -49.5% | 1.1 / -7.2 / -6.6 | 773 | 83 |
| 76 | EPS & sales · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -2.1 | 6.2% | -51.3% | -6.4 / 5.0 / -0.7 | 272 | 96 |
| 77 | live rules · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | -2.3 | 5.4% | -49.5% | 1.1 / -7.2 / -0.3 | 684 | 65 |
| 78 | trend template · breakouts + pullbacks · A2 trail · live gate · early re-entry | -2.3 | -1.9% | -55.4% | -7.4 / -10.9 / -9.3 | 469 | 58 |
| 79 | trend template · breakouts only · 50-day exit · live gate · early re-entry | -2.3 | 4.3% | -55.2% | -9.6 / 3.3 / -0.9 | 343 | 139 |
| 80 | trend template · breakouts only · A2 trail · S&P above 200-day · no re-entry | -2.3 | 5.6% | -54.6% | -7.6 / 4.9 / -0.9 | 330 | 0 |
| 81 | live rules · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -2.4 | 2.1% | -48.3% | -3.3 / -9.7 / -3.1 | 828 | 0 |
| 82 | trend template · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -2.4 | 3.7% | -49.8% | -5.6 / 1.1 / -5.8 | 546 | 0 |
| 83 | trend template · breakouts only · original stop + climax sell · live gate · early re-entry | -2.4 | 6.4% | -59.5% | -10.5 / 10.8 / -0.4 | 251 | 89 |
| 84 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · early re-entry | -2.4 | 6.2% | -57.6% | -9.6 / 10.0 / -1.5 | 273 | 105 |
| 85 | leaders · breakouts only · original stop · half size if not UPTREND · re-entry | -2.4 | 5.4% | -50.0% | -1.5 / -3.7 / -1.1 | 194 | 55 |
| 86 | leaders · breakouts only · original stop · S&P above 200-day · early re-entry | -2.4 | 5.7% | -47.0% | -1.5 / -4.9 / 1.3 | 137 | 36 |
| 87 | EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -2.4 | 6.2% | -47.4% | -0.5 / -0.9 / -2.4 | 407 | 0 |
| 88 | live rules · breakouts only · original stop · live gate · no re-entry | -2.5 | 5.0% | -45.9% | -3.6 / -0.6 / -2.8 | 134 | 0 |
| 89 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -2.5 | 3.1% | -54.9% | -6.2 / -6.7 / 1.0 | 272 | 0 |
| 90 | leaders · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -2.6 | 6.2% | -62.4% | -5.9 / -2.7 / 6.6 | 159 | 32 |
| 91 | live rules · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | -2.7 | 4.9% | -48.2% | 2.2 / -11.7 / 1.8 | 359 | 46 |
| 92 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | -2.8 | 8.6% | -58.0% | -4.0 / 4.3 / 4.5 | 231 | 44 |
| 93 | EPS & sales · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · early re-entry | -2.8 | 5.4% | -51.6% | -3.7 / 0.9 / -2.7 | 390 | 62 |
| 94 | trend template · breakouts + pullbacks · A2 trail · live gate · re-entry | -2.9 | -1.7% | -55.6% | -6.8 / -12.8 / -7.7 | 469 | 53 |
| 95 | leaders · breakouts only · original stop · half size if not UPTREND · early re-entry | -2.9 | 4.4% | -50.1% | -0.9 / -5.6 / -3.0 | 200 | 60 |
| 96 | live rules · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -3.0 | 3.8% | -48.5% | 0.0 / -11.9 / 1.2 | 355 | 46 |
| 97 | trend template · breakouts only · A2 trail · live gate · no re-entry | -3.0 | 4.3% | -58.2% | -9.8 / 5.1 / -2.7 | 330 | 0 |
| 98 | leaders · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -3.0 | 5.0% | -47.2% | 3.4 / -6.5 / -5.0 | 188 | 0 |
| 99 | live rules · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -3.1 | 1.8% | -47.7% | -2.6 / -15.0 / 1.3 | 355 | 0 |
| 100 | live rules · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -3.1 | 3.2% | -51.3% | -4.0 / -5.6 / -2.8 | 706 | 0 |
| 101 | live rules · breakouts only · original stop · half size if not UPTREND · re-entry | -3.1 | 5.0% | -49.5% | -4.8 / -1.7 / -0.1 | 189 | 67 |
| 102 | leaders · breakouts only · original stop · live gate · no re-entry | -3.1 | 3.5% | -43.3% | -3.1 / -7.6 / -1.0 | 142 | 0 |
| 103 | leaders · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -3.1 | 4.4% | -49.0% | -4.2 / -6.2 / 2.2 | 350 | 0 |
| 104 | live rules · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -3.2 | 5.2% | -47.2% | 2.1 / -8.9 / -0.2 | 819 | 82 |
| 105 | live rules · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -3.2 | 3.7% | -52.9% | -3.3 / -10.2 / 2.7 | 397 | 43 |
| 106 | live rules · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · early re-entry | -3.2 | 3.2% | -51.6% | -3.7 / -4.8 / -4.0 | 346 | 52 |
| 107 | live rules · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -3.2 | 4.6% | -51.3% | -6.4 / 4.2 / -4.9 | 271 | 99 |
| 108 | leaders · breakouts only · original stop · S&P above 200-day · re-entry | -3.2 | 5.1% | -46.7% | -2.7 / -5.0 / 1.0 | 133 | 35 |
| 109 | EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | -3.2 | 3.1% | -50.0% | 2.2 / -12.2 / -3.4 | 383 | 56 |
| 110 | live rules · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -3.3 | -0.5% | -44.8% | -4.8 / -12.8 / -6.5 | 631 | 0 |
| 111 | live rules · breakouts only · original stop · S&P above 200-day · re-entry | -3.3 | 4.4% | -51.1% | -6.5 / -1.0 / -0.3 | 145 | 42 |
| 112 | trend template · breakouts only · 50-day exit · live gate · re-entry | -3.3 | 4.4% | -59.5% | -12.1 / 6.1 / -0.2 | 337 | 126 |
| 113 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -3.3 | 3.1% | -48.1% | -4.5 / -7.4 / -0.8 | 250 | 0 |
| 114 | EPS & sales · breakouts only · original stop · half size if not UPTREND · re-entry | -3.3 | 4.9% | -49.5% | -4.8 / -3.0 / 0.7 | 190 | 67 |
| 115 | EPS & sales · breakouts only · original stop · S&P above 200-day · re-entry | -3.3 | 4.7% | -51.1% | -6.5 / -3.1 / 2.2 | 147 | 49 |
| 116 | live rules · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | -3.4 | 5.3% | -47.2% | 2.2 / -8.9 / -0.2 | 817 | 75 |
| 117 | live rules · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -3.4 | 2.5% | -51.4% | -3.6 / -4.9 / -6.3 | 345 | 56 |
| 118 | EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -3.4 | 1.5% | -47.7% | -2.6 / -12.3 / -2.8 | 362 | 0 |
| 119 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -3.5 | 3.1% | -44.8% | 0.3 / -8.4 / -5.5 | 776 | 0 |
| 120 | EPS & sales · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -3.5 | 0.4% | -51.3% | -4.0 / -10.5 / -7.2 | 801 | 0 |
| 121 | live rules · breakouts only · original stop · live gate · re-entry | -3.6 | 4.0% | -52.3% | -6.6 / -1.1 / -1.5 | 156 | 50 |
| 122 | trend template · breakouts only · A2 trail · S&P above 200-day · early re-entry | -3.6 | 4.6% | -57.3% | -8.9 / 3.9 / -1.6 | 360 | 137 |
| 123 | leaders · breakouts + pullbacks · original stop · live gate · re-entry | -3.6 | 4.1% | -59.7% | -4.5 / -0.2 / -4.9 | 177 | 28 |
| 124 | leaders · breakouts + pullbacks · original stop · half size if not UPTREND · early re-entry | -3.6 | 3.7% | -46.8% | 1.7 / -5.9 / -7.7 | 189 | 34 |
| 125 | EPS & sales · breakouts only · 50-day exit · live gate · no re-entry | -3.6 | 1.8% | -55.0% | -7.9 / -8.0 / 0.2 | 276 | 0 |
| 126 | live rules · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -3.7 | 3.9% | -54.9% | -6.2 / -3.9 / 0.7 | 292 | 0 |
| 127 | live rules · breakouts only · original stop · half size if not UPTREND · early re-entry | -3.8 | 2.9% | -52.1% | -6.0 / -2.4 / -4.7 | 202 | 70 |
| 128 | live rules · breakouts only · original stop + climax sell · half size if not UPTREND · early re-entry | -3.8 | 3.5% | -50.2% | -5.9 / 3.5 / -8.5 | 283 | 98 |
| 129 | trend template · breakouts only · A2 trail · half size if not UPTREND · re-entry | -3.8 | 4.8% | -57.7% | -9.5 / 5.1 / -1.3 | 415 | 152 |
| 130 | EPS & sales · breakouts + pullbacks · A2 trail · half size if not UPTREND · early re-entry | -3.8 | -0.0% | -60.6% | -10.1 / -6.7 / -4.7 | 680 | 71 |
| 131 | live rules · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -3.9 | 1.3% | -52.8% | -4.5 / -7.1 / -7.0 | 594 | 0 |
| 132 | trend template · breakouts only · A2 trail · half size if not UPTREND · early re-entry | -3.9 | 4.1% | -59.6% | -10.6 / 6.3 / -3.3 | 415 | 160 |
| 133 | leaders · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -3.9 | 2.8% | -50.5% | -1.7 / -5.1 / -7.4 | 199 | 31 |
| 134 | EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -3.9 | 1.9% | -49.5% | 0.0 / -11.9 / -5.0 | 379 | 52 |
| 135 | EPS & sales · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -3.9 | 0.4% | -54.5% | -6.5 / -6.7 / -7.9 | 576 | 0 |
| 136 | EPS & sales · breakouts only · original stop · live gate · no re-entry | -3.9 | 3.5% | -45.9% | -3.6 / -4.9 / -3.1 | 129 | 0 |
| 137 | EPS & sales · breakouts only · original stop · half size if not UPTREND · early re-entry | -3.9 | 3.8% | -52.1% | -6.0 / -2.8 / -1.5 | 187 | 66 |
| 138 | trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -4.0 | 3.2% | -60.5% | -10.9 / 3.9 / -3.4 | 302 | 55 |
| 139 | leaders · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | -4.0 | 4.5% | -61.2% | -7.2 / -2.9 / 2.7 | 153 | 30 |
| 140 | live rules · breakouts only · original stop · S&P above 200-day · early re-entry | -4.1 | 5.5% | -50.4% | -6.0 / -0.7 / 2.1 | 137 | 42 |
| 141 | EPS & sales · breakouts + pullbacks · A2 trail · live gate · early re-entry | -4.1 | -3.2% | -65.8% | -14.2 / -9.5 / -6.7 | 581 | 67 |
| 142 | EPS & sales · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -4.1 | 3.9% | -50.8% | -5.4 / -5.2 / 0.7 | 355 | 0 |
| 143 | live rules · breakouts only · original stop · S&P above 200-day · no re-entry | -4.2 | 3.4% | -53.4% | -7.6 / 1.6 / -4.8 | 115 | 0 |
| 144 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -4.2 | -0.0% | -57.7% | -9.9 / -5.3 / -6.0 | 186 | 0 |
| 145 | EPS & sales · breakouts + pullbacks · 50-day exit · live gate · re-entry | -4.2 | -0.3% | -42.3% | -0.2 / -14.5 / -9.0 | 730 | 91 |
| 146 | trend template · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -4.3 | 3.8% | -60.4% | -8.9 / 2.7 / -3.1 | 524 | 0 |
| 147 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -4.3 | 2.5% | -49.2% | -2.1 / -8.8 / -4.2 | 633 | 0 |
| 148 | leaders · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -4.3 | 2.3% | -49.2% | -5.1 / -6.4 / -3.5 | 352 | 0 |
| 149 | trend template · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -4.4 | 4.1% | -50.7% | -2.5 / -7.9 / 0.6 | 325 | 0 |
| 150 | EPS & sales · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -4.4 | 1.2% | -48.3% | -3.3 / -10.2 / -5.3 | 942 | 0 |
| 151 | EPS & sales · breakouts only · original stop + climax sell · live gate · no re-entry | -4.4 | 2.9% | -52.9% | -6.9 / -5.1 / -0.7 | 208 | 0 |
| 152 | live rules · breakouts + pullbacks · 50-day exit · live gate · re-entry | -4.5 | 1.4% | -39.8% | -0.2 / -14.2 / -4.2 | 669 | 67 |
| 153 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | -4.5 | 0.4% | -51.9% | -5.7 / -6.8 / -8.7 | 649 | 78 |
| 154 | trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · early re-entry | -4.5 | 0.9% | -62.5% | -11.9 / 0.7 / -6.4 | 295 | 59 |
| 155 | leaders · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -4.5 | 1.8% | -49.1% | -2.9 / -5.7 / -8.5 | 328 | 59 |
| 156 | EPS & sales · breakouts only · original stop + climax sell · S&P above 200-day · early re-entry | -4.5 | 3.1% | -50.0% | -5.8 / -4.0 / -2.9 | 237 | 89 |
| 157 | live rules · breakouts only · 50-day exit · live gate · no re-entry | -4.6 | 2.0% | -55.0% | -7.9 / -7.4 / 0.4 | 302 | 0 |
| 158 | live rules · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -4.6 | 3.6% | -50.8% | -5.4 / -4.2 / -1.4 | 354 | 0 |
| 159 | live rules · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -4.6 | 3.7% | -53.8% | -6.1 / -4.6 / 0.1 | 418 | 159 |
| 160 | leaders · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -4.6 | 4.0% | -50.0% | -3.0 / -7.1 / -0.0 | 670 | 0 |
| 161 | EPS & sales · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -4.6 | -0.2% | -60.7% | -10.2 / -6.5 / -5.4 | 691 | 78 |
| 162 | live rules · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -4.7 | -0.8% | -60.7% | -10.2 / -10.5 / -3.3 | 625 | 62 |
| 163 | live rules · breakouts + pullbacks · A2 trail · half size if not UPTREND · early re-entry | -4.7 | -0.8% | -60.6% | -10.1 / -8.1 / -5.9 | 621 | 63 |
| 164 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | -4.8 | 1.6% | -47.0% | -3.5 / -8.9 / -5.4 | 778 | 87 |
| 165 | EPS & sales · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -4.8 | 1.8% | -47.2% | 2.1 / -10.8 / -8.9 | 979 | 115 |
| 166 | EPS & sales · breakouts + pullbacks · A2 trail · S&P above 200-day · early re-entry | -4.8 | -0.2% | -62.7% | -12.5 / -5.9 / -2.9 | 561 | 61 |
| 167 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -4.9 | 0.0% | -52.5% | -6.0 / -8.8 / -7.5 | 656 | 80 |
| 168 | EPS & sales · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | -4.9 | 2.7% | -47.2% | 2.2 / -10.4 / -6.7 | 961 | 100 |
| 169 | leaders · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | -5.0 | -0.4% | -54.2% | -6.9 / -8.0 / -8.6 | 332 | 62 |
| 170 | trend template · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -5.1 | 0.5% | -56.9% | -7.9 / -5.7 / -6.5 | 345 | 64 |
| 171 | leaders · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -5.1 | 1.7% | -46.5% | -2.7 / -8.1 / -6.7 | 316 | 0 |
| 172 | EPS & sales · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -5.1 | 1.8% | -52.8% | -4.5 / -6.3 / -6.3 | 664 | 0 |
| 173 | EPS & sales · breakouts + pullbacks · 50-day exit · live gate · early re-entry | -5.2 | 0.5% | -39.6% | -0.1 / -12.8 / -8.4 | 719 | 77 |
| 174 | live rules · breakouts + pullbacks · 50-day exit · live gate · early re-entry | -5.3 | 2.2% | -38.6% | -0.1 / -13.3 / -2.5 | 655 | 61 |
| 175 | trend template · breakouts + pullbacks · 50-day exit · live gate · early re-entry | -5.3 | -1.8% | -50.3% | -6.1 / -11.9 / -9.6 | 617 | 66 |
| 176 | trend template · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -5.3 | 1.7% | -50.0% | -5.3 / -11.0 / -0.2 | 284 | 0 |
| 177 | trend template · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -5.3 | 1.2% | -68.8% | -13.4 / -1.1 / -2.0 | 548 | 71 |
| 178 | trend template · breakouts + pullbacks · A2 trail · S&P above 200-day · early re-entry | -5.4 | -1.1% | -73.9% | -17.1 / -4.0 / -1.8 | 496 | 64 |
| 179 | leaders · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -5.4 | 1.7% | -48.1% | -3.1 / -5.2 / -9.1 | 287 | 46 |
| 180 | live rules · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -5.5 | 0.8% | -54.5% | -6.5 / -7.7 / -5.5 | 494 | 0 |
| 181 | trend template · breakouts + pullbacks · 50-day exit · live gate · re-entry | -5.5 | -1.5% | -50.8% | -6.0 / -12.4 / -8.2 | 614 | 66 |
| 182 | trend template · breakouts only · A2 trail · S&P above 200-day · re-entry | -5.5 | 3.5% | -62.5% | -11.7 / 3.3 / -1.1 | 358 | 137 |
| 183 | EPS & sales · breakouts only · original stop · live gate · re-entry | -5.5 | 0.3% | -52.3% | -6.6 / -6.0 / -8.6 | 168 | 56 |
| 184 | EPS & sales · breakouts only · original stop · S&P above 200-day · no re-entry | -5.5 | 2.3% | -53.4% | -7.6 / -2.7 / -4.3 | 120 | 0 |
| 185 | trend template · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -5.6 | 1.7% | -42.2% | 0.6 / -10.1 / -8.3 | 616 | 0 |
| 186 | leaders · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -5.6 | 1.6% | -53.5% | -7.6 / -8.8 / -0.1 | 277 | 0 |
| 187 | EPS & sales · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -5.6 | 3.0% | -53.8% | -6.1 / -5.4 / -1.1 | 392 | 159 |
| 188 | live rules · breakouts + pullbacks · A2 trail · live gate · re-entry | -5.8 | -4.3% | -66.9% | -14.9 / -12.6 / -6.1 | 529 | 60 |
| 189 | trend template · breakouts + pullbacks · A2 trail · live gate · no re-entry | -5.8 | -3.7% | -66.6% | -13.0 / -10.5 / -8.9 | 444 | 0 |
| 190 | EPS & sales · breakouts only · original stop · live gate · early re-entry | -5.8 | 1.7% | -47.6% | -4.4 / -5.1 / -7.8 | 168 | 56 |
| 191 | live rules · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -5.9 | 0.3% | -60.5% | -11.2 / -9.3 / 0.6 | 497 | 49 |
| 192 | live rules · breakouts only · original stop + climax sell · live gate · no re-entry | -5.9 | 0.5% | -52.9% | -6.9 / -7.6 / -6.1 | 210 | 0 |
| 193 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -5.9 | 1.4% | -46.8% | -3.4 / -9.0 / -6.0 | 803 | 93 |
| 194 | live rules · breakouts + pullbacks · A2 trail · S&P above 200-day · early re-entry | -6.0 | 0.4% | -62.7% | -12.5 / -6.7 / -0.0 | 489 | 41 |
| 195 | live rules · breakouts only · original stop · live gate · early re-entry | -6.0 | 2.6% | -47.6% | -4.4 / -1.3 / -8.4 | 161 | 54 |
| 196 | leaders · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · early re-entry | -6.0 | -1.2% | -72.1% | -15.3 / -7.7 / -0.8 | 310 | 71 |
| 197 | EPS & sales · breakouts + pullbacks · A2 trail · live gate · no re-entry | -6.1 | -1.4% | -53.2% | -7.0 / -9.3 / -10.3 | 571 | 0 |
| 198 | EPS & sales · breakouts only · 50-day exit · half size if not UPTREND · early re-entry | -6.1 | 2.1% | -55.4% | -6.9 / -6.3 / -2.2 | 402 | 177 |
| 199 | live rules · breakouts + pullbacks · A2 trail · live gate · early re-entry | -6.2 | -3.7% | -65.8% | -14.2 / -11.0 / -7.0 | 536 | 60 |
| 200 | live rules · breakouts only · 50-day exit · half size if not UPTREND · early re-entry | -6.3 | 3.1% | -55.4% | -6.9 / -4.9 / -0.4 | 425 | 172 |
| 201 | trend template · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | -6.3 | 0.9% | -57.5% | -8.2 / -6.0 / -4.5 | 347 | 64 |
| 202 | leaders · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -6.3 | 0.8% | -51.2% | -4.1 / -10.0 / -6.0 | 558 | 0 |
| 203 | leaders · breakouts only · original stop + climax sell · live gate · no re-entry | -6.3 | -0.3% | -55.5% | -8.9 / -9.4 / -4.2 | 220 | 0 |
| 204 | EPS & sales · breakouts only · original stop · S&P above 200-day · early re-entry | -6.3 | 3.1% | -50.4% | -6.0 / -2.5 / -3.9 | 153 | 55 |
| 205 | EPS & sales · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -6.4 | -1.6% | -45.6% | -4.8 / -13.2 / -9.4 | 736 | 0 |
| 206 | EPS & sales · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -6.5 | 1.6% | -57.7% | -9.9 / -5.2 / -1.1 | 196 | 0 |
| 207 | trend template · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -6.6 | 0.6% | -58.0% | -9.5 / -6.5 / -3.2 | 300 | 53 |
| 208 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · early re-entry | -6.6 | -0.5% | -57.8% | -9.4 / -7.9 / -6.2 | 281 | 87 |
| 209 | EPS & sales · breakouts only · original stop + climax sell · live gate · early re-entry | -6.6 | 0.4% | -59.9% | -10.7 / -7.5 / -1.5 | 246 | 79 |
| 210 | trend template · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | -6.8 | -0.1% | -58.5% | -9.8 / -7.4 / -4.1 | 299 | 51 |
| 211 | leaders · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -6.8 | 0.6% | -64.4% | -10.3 / -6.8 / -2.6 | 310 | 60 |
| 212 | EPS & sales · breakouts only · A2 trail · live gate · no re-entry | -6.8 | 1.2% | -56.4% | -8.8 / -7.9 / -1.0 | 300 | 0 |
| 213 | EPS & sales · breakouts only · A2 trail · S&P above 200-day · no re-entry | -6.8 | 1.4% | -57.4% | -9.7 / -6.6 / -0.6 | 289 | 0 |
| 214 | live rules · breakouts + pullbacks · A2 trail · live gate · no re-entry | -6.9 | -1.6% | -53.2% | -7.0 / -10.8 / -9.4 | 498 | 0 |
| 215 | leaders · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -7.0 | -0.3% | -54.5% | -6.8 / -8.0 / -8.3 | 569 | 0 |
| 216 | leaders · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -7.1 | -1.9% | -60.9% | -9.3 / -9.5 / -9.2 | 457 | 0 |
| 217 | leaders · breakouts only · original stop · live gate · early re-entry | -7.1 | 1.6% | -49.7% | -3.5 / -7.6 / -6.9 | 172 | 55 |
| 218 | EPS & sales · breakouts + pullbacks · A2 trail · live gate · re-entry | -7.1 | -4.0% | -66.9% | -14.9 / -8.4 / -9.5 | 576 | 67 |
| 219 | EPS & sales · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -7.1 | -0.3% | -58.7% | -10.4 / -5.5 / -6.3 | 233 | 84 |
| 220 | trend template · breakouts only · A2 trail · live gate · early re-entry | -7.2 | 3.3% | -62.8% | -12.2 / 5.6 / -3.2 | 375 | 141 |
| 221 | leaders · breakouts only · 50-day exit · live gate · no re-entry | -7.2 | 0.5% | -53.5% | -7.9 / -11.9 / 0.3 | 292 | 0 |
| 222 | live rules · breakouts only · A2 trail · S&P above 200-day · no re-entry | -7.3 | 0.7% | -57.4% | -9.7 / -4.4 / -4.9 | 292 | 0 |
| 223 | live rules · breakouts only · 50-day exit · S&P above 200-day · re-entry | -7.3 | 1.7% | -54.9% | -7.6 / -6.1 / -2.5 | 351 | 133 |
| 224 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · early re-entry | -7.3 | 0.5% | -50.0% | -5.8 / -6.9 / -8.0 | 222 | 85 |
| 225 | leaders · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | -7.3 | 1.2% | -59.3% | -9.1 / -5.5 / -3.1 | 668 | 95 |
| 226 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -7.3 | 0.9% | -55.0% | -7.9 / -7.6 / -3.5 | 277 | 85 |
| 227 | EPS & sales · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -7.3 | 0.7% | -60.5% | -11.2 / -4.4 / -3.4 | 556 | 64 |
| 228 | live rules · breakouts only · 50-day exit · live gate · re-entry | -7.4 | 2.0% | -54.3% | -7.2 / -6.7 / -1.7 | 346 | 127 |
| 229 | leaders · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -7.4 | 1.7% | -55.2% | -7.1 / -5.6 / -4.1 | 687 | 106 |
| 230 | leaders · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -7.4 | -0.4% | -57.7% | -10.1 / -8.6 / -3.5 | 185 | 0 |
| 231 | trend template · breakouts only · A2 trail · live gate · re-entry | -7.5 | 3.3% | -61.5% | -11.5 / 5.3 / -3.7 | 374 | 136 |
| 232 | leaders · breakouts only · original stop · live gate · re-entry | -7.7 | 2.2% | -50.2% | -3.6 / -7.3 / -5.1 | 166 | 50 |
| 233 | live rules · breakouts only · A2 trail · live gate · no re-entry | -7.9 | 0.8% | -56.4% | -8.8 / -7.1 / -3.1 | 304 | 0 |
| 234 | leaders · breakouts only · original stop + climax sell · S&P above 200-day · early re-entry | -7.9 | -0.3% | -52.7% | -7.5 / -9.3 / -5.9 | 224 | 63 |
| 235 | leaders · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -8.0 | 1.3% | -64.1% | -9.6 / -7.4 / -0.0 | 316 | 0 |
| 236 | live rules · breakouts only · A2 trail · S&P above 200-day · early re-entry | -8.1 | 0.8% | -53.2% | -7.5 / -5.9 / -6.1 | 331 | 119 |
| 237 | leaders · breakouts only · 50-day exit · half size if not UPTREND · early re-entry | -8.1 | -1.6% | -64.5% | -13.2 / -8.9 / -3.6 | 414 | 147 |
| 238 | leaders · breakouts only · A2 trail · S&P above 200-day · no re-entry | -8.1 | -1.4% | -54.9% | -8.6 / -10.0 / -7.2 | 295 | 0 |
| 239 | leaders · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -8.2 | -0.7% | -63.6% | -12.6 / -8.3 / -1.9 | 407 | 147 |
| 240 | live rules · breakouts only · A2 trail · S&P above 200-day · re-entry | -8.4 | 0.1% | -55.3% | -8.6 / -6.6 / -6.2 | 342 | 128 |
| 241 | EPS & sales · breakouts only · A2 trail · half size if not UPTREND · early re-entry | -8.4 | -0.1% | -62.8% | -11.7 / -7.8 / -2.0 | 399 | 158 |
| 242 | live rules · breakouts only · 50-day exit · S&P above 200-day · early re-entry | -8.5 | 1.6% | -55.2% | -7.4 / -6.7 / -2.5 | 345 | 142 |
| 243 | leaders · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -8.6 | -1.9% | -56.8% | -8.3 / -12.0 / -7.6 | 543 | 0 |
| 244 | leaders · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | -8.6 | -0.4% | -54.0% | -5.8 / -8.7 / -9.1 | 292 | 54 |
| 245 | EPS & sales · breakouts only · A2 trail · S&P above 200-day · re-entry | -8.6 | 0.6% | -55.3% | -8.6 / -8.7 / -2.4 | 334 | 127 |
| 246 | leaders · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -8.8 | -0.9% | -52.9% | -4.9 / -9.3 / -11.0 | 298 | 0 |
| 247 | EPS & sales · breakouts only · 50-day exit · live gate · re-entry | -8.8 | 0.6% | -54.3% | -7.2 / -6.5 / -6.6 | 323 | 133 |
| 248 | EPS & sales · breakouts only · A2 trail · S&P above 200-day · early re-entry | -8.8 | 0.8% | -53.2% | -7.5 / -9.2 / -2.8 | 331 | 134 |
| 249 | EPS & sales · breakouts only · original stop + climax sell · live gate · re-entry | -9.0 | -0.5% | -61.5% | -11.6 / -5.6 / -5.3 | 246 | 83 |
| 250 | live rules · breakouts only · original stop + climax sell · live gate · early re-entry | -9.1 | -1.4% | -59.9% | -10.7 / -4.5 / -10.4 | 254 | 81 |
| 251 | live rules · breakouts only · A2 trail · half size if not UPTREND · early re-entry | -9.3 | -0.8% | -62.8% | -11.7 / -6.7 / -5.3 | 405 | 136 |
| 252 | leaders · breakouts only · 50-day exit · S&P above 200-day · re-entry | -9.3 | -2.3% | -59.4% | -11.0 / -11.3 / -6.2 | 310 | 113 |
| 253 | leaders · breakouts + pullbacks · A2 trail · live gate · no re-entry | -9.4 | -2.4% | -62.0% | -9.9 / -10.7 / -8.6 | 494 | 0 |
| 254 | live rules · breakouts only · original stop + climax sell · live gate · re-entry | -9.5 | -2.0% | -61.5% | -11.6 / -4.3 / -11.3 | 247 | 84 |
| 255 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -9.5 | -1.3% | -58.7% | -10.4 / -6.6 / -8.2 | 219 | 80 |
| 256 | leaders · breakouts only · A2 trail · half size if not UPTREND · early re-entry | -9.5 | -4.8% | -70.1% | -16.8 / -11.6 / -6.6 | 402 | 139 |
| 257 | EPS & sales · breakouts only · A2 trail · half size if not UPTREND · re-entry | -9.5 | -0.3% | -64.0% | -12.5 / -7.5 / -2.1 | 403 | 143 |
| 258 | leaders · breakouts only · A2 trail · live gate · no re-entry | -9.7 | -3.5% | -59.3% | -11.0 / -12.3 / -8.7 | 312 | 0 |
| 259 | EPS & sales · breakouts only · 50-day exit · live gate · early re-entry | -9.7 | -0.7% | -56.4% | -8.4 / -8.8 / -7.1 | 323 | 144 |
| 260 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · re-entry | -9.7 | 0.1% | -54.9% | -7.6 / -6.9 / -7.1 | 320 | 138 |
| 261 | leaders · breakouts only · original stop + climax sell · live gate · early re-entry | -9.8 | -3.7% | -59.0% | -10.8 / -10.7 / -11.7 | 234 | 67 |
| 262 | live rules · breakouts only · A2 trail · half size if not UPTREND · re-entry | -10.1 | -1.0% | -64.0% | -12.5 / -7.4 / -4.2 | 412 | 149 |
| 263 | live rules · breakouts only · 50-day exit · live gate · early re-entry | -10.4 | 1.4% | -56.4% | -8.4 / -7.0 / -1.7 | 345 | 141 |
| 264 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · early re-entry | -10.4 | 0.0% | -55.2% | -7.4 / -7.7 / -6.8 | 321 | 145 |
| 265 | EPS & sales · breakouts only · A2 trail · live gate · re-entry | -10.6 | -1.5% | -60.3% | -10.9 / -9.6 / -5.6 | 341 | 125 |
| 266 | leaders · breakouts + pullbacks · A2 trail · half size if not UPTREND · early re-entry | -10.8 | -2.9% | -61.3% | -10.6 / -11.6 / -8.1 | 545 | 82 |
| 267 | EPS & sales · breakouts only · A2 trail · live gate · early re-entry | -10.8 | -2.2% | -62.0% | -11.9 / -10.0 / -6.0 | 331 | 125 |
| 268 | leaders · breakouts only · A2 trail · half size if not UPTREND · re-entry | -10.9 | -5.1% | -69.3% | -16.2 / -11.4 / -8.4 | 405 | 136 |
| 269 | leaders · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -11.0 | -2.7% | -61.1% | -10.2 / -12.1 / -7.7 | 556 | 82 |
| 270 | leaders · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -11.1 | -3.0% | -61.7% | -12.4 / -11.1 / -6.6 | 211 | 56 |
| 271 | leaders · breakouts only · 50-day exit · live gate · re-entry | -11.4 | -2.8% | -62.2% | -12.6 / -12.6 / -4.2 | 315 | 112 |
| 272 | leaders · breakouts only · A2 trail · S&P above 200-day · re-entry | -11.6 | -5.7% | -65.6% | -14.3 / -12.7 / -11.3 | 314 | 110 |
| 273 | live rules · breakouts only · A2 trail · live gate · early re-entry | -11.8 | -2.8% | -62.0% | -11.9 / -7.9 / -10.0 | 348 | 120 |
| 274 | leaders · breakouts + pullbacks · A2 trail · live gate · early re-entry | -11.8 | -4.7% | -67.3% | -13.8 / -10.9 / -10.8 | 469 | 70 |
| 275 | leaders · breakouts only · original stop + climax sell · live gate · re-entry | -11.8 | -3.5% | -62.4% | -12.7 / -10.8 / -8.7 | 242 | 77 |
| 276 | leaders · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -12.0 | -3.5% | -60.8% | -11.0 / -11.0 / -10.2 | 552 | 78 |
| 277 | leaders · breakouts only · 50-day exit · live gate · early re-entry | -12.1 | -4.8% | -62.6% | -12.7 / -14.2 / -9.2 | 336 | 122 |
| 278 | live rules · breakouts only · A2 trail · live gate · re-entry | -12.2 | -2.1% | -60.3% | -10.9 / -7.6 / -9.3 | 365 | 133 |
| 279 | leaders · breakouts + pullbacks · 50-day exit · live gate · early re-entry | -12.3 | -7.1% | -70.3% | -17.0 / -12.9 / -12.3 | 461 | 66 |
| 280 | leaders · breakouts + pullbacks · A2 trail · S&P above 200-day · early re-entry | -12.5 | -6.0% | -75.1% | -19.1 / -9.4 / -9.5 | 457 | 81 |
| 281 | leaders · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | -12.5 | -2.5% | -60.5% | -10.9 / -10.6 / -7.7 | 530 | 73 |
| 282 | leaders · breakouts only · 50-day exit · S&P above 200-day · early re-entry | -12.9 | -5.0% | -64.8% | -14.2 / -12.4 / -9.4 | 298 | 108 |
| 283 | leaders · breakouts + pullbacks · 50-day exit · live gate · re-entry | -13.2 | -7.0% | -67.5% | -15.1 / -13.3 / -14.0 | 499 | 86 |
| 284 | leaders · breakouts only · A2 trail · S&P above 200-day · early re-entry | -13.3 | -4.9% | -66.0% | -14.5 / -12.8 / -8.4 | 298 | 104 |
| 285 | leaders · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -13.4 | -7.1% | -76.0% | -19.7 / -11.4 / -10.6 | 430 | 68 |
| 286 | leaders · breakouts only · A2 trail · live gate · early re-entry | -13.5 | -4.5% | -60.3% | -10.9 / -14.0 / -10.8 | 336 | 110 |
| 287 | leaders · breakouts only · A2 trail · live gate · re-entry | -13.8 | -5.9% | -63.5% | -13.1 / -13.7 / -12.9 | 342 | 113 |
| 288 | leaders · breakouts + pullbacks · A2 trail · live gate · re-entry | -14.5 | -5.7% | -66.3% | -12.8 / -13.1 / -13.1 | 471 | 67 |

_Sub-periods: 2005–2008 · 2009–2012 · 2013–2016. Tune vs SPY = median excess CAGR of 3 random same-day-order runs. Generated by scripts/backtest/run_round6.py._
