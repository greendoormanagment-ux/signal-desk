# Round 6 — best small combination of rules (2026-10-22)

**Data:** free (Yahoo, survivorship-limited) · 657 S&P 500 members (point in time) · cost 0.07% per side · idle money in SPY · signals at the close, filled next open.
**Periods:** TUNE 2017-10-15 → 2021-12-31 (used to choose) · JUDGE 2022-01-01 → 2025-12-31 (opened only for the top 3) · 2026 shown alone.

**Search:** 4 entry filters × 2 setup choices × 4 exits × 3 market rules × re-entry (off / standard / early) = 288 combinations. *Re-entry* = after any sale, buy back within 40 sessions if the stock closes above its high since the sale, above the 50-day, on 1.2× volume, not rated SELL, market not in CORRECTION (max 2 buy-backs in a row). *Early re-entry* = same, but the trigger is a close back above the 50-day that also tops the prior 10-day high (3+ sessions after the sale), so it can buy back below the sale price.

**Pass bar (raised because 288 combinations were tried):** beat SPY in tune AND judge, ≥ 80% of judge bootstrap resamples above zero, judge drawdown no worse than SPY's + 5 points.

> ⚠ **Free data:** failed/bought-out companies are missing, so stock picking is flattered. A pass here means 'worth the paid EODHD test', not proof.

**4 of 288 combinations beat SPY in the tune years.**

| SPY | CAGR | max drawdown |
| --- | --- | --- |
| tune | 15.9% | -34.1% |
| judge | 9.3% | -25.4% |
| 2026 | 16.7% | -9.1% |

## Top 3 (chosen on tune only) + the live system

| Combination | Rule changes | Tune vs SPY | Judge CAGR (vs SPY) | Judge range | Judge max DD | Bootstrap % | 2026 vs SPY | Passes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | 3 | 1.9 | **10.4% (1.1)** | 7.2 to 16.4 | -23.2% | 89.0 | -12.4 | ✅ |
| EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | 4 | 2.2 | **7.8% (-1.5)** | 4.5 to 10.6 | -23.2% | 61.0 | -16.8 | ✗ |
| EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | 4 | 0.3 | **9.9% (0.6)** | 7.8 to 12.1 | -22.7% | 81.0 | -17.3 | ✅ |
| live rules · breakouts + pullbacks · A2 trail · live gate · no re-entry **(live today)** | 0 | -14.3 | **6.8% (-2.5)** | 3.6 to 13.0 | -27.2% | 15.0 | -21.9 | – |

## Which single choices helped most (tune years, averaged over every combination that used them)

**Entry filter:** EPS & sales -4.8 (3/72 beat SPY) · live rules -6.7 (0/72 beat SPY) · leaders -8.0 (0/72 beat SPY) · trend template -8.2 (1/72 beat SPY)

**Setups:** breakouts + pullbacks -6.4 (3/144 beat SPY) · breakouts only -7.4 (1/144 beat SPY)

**Exit:** original stop + climax sell -5.5 (3/72 beat SPY) · 50-day exit -6.3 (0/72 beat SPY) · original stop -6.4 (1/72 beat SPY) · A2 trail -9.5 (0/72 beat SPY)

**Market rule:** half size if not UPTREND -6.5 (2/96 beat SPY) · S&P above 200-day -6.7 (1/96 beat SPY) · live gate -7.6 (1/96 beat SPY)

**Re-entry:** early re-entry -6.9 (2/96 beat SPY) · re-entry -6.9 (1/96 beat SPY) · no re-entry -7.0 (1/96 beat SPY)

**Re-entry effect by exit** (tune, minus no re-entry): A2 trail -0.3 · original stop +0.0 · 50-day exit +0.3 · original stop + climax sell +0.5

**Early re-entry effect by exit** (tune, minus no re-entry): A2 trail -0.0 · original stop -0.0 · 50-day exit -0.1 · original stop + climax sell +0.7

## All 288 on tune (best first)

