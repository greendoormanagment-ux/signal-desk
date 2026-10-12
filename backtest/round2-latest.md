# Round 2 — short-term pullbacks and a momentum stress test (2026-10-12)

Main universe: stocks only while they were in the S&P 500 (point-in-time membership), which is fairer than today's list.

## Benchmarks (CAGR / max drawdown)

| | full | 2017-21 | 2022-26 | 2017-25 (no 2026) | 2026 so far |
| --- | --- | --- | --- | --- | --- |
| SPY | 13.2% / -34.1% | 15.9% / -34.1% | 10.8% / -25.4% | 12.7% / -34.1% | 18.6% / -9.1% |
| RSP (equal-weight S&P) | 9.2% / -39.6% | 13.2% / -39.6% | 5.8% / -22.5% | 8.7% / -39.6% | 13.9% / -8.2% |

## (a) Short-term pullback (mean reversion)

Buy a sharp 2–3 day dip (RSI(2) under 10) in a stock above its 200-day; sell on the bounce. Portfolio: 10 slots of 10%, max 3 per sector, 0.1% cost per side unless noted. CAGR is the median of 10 runs with random tie-breaking among same-day buys (range in brackets).

| Universe | Variant | Trades | Win % | Avg trade | Avg win / loss | Days held | CAGR full (range) | Max DD | CAGR 2017–21 | CAGR 2022–26 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sp500 | base: above 200-day, RSI(2) < 10; buy next open; sell on close > 5-day avg (max 10 days); 10% disaster stop; 10 slots x 10% | 25,842 | 64.8 | 0.22% | 2.15% / -3.33% | 3.7 | -3.0% (-5.4 to -0.7) | -39.1% | -0.6% | -5.2% |
| sp500 | deeper dip: RSI(2) < 5 | 13,497 | 64.7 | 0.24% | 2.2% / -3.34% | 3.8 | -0.9% (-2.1 to 1.1) | -34.3% | 0.8% | -2.0% |
| sp500 | dip + 2 or more down days | 23,991 | 64.8 | 0.22% | 2.14% / -3.31% | 3.7 | -3.5% (-6.1 to -0.9) | -38.1% | 1.6% | -7.1% |
| sp500 | exit when RSI(2) > 70 | 24,681 | 65.9 | 0.27% | 2.47% / -3.98% | 4.8 | -0.9% (-5.2 to 2.5) | -37.6% | 2.2% | -3.5% |
| sp500 | exit on first up close | 27,400 | 58.7 | 0.18% | 2.1% / -2.56% | 2.8 | -8.9% (-10.9 to -7.5) | -59.0% | -6.4% | -10.9% |
| sp500 | max hold 5 days | 26,554 | 62.8 | 0.2% | 2.16% / -3.12% | 3.2 | -4.2% (-5.7 to -1.8) | -41.8% | 0.6% | -7.7% |
| sp500 | only when SPY is above its 200-day | 22,822 | 64.8 | 0.23% | 2.11% / -3.24% | 3.8 | -3.1% (-4.8 to -0.4) | -33.1% | 2.0% | -6.8% |
| sp500 | no disaster stop | 25,659 | 65.0 | 0.3% | 2.15% / -3.14% | 3.9 | -0.8% (-3.3 to 2.8) | -34.1% | 2.8% | -2.8% |
| sp500 | 20 slots x 5% | 25,842 | 64.8 | 0.22% | 2.15% / -3.33% | 3.7 | -3.0% (-3.9 to -2.0) | -38.5% | -2.2% | -3.5% |
| sp500 | buy at the signal-day close (market-on-close order) | 25,893 | 65.6 | 0.28% | 2.27% / -3.51% | 4.7 | 0.4% (-2.0 to 3.6) | -33.3% | 4.7% | -3.7% |
| sp500 | buy with a limit 2% under the signal close (next day only) | 8,156 | 63.0 | 0.41% | 3.11% / -4.18% | 4.3 | 4.5% (2.3 to 9.3) | -33.9% | 3.2% | 5.2% |
| sp500 | buy at close + rank by RS instead of deepest dip | 25,893 | 65.6 | 0.28% | 2.27% / -3.51% | 4.7 | 0.4% (-2.0 to 3.6) | -33.3% | 4.7% | -3.7% |
| sp500 | buy at close + lower trading cost (0.05% a side) | 25,893 | 65.6 | 0.28% | 2.27% / -3.51% | 4.7 | 5.1% (2.5 to 8.4) | -27.8% | 9.5% | 0.8% |
| sp500 | buy at close + RSI(2) < 5 + low cost | 13,518 | 65.5 | 0.32% | 2.33% / -3.52% | 4.7 | 6.6% (4.7 to 8.5) | -26.3% | 7.5% | 5.6% |
| broad | base: above 200-day, RSI(2) < 10; buy next open; sell on close > 5-day avg (max 10 days); 10% disaster stop; 10 slots x 10% | 73,389 | 63.7 | 0.31% | 2.79% / -4.04% | 3.6 | -2.8% (-8.0 to -0.0) | -55.0% | -2.4% | -6.1% |

