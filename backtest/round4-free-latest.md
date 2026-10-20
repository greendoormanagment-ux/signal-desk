# Round 4 — fixing the weaknesses (2026-10-20)

**Data:** free (Yahoo, survivorship-limited) · 657 S&P 500 members (point in time), 633 with SEC EPS history · cost 0.07% per side · signals at the close, filled next open.
**Periods:** TUNE 2017-10-15 → 2021-12-31 · JUDGE (unseen) 2022-01-01 → 2025-12-31 · 2026 shown alone.

**Pass bar (Playbook §4):** better average result per trade after costs than the live rules in BOTH periods, drawdown no worse (2-pt tolerance), at least 100 trades in the judge period. Beating SPY is not required — but it is shown.

> ⚠ **Free data:** companies that failed or were bought out are missing, so every result is flattered. Treat this as a preview; the EODHD run is the real test.

| SPY | CAGR | max drawdown |
| --- | --- | --- |
| tune | 15.9% | -34.1% |
| judge | 9.3% | -25.4% |
| 2026 | 16.0% | -9.1% |

Regime in the judge period: full size 24.6% of days · half 47.4% · no new buys 28.0%.

## Results

Avg R = average result per trade in units of the risk taken, after costs (0.10 = earned 10% of what it risked). Gave back = how many R a trade that reached +1R gave back before it was sold (lower = better selling). Portfolio = $100k, 10 positions, 1% risk each (half/none under regime sizing).

