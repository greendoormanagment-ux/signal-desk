# Backtest

Replays Signal Desk's entry rules and stop rule A2 over ~9 years, using only data that was public each day.
Nothing here touches the live app or the nightly data.

- `fetch_prices.py`: daily bars for every US stock at or above $2B market cap (Yahoo, with a Nasdaq fallback).
- `fetch_sec.py`: SEC EPS and revenue with filing dates, plus 8-K Item 2.02 dates as the earnings calendar.
- `engine.py`: the rules, ported 1:1 from `index.html` (checked against the app's own JavaScript: 0 mismatches on 664 random stock-days), plus the trade and portfolio simulation.
- `run.py`: runs the live rules and one-change-at-a-time variants, with in-sample (2017–21) and out-of-sample (2022–26) splits.
- `report.py`: writes `backtest/latest.md`.

To run it: Actions tab → "Backtest (run by hand)" → Run workflow (about 45 minutes; free). The results are committed to `backtest/`.

To test a new idea: add one line to `VARIANTS` in `run.py`. Change one thing at a time, and judge it on the out-of-sample columns.

Known limit: the universe is today's stocks, so there is survivorship bias (Fix List #69).

## Candidate systems (round 1, Oct 12 2026)

- `systems.py`: four candidate systems: leader breakout, earnings gap, leader pullback, and momentum rotation (the control). Exits are shared and include a partial sale at +kR, a time stop, and a runner exit.
- `run_systems.py`: runs each system and its one-change variants on two universes. *broad* is today's stocks (biased). *sp500* counts a stock only while it was actually in the S&P 500 (fairer).
- `fetch_sp500.py`: point-in-time S&P 500 membership (github.com/fja05680/sp500), plus prices and SEC data for past members.
- `report_systems.py`: writes `backtest/systems-latest.md`.

The same workflow runs these. Only the `.md` reports are committed, so the repo stays small.

## Round 2 (Oct 12 2026)

- `run_round2.py`: (a) a short-term pullback (mean-reversion) system: buy a 2–3 day dip in an uptrend, sell on the bounce. (b) A stress test of momentum rotation: other settings, rebalance days, market filters, results without 2026, and rolling 3-year windows vs SPY and RSP.
- `report_round2.py`: writes `backtest/round2-latest.md`.

## Round 3 (Oct 12 2026): audit first, then a realistic re-test

- `tests/test_backtest.py`: 15 planted test cases with hand-worked answers. Run with `python tests/test_backtest.py`.
- `audit.py`: data snapshot hashes, classification of every >60% daily move (split records + an independent Nasdaq price source + the next-day check), a corrections overlay (the cache is never edited), data gaps, and S&P 500 coverage by year.
- `engine.py`: `apply_corrections`, point-in-time `eligibility`, and `rs_rank` (ranked only against stocks eligible that day).
- `systems.py`: `momentum_open` (trades at the next open, gaps and costs included), `perf_metrics`, and `block_bootstrap_excess`.
- `run_round3.py` + `report_round3.py`: write `backtest/round3-latest.md` with the Gate 1 and Gate 2 verdicts.
