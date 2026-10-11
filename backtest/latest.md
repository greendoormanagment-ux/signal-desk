# Signal Desk backtest — 2026-10-11

Live entry rules (v2.9.7) + stop rule A2 replayed on 2,030 stocks (1,664 with SEC EPS history), Oct 2017 – today. Buys fill at the next day's open. Universe: US stocks >= $2.0B market cap today (survivorship-biased).

**Read with care:** the universe is today's stocks, so companies that failed or were delisted are missing (survivorship bias, Fix List #69). That flatters every variant, most of all the ones that hold winners longer. Portfolio figures are the median of 10 runs with random tie-breaking among same-day buys; the range shows how much luck matters.

## Benchmarks

| Period | SPY buy-and-hold CAGR | max drawdown | SPY 200-day rule CAGR | max drawdown |
| --- | --- | --- | --- | --- |
| full 2017-2026 | 13.2% | -34.1% | 8.6% | -22.0% |
| in-sample 2017-2021 | 15.9% | -34.1% | 10.5% | -20.0% |
| out-of-sample 2022-2026 | 10.8% | -25.4% | 6.8% | -22.2% |

## Variants (one change at a time vs the live rules)

Avg R = average result per trade in units of the initial risk (0.10 = earns 10% of what it risks). Portfolio = $100k, 10 positions max, 1% risk per trade.

