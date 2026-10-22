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

## Round 4 (Oct 20 2026): fixing the weaknesses

- `engine.py`: new options, all OFF by default so Rounds 1–3 reproduce exactly. Sell signals from app v2.13 (`exit_failbo`, `exit_ma50vol`, `exit_climax`, `hold8w`), the v3 leadership gate `near_high`, regime sizing (`portfolio(risk_fn=...)`), and `nosec_pass`. With `nosec_pass`, a company with no SEC file is judged on its price rules, so delisted names can still be bought.
- `run_round4.py` + `report_round4.py`: 18 variants (exits, entries, market, and the v3 candidate) on the point-in-time S&P 500. They are tuned on early years and judged on unseen years against the Playbook pass bar. Results show avg R after costs, how much gain was given back, portfolio vs SPY, and a bootstrap.
- `fetch_eodhd.py`: the paid-month data. It covers every S&P 500 member since 2004, including failed and delisted companies, with a coverage report. The key comes only from the `EODHD_KEY` secret. The data is never committed, because its licence forbids republishing.
- `fetch_sec.py`: finds SEC filings for delisted companies by exact company-name match.
- Run it from the Actions tab → "Backtest Round 4 (run by hand)". Choose data = `free` for a preview now, or `eodhd` once the paid month is active.
- Planted tests: 23 (8 new for the sell signals and regime sizing).

## Round 5 (Oct 21 2026): can it beat SPY?

- Round 4 exposed three gaps: cash drag (sitting in cash between setups while SPY is always invested), a trailing stop that cuts winners short, and an untested best idea.
- `engine.portfolio` / `systems.portfolio`: new `idle=(spy_open, spy_close)` option. Money not in a stock earns SPY, prior close → open, then open → close, and each switch costs 0.03%. `stats` reports the average share of the account held in stocks.
- `run_round5.py` + `report_round5.py`: 12 variants (idle SPY, exits that let winners run, trend template, and Round 1's combined system) on the point-in-time S&P 500.
- The pass bar was set before the run: beat SPY in BOTH tune and judge, ≥70% of bootstrap resamples above zero, and a drawdown no worse than SPY's + 5 pts.
- Actions → "Backtest Round 5 (run by hand)", data = `free` or `eodhd`. Planted tests: 25.

## Round 6 (Oct 22 2026): best small combination + buy back after a sale

- Goal: find the best SMALL set of rules, not add more. Five blocks: entry filter (4) × setups (2) × exit (4) × market rule (3) × re-entry (2) = 192 combinations. Idle money sits in SPY in all of them.
- `engine.py`: new `reentry` option (off by default). After any sale, the stock can be bought back within 40 sessions when it closes above its high since the sale, above the 50-day, on 1.2× volume, not rated SELL, and the market is not in CORRECTION. The stop is the low since the sale (or 8% max), and there are at most 2 buy-backs in a row.
- `run_round6.py` + `report_round6.py`: every combination is scored on the TUNE years only, and the judge years stay sealed. Only the top 3 (ties go to fewer rule changes, then steadier sub-periods) are opened on JUDGE. The pass bar is raised for multiple testing: beat SPY in tune and judge, bootstrap ≥ 80%, and DD no worse than SPY's + 5.
- Actions → "Backtest Round 6 (run by hand)", data = `free` or `eodhd`. Planted tests: 29. Added after the first run: `reentry="early"` — buy back on a close above the 50-day that also tops the prior 10-day high (3+ sessions after the sale), so it can rebuy below the sale price; the search grows to 288 combinations.
