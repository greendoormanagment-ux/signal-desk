# Candidate growth systems — round 1 (2026-10-12)

2,056 stocks, Oct 2017 – today. Every system buys at the next day's open after a signal. Portfolio = $100k, 8 positions, 1% risk per trade, max 2 per sector, ranked by RS. "Range" = 10 runs with random tie-breaking (how much luck matters).

**Two universes.** *broad* = stocks worth $2B+ today; it includes today's winners in the past, so it flatters everything (survivorship bias). *sp500* = a stock only counts while it was actually in the S&P 500, which is a fairer test. About 19% of past members have no free price history (mostly buyouts), so it is less biased, not bias-free.

**Pass bar (set before the run):** at least 300 trades, at least +0.3R per trade in both halves, a smaller drawdown than SPY, and beating SPY in 2022–26.

| Benchmark | Full CAGR | Max drawdown | 2022–26 CAGR |
| --- | --- | --- | --- |
| SPY buy-and-hold | 13.2% | -34.1% | 10.8% |
| SPY 200-day rule | 8.6% | -22.0% | 6.8% |

## Universe: broad

| System | Variant | Trades | Win % | Avg R (2017–21 / 2022–26) | Avg win / loss R | Portfolio CAGR, full (range) | Max DD | 2022–26 CAGR (range) | Pass? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| leader breakout | base: RS85, EPS25+sales20, tight 10-day range, 1.5x vol; 1/3 at +2R, rest on 50-day | 415 | 26.0 | -0.23 / 0.34 | 2.87 / -0.93 | 0.0% (-0.5 to 0.2) | -51.2% | 6.0% (5.5 to 6.8) | no |
| leader breakout | no partial (all on 50-day exit) | 415 | 21.9 | -0.32 / 0.58 | 4.0 / -0.96 | 0.8% (0.2 to 1.2) | -55.9% | 8.9% (8.5 to 10.8) | no |
| leader breakout | sell 1/2 at +2R | 415 | 30.1 | -0.19 / 0.23 | 2.36 / -0.99 | -0.6% (-0.8 to -0.3) | -48.7% | 4.0% (3.7 to 4.0) | no |
| leader breakout | partial at +3R | 415 | 26.3 | -0.22 / 0.39 | 3.06 / -0.97 | 1.1% (0.9 to 1.4) | -51.2% | 7.4% (7.0 to 7.6) | no |
| leader breakout | no time stop | 414 | 26.1 | -0.25 / 0.33 | 2.88 / -0.96 | -0.1% (-0.3 to 0.3) | -51.5% | 5.8% (5.6 to 6.5) | no |
| leader breakout | stop to breakeven after partial | 415 | 30.1 | -0.22 / 0.2 | 2.25 / -0.99 | -0.6% (-1.0 to -0.5) | -52.6% | 5.4% (5.0 to 6.2) | no |
| leader breakout | runner on 21-day EMA | 428 | 28.5 | -0.04 / -0.02 | 2.14 / -0.9 | -1.1% (-1.5 to -0.9) | -43.5% | 0.7% (0.2 to 0.8) | no |
| leader breakout | runner on 3x ATR trail | 433 | 29.3 | -0.02 / -0.09 | 1.89 / -0.86 | -2.8% (-3.2 to -2.4) | -42.7% | -3.4% (-3.8 to -3.3) | no |
| leader breakout | needs EPS acceleration | 193 | 25.4 | -0.32 / 0.14 | 2.43 / -0.96 | -1.7% (-2.0 to -1.6) | -35.0% | 1.6% (1.4 to 1.6) | no |
| leader breakout | RS >= 70 | 625 | 27.2 | -0.12 / 0.24 | 2.63 / -0.92 | 2.1% (1.1 to 2.6) | -36.9% | 5.2% (4.3 to 6.3) | no |
| leader breakout | EPS only (no sales filter) | 984 | 26.1 | -0.26 / 0.18 | 2.42 / -0.9 | -7.0% (-7.4 to -6.4) | -65.1% | -2.2% (-3.1 to 0.9) | no |
| leader breakout | looser base (10-day range <= 20%) | 649 | 25.4 | -0.18 / 0.55 | 3.53 / -0.91 | -3.0% (-3.9 to -2.3) | -59.5% | 1.1% (-1.0 to 2.1) | no |
| leader breakout | no market gate | 460 | 25.7 | -0.21 / 0.24 | 2.83 / -0.94 | -1.3% (-1.8 to -0.9) | -56.7% | 3.9% (3.5 to 4.6) | no |
| leader breakout | 5 positions max | 415 | 26.0 | -0.23 / 0.34 | 2.87 / -0.93 | 0.0% (-0.9 to 0.7) | -48.4% | 4.8% (4.1 to 6.2) | no |
| earnings gap | base: gap 4%+, up 5%+, 3x vol, upper half, above 200-day; stop gap low; 1/3 at +2R, rest on 21-day EMA | 1,094 | 36.9 | 0.18 / 0.08 | 1.69 / -0.8 | 3.2% (1.6 to 4.6) | -21.5% | 2.8% (0.9 to 4.4) | no |
| earnings gap | runner on 50-day | 1,084 | 33.5 | 0.34 / 0.23 | 2.44 / -0.82 | 7.5% (5.7 to 11.1) | -20.8% | 9.2% (3.0 to 12.2) | no |
| earnings gap | no partial | 1,094 | 35.9 | 0.19 / 0.11 | 1.85 / -0.82 | 2.8% (1.4 to 4.9) | -20.2% | 4.2% (0.2 to 6.1) | no |
| earnings gap | no time stop | 1,094 | 37.5 | 0.17 / 0.1 | 1.73 / -0.84 | 2.9% (1.6 to 3.7) | -21.1% | 4.0% (-0.7 to 7.8) | no |
| earnings gap | RS >= 70 | 762 | 37.9 | 0.16 / 0.12 | 1.67 / -0.8 | 0.4% (-0.8 to 2.1) | -21.2% | 0.7% (-1.2 to 2.0) | no |
| earnings gap | volume 2x | 1,720 | 36.5 | 0.11 / 0.03 | 1.58 / -0.82 | 1.4% (-1.9 to 2.6) | -24.9% | 1.1% (-0.5 to 4.7) | no |
| earnings gap | no 200-day filter | 1,272 | 36.7 | 0.21 / 0.08 | 1.75 / -0.8 | 3.2% (1.2 to 4.5) | -21.2% | 4.0% (0.6 to 6.5) | no |
| leader pullback | base: RS90, EPS25, tag 21-EMA on light volume, close > prior high; stop pullback low; 1/3 at +2R, rest on 21-EMA | 2,845 | 31.1 | -0.01 / 0.0 | 1.38 / -0.63 | 0.7% (-1.9 to 2.2) | -40.7% | 0.7% (-4.4 to 4.5) | no |
| leader pullback | runner on 50-day | 2,302 | 32.2 | 0.01 / 0.14 | 1.89 / -0.78 | 3.4% (1.6 to 8.7) | -39.7% | 5.3% (0.3 to 14.6) | no |
| leader pullback | no partial | 2,845 | 30.0 | -0.01 / 0.01 | 1.49 / -0.63 | 3.5% (0.6 to 5.2) | -36.5% | 2.8% (-2.8 to 6.7) | no |
| leader pullback | RS >= 80 | 6,583 | 31.7 | 0.02 / 0.02 | 1.34 / -0.59 | 2.3% (0.3 to 9.2) | -39.5% | -3.4% (-5.6 to 3.5) | no |
| leader pullback | no EPS filter | 7,349 | 31.4 | 0.05 / 0.05 | 1.53 / -0.63 | 6.7% (-0.6 to 9.6) | -47.9% | -1.2% (-10.3 to 3.5) | no |
| combined | base: breakout + earnings gap + pullback in one 8-slot portfolio; all exits on the 50-day | 6,535 | 28.7 | 0.17 / 0.26 | 2.83 / -0.83 | 17.1% (7.5 to 31.2) | -36.1% | 16.2% (1.9 to 38.5) | no |
| combined | 12 slots | 6,535 | 28.7 | 0.17 / 0.26 | 2.83 / -0.83 | 15.8% (8.7 to 26.7) | -37.7% | 18.2% (8.8 to 44.0) | no |
| momentum | momentum top 10 | 1,080 holdings | 51.2 | – | – | 47.1% | -47.5% | 56.9% | – |
| momentum | momentum top 10 + SPY 200-day regime | 880 holdings | 47.0 | – | – | 16.8% | -49.0% | 20.2% | – |
| momentum | momentum top 20 | 2,160 holdings | 52.6 | – | – | 43.8% | -42.7% | 52.9% | – |

