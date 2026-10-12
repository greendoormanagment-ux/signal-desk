# Round 3 — audit first, then a realistic re-test (2026-10-12)

Live Signal Desk rules were not changed. No strategy was required to beat SPY; "no robust edge" is an allowed result.

## Gate 1 — data and engine integrity

**Data snapshot:** 2,075 price files, combined SHA-256 `976795cc8ef8fb17…` (full list in `data-manifest.json`).

### Extreme daily moves (close-to-close over 60%)

270 moves in 131 stocks. Each was checked against Yahoo split records, an independent price source (Nasdaq historical quotes) and the next day's price. The cached prices were never edited; any correction would go in `corrections.json` and be applied in memory, with a line in `corrections_log.csv`.

| Classification | Count | Rule |
| --- | --- | --- |
| genuine | 239 | independent source shows the same move (within 5%, log terms) |
| unresolved | 31 | no second source for that date, or sources disagree without a clear error pattern |

Corrections applied: **0**. None of the unresolved moves fall on a day the stock was in the S&P 500, so they cannot affect the S&P 500 tests below; Gate 2 also reran momentum without those stocks (identical result). Stocks with unresolved moves: ASND, AYA, BVC, DFTX, INDV, IVT, KDP, MAAS, PECO, QXO, SBNY, SKE.