| Variant | Trades | Win % | Avg R (in / out of sample) | Profit factor | Portfolio CAGR median (range), full | Out-of-sample CAGR median (range) |
| --- | --- | --- | --- | --- | --- | --- |
| base (live rules v2.9.7) | 18,314 | 26.1 | 0.09 / 0.08 | 1.2 | 3.3% (-3.3 to 7.6) | -0.2% (-9.4 to 7.2) |
| block buys in PRESSURE (#53) | 8,955 | 25.5 | 0.02 / 0.07 | 1.1 | 1.1% (-5.4 to 2.5) | 3.2% (-5.4 to 8.7) |
| require RS pass | 10,351 | 27.2 | 0.12 / 0.06 | 1.19 | 2.9% (-2.2 to 7.1) | -0.9% (-8.9 to 6.9) |
| pullback: 0 to +3% above a RISING 50-day (#31) | 12,050 | 27.1 | 0.09 / 0.07 | 1.18 | 3.0% (-1.3 to 6.6) | 0.6% (-3.0 to 8.3) |
| pullback: also needs below-avg volume | 16,046 | 26.5 | 0.08 / 0.09 | 1.19 | 2.9% (-4.2 to 7.1) | -1.9% (-6.6 to 6.2) |
| breakouts only | 3,640 | 26.8 | 0.03 / 0.1 | 1.13 | -0.9% (-4.5 to 1.1) | -0.9% (-5.1 to 1.8) |
| pullbacks only | 16,828 | 26.0 | 0.09 / 0.09 | 1.2 | 3.4% (-1.3 to 8.5) | 4.2% (-2.1 to 8.7) |
| breakout volume 1.0x | 19,023 | 26.0 | 0.08 / 0.08 | 1.19 | 2.2% (-0.2 to 6.9) | 0.1% (-3.5 to 10.6) |
| breakout volume 2.0x | 17,612 | 26.2 | 0.09 / 0.09 | 1.2 | 2.2% (0.0 to 9.2) | 0.6% (-3.5 to 7.4) |
| EPS growth >= 15% | 21,252 | 26.5 | 0.1 / 0.09 | 1.22 | 5.5% (-4.2 to 8.7) | 0.3% (-4.5 to 9.6) |
| EPS growth >= 40% | 15,074 | 25.8 | 0.07 / 0.09 | 1.19 | 0.1% (-4.2 to 7.6) | 3.0% (-4.5 to 5.4) |
| EPS >= 25% AND sales >= 15% | 8,285 | 26.0 | 0.09 / 0.09 | 1.2 | 4.9% (3.5 to 10.4) | 3.7% (-1.9 to 17.5) |
| earnings block 7 days | 19,309 | 26.1 | 0.09 / 0.08 | 1.2 | 4.0% (-0.1 to 7.6) | -0.0% (-8.4 to 10.1) |
| no earnings block | 20,485 | 26.2 | 0.1 / 0.08 | 1.2 | 1.7% (-5.1 to 6.1) | -0.7% (-7.3 to 4.7) |
| stop: original only (no trail) | 10,007 | 22.0 | 0.15 / 0.84 | 1.78 | 4.0% (0.4 to 12.6) | 6.9% (0.4 to 26.0) |
| stop: breakeven at +1R, no trail | 12,734 | 12.8 | 0.09 / 0.57 | 1.75 | 4.2% (-0.7 to 10.5) | 5.9% (-2.2 to 15.0) |
| stop: 3xATR trail from day 1 | 23,348 | 35.7 | 0.06 / 0.05 | 1.16 | 0.5% (-3.1 to 4.6) | -0.8% (-11.8 to 12.6) |
| stop: A2 with 2xATR trail | 18,849 | 26.9 | 0.07 / 0.07 | 1.16 | 1.1% (-3.3 to 5.2) | -1.8% (-7.0 to 1.8) |
| stop: A2 with 4xATR trail | 17,686 | 24.8 | 0.09 / 0.11 | 1.24 | 5.6% (-0.7 to 8.7) | 0.0% (-5.3 to 5.5) |
| exit: close 2% under 50-day | 24,573 | 27.6 | 0.05 / 0.09 | 1.25 | 6.8% (-3.5 to 13.7) | 6.6% (1.9 to 20.1) |
| RS rank >= 80 (IBD-style, vs all stocks) | 7,101 | 26.5 | 0.08 / 0.09 | 1.19 | -0.2% (-2.0 to 8.1) | 2.0% (-8.9 to 11.0) |
| RS rank >= 90 | 3,439 | 25.0 | 0.07 / 0.09 | 1.16 | -0.6% (-2.3 to 4.9) | -0.6% (-6.8 to 6.1) |
| Minervini trend template | 11,554 | 27.6 | 0.1 / 0.1 | 1.21 | 2.5% (-1.2 to 8.2) | 0.1% (-6.5 to 9.4) |
| market gate: SPY above 200-day only | 18,224 | 25.7 | 0.08 / 0.07 | 1.17 | -0.7% (-5.0 to 3.2) | -1.4% (-11.1 to 4.0) |

## Do the ratings predict anything? (20 trading days, vs SPY)

First-time signals and rating changes only.

| Rating | Signals | Avg vs SPY, 20 days |
| --- | --- | --- |
| BUY | 41,635 | -0.15% |
| CHECK_FIRST | 41,744 | -0.02% |
| DONT_BUY | 133,493 | +0.16% |
| SELL | 39,525 | +0.23% |
| WATCH | 57,312 | -0.03% |

## BUY signals broken down (20 days vs SPY)

| Group | Signals | Avg | Median |
| --- | --- | --- | --- |
| setup: BREAKOUT | 5,655 | -0.04% | -0.45% |
| setup: PULLBACK | 35,980 | -0.16% | -0.63% |
| market: PRESSURE | 29,374 | -0.16% | -0.58% |
| market: UPTREND | 12,261 | -0.12% | -0.68% |
| rs: fail | 9,094 | -0.02% | -0.55% |
| rs: neutral | 12,151 | -0.04% | -0.57% |
| rs: pass | 20,390 | -0.27% | -0.67% |
| rsrank: (0, 50] | 10,120 | -0.38% | -0.76% |
| rsrank: (50, 70] | 11,758 | -0.21% | -0.55% |
| rsrank: (70, 80] | 6,854 | -0.07% | -0.47% |
| rsrank: (80, 90] | 7,294 | -0.07% | -0.56% |
| rsrank: (90, 100] | 5,609 | +0.24% | -0.59% |

## Base trades: exits and years

| Exit reason | Trades | Avg return | Avg R |
| --- | --- | --- | --- |
| 7.5% loss rule | 577 | -7.92% | -0.87 |
| open at end | 270 | +3.99% | +0.63 |
| stage 4 | 1,972 | -1.75% | -0.22 |
| stop | 13,469 | +1.21% | +0.16 |
| stop (gap) | 2,026 | +0.84% | +0.10 |

| Year | Trades | Win % | Avg R |
| --- | --- | --- | --- |
| 2017 | 497 | 30.0 | +0.25 |
| 2018 | 1,810 | 22.5 | -0.07 |
| 2019 | 1,420 | 30.6 | +0.24 |
| 2020 | 1,318 | 30.3 | +0.25 |
| 2021 | 3,721 | 24.6 | +0.02 |
| 2022 | 1,090 | 14.5 | -0.34 |
| 2023 | 1,795 | 25.0 | +0.10 |
| 2024 | 2,436 | 30.8 | +0.26 |
| 2025 | 1,888 | 28.5 | +0.22 |
| 2026 | 2,339 | 24.7 | -0.03 |

Average best point reached (MFE): 1.42R · average worst point (MAE): -0.52R · losing trades that were up at least +1R first: 31.6%.