## Universe: sp500

| System | Variant | Trades | Win % | Avg R (2017–21 / 2022–26) | Avg win / loss R | Portfolio CAGR, full (range) | Max DD | 2022–26 CAGR (range) | Pass? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| leader breakout | base: RS85, EPS25+sales20, tight 10-day range, 1.5x vol; 1/3 at +2R, rest on 50-day | 113 | 26.5 | -0.35 / 0.9 | 3.36 / -0.96 | 0.6% (0.6 to 0.6) | -34.9% | 5.5% (5.5 to 5.6) | no |
| leader breakout | no partial (all on 50-day exit) | 113 | 23.0 | -0.45 / 1.4 | 4.83 / -1.0 | 1.3% (1.3 to 1.3) | -39.4% | 8.2% (8.2 to 8.3) | no |
| leader breakout | sell 1/2 at +2R | 113 | 31.0 | -0.3 / 0.65 | 2.63 / -1.03 | 0.2% (0.1 to 0.2) | -32.8% | 4.1% (4.1 to 4.2) | no |
| leader breakout | partial at +3R | 113 | 26.5 | -0.35 / 0.91 | 3.53 / -1.02 | 0.5% (0.4 to 0.5) | -36.8% | 5.3% (5.3 to 5.4) | no |
| leader breakout | no time stop | 113 | 25.7 | -0.4 / 0.89 | 3.47 / -1.0 | 0.2% (0.1 to 0.2) | -36.8% | 5.4% (5.4 to 5.5) | no |
| leader breakout | stop to breakeven after partial | 113 | 31.0 | -0.32 / 0.5 | 2.39 / -1.03 | 0.0% (-0.0 to -0.0) | -35.6% | 4.1% (4.1 to 4.2) | no |
| leader breakout | runner on 21-day EMA | 117 | 26.5 | -0.07 / 0.08 | 2.43 / -0.88 | -0.7% (-0.7 to -0.7) | -26.3% | 0.4% (0.4 to 0.4) | no |
| leader breakout | runner on 3x ATR trail | 117 | 28.2 | 0.0 / -0.06 | 2.15 / -0.88 | -0.9% (-0.9 to -0.9) | -25.8% | -0.7% (-0.7 to -0.7) | no |
| leader breakout | needs EPS acceleration | 61 | 23.0 | -0.37 / 0.72 | 3.64 / -0.94 | 0.8% (0.8 to 0.8) | -22.7% | 3.7% (3.7 to 3.7) | no |
| leader breakout | RS >= 70 | 213 | 30.5 | -0.04 / 0.62 | 2.82 / -0.91 | 2.0% (1.9 to 2.3) | -23.6% | 6.8% (6.7 to 6.8) | no |
| leader breakout | EPS only (no sales filter) | 313 | 29.1 | -0.29 / 0.43 | 2.33 / -0.87 | -2.5% (-2.8 to -2.0) | -51.2% | 4.5% (4.1 to 4.8) | no |
| leader breakout | looser base (10-day range <= 20%) | 167 | 25.1 | -0.32 / 0.42 | 2.79 / -0.9 | -1.4% (-1.4 to -1.3) | -41.8% | 2.0% (2.0 to 2.1) | no |
| leader breakout | no market gate | 126 | 26.2 | -0.29 / 0.64 | 3.3 / -0.98 | 0.4% (0.2 to 0.5) | -35.6% | 4.2% (4.2 to 4.3) | no |
| leader breakout | 5 positions max | 113 | 26.5 | -0.35 / 0.9 | 3.36 / -0.96 | 0.7% (0.6 to 0.7) | -34.4% | 5.5% (5.5 to 5.6) | no |
| earnings gap | base: gap 4%+, up 5%+, 3x vol, upper half, above 200-day; stop gap low; 1/3 at +2R, rest on 21-day EMA | 362 | 36.7 | 0.26 / -0.01 | 1.64 / -0.79 | 3.3% (2.8 to 3.7) | -23.3% | 1.5% (0.8 to 2.0) | no |
| earnings gap | runner on 50-day | 360 | 31.1 | 0.23 / -0.05 | 1.94 / -0.78 | 3.2% (2.8 to 3.7) | -27.5% | 1.9% (1.4 to 2.5) | no |
| earnings gap | no partial | 362 | 35.6 | 0.29 / -0.01 | 1.8 / -0.82 | 3.8% (3.2 to 4.1) | -24.4% | 3.2% (2.4 to 3.6) | no |
| earnings gap | no time stop | 362 | 37.3 | 0.27 / 0.03 | 1.72 / -0.82 | 3.2% (2.8 to 3.9) | -18.0% | 1.8% (0.9 to 2.3) | no |
| earnings gap | RS >= 70 | 215 | 36.7 | 0.26 / -0.11 | 1.47 / -0.77 | 0.7% (0.7 to 0.9) | -17.7% | -1.2% (-1.3 to -1.2) | no |
| earnings gap | volume 2x | 631 | 36.3 | 0.16 / -0.07 | 1.48 / -0.83 | 0.6% (-0.4 to 1.8) | -30.9% | -2.5% (-4.1 to -1.3) | no |
| earnings gap | no 200-day filter | 407 | 37.6 | 0.32 / 0.02 | 1.71 / -0.79 | 5.1% (4.7 to 5.8) | -22.5% | 2.5% (2.0 to 3.4) | no |
| leader pullback | base: RS90, EPS25, tag 21-EMA on light volume, close > prior high; stop pullback low; 1/3 at +2R, rest on 21-EMA | 741 | 32.4 | -0.08 / 0.05 | 1.23 / -0.61 | -0.5% (-1.5 to 0.2) | -37.0% | 4.2% (2.8 to 5.6) | no |
| leader pullback | runner on 50-day | 608 | 32.4 | -0.16 / 0.17 | 1.6 / -0.77 | -0.4% (-0.9 to 0.3) | -38.3% | 3.5% (2.1 to 3.9) | no |
| leader pullback | no partial | 741 | 31.6 | -0.09 / 0.07 | 1.3 / -0.62 | 0.6% (-0.7 to 1.2) | -36.4% | 5.5% (4.1 to 7.1) | no |
| leader pullback | RS >= 80 | 2,320 | 32.6 | 0.01 / 0.0 | 1.22 / -0.58 | -0.3% (-1.6 to 1.9) | -36.2% | 3.5% (-0.1 to 4.7) | no |
| leader pullback | no EPS filter | 1,318 | 33.3 | -0.02 / 0.06 | 1.3 / -0.62 | 3.8% (1.4 to 5.3) | -33.8% | 10.1% (7.5 to 12.7) | no |
| combined | base: breakout + earnings gap + pullback in one 8-slot portfolio; all exits on the 50-day | 1,346 | 29.6 | 0.01 / 0.17 | 2.28 / -0.82 | -0.4% (-4.2 to 1.3) | -43.0% | -1.0% (-3.1 to 8.3) | no |
| combined | 12 slots | 1,346 | 29.6 | 0.01 / 0.17 | 2.28 / -0.82 | -0.4% (-4.2 to 1.2) | -43.0% | -1.0% (-3.1 to 8.3) | no |
| momentum | momentum top 10 | 1,080 holdings | 54.4 | – | – | 18.5% | -41.1% | 32.4% | – |
| momentum | momentum top 10 + SPY 200-day regime | 880 holdings | 49.9 | – | – | 1.8% | -55.3% | 10.8% | – |
| momentum | momentum top 20 | 2,160 holdings | 54.1 | – | – | 16.8% | -39.7% | 26.2% | – |

## Year by year (portfolio return %)

| | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPY | 4.5 | -6.3 | 28.8 | 16.2 | 27.0 | -19.5 | 24.3 | 23.3 | 16.4 | 14.2 |
| broad · combined | 3.8 | 7.0 | -0.4 | 27.6 | 30.3 | -27.4 | -6.3 | 85.8 | 21.7 | 23.7 |
| broad · momentum rotation | -9.6 | -19.9 | 103.1 | 66.9 | 47.9 | 21.9 | 25.9 | 16.4 | 147.9 | 98.8 |
| sp500 · combined | -1.1 | -1.3 | 9.9 | 7.3 | -4.2 | -21.9 | -5.4 | 9.8 | -0.1 | 12.7 |
| sp500 · momentum rotation | -2.3 | -21.6 | 37.4 | 12.4 | 0.7 | -1.5 | 20.4 | 21.0 | 28.0 | 110.0 |
