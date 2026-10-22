# Round 7 — which thinkorswim studies and Fibonacci levels help? (2026-10-22)

**Data:** EODHD · 923 S&P 500 members since 2004 (point in time, failed companies included) · TUNE 2005–2016 chooses · JUDGE 2017–2025 only checks.

**Data repair:** 157 files fixed (unadjusted splits, bad one-day prints, re-used tickers cut back to the right company); 29 files too broken to trust were left out: ACS, ANDV, AYE, CBE, CCTYQ, CERN, CFC, CIN, CPRI, EP, FBF, FERG, FL, FLIR, GDW, GR, HMA, HPC, LB, MBI, NBR, PBCT, SOV, TEK, UVN, VAR, WLTW, WWY, X.

**How each study was scored:** buy at the next open after the signal; compare the return over the next 20 and 60 sessions with a RANDOM eligible stock bought the same day (for 'uptrend only' rows: a random uptrend stock). **Edge** = the study's average minus the random pick's, in % points. t = Newey-West t-statistic (≥ 2 is usually 'real'; we required ≥ 2.5 because ~80 versions were tried). Thinkorswim default settings, no tuning.

**A study survives** if in TUNE it has ≥ 200 signals, positive 20- and 60-day edge, 60-day t ≥ 2.5, and a positive 60-day edge in both halves (2005–10 and 2011–16). Judge columns were filled in after the choices were frozen.

**1 of 74 study versions survived the tune screen.**

## 1. Every study, ranked by tune t-statistic (60-day edge)