Not detectable with these sources: spin-offs and special cash dividends (prices are not adjusted for them; KDP's 2018 special dividend is one of the unresolved items, before it joined the S&P 500).

### Gaps and coverage

- Missing sessions inside a stock's own history: 1 (in 1 stock). Bad or duplicate rows: 0 / 0.
- Stocks with at least one zero-volume day: 180 (mostly thin non-S&P names; the $20M/day liquidity rule screens them out).
- Stocks whose history starts after 2016 (IPOs, spin-offs, listings): 558. They become eligible only after 252 sessions.

**S&P 500 history.** The membership list records the ticker used at the time; prices are stored under today's ticker. Renamed companies (Anthem → ELV, Ball BLL → BALL, FleetCor → CPAY, …) are now joined to today's ticker through `scripts/backtest/ticker_aliases.csv` — 29 renames, each checked against the company's SEC record (same SEC company number, old name listed as a former name). `ticker_map.py` proposes candidates; look-alikes it found (e.g. IPG vs IPG Photonics) were rejected. What is still missing is almost entirely companies that were **acquired, merged away or went bankrupt**: the free price sources delete their history, so they cannot be recovered without a dataset that keeps delisted stocks.

| Year | S&P 500 members that year | With price data | Missing (acquired / delisted, no free history) | Member-days covered |
| --- | --- | --- | --- | --- |
| 2017 | 532 | 445 | 87 (16.4%) | 84.9% |
| 2018 | 529 | 454 | 75 (14.2%) | 87.0% |
| 2019 | 528 | 468 | 60 (11.4%) | 89.1% |
| 2020 | 523 | 472 | 51 (9.8%) | 91.0% |
| 2021 | 527 | 483 | 44 (8.3%) | 92.5% |
| 2022 | 523 | 488 | 35 (6.7%) | 94.2% |
| 2023 | 518 | 494 | 24 (4.6%) | 95.7% |
| 2024 | 521 | 501 | 20 (3.8%) | 96.6% |
| 2025 | 523 | 508 | 15 (2.9%) | 97.9% |
| 2026 | 516 | 507 | 9 (1.7%) | 98.9% |

Effect on results: dropped names are mostly takeover targets, which often jumped on the deal announcement, plus a few bankruptcies. Their absence can bias a test either way; adding the 29 renamed companies lowered momentum's return in the October 2026 run from 9.5% to 8.3% a year (see Gate 2), so results on the earliest years (≈85% coverage in 2017) carry the most doubt.

### Point-in-time rules now enforced

- **Universe:** a stock counts only on days it was in the S&P 500, traded at $5+, averaged $20M+/day over the prior 50 days, and had 252 sessions of history.
- **RS ranking:** each day ranks only the stocks eligible that day (previously: against today's whole list).
- **Earnings data:** a quarter is used only from its SEC filing date; later restatements don't leak backwards (planted test 5).
- **Execution:** a signal from a close trades no earlier than the next session — next open, or a next-day limit order. The round-2 "buy at the signal close" version was dropped. A stop crossed by an opening gap fills at the open.
- **Costs:** 0.07% per side ($0 commission + ~0.05% slippage + ~0.02% half-spread), stress test at 0.15%.
- **Sector/theme caps** use today's sector and industry labels (historical classifications aren't available free).
- **Dividends:** prices exclude dividends. SPY returned 12.7%/yr on price but 14.5%/yr with dividends over the same window, so price-only comparisons flatter the strategies by roughly 1–2%/yr.

### Planted tests

`python tests/test_backtest.py` → **15 of 15 passed**. Synthetic stocks with hand-worked answers: next-open entry, stop gapped at the open, A2 breakeven and trail, 7.5% rule, partial exit maths, portfolio sizing and costs, momentum next-open execution, point-in-time EPS with a restatement, RS eligibility, and the move classifier.

**Gate 1 verdict:** passes for S&P 500-based tests, with one documented limitation — 2–15% of member-days per year (acquired/delisted companies) have no free price history. It does **not** pass for a broad growth-stock universe: delisted small and mid caps are absent, so those tests must wait for a dataset that includes them.

## Gate 2 — momentum and pullback, realistic execution

Evaluation window 2017-10-15 to 2025-12-31 (2026 shown separately). Benchmark SPY: 12.7%/yr price-only (14.5% with dividends), max drawdown -34.1%, volatility 19.3%.

### Momentum rotation (S&P 500, next-open execution)

| Variant | Return/yr | vs SPY | Max DD | Volatility | Sharpe | Turnover/yr | 2026 so far |
| --- | --- | --- | --- | --- | --- | --- | --- |
| base: top 10, 12-1 month, monthly, next-open, 0.07%/side | 8.3% | -4.4 pts | -45.3% | 31.6% | 0.41 | 4.33× | 145.8% |
| cost stress: 0.15%/side | 7.6% | -5.1 pts | -46.0% | 31.6% | 0.39 | 4.33× | 144.5% |
| top 20 | 10.3% | -2.4 pts | -40.6% | 27.1% | 0.5 | 4.14× | 112.5% |
| theme cap: max 2 per industry | 8.6% | -4.1 pts | -45.3% | 30.6% | 0.42 | 4.5× | 152.9% |
| sector cap: max 3 per sector | 8.2% | -4.5 pts | -45.9% | 29.9% | 0.41 | 4.61× | 147.4% |
| without stocks that have unresolved data moves | 8.3% | -4.4 pts | -45.3% | 31.6% | 0.41 | 4.33× | 145.8% |
| rebalance on trading day 2 | 8.0% | -4.7 pts | -49.8% | 31.1% | 0.4 | 4.35× | 123.4% |
| rebalance on trading day 3 | 10.2% | -2.5 pts | -44.3% | 31.0% | 0.47 | 4.37× | 137.6% |
| rebalance on trading day 4 | 11.1% | -1.6 pts | -41.0% | 31.0% | 0.5 | 4.56× | 141.6% |
| rebalance on trading day 5 | 12.7% | -0.0 pts | -41.3% | 31.0% | 0.54 | 4.54× | 155.5% |

Non-overlapping two-year periods (base version):

| Period | Momentum | SPY | Difference | Momentum max DD |
| --- | --- | --- | --- | --- |
| 2018-2019 | -0.3% | 9.5% | -9.8 pts | -38.1% |
| 2020-2021 | 1.4% | 21.0% | -19.6 pts | -42.6% |
| 2022-2023 | 8.6% | -0.3% | +8.9 pts | -23.2% |
| 2024-2025 | 24.5% | 20.2% | +4.3 pts | -32.0% |

**Resampling (replaces the round-2 "3-year windows" figure):** 96 monthly differences vs SPY, resampled 5,000 times in 6-month blocks. Annual difference vs SPY: 5th percentile -12.6 pts, median -3.8 pts, 95th percentile 4.6 pts; 23% of resamples above zero. This describes uncertainty about the PAST average only — it is not a probability of beating SPY in the future.

### Short-term pullback — control (S&P 500, next-session execution only)

| Variant | Trades | Win % after costs | Avg trade after costs | Avg win / loss | Days held | Return/yr (range) | vs SPY | Max DD | Volatility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| next-open entry, RSI(2) < 10, 0.07%/side | 4,278 (521/yr) | 62.3 | 0.052% | 2.0% / -3.17% | 3.8 | 2.1% (0.1 to 4.7) | -10.6 pts | -29.0% | 15.7% |
| next-open entry, RSI(2) < 5 | 3,445 (420/yr) | 62.2 | 0.103% | 2.03% / -3.06% | 3.9 | 3.3% (-0.5 to 3.7) | -9.4 pts | -29.7% | 13.9% |
| limit 2% under signal close (next day), RSI(2) < 10 | 2,365 (288/yr) | 61.6 | 0.286% | 2.89% / -3.89% | 4.5 | 8.2% (4.6 to 9.0) | -4.5 pts | -26.8% | 15.6% |
| limit 2% under signal close, RSI(2) < 5 | 1,610 (196/yr) | 61.8 | 0.201% | 2.79% / -3.99% | 4.5 | 3.7% (2.5 to 4.4) | -9.0 pts | -23.0% | 12.6% |
| limit 2%, RSI(2) < 10, cost stress 0.15%/side | 2,351 (286/yr) | 60.6 | 0.12% | 2.78% / -3.97% | 4.5 | 2.8% (-0.7 to 3.3) | -9.9 pts | -32.2% | 15.7% |

Best pullback version by period (limit 2% under signal close (next day), RSI(2) < 10):

| Period | Pullback | SPY | Difference | Pullback max DD |
| --- | --- | --- | --- | --- |
| 2018-2019 | 1.4% | 9.5% | -8.1 pts | -25.6% |
| 2020-2021 | 13.8% | 21.0% | -7.2 pts | -23.4% |
| 2022-2023 | 1.8% | -0.3% | +2.1 pts | -16.9% |
| 2024-2025 | 14.2% | 20.2% | -6.0 pts | -15.1% |

Resampled annual difference vs SPY: 5th -9.5 / median -3.9 / 95th 2.1 pts; 15% of resamples above zero.

**Gate 2 verdict:** neither system shows a robust advantage over SPY once execution is realistic and 2026 is excluded. Momentum: across the five rebalance days the difference vs SPY ranges from -4.7 to +0.0 points a year (4 of 5 behind), and every cost, cap and size variant is behind. Pullback: the best version earns 0.286% per trade after costs with lower volatility and drawdown than SPY, but returns -4.5 points a year vs SPY and most of the edge disappears at the stress cost.

## Gate 3 — external data

Not started. Before paying for any dataset, confirm on a free tier that it actually contains the missing S&P 500 members listed in `sp500_coverage.csv` and delisted small/mid caps. The purpose would be testing the leader-breakout idea on a broad growth universe — not rescuing these two systems.

## Reproduce

```
cd scripts/backtest
python tests/test_backtest.py
SEC_DIR=<sec cache> python audit.py <prices> <prices-sp> <sp500_ticker_start_end.csv> <audit out>
python run_round3.py <prices> <sec cache> <results out> <prices-sp> <sp500_ticker_start_end.csv> <audit out>
python report_round3.py <audit out> <results out> ../../backtest/round3-latest.md
```
Results depend on the data snapshot; compare the combined SHA-256 above before comparing numbers.
