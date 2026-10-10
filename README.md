# Signal Desk — Handbook

Stock screener for Tony's 30-day rules test (O'Neil breakouts/pullbacks, Weinstein stages, chandelier stops).
**Rules decide; Claude only explains.** Live app: https://greendoormanagment-ux.github.io/signal-desk/

_Last updated: Oct 10, 2026 · app v2.8_

## The pieces
| Piece | Where | What it does |
|---|---|---|
| App | `index.html` (this repo, GitHub Pages) | Entry Scan, Position Review, Holdings, Log |
| Price data | Twelve Data (free key, saved in the app's setup bar) | quotes + daily bars; SPY/QQQ once a day for the market gate |
| AI | Anthropic API (key in the app's setup bar) | explanations; runs only when price rules pass and SEC EPS passes, or on RUN AI CHECK |
| EPS | `eps.json` — built nightly from SEC filings | latest quarter EPS vs same quarter last year (GAAP, includes one-time items) |
| Earnings dates | `earnings.json` — built nightly from Alpha Vantage | next report date + analyst EPS estimate (next 3 months) |
| Nightly job | `.github/workflows/nightly-eps.yml` → `scripts/build_earnings.py`, `scripts/build_eps.py` | ~4:17 a.m. ET; run by hand from the **Actions** tab; secret `ALPHAVANTAGE_KEY` |
| Decision Log | Google Sheet "Signal_Desk_Decision_Log" | Scans (auto), Trades, Stats, Outcomes, Fix List, Account Activity |
| Sheet script | Sheet → Extensions → Apps Script ("Signal Desk Logger") | logs scans; sends open trades to Position Review; auto-notes stop changes |

## Rules (v2.8)
- **Market gate** (rules-based): SPY and QQQ vs their 50-day average + distribution days (down ≥0.2% on higher volume, last 25 sessions). UPTREND / PRESSURE (5+ distribution days or below 50-day) / CORRECTION (below a falling 50-day).
- **Trend:** price above 50-day and 200-day; 50-day above 200-day.
- **Entry:** BREAKOUT = close above pivot (prior-year high excl. last 5 sessions) on ≥1.4× volume; PULLBACK = within ±3% of the 50-day; WATCH = within 5% below pivot.
- **EPS:** latest quarter ≥25% above the year-ago quarter; ⚠ warning if growth >100% (possible one-time item — check Finviz "EPS Q/Q").
- **Earnings:** no new buys within 14 days of a report.
- **Relative strength:** Mansfield RS + 3-month performance vs the S&P 500.
- **Stops:** max 8% below entry. Rule A2 "earn the trail": original stop until +1R → breakeven at +1R → at +2R trail = higher of breakeven and (high since entry − 3×ATR). Never lower a stop.

## Trades tab
- Column **I = Original Stop** (never change), **J = Current Stop** (update when the app says raise). Changing J auto-writes a dated note in Notes.
- Also update the stop order at the broker (all shares, GTC).

## Routine
- Scan → I BOUGHT IT / I PASSED (logged automatically).
- Position Review every few days on open trades; raise stops when told.
- If GitHub emails "workflow failed": nothing breaks — the app uses the last good files; the next night usually fixes it.
- If GitHub emails "scheduled workflow disabled": Actions tab → Enable workflow.

## History
- v2.7 SEC EPS check · v2.7.1 nightly eps.json · v2.7.2 big-jump warning · v2.8 rules-based market gate, RS, earnings calendar (comparison week vs Claude from Oct 10)