| Study | Stocks | Signals | Edge 20d | Edge 60d | t (60d) | Halves 60d | Survives | Judge edge 60d | Judge t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ichimoku: close above the cloud | uptrend only | 22,869 | 0.1 | **0.4** | 2.78 | 0.43 / 0.37 | ✅ | -0.5 | -2.62 |
| Close crosses above 50-day | uptrend only | 29,911 | -0.03 | **0.34** | 2.23 | 0.49 / 0.19 | ✗ | -0.27 | -1.56 |
| fake 56% | uptrend only | 1,173 | 0.28 | **0.89** | 1.6 | 1.11 / 0.66 | ✗ | -1.36 | -3.38 |
| Rate of Change(14) crosses 0 | uptrend only | 48,681 | 0.06 | **0.11** | 1.07 | -0.02 / 0.24 | ✗ | -0.09 | -0.61 |
| EMA 8 crosses EMA 21 | uptrend only | 19,013 | -0.05 | **0.13** | 0.95 | 0.08 / 0.18 | ✗ | -0.01 | -0.06 |
| Volume surge up day (2x vol, +2%) | uptrend only | 6,440 | 0.1 | **0.21** | 0.93 | 0.19 / 0.22 | ✗ | -0.36 | -0.85 |
| Williams %R crosses up -80 | any stock | 85,790 | 0.03 | **0.14** | 0.83 | 0.29 / -0.0 | ✗ | -0.11 | -0.62 |
| CCI crosses up -100 | any stock | 73,815 | 0.03 | **0.08** | 0.57 | 0.25 / -0.1 | ✗ | -0.02 | -0.09 |
| Parabolic SAR flips up | uptrend only | 36,458 | 0.03 | **0.05** | 0.55 | 0.05 / 0.04 | ✗ | -0.11 | -0.7 |
| fake 44% | uptrend only | 1,889 | 0.14 | **0.25** | 0.53 | 0.0 / 0.51 | ✗ | -0.26 | -0.47 |
| fib 61.8% | uptrend only | 905 | -0.52 | **0.23** | 0.49 | 0.47 / -0.04 | ✗ | -0.24 | -0.49 |
| MACD crosses zero | uptrend only | 13,404 | -0.06 | **0.08** | 0.42 | -0.02 / 0.17 | ✗ | -0.19 | -0.8 |
| Bollinger: back above lower band | uptrend only | 16,289 | -0.01 | **0.08** | 0.39 | -0.08 / 0.24 | ✗ | 0.01 | 0.04 |
| RSI(14) crosses up 50 | uptrend only | 46,973 | -0.02 | **0.04** | 0.34 | -0.08 / 0.15 | ✗ | -0.12 | -0.85 |
| fake 70% | uptrend only | 701 | 0.36 | **0.25** | 0.29 | 1.98 / -1.92 | ✗ | -1.51 | -1.44 |
| TTM Squeeze fires up | uptrend only | 7,225 | -0.01 | **0.04** | 0.23 | -0.06 / 0.13 | ✗ | -0.19 | -0.75 |
| CCI crosses up -100 | uptrend only | 37,953 | 0.07 | **0.03** | 0.19 | 0.08 / -0.02 | ✗ | -0.08 | -0.46 |
| fib 50% | uptrend only | 1,411 | -0.08 | **0.11** | 0.18 | 0.11 / 0.1 | ✗ | 0.34 | 0.61 |
| fake 56% | any stock | 1,726 | 0.13 | **0.12** | 0.17 | -0.33 / 0.61 | ✗ | -1.52 | -4.13 |
| fib 50% | any stock | 2,026 | 0.05 | **0.09** | 0.16 | -0.65 / 0.92 | ✗ | 0.4 | 0.76 |
| Pocket pivot (vol > any down day in 10) | uptrend only | 70,016 | -0.12 | **0.02** | 0.14 | 0.01 / 0.02 | ✗ | -0.04 | -0.22 |
| Close crosses above 50-day | any stock | 48,629 | -0.02 | **0.02** | 0.13 | -0.3 / 0.34 | ✗ | -0.61 | -3.54 |
| Rate of Change(14) crosses 0 | any stock | 82,556 | 0.03 | **0.01** | 0.11 | -0.12 / 0.14 | ✗ | -0.21 | -1.31 |
| New 52-week high | any stock | 28,000 | -0.16 | **0.03** | 0.08 | 0.04 / 0.02 | ✗ | 0.09 | 0.21 |
| Stochastic %K crosses %D under 20 | any stock | 37,449 | -0.05 | **-0.01** | -0.04 | 0.11 / -0.13 | ✗ | 0.04 | 0.14 |
| OBV new 50-day high | uptrend only | 44,370 | 0.04 | **-0.02** | -0.12 | -0.1 / 0.06 | ✗ | -0.06 | -0.3 |
| Volume surge up day (2x vol, +2%) | any stock | 12,215 | -0.14 | **-0.03** | -0.12 | -0.2 / 0.14 | ✗ | -0.17 | -0.47 |
| New 52-week high | uptrend only | 27,622 | -0.14 | **-0.03** | -0.16 | -0.06 / -0.01 | ✗ | 0.0 | 0.01 |
| Ichimoku: close above the cloud | any stock | 36,673 | -0.01 | **-0.03** | -0.2 | -0.22 / 0.15 | ✗ | -0.57 | -3.04 |
| Chaikin Money Flow crosses 0 | uptrend only | 35,512 | -0.09 | **-0.03** | -0.24 | -0.1 / 0.04 | ✗ | -0.16 | -1.07 |
| MFI crosses up 20 | uptrend only | 2,981 | -0.22 | **-0.12** | -0.36 | 0.38 / -0.54 | ✗ | -0.17 | -0.5 |
| RSI(2) under 10 | any stock | 78,818 | 0.07 | **-0.06** | -0.4 | 0.03 / -0.14 | ✗ | 0.03 | 0.2 |
| Bollinger: back above lower band | any stock | 36,269 | -0.08 | **-0.09** | -0.43 | -0.12 / -0.07 | ✗ | 0.05 | 0.21 |
| Williams %R crosses up -80 | uptrend only | 43,376 | -0.02 | **-0.06** | -0.43 | -0.18 / 0.05 | ✗ | -0.06 | -0.33 |
| Golden cross (50 over 200) | uptrend only | 3,419 | -0.06 | **-0.16** | -0.48 | -0.45 / 0.1 | ✗ | -0.53 | -0.97 |
| Golden cross (50 over 200) | any stock | 3,751 | -0.0 | **-0.17** | -0.53 | -0.38 / 0.03 | ✗ | -0.12 | -0.3 |
| Bollinger: close above upper band | uptrend only | 29,840 | -0.11 | **-0.09** | -0.54 | -0.14 / -0.04 | ✗ | 0.01 | 0.05 |
| DMI: +DI crosses -DI with ADX > 20 | uptrend only | 11,595 | -0.21 | **-0.09** | -0.54 | -0.03 / -0.15 | ✗ | -0.22 | -1.12 |
| MACD crosses signal | uptrend only | 32,585 | -0.08 | **-0.06** | -0.57 | -0.19 / 0.07 | ✗ | 0.0 | 0.01 |
| Gap up 3%+ on 1.5x volume | any stock | 3,875 | -0.04 | **-0.24** | -0.59 | -0.11 / -0.39 | ✗ | 0.22 | 0.4 |
| Keltner: close above upper channel | uptrend only | 41,819 | -0.14 | **-0.08** | -0.61 | -0.15 / -0.02 | ✗ | -0.12 | -0.61 |
| NR7 then close above its high | uptrend only | 41,596 | -0.03 | **-0.07** | -0.68 | -0.18 / 0.04 | ✗ | 0.07 | 0.51 |
| MFI crosses up 20 | any stock | 9,576 | -0.25 | **-0.23** | -0.69 | -0.11 / -0.35 | ✗ | -0.01 | -0.04 |
| fake 70% | any stock | 1,128 | -0.36 | **-0.58** | -0.84 | 0.25 / -1.6 | ✗ | -2.11 | -2.38 |
| fake 44% | any stock | 2,704 | -0.21 | **-0.39** | -0.86 | -0.68 / -0.06 | ✗ | -0.04 | -0.07 |
| fib 78.6% | uptrend only | 491 | -0.15 | **-0.54** | -0.87 | 0.2 / -1.63 | ✗ | 0.05 | 0.08 |
| MACD crosses zero | any stock | 23,201 | 0.04 | **-0.16** | -0.92 | -0.44 / 0.11 | ✗ | -0.5 | -2.46 |
| OBV new 50-day high | any stock | 60,942 | -0.07 | **-0.2** | -0.93 | -0.51 / 0.11 | ✗ | -0.21 | -0.85 |
| RSI(14) crosses up 30 | any stock | 13,681 | -0.32 | **-0.41** | -0.95 | 0.25 / -1.07 | ✗ | 0.24 | 0.5 |
| Inside day then close above its high | uptrend only | 31,275 | -0.13 | **-0.12** | -0.97 | -0.17 / -0.07 | ✗ | -0.08 | -0.58 |
| fake 30% | uptrend only | 3,300 | -0.04 | **-0.42** | -0.99 | -0.99 / 0.14 | ✗ | -1.69 | -3.91 |
| Gap up 3%+ on 1.5x volume | uptrend only | 1,738 | 0.22 | **-0.37** | -1.02 | -0.27 / -0.48 | ✗ | 0.21 | 0.29 |
| RSI(2) under 10 | uptrend only | 40,358 | 0.08 | **-0.11** | -1.06 | -0.12 / -0.1 | ✗ | -0.22 | -1.59 |
| MACD crosses signal | any stock | 54,555 | -0.11 | **-0.14** | -1.1 | -0.25 / -0.02 | ✗ | -0.0 | -0.01 |
| EMA 8 crosses EMA 21 | any stock | 32,004 | 0.01 | **-0.14** | -1.17 | -0.27 / -0.01 | ✗ | -0.38 | -1.93 |
| Parabolic SAR flips up | any stock | 61,427 | -0.13 | **-0.18** | -1.18 | -0.19 / -0.17 | ✗ | -0.23 | -1.41 |
| fib 61.8% | any stock | 1,341 | -0.7 | **-0.82** | -1.19 | -0.91 / -0.72 | ✗ | -0.58 | -1.1 |
| Donchian 20-day breakout | uptrend only | 46,894 | -0.19 | **-0.19** | -1.24 | -0.23 / -0.15 | ✗ | 0.08 | 0.38 |
| Chaikin Money Flow crosses 0 | any stock | 62,858 | 0.0 | **-0.13** | -1.28 | -0.26 / 0.0 | ✗ | -0.16 | -1.44 |
| TTM Squeeze fires up | any stock | 11,107 | -0.22 | **-0.3** | -1.35 | -0.74 / 0.14 | ✗ | -0.43 | -1.76 |
| NR7 then close above its high | any stock | 68,462 | -0.06 | **-0.15** | -1.35 | -0.44 / 0.14 | ✗ | 0.04 | 0.21 |
| fake 30% | any stock | 4,267 | -0.34 | **-0.64** | -1.39 | -1.48 / 0.22 | ✗ | -1.63 | -3.75 |
| Pocket pivot (vol > any down day in 10) | any stock | 99,693 | -0.13 | **-0.31** | -1.47 | -0.54 / -0.08 | ✗ | -0.23 | -0.99 |
| RSI(14) crosses up 50 | any stock | 77,682 | 0.02 | **-0.17** | -1.49 | -0.43 / 0.09 | ✗ | -0.3 | -1.99 |
| DMI: +DI crosses -DI with ADX > 20 | any stock | 19,912 | -0.14 | **-0.25** | -1.51 | -0.4 / -0.11 | ✗ | -0.32 | -1.68 |
| fib 78.6% | any stock | 848 | -0.43 | **-1.46** | -1.65 | -0.32 / -3.04 | ✗ | -1.12 | -1.73 |
| RSI(14) crosses up 30 | uptrend only | 2,241 | -0.53 | **-0.74** | -1.71 | -1.23 / -0.35 | ✗ | 0.13 | 0.31 |
| fib 38.2% | uptrend only | 2,392 | -0.25 | **-0.64** | -1.73 | -0.82 / -0.47 | ✗ | -0.38 | -0.72 |
| Inside day then close above its high | any stock | 50,551 | -0.18 | **-0.25** | -1.98 | -0.42 / -0.08 | ✗ | -0.23 | -1.23 |
| Keltner: close above upper channel | any stock | 60,930 | -0.23 | **-0.41** | -2.02 | -0.67 / -0.16 | ✗ | -0.43 | -1.68 |
| fib 38.2% | any stock | 3,338 | -0.1 | **-0.92** | -2.1 | -1.11 / -0.71 | ✗ | -0.49 | -1.0 |
| Stochastic %K crosses %D under 20 | uptrend only | 14,209 | -0.14 | **-0.55** | -2.25 | -0.6 / -0.5 | ✗ | -0.04 | -0.19 |
| Bollinger: close above upper band | any stock | 44,675 | -0.31 | **-0.55** | -2.47 | -0.74 / -0.37 | ✗ | -0.27 | -1.15 |
| Donchian 20-day breakout | any stock | 68,688 | -0.27 | **-0.59** | -2.58 | -0.78 / -0.41 | ✗ | -0.18 | -0.74 |

