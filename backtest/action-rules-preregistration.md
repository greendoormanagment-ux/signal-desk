# Exit "ACTION" rules test — pre-registration (LOCKED 2026-11-11, before any result was run)

**Why.** v2.16's ACTION box tells you to sell half or raise the stop on warning signs and before earnings. These were added as guidance, never backtested as partial sells. "Let data decide": an action rule must earn its place. Round 4 found the same warning signs used as *full* exits cut winners more than they saved.

## Base
Breakouts only + live market gate, all US stocks, point-in-time eligibility, costs 0.07%/side plus liquidity slippage (as in Round 8). Two stop bases: **A2 trail (live v2.16)** = primary, **original stop** = secondary (report only). Development 2005–16 decides; validation 2017–25 checks.

## Variants (each compared with "hold the full position" on the SAME trades)
| | Variant | Exact rule (judged at the close, acted on at the next open unless stated) |
| --- | --- | --- |
| V0 | Hold full | today's backtest (stop rule + 7.5% loss rule) |
| V1 | Warning trim | the first day the app's `sellSignals()` points reach **≥ 4** → sell **half**; once per trade; the stop then covers the rest |
| V2 | Warning stop-raise | whenever points are **≥ 2** → raise the stop to just under the lowest low of the last 5 sessions (never lower; only if below 99.5% of the close) |
| V3 | Earnings trim | from the app's `earningsCheck()`: within **7 calendar days** of a report, if the gain is below 0 or below the expected move (average of the stock's 4 largest opening gaps in the past year) → sell **half at the close of the trading day before the report date**; once per report |
| V4 | Full ACTION box | V1 + V2 + V3 together |

`sellSignals()` replicated exactly from index.html (v2.16): failed breakout (2), 50-day break on volume (2), climax run (1), worst day of the move (1), distribution cluster (1), stage change (2), market PRESSURE (1) / CORRECTION (2).

**Earnings dates:** SEC 8-K filings with Item 2.02 ("Results of Operations"), filing date = report date. V3 is judged only on trades of stocks with SEC earnings dates in the holding period; coverage is reported.

## Measures and verdict (V1, V2, V3 = one Holm family; V4 reported)
- **Primary:** paired difference in R per trade (variant − hold), mean with a 95% interval two-way clustered by stock and entry month, after costs.
- **KEEP** (the rule earns its place): development difference > 0 with the Holm-adjusted 95% interval above 0, **and** validation difference > 0, **and** it keeps at least 90% of the total R of the top 5% winners.
- **REMOVE** (data shows harm): development difference < 0 with its interval below 0, and validation difference < 0.
- **INCONCLUSIVE** otherwise → under "no rule without proof", the rule becomes **optional information, not an instruction**, in the next version.
- Also reported: share of the top-5% winners' R kept, portfolio return and drawdown (approximate: a partial sale is booked at the final exit date), results by year.

## Guardrails
No changes after results. Nothing changes in the live test before January 29, 2027 — the live ACTION box is followed as is; results go into the next version.
