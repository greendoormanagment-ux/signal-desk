# Round 6 — best small combination of rules (2026-10-22)

**Data:** free (Yahoo, survivorship-limited) · 657 S&P 500 members (point in time) · cost 0.07% per side · idle money in SPY · signals at the close, filled next open.
**Periods:** TUNE 2017-10-15 → 2021-12-31 (used to choose) · JUDGE 2022-01-01 → 2025-12-31 (opened only for the top 3) · 2026 shown alone.

**Search:** 4 entry filters × 2 setup choices × 4 exits × 3 market rules × re-entry on/off = 192 combinations. *Re-entry* = after any sale, buy back within 40 sessions if the stock closes above its high since the sale, above the 50-day, on 1.2× volume, not rated SELL, market not in CORRECTION (max 2 buy-backs in a row).

**Pass bar (raised because 192 combinations were tried):** beat SPY in tune AND judge, ≥ 80% of judge bootstrap resamples above zero, judge drawdown no worse than SPY's + 5 points.

> ⚠ **Free data:** failed/bought-out companies are missing, so stock picking is flattered. A pass here means 'worth the paid EODHD test', not proof.

**3 of 192 combinations beat SPY in the tune years.**

| SPY | CAGR | max drawdown |
| --- | --- | --- |
| tune | 15.9% | -34.1% |
| judge | 9.3% | -25.4% |
| 2026 | 16.7% | -9.1% |

## Top 3 (chosen on tune only) + the live system

| Combination | Rule changes | Tune vs SPY | Judge CAGR (vs SPY) | Judge range | Judge max DD | Bootstrap % | 2026 vs SPY | Passes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| live rules · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | 2 | 0.5 | **8.7% (-0.6)** | -1.4 to 14.9 | -18.3% | 40.0 | -12.4 | ✗ |
| trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | 3 | 0.5 | **6.8% (-2.5)** | 3.3 to 11.7 | -27.7% | 26.0 | -1.0 | ✗ |
| trend template · breakouts only · original stop · S&P above 200-day · no re-entry | 4 | 0.7 | **11.4% (2.2)** | 11.3 to 13.5 | -24.8% | 30.0 | 1.7 | ✗ |
| live rules · breakouts + pullbacks · A2 trail · live gate · no re-entry **(live today)** | 0 | -10.5 | **6.1% (-3.2)** | 3.6 to 10.8 | -23.2% | 50.0 | -23.9 | – |

## Which single choices helped most (tune years, averaged over every combination that used them)

**Entry filter:** EPS & sales -4.6 (0/48 beat SPY) · live rules -6.0 (1/48 beat SPY) · trend template -7.3 (2/48 beat SPY) · leaders -7.4 (0/48 beat SPY)

**Setups:** breakouts + pullbacks -5.7 (2/96 beat SPY) · breakouts only -6.9 (1/96 beat SPY)

**Exit:** original stop + climax sell -5.1 (2/48 beat SPY) · original stop -5.8 (1/48 beat SPY) · 50-day exit -5.9 (0/48 beat SPY) · A2 trail -8.6 (0/48 beat SPY)

**Market rule:** half size if not UPTREND -5.9 (0/64 beat SPY) · S&P above 200-day -6.4 (2/64 beat SPY) · live gate -6.6 (1/64 beat SPY)

**Re-entry:** re-entry -6.1 (1/96 beat SPY) · no re-entry -6.6 (2/96 beat SPY)

**Re-entry effect by exit** (tune, re-entry minus no re-entry): A2 trail +0.0 · original stop +1.7 · 50-day exit +0.3 · original stop + climax sell -0.1

## All 192 on tune (best first)