## (b) Momentum rotation stress test

Each month, hold the 10 S&P 500 members with the best 12-month return (skipping the last month) that are above their 200-day. "Beat SPY in 3-yr windows" = the share of rolling 3-year periods in which it finished ahead of SPY.

| Variant | CAGR full | CAGR 2017-21 | CAGR 2022-26 | CAGR 2017-25 (no 2026) | CAGR 2026 so far | Max DD | Beat SPY in 3-yr windows | Beat RSP in 3-yr windows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base: top 10 by 12-1 month return, above 200-day, monthly | 17.7% | 3.3% | 31.9% | 9.2% | 149.8% | -41.2% | 36.0% | 45.0% |
| top 5 | 21.2% | -0.6% | 45.1% | 10.2% | 230.1% | -47.2% | 51.0% | 49.0% |
| top 20 | 16.2% | 5.9% | 25.8% | 9.9% | 103.8% | -39.6% | 36.0% | 47.0% |
| 6-month momentum (6-1) | 17.7% | 11.1% | 23.7% | 9.0% | 146.5% | -36.7% | 21.0% | 34.0% |
| 3-month momentum, no skip | 16.0% | 17.6% | 13.7% | 9.8% | 91.4% | -42.4% | 59.0% | 58.0% |
| 12-month, no skip | 21.7% | 6.5% | 36.8% | 12.6% | 170.2% | -40.2% | 70.0% | 75.0% |
| weight by low volatility | 16.6% | 3.0% | 30.0% | 8.9% | 132.7% | -43.7% | 44.0% | 49.0% |
| cash when SPY < 200-day (checked monthly) | 1.3% | -8.4% | 10.4% | -3.5% | 62.4% | -55.2% | 10.0% | 14.0% |
| cash when SPY < 200-day (checked daily) | 9.1% | -0.2% | 17.8% | 1.6% | 122.2% | -36.6% | 14.0% | 21.0% |
| no 200-day filter on the stocks | 17.3% | 4.9% | 29.2% | 9.4% | 135.8% | -41.8% | 32.0% | 45.0% |
| max 3 per sector | 16.9% | 1.7% | 32.1% | 8.8% | 143.7% | -41.6% | 45.0% | 47.0% |
| rebalance on trading day 2 of the month | 17.8% | 2.1% | 33.4% | 9.6% | 146.6% | -43.7% | 42.0% | 47.0% |
| rebalance on trading day 3 of the month | 18.5% | 2.1% | 34.8% | 9.9% | 152.3% | -42.8% | 44.0% | 47.0% |
| rebalance on trading day 4 of the month | 19.0% | 5.1% | 32.4% | 10.4% | 152.7% | -40.2% | 38.0% | 49.0% |
| rebalance on trading day 5 of the month | 21.4% | 3.9% | 39.1% | 12.5% | 160.2% | -40.7% | 48.0% | 49.0% |

## Year by year (%)

| | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPY | 4.5 | -6.3 | 28.8 | 16.2 | 27.0 | -19.5 | 24.3 | 23.3 | 16.4 | 14.2 |
| RSP | 4.6 | -9.5 | 26.6 | 10.2 | 27.6 | -13.2 | 11.7 | 11.0 | 9.3 | 11.2 |
| momentum base | -2.0 | -21.9 | 36.8 | 11.3 | -1.7 | -2.2 | 20.4 | 22.2 | 25.4 | 109.7 |
| pullback: buy with a limit 2% under the signal close (next day only) | 5.0 | -15.4 | 18.2 | 14.6 | 6.2 | -9.9 | 7.6 | 15.5 | 12.9 | 5.8 |
| pullback: buy at close + RSI(2) < 5 + low cost | 7.5 | -19.5 | 14.5 | 12.5 | 11.5 | -0.8 | 7.1 | 15.0 | 7.9 | -2.6 |

## Momentum: most recent monthly picks

- 2026-05-01: SNDK, LITE, WDC, CIEN, MU, STX, TER, COHR, FIX, GLW
- 2026-06-01: SNDK, LITE, WDC, CIEN, STX, MU, INTC, TER, COHR, FIX
- 2026-07-01: SNDK, LITE, WDC, MU, CIEN, STX, INTC, TER, COHR, DELL
- 2026-08-03: SNDK, MU, WDC, LITE, INTC, STX, CIEN, LRCX, TER, AMAT
- 2026-09-01: SNDK, MU, WDC, LITE, STX, INTC, DELL, AMAT, TER, MRVL
- 2026-10-01: SNDK, MRNA, MU, LITE, WDC, STX, DELL, AMD, INTC, COHR