| Variant | Trades (tune / judge) | Avg R tune | Avg R judge | Win % judge | Gave back (R) | Portfolio CAGR judge (MC range) | Max DD judge | vs SPY judge | Passes bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base: live rules (v2.9.7 entries, stop A2) | 3113 / 2178 | 0.089 | **0.101** | 27.1 | 1.35 | 10.9% (3.9 to 8.8) | -21.6% | 1.6 pts | — |
| exit: original stop only (no trail) | 1685 / 1172 | 0.073 | **1.065** | 24.5 | 4.51 | 9.7% (8.3 to 16.5) | -17.8% | 0.4 pts | ✗ |
| exit: close 2% under 50-day | 4672 / 3089 | 0.014 | **0.078** | 26.2 | 1.92 | 9.8% (4.1 to 10.9) | -26.8% | 0.5 pts | ✗ |
| exit: 50-day break on volume | 4344 / 2861 | 0.047 | **0.046** | 30.7 | 1.3 | 2.3% (2.4 to 14.2) | -29.8% | -7.0 pts | ✗ |
| exit: sell into a climax run | 3137 / 2193 | 0.093 | **0.094** | 27.1 | 1.2 | 9.0% (2.6 to 10.6) | -23.5% | -0.3 pts | ✗ |
| exit: cut failed breakouts (-2% within 20 days) | 4392 / 2986 | 0.048 | **0.061** | 19.5 | 1.39 | 6.6% (2.6 to 11.8) | -24.9% | -2.7 pts | ✗ |
| exit: O'Neil 8-week hold after +20% in 3 weeks | 3101 / 2172 | 0.095 | **0.097** | 27.0 | 1.38 | 8.1% (2.3 to 12.6) | -21.6% | -1.2 pts | ✗ |
| exit: full sell playbook (all four) | 5336 / 3515 | 0.027 | **0.031** | 24.8 | 1.24 | 0.0% (2.4 to 9.0) | -29.5% | -9.3 pts | ✗ |
| exit: sell playbook + no trail | 4822 / 3210 | 0.032 | **0.066** | 26.5 | 1.42 | 2.9% (2.1 to 11.2) | -22.6% | -6.4 pts | ✗ |
| entry: breakouts only | 621 / 421 | 0.008 | **0.222** | 32.8 | 1.19 | 0.1% (-2.5 to 1.3) | -27.0% | -9.2 pts | ✗ |
| entry: pullback needs a RISING 50-day (#31) | 2063 / 1429 | 0.077 | **0.106** | 27.6 | 1.24 | -1.9% (-7.0 to 2.8) | -32.6% | -11.2 pts | ✗ |
| entry: leaders only (RS top 20% + within 15% of high) | 1121 / 896 | -0.004 | **0.116** | 29.4 | 1.33 | 2.0% (-1.5 to 5.4) | -31.1% | -7.3 pts | ✗ |
| entry: Minervini trend template | 2032 / 1267 | 0.092 | **0.176** | 29.9 | 1.39 | 8.1% (4.8 to 10.0) | -33.5% | -1.2 pts | ✗ |
| entry: EPS >= 25% AND sales >= 15% | 1456 / 868 | 0.086 | **0.117** | 26.0 | 1.48 | 8.4% (5.3 to 11.0) | -28.2% | -0.9 pts | ✗ |
| market: block new buys in PRESSURE | 1622 / 1188 | 0.055 | **0.062** | 26.1 | 1.27 | -1.5% (-3.5 to 3.1) | -16.2% | -10.8 pts | ✗ |
| market: v3 regime sizing (full / half / none) | 3113 / 2178 | 0.089 | **0.101** | 27.1 | 1.35 | 7.7% (-0.5 to 8.9) | -20.0% | -1.6 pts | ✗ |
| v3 candidate: leaders + EPS&sales + sell playbook + regime | 828 / 661 | -0.039 | **0.048** | 22.1 | 1.32 | 5.7% (4.7 to 6.9) | -19.4% | -3.6 pts | ✗ |
| v3 candidate, breakouts only | 207 / 184 | -0.037 | **0.116** | 20.1 | 1.21 | 6.9% (6.4 to 7.0) | -9.1% | -2.4 pts | ✗ |

## 2026 so far (not used for any decision)

| Variant | Trades | Avg R | CAGR |
| --- | --- | --- | --- |
| base: live rules (v2.9.7 entries, stop A2) | 728 | -0.139 | -11.3% |
| exit: original stop only (no trail) | 316 | -0.044 | 4.8% |
| exit: close 2% under 50-day | 933 | -0.059 | 11.4% |
| exit: 50-day break on volume | 873 | -0.091 | 3.1% |
| exit: sell into a climax run | 740 | -0.124 | -4.7% |
| exit: cut failed breakouts (-2% within 20 days) | 991 | -0.101 | -0.1% |
| exit: O'Neil 8-week hold after +20% in 3 weeks | 706 | -0.098 | 35.8% |
| exit: full sell playbook (all four) | 1074 | -0.051 | 18.4% |
| exit: sell playbook + no trail | 951 | -0.067 | 38.9% |
| entry: breakouts only | 127 | -0.291 | -10.6% |
| entry: pullback needs a RISING 50-day (#31) | 465 | -0.207 | -17.6% |
| entry: leaders only (RS top 20% + within 15% of high) | 263 | -0.111 | 9.6% |
| entry: Minervini trend template | 460 | -0.196 | -8.4% |
| entry: EPS >= 25% AND sales >= 15% | 384 | -0.134 | -9.4% |
| market: block new buys in PRESSURE | 239 | -0.189 | -12.0% |
| market: v3 regime sizing (full / half / none) | 728 | -0.139 | -10.0% |
| v3 candidate: leaders + EPS&sales + sell playbook + regime | 201 | 0.006 | -6.3% |
| v3 candidate, breakouts only | 48 | 0.022 | -4.4% |

## Why trades ended (live rules, judge period)

| Exit | Trades |
| --- | --- |
| stop | 1533 |
| stage 4 | 296 |
| stop (gap) | 268 |
| 7.5% loss rule | 81 |

## Uncertainty (judge period, block bootstrap of monthly excess return vs SPY)

| Variant | 5th pct | median | 95th pct | % of resamples above zero |
| --- | --- | --- | --- | --- |
| base: live rules (v2.9.7 entries, stop A2) | -9.2 | -1.4 | 6.8 | 38.0 |
| exit: original stop only (no trail) | -11.4 | -5.2 | 4.0 | 17.0 |
| exit: close 2% under 50-day | -16.5 | -7.9 | 2.4 | 10.0 |
| exit: 50-day break on volume | -18.1 | -9.2 | -0.4 | 4.0 |
| exit: sell into a climax run | -11.4 | -2.5 | 6.8 | 33.0 |
| exit: cut failed breakouts (-2% within 20 days) | -15.0 | -6.5 | 2.2 | 11.0 |
| exit: O'Neil 8-week hold after +20% in 3 weeks | -11.2 | -4.3 | 3.4 | 17.0 |
| exit: full sell playbook (all four) | -21.5 | -13.1 | -4.5 | 1.0 |
| exit: sell playbook + no trail | -18.8 | -10.2 | -0.6 | 4.0 |
| entry: breakouts only | -17.1 | -10.6 | -3.3 | 1.0 |
| entry: pullback needs a RISING 50-day (#31) | -21.7 | -13.0 | -3.0 | 1.0 |
| entry: leaders only (RS top 20% + within 15% of high) | -19.6 | -9.8 | -0.8 | 4.0 |
| entry: Minervini trend template | -15.1 | -3.3 | 6.6 | 30.0 |
| entry: EPS >= 25% AND sales >= 15% | -15.2 | -3.8 | 7.1 | 28.0 |
| market: block new buys in PRESSURE | -21.4 | -14.2 | -4.8 | 1.0 |
| market: v3 regime sizing (full / half / none) | -11.4 | -4.3 | 3.5 | 18.0 |
| v3 candidate: leaders + EPS&sales + sell playbook + regime | -17.3 | -7.2 | 3.0 | 12.0 |
| v3 candidate, breakouts only | -15.7 | -5.9 | 5.0 | 18.0 |

_Generated by scripts/backtest/run_round4.py + report_round4.py. One change at a time vs the live rules; the v3 rows combine the layers. Nothing here changes the live app._
