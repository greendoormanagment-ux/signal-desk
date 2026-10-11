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
