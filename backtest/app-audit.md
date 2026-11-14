# Audit — does the live app follow the same rules the backtests tested? (2026-11-14)

Re-run any time: `cd scripts/backtest && python tests/parity_app_vs_engine.py [UNIVERSE_PKL]` (feeds identical bars to the app's own JavaScript and to the backtest engine).

## Checked by running both on the same data — they agree
| Part | Result |
| --- | --- |
| Buy rating from price rules (trend, pivot, breakout on 1.4× volume, 5% limit, Stage 4) | **4,429 stock-days, 1,500 BUYs: identical** rating, setup, stop, pivot, 50/200-day averages |
| Market gate (SPY + QQQ, 50-day, distribution days) | **300 days: identical** |
| ATR and RSI | within 2% (smoothing depends on history length) |
| Footprints (checked 11/11) | 400 cases: identical |
| Warning-sign points (checked 11/11, via round8d) | engine exits reproduced on 40,846 trades |
| Trailing stop A2 | same formula. One difference: the app starts "high since entry" the day **after** the buy, the engine on the buy day. Measured on 2,495 trades: 99.3% identical exits, average difference +0.001R — negligible |
| 7.5% loss rule, Stage 4 exit, stop-hit = sell all | same rule in both (read line by line) |
| EPS rule (loss = fail · turned profitable = pass · growth ≥ 25% = pass · reading older than 135 days ignored) | same rule in both |
| 14-day earnings block | same rule in both |

Label-only difference: a pullback is "WATCH" in the app and "DON'T BUY" in the engine. Neither buys.

## Real differences between the live app and what Round 8 tested (not bugs — untested gaps)
| # | Live app | Round 8 backtests | Where it's handled |
| --- | --- | --- | --- |
| 1 | EPS ≥ 25% hard block | no EPS filter (price rules only) | test Nov 16 |
| 2 | 14-day earnings block | not applied | test Nov 16 |
| 3 | Buys after a 24-hour rescan | buys at the next open | test Nov 16 |
| 4 | When the AI check runs, **adjusted** EPS is used ahead of official SEC EPS | official SEC EPS only (older rounds) | add to the Nov 16 EPS test |
| 5 | Earnings date unknown → CHECK FIRST | recently reported + no next date → counts as pass | matters between seasons (now); fix = estimated dates (next version) |
| 6 | Position size = a fixed risk in dollars (default $1,000); no cap per position; no limit on the number of positions | 1% of the account per trade, max 20% per position, max 10 positions | portfolio test Nov 30; add an account-% size and caps in the next version |
| 7 | Any stock can be scanned (thin stocks get a warning) | only stocks ≥ $5 and ≥ $20M traded per day | add the same eligibility check to the app (next version) |
| 8 | Trailing stop A2 | original stop tested better | next version (Jan 29 decision) |

## Fixed in this audit (v2.16.5, display only)
- After **I SOLD SOME**, the app now reloads your trades, so a second account's row number is correct (the "row 3 is already closed" error).
- The +20% prompt now says **optional** everywhere (top badge reads "UP 20%+ · Optional trim — holding is fine").