| # | Combination | Tune vs SPY | Tune CAGR | Tune DD | Sub-periods vs SPY | Trades | Buy-backs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | trend template · breakouts only · original stop · S&P above 200-day · no re-entry | 0.7 | 15.5% | -32.4% | 1.2 / -5.5 / 8.9 | 49 | 0 |
| 2 | live rules · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | 0.5 | 11.9% | -31.6% | 3.3 / -4.1 / -15.1 | 122 | 13 |
| 3 | trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | 0.5 | 13.8% | -31.6% | -3.5 / -3.0 / 1.9 | 118 | 0 |
| 4 | EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | 0.0 | 16.1% | -34.2% | -2.4 / 4.0 / -5.2 | 136 | 0 |
| 5 | live rules · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -0.1 | 16.2% | -31.6% | 3.9 / -1.1 / -2.7 | 300 | 0 |
| 6 | EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -0.1 | 15.4% | -32.2% | -1.8 / 0.9 / -4.4 | 186 | 39 |
| 7 | EPS & sales · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -0.2 | 15.0% | -33.1% | -2.9 / 3.6 / -8.8 | 163 | 0 |
| 8 | trend template · breakouts only · original stop · half size if not UPTREND · re-entry | -0.5 | 15.1% | -34.0% | -2.1 / -4.0 / 9.1 | 75 | 40 |
| 9 | EPS & sales · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -0.9 | 16.1% | -31.6% | -2.1 / 0.8 / 2.8 | 377 | 51 |
| 10 | EPS & sales · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -1.0 | 14.7% | -30.9% | -4.6 / 1.2 / -3.7 | 157 | 32 |
| 11 | EPS & sales · breakouts + pullbacks · original stop · live gate · re-entry | -1.1 | 12.2% | -33.6% | 0.7 / -3.3 / -11.0 | 79 | 12 |
| 12 | trend template · breakouts only · original stop · live gate · re-entry | -1.2 | 14.4% | -34.4% | -3.2 / -5.3 / 11.0 | 63 | 37 |
| 13 | EPS & sales · breakouts + pullbacks · A2 trail · live gate · re-entry | -1.3 | 10.3% | -33.8% | -6.3 / 2.9 / -22.2 | 285 | 35 |
| 14 | live rules · breakouts + pullbacks · original stop · live gate · re-entry | -1.7 | 10.9% | -34.2% | 0.0 / -10.0 / -1.0 | 77 | 10 |
| 15 | leaders · breakouts only · 50-day exit · S&P above 200-day · re-entry | -1.9 | 11.9% | -34.2% | 4.4 / -9.7 / -6.0 | 184 | 54 |
| 16 | EPS & sales · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -1.9 | 14.0% | -37.2% | -0.4 / -9.1 / 11.7 | 96 | 27 |
| 17 | leaders · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -2.0 | 12.2% | -36.0% | 3.8 / -8.6 / -6.2 | 148 | 35 |
| 18 | leaders · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -2.0 | 12.5% | -33.8% | 10.8 / -12.5 / -3.3 | 62 | 11 |
| 19 | EPS & sales · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -2.0 | 13.2% | -35.0% | -0.6 / -4.0 / -3.5 | 368 | 0 |
| 20 | EPS & sales · breakouts only · original stop + climax sell · live gate · re-entry | -2.0 | 13.9% | -33.8% | -0.3 / -9.1 / 10.5 | 105 | 34 |
| 21 | live rules · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -2.1 | 10.1% | -31.2% | 3.2 / -10.4 / -10.8 | 139 | 16 |
| 22 | leaders · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -2.2 | 10.4% | -35.4% | 9.4 / -13.2 / -9.6 | 79 | 14 |
| 23 | EPS & sales · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -2.2 | 13.3% | -35.0% | -2.9 / -2.2 / -3.0 | 311 | 0 |
| 24 | leaders · breakouts + pullbacks · original stop · live gate · re-entry | -2.3 | 7.8% | -37.5% | 10.8 / -15.1 / -18.9 | 72 | 13 |
| 25 | EPS & sales · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -2.3 | 11.6% | -35.4% | 0.5 / -5.1 / -9.8 | 94 | 21 |
| 26 | EPS & sales · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -2.4 | 11.2% | -34.0% | -2.6 / 0.6 / -19.2 | 317 | 42 |
| 27 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -2.4 | 8.5% | -36.7% | -0.7 / -9.2 / -13.1 | 95 | 14 |
| 28 | live rules · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -2.5 | 11.0% | -33.4% | 2.4 / -9.1 / -5.5 | 83 | 12 |
| 29 | EPS & sales · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -2.6 | 13.4% | -35.4% | -3.2 / -7.5 / 9.2 | 109 | 37 |
| 30 | live rules · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -2.8 | 12.7% | -36.2% | -1.5 / -5.2 / -1.1 | 128 | 0 |
| 31 | leaders · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -2.9 | 12.8% | -34.2% | -0.5 / -9.4 / 5.7 | 197 | 68 |
| 32 | EPS & sales · breakouts + pullbacks · 50-day exit · live gate · re-entry | -3.0 | 13.0% | -35.2% | -2.7 / -0.4 / -8.5 | 332 | 40 |
| 33 | EPS & sales · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -3.0 | 11.2% | -35.3% | -1.5 / 0.1 / -20.3 | 302 | 0 |
| 34 | live rules · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -3.4 | 10.6% | -35.9% | 1.4 / -12.2 / 1.0 | 122 | 19 |
| 35 | leaders · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -3.4 | 11.0% | -34.2% | 3.7 / -10.4 / -6.9 | 131 | 30 |
| 36 | EPS & sales · breakouts only · 50-day exit · live gate · re-entry | -3.5 | 9.5% | -35.4% | 0.0 / -5.1 / -19.7 | 141 | 51 |
| 37 | trend template · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -3.6 | 10.3% | -35.2% | -2.1 / -9.5 / -1.3 | 112 | 22 |
| 38 | EPS & sales · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -3.6 | 11.4% | -34.6% | -9.6 / -5.1 / 4.8 | 88 | 0 |
| 39 | leaders · breakouts + pullbacks · 50-day exit · live gate · re-entry | -3.7 | 8.1% | -37.8% | 2.5 / -9.3 / -21.6 | 275 | 45 |
| 40 | leaders · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -3.8 | 13.4% | -34.9% | 3.3 / -6.4 / -3.7 | 146 | 34 |
| 41 | live rules · breakouts only · 50-day exit · S&P above 200-day · re-entry | -3.9 | 10.9% | -34.0% | 3.5 / -11.8 / -3.7 | 177 | 59 |
| 42 | leaders · breakouts only · 50-day exit · live gate · no re-entry | -3.9 | 11.7% | -36.5% | 1.8 / -14.3 / 7.4 | 154 | 0 |
| 43 | leaders · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -3.9 | 10.6% | -36.2% | -2.6 / -13.5 / 7.0 | 163 | 0 |
| 44 | EPS & sales · breakouts + pullbacks · A2 trail · live gate · no re-entry | -3.9 | 7.3% | -35.2% | -5.8 / -3.4 / -24.4 | 276 | 0 |
| 45 | EPS & sales · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · re-entry | -3.9 | 10.6% | -38.4% | -7.4 / -4.6 / -4.0 | 160 | 31 |
| 46 | live rules · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -4.0 | 11.9% | -31.2% | -1.6 / -1.1 / -14.4 | 260 | 26 |
| 47 | trend template · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -4.0 | 9.8% | -36.1% | -4.1 / -11.3 / -0.2 | 121 | 0 |
| 48 | leaders · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -4.0 | 11.4% | -36.8% | 6.2 / -11.1 / -6.2 | 149 | 0 |
| 49 | EPS & sales · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -4.1 | 10.6% | -35.9% | 0.6 / -5.2 / -15.2 | 97 | 0 |
| 50 | live rules · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -4.2 | 11.2% | -33.4% | 3.9 / -8.8 / -9.4 | 318 | 41 |
| 51 | trend template · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -4.2 | 9.2% | -34.0% | -3.3 / -11.6 / -4.4 | 128 | 0 |
| 52 | EPS & sales · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -4.2 | 10.2% | -35.9% | -3.4 / -4.0 / -13.9 | 163 | 57 |
| 53 | trend template · breakouts + pullbacks · original stop · half size if not UPTREND · re-entry | -4.3 | 10.0% | -30.6% | 1.6 / -9.8 / -9.3 | 79 | 17 |
| 54 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -4.3 | 11.5% | -33.6% | 7.2 / -7.2 / -15.3 | 350 | 0 |
| 55 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -4.3 | 10.8% | -32.0% | -1.4 / -8.4 / -3.7 | 82 | 0 |
| 56 | EPS & sales · breakouts only · original stop + climax sell · live gate · no re-entry | -4.3 | 11.1% | -34.6% | -9.6 / -5.6 / 4.5 | 87 | 0 |
| 57 | live rules · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -4.4 | 11.1% | -34.7% | 0.1 / -7.6 / -6.8 | 338 | 0 |
| 58 | EPS & sales · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -4.4 | 9.8% | -32.9% | -9.8 / -3.4 / -6.0 | 347 | 36 |
| 59 | leaders · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -4.5 | 10.4% | -31.7% | 5.3 / -12.5 / -6.2 | 136 | 0 |
| 60 | live rules · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -4.6 | 10.0% | -34.5% | 0.2 / -9.8 / -7.8 | 306 | 0 |
| 61 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | -4.6 | 9.7% | -34.4% | 1.0 / -5.9 / -16.4 | 76 | 0 |
| 62 | leaders · breakouts only · 50-day exit · live gate · re-entry | -4.7 | 9.1% | -33.6% | 0.1 / -13.6 / -2.7 | 178 | 63 |
| 63 | EPS & sales · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -4.7 | 10.4% | -36.1% | -8.0 / -5.4 / -1.8 | 94 | 0 |
| 64 | live rules · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -4.8 | 8.3% | -34.5% | 1.5 / -9.0 / -17.0 | 82 | 14 |
| 65 | leaders · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -4.8 | 11.8% | -34.9% | 0.9 / -12.2 / 4.2 | 174 | 0 |
| 66 | EPS & sales · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -4.8 | 10.6% | -36.0% | -0.8 / -3.7 / -16.0 | 139 | 0 |
| 67 | live rules · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -4.9 | 10.0% | -31.4% | -0.3 / -8.3 / -11.3 | 125 | 0 |
| 68 | live rules · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -4.9 | 7.6% | -31.9% | -4.6 / -7.1 / -17.4 | 330 | 43 |
| 69 | live rules · breakouts only · original stop · half size if not UPTREND · re-entry | -4.9 | 11.2% | -33.0% | 0.1 / -8.4 / -2.8 | 82 | 39 |
| 70 | live rules · breakouts + pullbacks · original stop + climax sell · live gate · no re-entry | -5.0 | 12.0% | -31.0% | -0.3 / -6.6 / -6.2 | 124 | 0 |
| 71 | live rules · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -5.0 | 8.4% | -34.4% | -3.4 / -12.7 / -2.2 | 202 | 78 |
| 72 | live rules · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -5.2 | 10.1% | -33.4% | -1.5 / -4.7 / -14.8 | 365 | 45 |
| 73 | live rules · breakouts only · 50-day exit · live gate · re-entry | -5.2 | 6.4% | -33.7% | -5.7 / -11.2 / -12.3 | 185 | 73 |
| 74 | live rules · breakouts + pullbacks · A2 trail · live gate · re-entry | -5.4 | 10.0% | -30.9% | -1.4 / -5.1 / -14.9 | 285 | 42 |
| 75 | live rules · breakouts + pullbacks · 50-day exit · live gate · re-entry | -5.4 | 7.2% | -32.7% | -8.2 / -8.0 / -11.9 | 308 | 40 |
| 76 | trend template · breakouts only · original stop · live gate · no re-entry | -5.5 | 9.1% | -34.7% | -0.3 / -14.8 / 1.3 | 57 | 0 |
| 77 | EPS & sales · breakouts only · A2 trail · live gate · no re-entry | -5.5 | 10.1% | -35.0% | -1.1 / -3.6 / -17.7 | 126 | 0 |
| 78 | EPS & sales · breakouts only · A2 trail · S&P above 200-day · no re-entry | -5.5 | 11.0% | -33.7% | -0.5 / -3.2 / -15.5 | 126 | 0 |
| 79 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -5.6 | 9.8% | -29.6% | 0.3 / -11.3 / -3.9 | 87 | 0 |
| 80 | EPS & sales · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -5.6 | 10.6% | -36.4% | -3.6 / -4.5 / -10.5 | 132 | 0 |
| 81 | live rules · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -5.7 | 7.8% | -35.3% | 0.2 / -18.0 / 1.0 | 169 | 0 |
| 82 | live rules · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -5.7 | 5.1% | -38.7% | -3.2 / -19.6 / -3.8 | 155 | 0 |
| 83 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -5.8 | 6.8% | -35.0% | 3.6 / -12.6 / -20.7 | 328 | 0 |
| 84 | EPS & sales · breakouts + pullbacks · original stop · live gate · no re-entry | -5.8 | 10.8% | -36.6% | 0.5 / -4.0 / -16.7 | 76 | 0 |
| 85 | EPS & sales · breakouts only · original stop · live gate · re-entry | -5.8 | 9.1% | -36.0% | -4.2 / -9.9 / -5.0 | 69 | 24 |
| 86 | live rules · breakouts + pullbacks · original stop · live gate · no re-entry | -6.0 | 10.5% | -33.2% | 0.6 / -7.7 / -9.8 | 87 | 0 |
| 87 | leaders · breakouts only · original stop · half size if not UPTREND · no re-entry | -6.0 | 8.1% | -35.2% | -3.6 / -10.8 / -9.0 | 89 | 0 |
| 88 | live rules · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -6.1 | 11.2% | -31.9% | 1.8 / -1.5 / -21.3 | 268 | 0 |
| 89 | live rules · breakouts only · original stop · S&P above 200-day · no re-entry | -6.1 | 7.4% | -36.6% | 1.0 / -18.4 / -0.3 | 63 | 0 |
| 90 | trend template · breakouts only · original stop · S&P above 200-day · re-entry | -6.1 | 10.5% | -34.6% | -0.5 / -14.2 / 7.5 | 54 | 14 |
| 91 | leaders · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -6.1 | 9.5% | -39.7% | 2.5 / -11.9 / -9.7 | 311 | 52 |
| 92 | EPS & sales · breakouts + pullbacks · original stop + climax sell · S&P above 200-day · no re-entry | -6.1 | 12.3% | -36.1% | -5.0 / 1.5 / -12.5 | 155 | 0 |
| 93 | EPS & sales · breakouts only · original stop · S&P above 200-day · no re-entry | -6.1 | 9.8% | -37.2% | -2.7 / -8.0 / -8.9 | 56 | 0 |
| 94 | EPS & sales · breakouts only · original stop · S&P above 200-day · re-entry | -6.1 | 9.7% | -35.0% | -2.7 / -10.5 / -3.2 | 63 | 18 |
| 95 | trend template · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -6.2 | 9.5% | -29.9% | 1.2 / -8.6 / -13.5 | 77 | 0 |
| 96 | leaders · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -6.2 | 9.9% | -32.3% | -3.7 / -8.3 / -5.0 | 95 | 17 |
| 97 | EPS & sales · breakouts only · original stop · half size if not UPTREND · re-entry | -6.2 | 9.0% | -36.1% | -5.4 / -7.3 / -9.8 | 81 | 28 |
| 98 | trend template · breakouts only · 50-day exit · half size if not UPTREND · re-entry | -6.4 | 9.7% | -33.7% | -2.5 / -11.6 / -0.3 | 196 | 82 |
| 99 | leaders · breakouts only · original stop + climax sell · S&P above 200-day · no re-entry | -6.4 | 9.8% | -32.7% | -4.7 / -8.6 / -3.5 | 89 | 0 |
| 100 | leaders · breakouts only · A2 trail · S&P above 200-day · no re-entry | -6.5 | 9.4% | -35.5% | 1.4 / -7.6 / -16.4 | 177 | 0 |
| 101 | EPS & sales · breakouts only · 50-day exit · live gate · no re-entry | -6.5 | 9.8% | -36.0% | -3.4 / -6.1 / -11.3 | 120 | 0 |
| 102 | trend template · breakouts only · original stop · half size if not UPTREND · no re-entry | -6.6 | 7.9% | -34.4% | -0.3 / -17.2 / 1.2 | 74 | 0 |
| 103 | live rules · breakouts only · 50-day exit · live gate · no re-entry | -6.7 | 5.9% | -38.5% | -1.7 / -19.0 / -3.7 | 153 | 0 |
| 104 | trend template · breakouts + pullbacks · original stop · live gate · re-entry | -6.7 | 9.2% | -31.8% | 3.6 / -9.1 / -16.3 | 66 | 11 |
| 105 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -6.8 | 7.6% | -34.0% | -2.6 / -12.9 / -8.4 | 103 | 0 |
| 106 | trend template · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -6.8 | 8.7% | -35.2% | -1.3 / -13.8 / -1.6 | 87 | 18 |
| 107 | leaders · breakouts + pullbacks · original stop · live gate · no re-entry | -6.8 | 6.4% | -38.6% | 9.5 / -17.2 / -19.3 | 78 | 0 |
| 108 | trend template · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -6.9 | 6.6% | -33.8% | 2.8 / -11.4 / -22.9 | 314 | 0 |
| 109 | trend template · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -6.9 | 7.6% | -34.0% | -3.9 / -12.7 / -6.5 | 120 | 44 |
| 110 | EPS & sales · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -6.9 | 11.0% | -35.0% | -7.6 / -2.8 / -5.7 | 335 | 0 |
| 111 | live rules · breakouts only · original stop · live gate · no re-entry | -7.0 | 6.5% | -36.9% | 0.2 / -19.3 / -1.2 | 65 | 0 |
| 112 | live rules · breakouts only · original stop · half size if not UPTREND · no re-entry | -7.0 | 7.4% | -36.6% | 0.3 / -17.4 / -1.3 | 73 | 0 |
| 113 | leaders · breakouts only · original stop · S&P above 200-day · no re-entry | -7.0 | 9.0% | -33.8% | -4.1 / -7.0 / -10.8 | 61 | 0 |
| 114 | EPS & sales · breakouts only · A2 trail · half size if not UPTREND · re-entry | -7.0 | 7.9% | -34.7% | -4.4 / -6.5 / -17.4 | 171 | 60 |
| 115 | live rules · breakouts only · original stop + climax sell · S&P above 200-day · re-entry | -7.1 | 8.5% | -32.6% | -2.1 / -13.3 / -3.2 | 100 | 19 |
| 116 | leaders · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -7.1 | 8.0% | -37.2% | 8.1 / -18.6 / -7.0 | 84 | 0 |
| 117 | trend template · breakouts + pullbacks · original stop · live gate · no re-entry | -7.2 | 8.6% | -31.8% | 4.5 / -12.0 / -14.4 | 63 | 0 |
| 118 | leaders · breakouts + pullbacks · 50-day exit · live gate · no re-entry | -7.2 | 11.5% | -37.3% | 5.4 / -11.4 / -5.7 | 264 | 0 |
| 119 | live rules · breakouts + pullbacks · original stop · half size if not UPTREND · no re-entry | -7.4 | 11.0% | -33.5% | 3.2 / -7.6 / -10.7 | 81 | 0 |
| 120 | live rules · breakouts only · original stop · S&P above 200-day · re-entry | -7.4 | 8.6% | -35.9% | -0.1 / -15.1 / -0.3 | 74 | 22 |
| 121 | trend template · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | -7.5 | 8.3% | -32.4% | 4.7 / -10.5 / -18.8 | 71 | 0 |
| 122 | leaders · breakouts + pullbacks · 50-day exit · half size if not UPTREND · no re-entry | -7.5 | 11.9% | -36.9% | 3.0 / -12.0 / 1.9 | 300 | 0 |
| 123 | live rules · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -7.6 | 7.2% | -33.9% | -1.4 / -15.5 / -4.9 | 100 | 0 |
| 124 | trend template · breakouts only · 50-day exit · half size if not UPTREND · no re-entry | -7.6 | 8.1% | -34.3% | 0.7 / -16.0 / -2.8 | 160 | 0 |
| 125 | leaders · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · no re-entry | -7.6 | 8.2% | -37.8% | 5.0 / -15.1 / -11.0 | 152 | 0 |
| 126 | EPS & sales · breakouts only · A2 trail · S&P above 200-day · re-entry | -7.6 | 8.2% | -32.9% | -5.2 / -5.0 / -17.1 | 153 | 55 |
| 127 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · no re-entry | -7.7 | 7.5% | -34.4% | -3.2 / -12.9 / -7.1 | 122 | 0 |
| 128 | leaders · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | -7.8 | 4.8% | -37.9% | 9.5 / -19.2 / -22.5 | 83 | 0 |
| 129 | leaders · breakouts only · A2 trail · S&P above 200-day · re-entry | -7.8 | 7.4% | -33.0% | -2.0 / -9.5 / -16.1 | 199 | 56 |
| 130 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -7.8 | 7.9% | -36.0% | -6.8 / -6.6 / -13.5 | 120 | 0 |
| 131 | live rules · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -7.9 | 4.6% | -37.1% | -0.3 / -20.5 / -8.1 | 180 | 0 |
| 132 | trend template · breakouts only · original stop + climax sell · live gate · re-entry | -7.9 | 7.3% | -33.8% | -5.8 / -11.7 / -7.6 | 113 | 42 |
| 133 | EPS & sales · breakouts only · 50-day exit · S&P above 200-day · re-entry | -8.0 | 7.4% | -35.3% | -4.2 / -6.9 / -19.3 | 146 | 53 |
| 134 | trend template · breakouts only · A2 trail · half size if not UPTREND · re-entry | -8.1 | 5.6% | -35.6% | -6.5 / -14.6 / -7.0 | 201 | 71 |
| 135 | leaders · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -8.1 | 6.9% | -32.6% | -6.2 / -14.4 / -1.4 | 122 | 43 |
| 136 | EPS & sales · breakouts only · original stop · half size if not UPTREND · no re-entry | -8.1 | 7.4% | -36.0% | -5.0 / -6.8 / -18.7 | 72 | 0 |
| 137 | live rules · breakouts only · A2 trail · S&P above 200-day · re-entry | -8.2 | 5.5% | -34.1% | -2.7 / -15.3 / -11.3 | 181 | 58 |
| 138 | trend template · breakouts + pullbacks · A2 trail · live gate · re-entry | -8.2 | 8.1% | -34.0% | -1.5 / -11.1 / -12.2 | 265 | 30 |
| 139 | trend template · breakouts + pullbacks · original stop · S&P above 200-day · re-entry | -8.2 | 8.1% | -30.7% | 3.4 / -8.9 / -21.0 | 74 | 11 |
| 140 | trend template · breakouts only · original stop + climax sell · live gate · no re-entry | -8.4 | 7.5% | -33.5% | -4.7 / -12.9 / -4.5 | 91 | 0 |
| 141 | trend template · breakouts + pullbacks · 50-day exit · half size if not UPTREND · re-entry | -8.5 | 9.7% | -33.2% | 0.4 / -3.5 / -20.4 | 359 | 64 |
| 142 | trend template · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -8.5 | 6.1% | -36.2% | 0.6 / -17.3 / -9.6 | 163 | 0 |
| 143 | leaders · breakouts only · original stop · S&P above 200-day · re-entry | -8.5 | 8.5% | -35.8% | -5.3 / -9.8 / -4.8 | 59 | 10 |
| 144 | live rules · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -8.6 | 9.9% | -34.2% | 1.0 / -9.8 / -9.2 | 308 | 0 |
| 145 | live rules · breakouts only · original stop · live gate · re-entry | -8.7 | 11.6% | -33.1% | 0.1 / -7.6 / -2.9 | 71 | 36 |
| 146 | trend template · breakouts only · 50-day exit · S&P above 200-day · re-entry | -8.7 | 7.3% | -34.1% | 1.5 / -17.3 / -5.0 | 184 | 67 |
| 147 | leaders · breakouts only · A2 trail · half size if not UPTREND · no re-entry | -8.7 | 6.9% | -35.4% | 4.3 / -15.7 / -15.6 | 196 | 0 |
| 148 | EPS & sales · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -8.7 | 3.2% | -38.9% | -12.0 / -8.9 / -22.9 | 294 | 0 |
| 149 | trend template · breakouts + pullbacks · original stop + climax sell · half size if not UPTREND · re-entry | -8.8 | 6.5% | -33.5% | -0.5 / -13.6 / -15.7 | 147 | 29 |
| 150 | EPS & sales · breakouts only · original stop · live gate · no re-entry | -8.8 | 7.7% | -38.2% | -4.1 / -9.6 / -13.0 | 60 | 0 |
| 151 | trend template · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -9.0 | 9.6% | -32.4% | -3.1 / -7.2 / -11.4 | 264 | 37 |
| 152 | trend template · breakouts only · 50-day exit · live gate · no re-entry | -9.0 | 6.6% | -35.2% | 1.0 / -16.9 / -8.4 | 142 | 0 |
| 153 | EPS & sales · breakouts + pullbacks · original stop · S&P above 200-day · no re-entry | -9.1 | 7.4% | -38.9% | -0.3 / -8.1 / -21.4 | 101 | 0 |
| 154 | EPS & sales · breakouts only · A2 trail · live gate · re-entry | -9.1 | 6.5% | -34.0% | -6.9 / -6.3 / -19.5 | 153 | 54 |
| 155 | live rules · breakouts only · A2 trail · S&P above 200-day · no re-entry | -9.2 | 4.2% | -35.7% | -5.0 / -14.5 / -15.8 | 159 | 0 |
| 156 | leaders · breakouts only · original stop + climax sell · live gate · no re-entry | -9.2 | 6.7% | -33.4% | -6.5 / -12.9 / -6.2 | 100 | 0 |
| 157 | live rules · breakouts only · original stop + climax sell · live gate · re-entry | -9.3 | 6.2% | -29.8% | -2.5 / -15.6 / -7.9 | 110 | 40 |
| 158 | live rules · breakouts only · original stop + climax sell · half size if not UPTREND · re-entry | -9.3 | 6.1% | -32.1% | -2.3 / -16.2 / -7.9 | 116 | 46 |
| 159 | EPS & sales · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -9.3 | 4.6% | -39.8% | -13.5 / -3.6 / -24.3 | 297 | 37 |
| 160 | live rules · breakouts only · A2 trail · live gate · no re-entry | -9.4 | 2.8% | -36.8% | -3.8 / -18.8 / -15.7 | 166 | 0 |
| 161 | trend template · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -9.4 | 8.5% | -35.4% | -2.3 / -8.2 / -14.8 | 276 | 0 |
| 162 | trend template · breakouts only · 50-day exit · live gate · re-entry | -9.4 | 6.4% | -34.2% | -8.3 / -10.9 / -8.5 | 179 | 73 |
| 163 | live rules · breakouts only · original stop + climax sell · live gate · no re-entry | -9.5 | 6.5% | -31.9% | -2.5 / -16.2 / -4.8 | 92 | 0 |
| 164 | leaders · breakouts only · A2 trail · live gate · no re-entry | -9.5 | 7.0% | -35.6% | 4.3 / -14.2 / -18.4 | 180 | 0 |
| 165 | leaders · breakouts only · A2 trail · half size if not UPTREND · re-entry | -9.5 | 4.7% | -33.9% | -0.4 / -17.1 / -15.9 | 225 | 71 |
| 166 | trend template · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -9.9 | 6.8% | -31.2% | 3.5 / -12.4 / -20.6 | 322 | 47 |
| 167 | trend template · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -10.3 | 8.2% | -33.1% | -0.9 / -10.1 / -14.4 | 303 | 42 |
| 168 | trend template · breakouts only · A2 trail · live gate · re-entry | -10.3 | 3.2% | -38.3% | -8.4 / -18.4 / -7.0 | 186 | 65 |
| 169 | leaders · breakouts only · original stop + climax sell · live gate · re-entry | -10.3 | 5.5% | -34.5% | -6.9 / -16.4 / -3.0 | 118 | 41 |
| 170 | trend template · breakouts only · A2 trail · S&P above 200-day · re-entry | -10.4 | 5.2% | -35.6% | -4.7 / -16.7 / -6.3 | 179 | 57 |
| 171 | live rules · breakouts + pullbacks · A2 trail · live gate · no re-entry | -10.5 | 8.6% | -32.8% | -3.4 / -7.9 / -12.5 | 288 | 0 |
| 172 | leaders · breakouts + pullbacks · 50-day exit · S&P above 200-day · re-entry | -10.5 | 4.0% | -34.8% | 4.0 / -17.0 / -24.1 | 285 | 43 |
| 173 | trend template · breakouts + pullbacks · 50-day exit · live gate · re-entry | -10.6 | 8.5% | -33.0% | 0.7 / -9.0 / -16.5 | 318 | 56 |
| 174 | leaders · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -10.7 | 4.2% | -39.2% | -1.4 / -16.4 / -17.2 | 249 | 0 |
| 175 | leaders · breakouts only · A2 trail · live gate · re-entry | -10.7 | 1.1% | -37.4% | -5.9 / -19.9 / -18.2 | 207 | 62 |
| 176 | live rules · breakouts only · A2 trail · half size if not UPTREND · re-entry | -10.8 | 1.1% | -36.9% | -3.6 / -23.1 / -13.5 | 218 | 75 |
| 177 | leaders · breakouts only · original stop · half size if not UPTREND · re-entry | -10.8 | 6.9% | -35.2% | -4.9 / -16.3 / 1.9 | 86 | 31 |
| 178 | trend template · breakouts + pullbacks · A2 trail · live gate · no re-entry | -11.1 | 5.5% | -34.8% | -4.8 / -11.0 / -19.1 | 260 | 0 |
| 179 | trend template · breakouts + pullbacks · A2 trail · S&P above 200-day · no re-entry | -11.1 | 6.9% | -34.4% | 0.1 / -13.7 / -13.7 | 249 | 0 |
| 180 | trend template · breakouts only · A2 trail · S&P above 200-day · no re-entry | -11.3 | 3.8% | -36.9% | -2.8 / -17.9 / -13.8 | 150 | 0 |
| 181 | trend template · breakouts only · A2 trail · live gate · no re-entry | -11.4 | 3.9% | -37.3% | -0.4 / -18.4 / -16.1 | 153 | 0 |
| 182 | leaders · breakouts only · original stop · live gate · re-entry | -11.4 | 5.2% | -35.8% | -6.8 / -16.2 / -3.9 | 78 | 31 |
| 183 | leaders · breakouts only · original stop · live gate · no re-entry | -11.5 | 3.5% | -34.8% | -5.4 / -15.8 / -16.0 | 74 | 0 |
| 184 | leaders · breakouts + pullbacks · A2 trail · half size if not UPTREND · re-entry | -11.6 | 2.5% | -37.0% | 1.3 / -21.1 / -19.5 | 310 | 54 |
| 185 | live rules · breakouts only · A2 trail · live gate · re-entry | -12.1 | -0.5% | -40.1% | -5.7 / -25.1 / -13.7 | 194 | 65 |
| 186 | leaders · breakouts + pullbacks · 50-day exit · S&P above 200-day · no re-entry | -12.3 | 4.8% | -36.3% | 3.9 / -18.2 / -18.3 | 282 | 0 |
| 187 | trend template · breakouts + pullbacks · original stop + climax sell · live gate · re-entry | -12.4 | 8.6% | -31.2% | -0.3 / -11.1 / -11.3 | 132 | 22 |
| 188 | leaders · breakouts + pullbacks · A2 trail · half size if not UPTREND · no re-entry | -12.6 | 5.3% | -37.7% | 2.3 / -18.4 / -14.3 | 291 | 0 |
| 189 | trend template · breakouts only · 50-day exit · S&P above 200-day · no re-entry | -12.7 | 2.2% | -42.0% | -2.4 / -22.9 / -10.7 | 156 | 0 |
| 190 | leaders · breakouts + pullbacks · A2 trail · live gate · no re-entry | -13.2 | 4.2% | -38.2% | 5.2 / -20.4 / -19.0 | 270 | 0 |
| 191 | leaders · breakouts + pullbacks · A2 trail · live gate · re-entry | -13.4 | 5.6% | -38.1% | 7.5 / -18.9 / -17.7 | 270 | 39 |
| 192 | leaders · breakouts + pullbacks · A2 trail · S&P above 200-day · re-entry | -15.4 | 2.8% | -36.8% | -4.2 / -14.6 / -23.1 | 253 | 43 |

_Sub-periods: 2017–2018 · 2019–2020 · 2021–2021. Tune vs SPY = median excess CAGR of 3 random same-day-order runs. Generated by scripts/backtest/run_round6.py._