## 2. Fibonacci vs made-up levels

Same swing, same turn-up rule, same stop logic — only the level differs. If the Fibonacci rows don't beat the made-up rows, the Fibonacci numbers carry no extra information.

| Level | Stocks | Signals (tune) | Edge 60d tune | t | Edge 60d judge | t | Hit rate 60d (tune) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fake 30% | any stock | 4,267 | -0.64 | -1.39 | -1.63 | -3.75 | 48.9% |
| **fib 38.2%** | any stock | 3,338 | -0.92 | -2.1 | -0.49 | -1.0 | 47.0% |
| fake 44% | any stock | 2,704 | -0.39 | -0.86 | -0.04 | -0.07 | 49.6% |
| **fib 50%** | any stock | 2,026 | 0.09 | 0.16 | 0.4 | 0.76 | 52.0% |
| fake 56% | any stock | 1,726 | 0.12 | 0.17 | -1.52 | -4.13 | 51.8% |
| **fib 61.8%** | any stock | 1,341 | -0.82 | -1.19 | -0.58 | -1.1 | 50.3% |
| fake 70% | any stock | 1,128 | -0.58 | -0.84 | -2.11 | -2.38 | 52.0% |
| **fib 78.6%** | any stock | 848 | -1.46 | -1.65 | -1.12 | -1.73 | 50.1% |
| fake 30% | uptrend only | 3,300 | -0.42 | -0.99 | -1.69 | -3.91 | 49.3% |
| **fib 38.2%** | uptrend only | 2,392 | -0.64 | -1.73 | -0.38 | -0.72 | 46.3% |
| fake 44% | uptrend only | 1,889 | 0.25 | 0.53 | -0.26 | -0.47 | 49.7% |
| **fib 50%** | uptrend only | 1,411 | 0.11 | 0.18 | 0.34 | 0.61 | 52.5% |
| fake 56% | uptrend only | 1,173 | 0.89 | 1.6 | -1.36 | -3.38 | 53.1% |
| **fib 61.8%** | uptrend only | 905 | 0.23 | 0.49 | -0.24 | -0.49 | 50.3% |
| fake 70% | uptrend only | 701 | 0.25 | 0.29 | -1.51 | -1.44 | 52.4% |
| **fib 78.6%** | uptrend only | 491 | -0.54 | -0.87 | 0.05 | 0.08 | 48.9% |