| # | Combination | Tune vs SPY | Tune CAGR | Tune DD | Sub-periods vs SPY | Trades | Buy-backs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | 2.2 | 17.9% | -32.1% | -0.2 / 2.0 / 2.5 | 168 | 32 |
| 2 | EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | 1.9 | 15.5% | -29.9% | -5.2 / -0.3 / 4.4 | 160 | 29 |
| 3 | EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | 0.3 | 17.1% | -32.2% | 1.1 / 0.8 / -1.2 | 173 | 36 |
| 4 | trend template · breakouts only · original stop · S&P above 200-day · no re-entry | 0.1 | 15.2% | -31.5% | 1.2 / -6.0 / 8.4 | 51 | 0 |
| 5 | live rules · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | -0.1 | 12.4% | -34.6% | 4.5 / -6.0 / -11.5 | 319 | 43 |
| 6 | live rules · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -0.6 | 16.0% | -33.2% | 12.3 / -2.4 / -12.8 | 308 | 0 |
| 7 | leaders · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | -1.0 | 13.2% | -33.4% | 11.1 / -9.1 / -8.1 | 62 | 12 |
| 8 | EPS & sales · breakouts only · original stop + climax sell · live gate · re-entry | -1.1 | 15.0% | -33.8% | -1.0 / -9.1 / 17.8 | 102 | 33 |
| 9 | live rules · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -1.5 | 7.7% | -29.8% | -2.5 / -9.2 / -16.4 | 139 | 18 |
| 10 | EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -1.5 | 17.0% | -30.6% | -2.6 / 1.3 / 3.8 | 154 | 32 |
| 11 | leaders · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -1.7 | 13.3% | -33.4% | 11.1 / -8.9 / -8.1 | 61 | 11 |
| 12 | EPS & sales · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | -1.7 | 15.2% | -31.6% | -2.8 / 1.9 / -2.7 | 352 | 52 |
| 13 | EPS & sales · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -1.9 | 9.8% | -35.3% | -5.8 / -3.4 / -13.6 | 293 | 0 |
| 14 | live rules · breakouts only · 50-day exit · S&P above 200-day · re-entry | -2.1 | 10.6% | -33.7% | 5.6 / -12.2 / -7.0 | 173 | 60 |
| 15 | trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -2.1 | 14.1% | -32.6% | -7.8 / -0.4 / 6.6 | 122 | 0 |
| 16 | EPS & sales · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -2.1 | 14.6% | -31.9% | -1.2 / -0.5 / -3.3 | 354 | 51 |
| 17 | EPS & sales · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -2.1 | 15.3% | -37.2% | -0.4 / -9.1 / 18.2 | 95 | 27 |
| 18 | EPS & sales · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -2.2 | 12.0% | -35.4% | 3.2 / -5.3 / -11.9 | 95 | 23 |
| 19 | EPS & sales · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · early re-entry | -2.2 | 12.2% | -38.9% | -7.9 / -3.8 / 3.6 | 165 | 30 |
| 20 | EPS & sales · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -2.2 | 14.0% | -35.4% | -3.5 / -7.5 / 12.9 | 106 | 37 |
| 21 | EPS & sales · breakouts only · original stop + climax sell · S&P above 200-day · early re-entry | -2.3 | 14.1% | -36.9% | 0.3 / -6.9 / 5.6 | 101 | 30 |
| 22 | EPS & sales · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -2.5 | 14.1% | -33.4% | -2.5 / 0.3 / -5.3 | 320 | 0 |
| 23 | EPS & sales · breakouts only · original stop + climax sell · half size if not UPTREND · early re-entry | -2.5 | 13.8% | -35.2% | -2.9 / -6.9 / 9.9 | 111 | 41 |
| 24 | live rules · breakouts + pullbacks · 50-day exit · live gate · early re-entry | -2.6 | 14.4% | -31.7% | 3.8 / -1.9 / -10.3 | 293 | 39 |
| 25 | EPS & sales · breakouts + pullbacks · 50-day exit · live gate · early re-entry | -2.6 | 14.8% | -35.1% | -3.1 / 1.3 / -2.9 | 311 | 49 |
| 26 | EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -2.6 | 15.6% | -33.1% | 0.7 / 2.0 / -7.9 | 157 | 0 |
| 27 | live rules · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -2.7 | 7.5% | -33.9% | -2.9 / -12.4 / -7.5 | 113 | 19 |
| 28 | leaders · breakouts + pullbacks · original stop · half size if not UPTREND · early re-entry | -2.7 | 12.5% | -34.1% | 9.3 / -8.1 / -11.1 | 73 | 13 |
| 29 | leaders · breakouts only · 50-day exit · S&P above 200-day · re-entry | -2.7 | 13.1% | -34.1% | 4.2 / -9.7 / 0.1 | 183 | 56 |
| 30 | live rules · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -2.8 | 11.1% | -29.4% | -3.9 / -1.1 / -15.0 | 121 | 12 |
| 31 | leaders · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · early re-entry | -2.8 | 13.0% | -32.1% | 3.7 / -6.5 / -5.5 | 129 | 28 |
| 32 | EPS & sales · breakouts + pullbacks · A2 trail · live gate · early re-entry | -2.8 | 10.4% | -33.0% | -10.2 / 1.7 / -13.5 | 285 | 39 |
| 33 | EPS & sales · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -2.8 | 15.0% | -32.6% | 0.9 / -1.2 / -3.7 | 352 | 0 |
| 34 | leaders · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -2.9 | 12.3% | -34.1% | 9.3 / -8.0 / -12.1 | 72 | 13 |
| 35 | EPS & sales · breakouts only · original stop + climax sell · live gate · early re-entry | -2.9 | 13.5% | -33.5% | 0.3 / -8.1 / 5.4 | 108 | 37 |
| 36 | live rules · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -3.0 | 12.5% | -34.6% | 4.3 / -5.9 / -11.3 | 322 | 44 |
| 37 | EPS & sales · breakouts + pullbacks · 50-day exit · live gate · re-entry | -3.0 | 13.9% | -34.9% | -3.2 / -0.1 / -4.2 | 313 | 43 |
| 38 | live rules · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -3.2 | 14.4% | -32.3% | 8.5 / -5.8 / -7.8 | 330 | 0 |
| 39 | EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -3.2 | 14.7% | -34.2% | -1.0 / -1.3 / -3.5 | 144 | 0 |
| 40 | live rules · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -3.4 | 17.1% | -32.8% | 10.7 / -2.7 / -5.1 | 283 | 0 |
| 41 | live rules · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | -3.4 | 16.3% | -30.8% | 5.2 / 1.5 / -10.6 | 343 | 45 |
| 42 | live rules · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -3.5 | 13.9% | -30.9% | -1.7 / -5.7 / 5.6 | 120 | 0 |
| 43 | leaders · breakouts only · 50-day exit · half size if not UPTREND · early re-entry | -3.5 | 14.0% | -33.2% | 2.7 / -9.6 / 6.6 | 196 | 74 |
| 44 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -3.7 | 6.5% | -35.0% | -2.8 / -9.1 / -18.9 | 88 | 16 |
| 45 | leaders · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -3.7 | 10.4% | -35.3% | 4.3 / -10.4 / -10.8 | 149 | 35 |
| 46 | live rules · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -3.8 | 9.6% | -31.0% | -3.0 / -12.4 / -0.3 | 139 | 0 |
| 47 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | -3.8 | 7.6% | -33.9% | -2.6 / -7.1 / -18.4 | 77 | 0 |
| 48 | leaders · breakouts only · 50-day exit · S&P above 200-day · early re-entry | -3.8 | 13.6% | -33.0% | 2.0 / -8.9 / 4.3 | 183 | 57 |
| 49 | EPS & sales · breakouts + pullbacks · A2 trail · half size if not UPTREND · early re-entry | -3.8 | 8.9% | -34.2% | -8.7 / -1.1 / -17.1 | 309 | 41 |
| 50 | EPS & sales · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -3.8 | 10.4% | -34.2% | -8.2 / -2.5 / -7.7 | 346 | 0 |
| 51 | EPS & sales · breakouts only · 50-day exit · live gate · re-entry | -3.8 | 9.2% | -35.4% | 0.0 / -5.1 / -20.8 | 143 | 51 |
| 52 | EPS & sales · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -3.9 | 12.3% | -34.6% | -9.6 / -5.1 / 9.5 | 88 | 0 |
| 53 | live rules · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | -4.0 | 11.1% | -28.9% | -1.1 / -8.0 / -5.1 | 141 | 16 |
| 54 | EPS & sales · breakouts only · 50-day exit · half size if not UPTREND · early re-entry | -4.0 | 11.3% | -35.9% | -3.4 / -3.8 / -9.3 | 165 | 63 |
| 55 | leaders · breakouts + pullbacks · original stop · live gate · re-entry | -4.1 | 13.1% | -34.2% | 11.1 / -5.9 / -15.7 | 61 | 10 |
| 56 | EPS & sales · breakouts only · original stop + climax sell · live gate · no re-entry | -4.1 | 11.8% | -34.6% | -10.4 / -5.6 / 9.6 | 87 | 0 |
| 57 | trend template · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -4.2 | 4.4% | -33.9% | -2.5 / -16.2 / -16.7 | 144 | 29 |
| 58 | EPS & sales · breakouts + pullbacks · original stop · live gate · re-entry | -4.2 | 12.5% | -36.2% | 1.0 / -3.3 / -10.3 | 78 | 13 |
| 59 | trend template · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -4.3 | 9.0% | -31.5% | -0.8 / -7.3 / -14.5 | 83 | 14 |
| 60 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -4.3 | 11.3% | -33.0% | -1.6 / -8.7 / 0.2 | 82 | 0 |
| 61 | leaders · breakouts + pullbacks · original stop · live gate · no re-entry | -4.3 | 12.6% | -31.8% | 6.7 / -2.5 / -19.3 | 73 | 0 |
| 62 | leaders · breakouts + pullbacks · original stop · live gate · early re-entry | -4.3 | 12.4% | -34.2% | 11.1 / -6.1 / -18.1 | 60 | 10 |
| 63 | EPS & sales · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -4.3 | 11.5% | -35.7% | 3.4 / -5.4 / -14.7 | 93 | 0 |
| 64 | live rules · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -4.4 | 12.4% | -31.6% | -1.7 / 0.6 / -15.3 | 264 | 29 |
| 65 | EPS & sales · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -4.5 | 11.0% | -35.9% | -3.2 / -4.0 / -10.5 | 162 | 57 |
| 66 | live rules · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | -4.6 | 15.6% | -28.9% | -2.1 / 0.7 / -1.5 | 123 | 12 |
| 67 | leaders · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -4.6 | 10.3% | -35.3% | 2.0 / -10.3 / -7.3 | 161 | 38 |
| 68 | leaders · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -4.6 | 11.9% | -34.9% | 1.5 / -12.2 / 3.5 | 174 | 0 |
| 69 | EPS & sales · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -4.7 | 11.1% | -36.1% | -8.1 / -5.4 / 1.8 | 91 | 0 |
| 70 | leaders · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | -4.8 | 9.4% | -35.7% | 2.1 / -12.2 / -7.6 | 153 | 34 |
| 71 | live rules · breakouts + pullbacks · original stop · live gate · no re-entry | -4.9 | 10.3% | -32.7% | -1.2 / -4.8 / -14.4 | 75 | 0 |
| 72 | live rules · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -4.9 | 15.5% | -29.4% | -0.2 / -5.2 / 7.4 | 118 | 0 |
| 73 | leaders · breakouts only · original stop + climax sell · S&P above 200-day · early re-entry | -4.9 | 10.7% | -32.0% | -3.5 / -6.7 / -5.0 | 98 | 17 |
| 74 | trend template · breakouts only · original stop · live gate · no re-entry | -5.0 | 9.3% | -33.5% | 1.7 / -15.3 / 0.6 | 57 | 0 |
| 75 | trend template · breakouts only · original stop · S&P above 200-day · early re-entry | -5.0 | 9.7% | -34.6% | -0.5 / -12.5 / -0.3 | 58 | 16 |
| 76 | leaders · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | -5.0 | 11.3% | -36.0% | 4.2 / -11.3 / -4.9 | 145 | 32 |
| 77 | leaders · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -5.1 | 10.5% | -34.4% | 3.8 / -9.6 / -10.3 | 130 | 29 |
| 78 | EPS & sales · breakouts only · original stop · S&P above 200-day · no re-entry | -5.1 | 9.8% | -37.2% | -2.7 / -8.0 / -8.9 | 56 | 0 |
| 79 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · early re-entry | -5.2 | 10.1% | -33.2% | -2.4 / -10.5 / -0.2 | 94 | 22 |
| 80 | EPS & sales · breakouts only · 50-day exit · live gate · early re-entry | -5.2 | 9.4% | -35.4% | -0.4 / -5.3 / -19.1 | 147 | 57 |
| 81 | live rules · breakouts + pullbacks · original stop · live gate · early re-entry | -5.3 | 9.1% | -33.3% | -5.3 / -8.3 / -5.6 | 85 | 11 |
| 82 | leaders · breakouts only · 50-day exit · live gate · early re-entry | -5.3 | 9.9% | -33.3% | 3.9 / -16.1 / 1.7 | 176 | 69 |
| 83 | EPS & sales · breakouts + pullbacks · original stop · live gate · no re-entry | -5.3 | 9.6% | -38.7% | 0.8 / -8.0 / -14.3 | 79 | 0 |
| 84 | EPS & sales · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -5.3 | 10.7% | -36.0% | -0.8 / -3.7 / -15.3 | 139 | 0 |
| 85 | EPS & sales · breakouts only · original stop · half size if not UPTREND · early re-entry | -5.3 | 10.1% | -36.0% | -5.1 / -5.4 / -9.1 | 77 | 28 |
| 86 | leaders · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -5.4 | 11.2% | -36.7% | -0.5 / -12.3 / 4.1 | 307 | 0 |
| 87 | leaders · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -5.4 | 10.0% | -33.3% | -4.8 / -8.2 / -2.5 | 93 | 0 |
| 88 | EPS & sales · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | -5.4 | 12.1% | -32.6% | -6.0 / -2.3 / -4.0 | 334 | 39 |
| 89 | live rules · breakouts + pullbacks · 50-day exit · live gate · re-entry | -5.5 | 15.3% | -30.6% | 3.8 / 0.2 / -9.7 | 287 | 36 |
| 90 | leaders · breakouts only · 50-day exit · live gate · no re-entry | -5.5 | 12.1% | -35.9% | 2.7 / -13.4 / 6.2 | 160 | 0 |
| 91 | leaders · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -5.5 | 10.1% | -33.1% | -4.0 / -7.6 / -5.1 | 96 | 17 |
| 92 | EPS & sales · breakouts + pullbacks · original stop · half size if not UPTREND · early re-entry | -5.5 | 11.2% | -35.4% | 3.3 / -7.6 / -10.7 | 94 | 22 |
| 93 | EPS & sales · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -5.5 | 11.7% | -37.2% | -4.5 / -4.0 / -3.9 | 160 | 34 |
| 94 | EPS & sales · breakouts only · original stop · S&P above 200-day · early re-entry | -5.5 | 10.4% | -34.9% | -2.7 / -8.2 / -5.2 | 63 | 19 |
| 95 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | -5.6 | 7.4% | -35.0% | -2.8 / -8.7 / -16.1 | 87 | 17 |
| 96 | trend template · breakouts + pullbacks · original stop + climax sell · live gate · early re-entry | -5.6 | 3.6% | -34.3% | -6.9 / -14.3 / -17.7 | 138 | 23 |
| 97 | trend template · breakouts only · original stop · half size if not UPTREND · re-entry | -5.6 | 9.1% | -36.1% | -1.2 / -15.2 / 3.6 | 82 | 42 |
| 98 | leaders · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -5.6 | 9.3% | -33.2% | 7.0 / -10.5 / -17.5 | 81 | 0 |
| 99 | leaders · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -5.7 | 13.7% | -31.9% | 7.4 / -4.1 / -11.4 | 132 | 0 |
| 100 | leaders · breakouts only · 50-day exit · live gate · re-entry | -5.7 | 10.0% | -33.6% | 0.2 / -13.9 / 2.6 | 176 | 64 |
| 101 | EPS & sales · breakouts only · A2 trail · half size if not UPTREND · early re-entry | -5.7 | 10.2% | -34.4% | -4.1 / -5.2 / -10.2 | 163 | 56 |
| 102 | EPS & sales · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -5.7 | 9.9% | -36.4% | -3.5 / -4.5 / -13.9 | 132 | 0 |
| 103 | live rules · breakouts only · original stop · half size if not UPTREND · re-entry | -5.8 | 6.3% | -34.8% | 0.7 / -17.8 / -6.0 | 85 | 41 |
| 104 | live rules · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -5.8 | 8.0% | -34.6% | 0.2 / -16.1 / -1.9 | 169 | 0 |
| 105 | trend template · breakouts only · original stop · half size if not UPTREND · early re-entry | -5.8 | 7.8% | -38.4% | -1.4 / -18.5 / 5.3 | 82 | 43 |
| 106 | EPS & sales · breakouts only · A2 trail · S&P above 200-day · no re-entry | -5.8 | 10.9% | -33.7% | -0.2 / -3.2 / -16.2 | 125 | 0 |
| 107 | live rules · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -5.9 | 14.8% | -30.8% | 5.1 / -1.6 / -9.8 | 346 | 45 |
| 108 | live rules · breakouts + pullbacks · A2 trail · S&P above 200-day · early re-entry | -5.9 | 15.2% | -30.4% | 2.9 / 2.8 / -14.3 | 253 | 30 |
| 109 | trend template · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -5.9 | 8.9% | -33.4% | -3.0 / -11.2 / -3.6 | 200 | 83 |
| 110 | EPS & sales · breakouts only · original stop · live gate · early re-entry | -5.9 | 9.4% | -35.9% | -3.3 / -10.1 / -4.9 | 69 | 24 |
| 111 | leaders · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -6.0 | 10.0% | -37.9% | 5.4 / -10.4 / -12.9 | 140 | 0 |
| 112 | live rules · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -6.1 | 8.8% | -32.4% | -1.8 / -6.2 / -16.9 | 86 | 0 |
| 113 | live rules · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -6.1 | 8.5% | -34.1% | -4.2 / -11.0 / -4.2 | 202 | 76 |
| 114 | trend template · breakouts only · original stop · half size if not UPTREND · no re-entry | -6.1 | 7.9% | -34.4% | 0.3 / -17.5 / 0.7 | 75 | 0 |
| 115 | EPS & sales · breakouts + pullbacks · original stop · live gate · early re-entry | -6.1 | 11.3% | -36.2% | 1.0 / -6.8 / -8.8 | 82 | 11 |
| 116 | EPS & sales · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -6.1 | 10.9% | -34.0% | -8.7 / 2.2 / -14.2 | 304 | 40 |
| 117 | EPS & sales · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -6.1 | 13.6% | -33.4% | -3.5 / 1.7 / -9.7 | 151 | 0 |
| 118 | EPS & sales · breakouts only · original stop · S&P above 200-day · re-entry | -6.1 | 9.7% | -35.0% | -2.7 / -10.5 / -3.2 | 63 | 18 |
| 119 | EPS & sales · breakouts + pullbacks · A2 trail · live gate · no re-entry | -6.2 | 7.5% | -34.9% | -10.5 / -3.0 / -17.7 | 275 | 0 |
| 120 | EPS & sales · breakouts only · A2 trail · live gate · no re-entry | -6.2 | 9.9% | -35.0% | -0.9 / -3.6 / -18.7 | 125 | 0 |
| 121 | EPS & sales · breakouts only · original stop · live gate · re-entry | -6.2 | 9.5% | -36.0% | -3.3 / -9.9 / -5.0 | 69 | 24 |
| 122 | EPS & sales · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -6.3 | 12.0% | -33.1% | -6.0 / -2.4 / -4.1 | 333 | 41 |
| 123 | EPS & sales · breakouts only · original stop · half size if not UPTREND · re-entry | -6.3 | 9.4% | -36.1% | -5.1 / -7.3 / -8.3 | 78 | 28 |
| 124 | live rules · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · early re-entry | -6.4 | 9.4% | -34.2% | -1.2 / -10.9 / -4.0 | 113 | 17 |
| 125 | live rules · breakouts only · original stop + climax sell · half size if not UPTREND · early re-entry | -6.4 | 7.1% | -32.6% | -2.3 / -15.3 / -4.9 | 114 | 53 |
| 126 | live rules · breakouts only · original stop · S&P above 200-day · no re-entry | -6.4 | 8.1% | -36.4% | 1.1 / -17.7 / 1.3 | 63 | 0 |
| 127 | leaders · breakouts + pullbacks · 50-day exit · live gate · early re-entry | -6.4 | 8.5% | -38.1% | -3.3 / -8.3 / -14.1 | 262 | 38 |
| 128 | leaders · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -6.4 | 12.7% | -34.2% | -0.9 / -9.8 / 6.5 | 200 | 74 |
| 129 | leaders · breakouts only · original stop · S&P above 200-day · early re-entry | -6.4 | 9.5% | -35.6% | -4.0 / -8.6 / -4.8 | 57 | 9 |
| 130 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · re-entry | -6.4 | 7.1% | -35.3% | -4.0 / -6.9 / -20.7 | 148 | 53 |
| 131 | live rules · breakouts only · original stop · S&P above 200-day · early re-entry | -6.5 | 7.1% | -35.9% | 0.0 / -15.2 / -7.9 | 70 | 21 |
| 132 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | -6.5 | 12.8% | -37.4% | 0.0 / -4.7 / -4.3 | 88 | 0 |
| 133 | trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · early re-entry | -6.6 | 5.8% | -34.9% | -6.5 / -9.3 / -16.4 | 122 | 27 |
| 134 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · early re-entry | -6.6 | 8.7% | -35.3% | -2.6 / -6.0 / -17.7 | 150 | 55 |
| 135 | live rules · breakouts + pullbacks · original stop · half size if not UPTREND · early re-entry | -6.7 | 9.1% | -30.7% | -3.1 / -9.0 / -7.0 | 99 | 11 |
| 136 | live rules · breakouts only · 50-day exit · half size if not UPTREND · early re-entry | -6.7 | 9.2% | -33.7% | -4.4 / -13.0 / 3.9 | 196 | 81 |
| 137 | trend template · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -6.7 | 6.9% | -29.7% | -1.0 / -11.8 / -14.4 | 84 | 0 |
| 138 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · early re-entry | -6.7 | 8.4% | -34.4% | -4.0 / -15.5 / 5.0 | 120 | 53 |
| 139 | EPS & sales · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -6.7 | 4.9% | -40.1% | -14.7 / -3.6 / -20.9 | 296 | 35 |
| 140 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -6.8 | 11.0% | -31.1% | -0.1 / -10.5 / 1.0 | 84 | 0 |
| 141 | trend template · breakouts only · original stop · live gate · early re-entry | -6.8 | 6.2% | -39.9% | -3.4 / -18.3 / 0.0 | 77 | 42 |
| 142 | leaders · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -6.8 | 10.6% | -35.8% | -2.0 / -13.1 / 5.7 | 166 | 0 |
| 143 | live rules · breakouts only · original stop · S&P above 200-day · re-entry | -6.9 | 7.1% | -35.7% | 0.0 / -15.0 / -7.9 | 70 | 21 |
| 144 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -6.9 | 9.1% | -33.7% | 1.5 / -8.7 / -14.8 | 348 | 58 |
| 145 | trend template · breakouts only · original stop · live gate · re-entry | -6.9 | 8.0% | -35.9% | -3.1 / -15.3 / 1.4 | 69 | 36 |
| 146 | leaders · breakouts + pullbacks · 50-day exit · live gate · re-entry | -6.9 | 7.4% | -38.7% | -1.6 / -8.7 / -20.5 | 263 | 36 |
| 147 | leaders · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | -7.0 | 8.4% | -34.7% | 10.2 / -12.2 / -21.5 | 74 | 0 |
| 148 | live rules · breakouts only · 50-day exit · live gate · re-entry | -7.1 | 7.2% | -33.7% | -4.9 / -10.8 / -9.8 | 183 | 70 |
| 149 | trend template · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -7.1 | 8.5% | -35.2% | -3.0 / -7.7 / -14.3 | 296 | 37 |
| 150 | trend template · breakouts + pullbacks · original stop · half size if not UPTREND · early re-entry | -7.1 | 8.2% | -31.5% | -0.8 / -8.4 / -16.2 | 85 | 14 |
| 151 | EPS & sales · breakouts only · A2 trail · half size if not UPTREND · re-entry | -7.1 | 8.8% | -34.7% | -4.3 / -6.5 / -13.3 | 174 | 61 |
| 152 | live rules · breakouts only · A2 trail · S&P above 200-day · early re-entry | -7.2 | 5.3% | -33.1% | -1.0 / -13.0 / -19.0 | 167 | 48 |
| 153 | trend template · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -7.2 | 6.5% | -36.0% | -7.5 / -13.6 / -5.2 | 124 | 0 |
| 154 | leaders · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -7.2 | 8.9% | -39.9% | 2.7 / -12.0 / -12.7 | 300 | 50 |
| 155 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | -7.2 | 8.8% | -39.0% | -0.4 / -9.1 / -12.6 | 97 | 16 |
| 156 | EPS & sales · breakouts only · A2 trail · live gate · early re-entry | -7.2 | 8.5% | -33.9% | -6.0 / -5.3 / -14.7 | 151 | 52 |
| 157 | EPS & sales · breakouts only · 50-day exit · live gate · no re-entry | -7.2 | 8.2% | -36.0% | -6.5 / -6.1 / -14.1 | 121 | 0 |
| 158 | EPS & sales · breakouts only · A2 trail · S&P above 200-day · early re-entry | -7.3 | 8.4% | -33.1% | -8.6 / -3.2 / -15.2 | 153 | 56 |
| 159 | live rules · breakouts + pullbacks · A2 trail · half size if not UPTREND · early re-entry | -7.4 | 14.8% | -32.1% | 3.2 / -2.5 / -5.4 | 310 | 36 |
| 160 | live rules · breakouts only · original stop · half size if not UPTREND · no re-entry | -7.4 | 7.5% | -37.0% | 0.6 / -17.3 / -1.8 | 73 | 0 |
| 161 | live rules · breakouts only · 50-day exit · S&P above 200-day · early re-entry | -7.4 | 11.2% | -31.8% | 5.1 / -11.2 / -5.4 | 168 | 56 |
| 162 | trend template · breakouts + pullbacks · original stop · live gate · re-entry | -7.4 | 6.0% | -29.6% | -3.3 / -10.4 / -18.1 | 78 | 9 |
| 163 | trend template · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | -7.4 | 6.0% | -31.3% | -3.3 / -9.6 / -19.3 | 77 | 0 |
| 164 | trend template · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -7.4 | 6.7% | -28.2% | -4.0 / -7.7 / -19.4 | 73 | 10 |
| 165 | trend template · breakouts only · original stop · S&P above 200-day · re-entry | -7.4 | 8.7% | -35.6% | -0.9 / -14.4 / -0.3 | 59 | 16 |
| 166 | live rules · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -7.5 | 5.9% | -32.1% | -2.2 / -16.5 / -7.7 | 114 | 46 |
| 167 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · early re-entry | -7.5 | 7.8% | -33.4% | -2.3 / -11.7 / -9.8 | 98 | 19 |
| 168 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -7.5 | 10.7% | -34.1% | 3.7 / -9.8 / -9.3 | 352 | 0 |
| 169 | trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -7.5 | 6.2% | -35.8% | -6.3 / -10.1 / -13.0 | 122 | 26 |
| 170 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -7.6 | 8.8% | -39.0% | -0.4 / -9.1 / -12.6 | 97 | 16 |
| 171 | EPS & sales · breakouts only · original stop · live gate · no re-entry | -7.6 | 8.0% | -38.2% | -3.1 / -9.5 / -13.0 | 60 | 0 |
| 172 | live rules · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -7.7 | 9.0% | -33.9% | -0.9 / -14.1 / 0.3 | 91 | 0 |
| 173 | trend template · breakouts + pullbacks · original stop · live gate · early re-entry | -7.7 | 6.0% | -29.6% | -3.3 / -10.4 / -18.1 | 78 | 9 |
| 174 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -7.7 | 9.2% | -34.0% | -2.1 / -13.3 / 0.3 | 99 | 0 |
| 175 | leaders · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -7.7 | 11.5% | -37.5% | -3.1 / -9.9 / 3.9 | 266 | 0 |
| 176 | live rules · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -7.8 | 11.2% | -32.6% | 1.6 / -0.9 / -22.6 | 255 | 0 |
| 177 | live rules · breakouts only · original stop · live gate · re-entry | -7.8 | 6.0% | -34.9% | 0.2 / -18.0 / -6.2 | 80 | 40 |
| 178 | trend template · breakouts only · original stop + climax sell · live gate · no re-entry | -7.8 | 8.4% | -33.4% | -4.4 / -13.2 / 0.3 | 89 | 0 |
| 179 | trend template · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -7.8 | 7.0% | -34.3% | 0.6 / -16.2 / -6.7 | 162 | 0 |
| 180 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -7.8 | 8.1% | -36.0% | -7.8 / -6.6 / -11.3 | 121 | 0 |
| 181 | live rules · breakouts only · original stop · live gate · no re-entry | -7.9 | 7.6% | -36.9% | 1.9 / -18.6 / -0.7 | 65 | 0 |
| 182 | trend template · breakouts + pullbacks · A2 trail · live gate · re-entry | -7.9 | 8.9% | -34.1% | -5.2 / -5.2 / -15.3 | 265 | 24 |
| 183 | trend template · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -7.9 | 6.7% | -35.7% | -2.7 / -10.9 / -16.1 | 289 | 0 |
| 184 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -7.9 | 8.8% | -34.3% | -2.0 / -12.4 / -2.7 | 91 | 17 |
| 185 | leaders · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -7.9 | 11.6% | -36.7% | 3.6 / -8.9 / -6.6 | 154 | 0 |
| 186 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -8.0 | 7.7% | -33.9% | -2.0 / -12.7 / -8.4 | 95 | 20 |
| 187 | trend template · breakouts + pullbacks · original stop · S&P above 200-day · early re-entry | -8.0 | 6.8% | -28.0% | -4.0 / -7.5 / -19.4 | 71 | 12 |
| 188 | trend template · breakouts only · 50-day exit · half size if not UPTREND · early re-entry | -8.0 | 6.9% | -33.6% | -4.7 / -13.6 / -5.4 | 204 | 94 |
| 189 | leaders · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | -8.0 | 9.9% | -40.0% | 0.2 / -11.9 / -4.6 | 301 | 46 |
| 190 | EPS & sales · breakouts only · original stop · half size if not UPTREND · no re-entry | -8.0 | 7.5% | -36.0% | -4.7 / -6.8 / -18.7 | 72 | 0 |
| 191 | EPS & sales · breakouts only · A2 trail · S&P above 200-day · re-entry | -8.0 | 8.1% | -32.9% | -5.2 / -5.0 / -17.6 | 154 | 55 |
| 192 | live rules · breakouts only · original stop + climax sell · live gate · re-entry | -8.1 | 5.6% | -29.7% | -2.2 / -16.6 / -8.9 | 111 | 44 |
| 193 | leaders · breakouts only · original stop · half size if not UPTREND · no re-entry | -8.1 | 8.0% | -34.7% | -3.4 / -10.8 / -10.1 | 87 | 0 |
| 194 | live rules · breakouts only · 50-day exit · live gate · no re-entry | -8.2 | 5.2% | -38.6% | -2.0 / -18.5 / -7.3 | 152 | 0 |
| 195 | live rules · breakouts only · A2 trail · S&P above 200-day · re-entry | -8.2 | 4.5% | -34.1% | -1.9 / -15.5 / -16.4 | 189 | 57 |
| 196 | trend template · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -8.2 | 6.5% | -35.3% | -5.2 / -14.1 / -8.0 | 138 | 0 |
| 197 | trend template · breakouts only · A2 trail · half size if not UPTREND · re-entry | -8.2 | 4.8% | -35.6% | -2.8 / -14.8 / -15.5 | 204 | 72 |
| 198 | leaders · breakouts only · A2 trail · S&P above 200-day · re-entry | -8.2 | 7.6% | -33.0% | -1.8 / -9.5 / -15.6 | 197 | 56 |
| 199 | EPS & sales · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -8.2 | 4.6% | -39.2% | -15.3 / -6.7 / -15.5 | 282 | 0 |
| 200 | live rules · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -8.3 | 8.6% | -30.7% | -3.1 / -8.2 / -10.6 | 100 | 14 |
| 201 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -8.3 | 8.4% | -35.1% | 7.1 / -15.1 / -13.1 | 319 | 0 |
| 202 | trend template · breakouts only · A2 trail · half size if not UPTREND · early re-entry | -8.3 | 6.2% | -35.8% | -2.6 / -14.3 / -11.0 | 193 | 70 |
| 203 | live rules · breakouts only · 50-day exit · live gate · early re-entry | -8.4 | 7.4% | -32.2% | 0.0 / -15.2 / -6.6 | 184 | 75 |
| 204 | leaders · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -8.4 | 7.7% | -34.3% | 2.2 / -13.1 / -14.5 | 271 | 0 |
| 205 | EPS & sales · breakouts + pullbacks · A2 trail · live gate · re-entry | -8.4 | 10.1% | -33.8% | -9.6 / 3.1 / -18.1 | 282 | 33 |
| 206 | live rules · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -8.5 | 5.2% | -38.5% | -3.0 / -19.5 / -3.3 | 158 | 0 |
| 207 | trend template · breakouts only · original stop + climax sell · live gate · re-entry | -8.5 | 10.1% | -33.9% | -5.5 / -12.3 / 8.7 | 117 | 46 |
| 208 | live rules · breakouts only · original stop + climax sell · live gate · early re-entry | -8.6 | 5.3% | -32.8% | -2.3 / -20.0 / -2.6 | 106 | 50 |
| 209 | trend template · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -8.6 | 3.4% | -34.7% | -3.1 / -12.9 / -26.4 | 256 | 0 |
| 210 | trend template · breakouts only · 50-day exit · live gate · re-entry | -8.6 | 5.6% | -35.6% | -8.9 / -11.8 / -8.8 | 178 | 72 |
| 211 | live rules · breakouts only · A2 trail · half size if not UPTREND · early re-entry | -8.7 | 2.3% | -37.6% | -2.2 / -21.5 / -13.6 | 202 | 75 |
| 212 | live rules · breakouts only · original stop · half size if not UPTREND · early re-entry | -8.7 | 7.4% | -35.2% | 0.7 / -17.0 / -3.2 | 81 | 42 |
| 213 | live rules · breakouts + pullbacks · A2 trail · live gate · early re-entry | -8.8 | 15.0% | -32.1% | 3.4 / -0.4 / -9.7 | 278 | 29 |
| 214 | live rules · breakouts only · original stop + climax sell · live gate · no re-entry | -8.8 | 7.7% | -32.7% | -2.3 / -16.3 / 1.5 | 89 | 0 |
| 215 | trend template · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · early re-entry | -8.8 | 2.9% | -34.3% | -2.6 / -17.1 / -21.5 | 147 | 30 |
| 216 | trend template · breakouts only · original stop + climax sell · live gate · early re-entry | -8.9 | 7.6% | -36.7% | -5.8 / -17.8 / 9.7 | 107 | 47 |
| 217 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -8.9 | 8.7% | -34.0% | -3.8 / -13.3 / 1.0 | 125 | 48 |
| 218 | leaders · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -8.9 | 5.8% | -35.4% | 0.9 / -15.7 / -16.3 | 194 | 0 |
| 219 | leaders · breakouts only · A2 trail · S&P above 200-day · no re-entry | -8.9 | 9.1% | -35.5% | 0.5 / -7.7 / -16.4 | 176 | 0 |
| 220 | trend template · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -9.1 | 5.5% | -36.3% | 0.9 / -17.6 / -12.1 | 161 | 0 |
| 221 | leaders · breakouts only · original stop · S&P above 200-day · re-entry | -9.1 | 8.6% | -35.8% | -5.3 / -9.8 / -4.8 | 59 | 10 |
| 222 | EPS & sales · breakouts only · A2 trail · live gate · re-entry | -9.1 | 6.6% | -34.0% | -6.9 / -6.3 / -19.2 | 155 | 54 |
| 223 | live rules · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -9.3 | 9.4% | -34.1% | -3.5 / -6.4 / -12.2 | 318 | 0 |
| 224 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · early re-entry | -9.3 | 9.8% | -34.1% | -0.2 / -9.3 / -7.8 | 349 | 63 |
| 225 | leaders · breakouts only · original stop · half size if not UPTREND · early re-entry | -9.3 | 7.5% | -35.6% | -5.2 / -17.6 / 8.5 | 83 | 34 |
| 226 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -9.3 | 7.4% | -33.5% | -3.7 / -11.1 / -11.6 | 119 | 0 |
| 227 | leaders · breakouts only · original stop · S&P above 200-day · no re-entry | -9.3 | 8.9% | -33.8% | -4.1 / -7.1 / -10.6 | 62 | 0 |
| 228 | live rules · breakouts + pullbacks · original stop · live gate · re-entry | -9.4 | 8.8% | -33.3% | -5.3 / -8.1 / -7.4 | 88 | 13 |
| 229 | trend template · breakouts + pullbacks · original stop · live gate · no re-entry | -9.4 | 6.6% | -31.6% | -2.9 / -12.4 / -12.2 | 73 | 0 |
| 230 | leaders · breakouts only · original stop + climax sell · live gate · no re-entry | -9.4 | 6.8% | -32.7% | -7.5 / -12.0 / -5.0 | 103 | 0 |
| 231 | trend template · breakouts only · 50-day exit · live gate · no re-entry | -9.5 | 5.4% | -35.2% | -0.2 / -17.0 / -11.4 | 146 | 0 |
| 232 | leaders · breakouts only · A2 trail · half size if not UPTREND · re-entry | -9.5 | 4.1% | -34.1% | -1.7 / -17.5 / -16.1 | 224 | 72 |
| 233 | live rules · breakouts only · A2 trail · live gate · early re-entry | -9.6 | 0.8% | -35.8% | -3.0 / -20.7 / -21.0 | 180 | 66 |
| 234 | live rules · breakouts only · A2 trail · half size if not UPTREND · re-entry | -9.6 | 1.5% | -34.7% | -2.7 / -21.8 / -15.8 | 214 | 73 |
| 235 | trend template · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -9.6 | 5.2% | -32.8% | -5.4 / -10.2 / -21.1 | 274 | 38 |
| 236 | trend template · breakouts only · 50-day exit · S&P above 200-day · re-entry | -9.6 | 6.9% | -34.7% | 2.2 / -18.1 / -5.6 | 185 | 68 |
| 237 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -9.6 | 6.3% | -32.6% | -6.1 / -15.6 / -1.4 | 123 | 42 |
| 238 | live rules · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -9.7 | 4.9% | -37.1% | 1.2 / -18.8 / -12.3 | 177 | 0 |
| 239 | leaders · breakouts only · A2 trail · live gate · no re-entry | -9.7 | 6.2% | -35.6% | 1.3 / -14.5 / -17.2 | 182 | 0 |
| 240 | trend template · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -9.8 | 4.4% | -34.0% | -6.7 / -12.6 / -17.9 | 135 | 21 |
| 241 | EPS & sales · breakouts + pullbacks · A2 trail · S&P above 200-day · early re-entry | -9.8 | 7.3% | -38.3% | -14.4 / -1.4 / -14.7 | 290 | 41 |
| 242 | leaders · breakouts only · original stop · half size if not UPTREND · re-entry | -9.9 | 6.5% | -35.2% | -5.2 / -16.2 / 0.0 | 85 | 30 |
| 243 | live rules · breakouts only · original stop · live gate · early re-entry | -10.0 | 6.1% | -35.1% | 0.2 / -16.6 / -9.1 | 72 | 39 |
| 244 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -10.0 | 5.4% | -35.3% | -1.8 / -14.8 / -15.1 | 333 | 53 |
| 245 | trend template · breakouts + pullbacks · 50-day exit · live gate · early re-entry | -10.1 | 6.2% | -34.3% | -4.6 / -12.7 / -11.7 | 308 | 53 |
| 246 | trend template · breakouts only · A2 trail · S&P above 200-day · re-entry | -10.1 | 2.7% | -35.3% | -4.7 / -16.6 / -18.5 | 183 | 57 |
| 247 | leaders · breakouts only · original stop + climax sell · live gate · re-entry | -10.1 | 4.1% | -34.3% | -6.7 / -17.3 / -8.3 | 125 | 41 |
| 248 | leaders · breakouts only · A2 trail · half size if not UPTREND · early re-entry | -10.1 | 4.0% | -34.2% | -1.2 / -18.1 / -15.1 | 221 | 66 |
| 249 | trend template · breakouts + pullbacks · A2 trail · S&P above 200-day · early re-entry | -10.2 | 4.7% | -34.0% | -6.4 / -10.8 / -20.6 | 271 | 41 |
| 250 | trend template · breakouts + pullbacks · 50-day exit · live gate · re-entry | -10.3 | 7.7% | -34.6% | -3.8 / -10.7 / -10.2 | 309 | 52 |
| 251 | trend template · breakouts only · 50-day exit · S&P above 200-day · early re-entry | -10.3 | 7.2% | -34.5% | -2.0 / -17.7 / 1.7 | 184 | 65 |
| 252 | leaders · breakouts only · A2 trail · S&P above 200-day · early re-entry | -10.3 | 8.5% | -33.1% | -0.3 / -10.2 / -12.2 | 178 | 45 |
| 253 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · early re-entry | -10.4 | 6.1% | -35.4% | -6.0 / -18.5 / 4.0 | 125 | 47 |
| 254 | live rules · breakouts only · A2 trail · live gate · re-entry | -10.6 | -0.1% | -36.1% | -4.6 / -22.7 / -18.8 | 197 | 64 |
| 255 | trend template · breakouts only · A2 trail · S&P above 200-day · early re-entry | -10.7 | 3.0% | -36.2% | -4.4 / -16.1 / -18.4 | 174 | 49 |
| 256 | live rules · breakouts only · A2 trail · S&P above 200-day · no re-entry | -10.8 | 2.8% | -36.3% | -3.7 / -15.9 / -21.2 | 162 | 0 |
| 257 | trend template · breakouts only · A2 trail · live gate · early re-entry | -10.8 | 1.1% | -39.1% | -7.7 / -18.3 / -18.6 | 188 | 63 |
| 258 | live rules · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -10.9 | 14.3% | -32.8% | 3.5 / -3.0 / -6.8 | 308 | 35 |
| 259 | live rules · breakouts only · A2 trail · live gate · no re-entry | -10.9 | 2.8% | -36.8% | -0.6 / -17.9 / -21.8 | 165 | 0 |
| 260 | trend template · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -10.9 | 8.2% | -35.0% | 0.9 / -12.1 / -12.6 | 301 | 0 |
| 261 | trend template · breakouts only · A2 trail · S&P above 200-day · no re-entry | -11.0 | 1.6% | -37.8% | -3.6 / -19.0 / -19.9 | 158 | 0 |
| 262 | leaders · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -11.1 | 4.6% | -36.0% | 2.7 / -14.9 / -24.8 | 274 | 41 |
| 263 | leaders · breakouts only · original stop · live gate · re-entry | -11.2 | 6.2% | -35.6% | -6.6 / -16.6 / 2.3 | 79 | 31 |
| 264 | leaders · breakouts only · original stop · live gate · early re-entry | -11.3 | 4.9% | -36.5% | -6.1 / -17.7 / -3.2 | 75 | 30 |
| 265 | leaders · breakouts only · original stop · live gate · no re-entry | -11.4 | 3.6% | -34.2% | -5.6 / -15.3 / -15.6 | 77 | 0 |
| 266 | leaders · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -11.6 | 3.0% | -38.1% | -4.4 / -14.0 / -23.9 | 253 | 0 |
| 267 | leaders · breakouts only · A2 trail · live gate · re-entry | -11.6 | 1.6% | -36.8% | -3.4 / -21.1 / -16.7 | 206 | 60 |
| 268 | trend template · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -11.7 | 4.3% | -36.7% | -1.7 / -19.0 / -10.1 | 152 | 0 |
| 269 | leaders · breakouts only · original stop + climax sell · live gate · early re-entry | -11.7 | 3.8% | -39.2% | -6.7 / -20.9 / -1.6 | 114 | 46 |
| 270 | trend template · breakouts only · A2 trail · live gate · re-entry | -11.8 | 1.4% | -36.9% | -6.1 / -18.7 / -18.3 | 191 | 64 |
| 271 | leaders · breakouts only · A2 trail · live gate · early re-entry | -11.8 | 2.5% | -38.2% | -3.4 / -20.2 / -14.3 | 202 | 62 |
| 272 | trend template · breakouts + pullbacks · A2 trail · live gate · no re-entry | -12.0 | 3.5% | -35.1% | -5.9 / -12.3 / -23.2 | 256 | 0 |
| 273 | trend template · breakouts only · A2 trail · live gate · no re-entry | -12.0 | 2.1% | -37.4% | -1.1 / -19.0 / -22.0 | 158 | 0 |
| 274 | trend template · breakouts only · 50-day exit · live gate · early re-entry | -12.1 | 5.5% | -34.0% | -6.4 / -13.8 / -9.0 | 187 | 80 |
| 275 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | -12.2 | 6.0% | -35.3% | -1.8 / -14.6 / -12.3 | 338 | 48 |
| 276 | trend template · breakouts + pullbacks · A2 trail · half size if not UPTREND · early re-entry | -12.4 | 5.8% | -35.8% | -4.2 / -15.4 / -8.9 | 316 | 48 |
| 277 | leaders · breakouts + pullbacks · A2 trail · half size if not UPTREND · early re-entry | -12.6 | 5.0% | -36.3% | 0.1 / -16.8 / -14.9 | 302 | 45 |
| 278 | leaders · breakouts + pullbacks · 50-day exit · S&P above 200-day · early re-entry | -12.6 | 4.2% | -35.8% | 1.6 / -14.6 / -25.7 | 275 | 36 |
| 279 | live rules · breakouts + pullbacks · A2 trail · live gate · re-entry | -12.7 | 11.7% | -32.7% | 0.8 / -3.3 / -14.2 | 291 | 32 |
| 280 | trend template · breakouts + pullbacks · A2 trail · live gate · early re-entry | -12.7 | 5.7% | -35.4% | -8.9 / -9.7 / -15.2 | 276 | 32 |
| 281 | leaders · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -13.7 | 6.1% | -37.6% | 0.1 / -14.8 / -14.9 | 291 | 0 |
| 282 | leaders · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -13.7 | 1.5% | -37.5% | -8.8 / -12.5 / -26.3 | 258 | 43 |
| 283 | live rules · breakouts + pullbacks · A2 trail · live gate · no re-entry | -14.3 | 8.5% | -34.6% | -1.7 / -3.5 / -24.7 | 284 | 0 |
| 284 | leaders · breakouts + pullbacks · A2 trail · live gate · no re-entry | -14.6 | 3.8% | -38.1% | -1.1 / -15.2 / -22.8 | 260 | 0 |
| 285 | leaders · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -14.9 | 2.2% | -36.8% | -1.5 / -20.3 / -17.7 | 311 | 44 |
| 286 | leaders · breakouts + pullbacks · A2 trail · live gate · early re-entry | -15.1 | 1.4% | -38.9% | -0.4 / -19.6 / -23.9 | 267 | 37 |
| 287 | leaders · breakouts + pullbacks · A2 trail · S&P above 200-day · early re-entry | -15.2 | 0.0% | -37.7% | -7.9 / -13.0 / -32.9 | 265 | 43 |
| 288 | leaders · breakouts + pullbacks · A2 trail · live gate · re-entry | -17.6 | 3.0% | -38.5% | -0.1 / -19.8 / -16.8 | 263 | 35 |

_Sub-periods: 2017–2018 · 2019–2020 · 2021–2021. Tune vs SPY = median excess CAGR of 3 random same-day-order runs. Generated by scripts/backtest/run_round6.py._