*Any stock:* average tune 60-day edge — Fibonacci levels -0.78 vs made-up levels -0.37.

*Uptrend only:* average tune 60-day edge — Fibonacci levels -0.21 vs made-up levels +0.24.

## 4. Portfolio test (10 slots, 1% risk, idle money in SPY, 0.07% cost per side)

SPY: tune 7.5%/yr (max DD -55.2%), judge 14.9%/yr (max DD -33.7%). RANDOM = random uptrend stocks with the same exits — the bar a study must clear.

| Entry | Stocks | Exit | S&P > 200-day gate | Tune CAGR | Tune vs SPY | Tune DD | Judge CAGR (vs SPY) | Bootstrap % | Judge DD | 2026 vs SPY | Passes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ichimoku: close above the cloud | uptrend only | original stop | no | 6.0% | -0.9 | -57.8% | – (–) | – | – | – |  |
| Ichimoku: close above the cloud | uptrend only | original stop | yes | 9.4% | 0.6 | -56.9% | 8.5% (-6.4) | 2.0 | -33.0% | -11.8 | ✗ |
| Ichimoku: close above the cloud | uptrend only | 50-day exit | no | 6.5% | -0.3 | -59.8% | 6.5% (-8.4) | 1.0 | -34.4% | -6.5 | ✗ |
| Ichimoku: close above the cloud | uptrend only | 50-day exit | yes | 8.3% | 1.3 | -56.3% | 9.2% (-5.7) | 2.0 | -35.8% | -9.7 | ✗ |
| RANDOM | uptrend only | original stop | no | 6.9% | -2.8 | -46.2% | 5.2% (-9.7) | 0.0 | -33.1% | -12.7 | ✗ |
| RANDOM | uptrend only | original stop | yes | 6.5% | -2.0 | -50.3% | 9.0% (-5.9) | 3.0 | -31.2% | -9.3 | ✗ |
| RANDOM | uptrend only | 50-day exit | no | 6.8% | 1.0 | -46.7% | 9.6% (-5.3) | 2.0 | -33.1% | -27.5 | ✗ |
| RANDOM | uptrend only | 50-day exit | yes | 6.0% | -0.6 | -53.7% | 10.4% (-4.5) | 5.0 | -31.7% | -23.4 | ✗ |

_Edges are averages per signal over 20 / 60 trading days (≈ 1 / 3 months), not yearly returns. Generated by scripts/backtest/run_round7.py from privately held EODHD data (not in this repo)._
