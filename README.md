# Signal Desk — Handbook

Stock screener for Tony's 30-day rules test (O'Neil breakouts/pullbacks, Weinstein stages, chandelier stops).
**Rules decide; Claude only explains.** Live app: https://greendoormanagment-ux.github.io/signal-desk/

_Last updated: Oct 11, 2026 · app v2.9_

## Mission
> *Signal Desk finds high-quality setups, sizes the risk, enforces the exits, and keeps score honestly — so every rule has to earn its place.*

The goal is an **edge**, not impressive-looking signals. For an individual investor that edge is discipline (rules over emotion), cutting losers fast, staying out of bad markets, and learning from an honest record — not predicting every move.

## The vision — four pillars
| Pillar | Status (Oct 2026) | Still to do |
|---|---|---|
| **1. Find opportunities early** — unusual volume, improving price action, strong RS, catalysts, institutional interest | Partly: RS, volume, breakouts, thinkorswim scan | Catalysts, unusual-volume screen, institutional buying — **only after** each proves it helps (What's Working / backtest) |
| **2. Separate signal from noise** — no single indicator decides | Mostly: rules decide, every hard gate must pass | Sales growth (CAN SLIM "C"); fix pullback rule (Fix List #31) |
| **3. Protect capital** — sizing, reward vs risk, concentration, invalidation | Mostly: 8% stops, earn-the-trail stops, risk sizing, concentration warnings, Stage 4 sells | Reward-vs-risk check, gap cushion, "thesis broken" checklist |
| **4. Prove it works** — benchmarks, costs, unseen data | Started: every scan logged, outcomes tracked, vs S&P in What's Working | Historical backtest (Nov 2026), tune on older years / test on unseen years, 60–90 days live |

**Order of work:** (1) finish the 30-day test (10/29) → (2) backtest + pullback fix (November) → (3) add new signals one at a time, keeping only what improves results → (4) if it proves out, the track record is the product.

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
| Sheet script | Sheet → Extensions → Apps Script ("Signal Desk Logger"), web-app version 7 | logs scans; sends open trades to Position Review (ticker, account code, entry, stops — never Notes); auto-notes stop changes; builds the What's Working tab |

## Rules (v2.8)
- **Market gate** (rules-based): SPY and QQQ vs their 50-day average + distribution days (down ≥0.2% on higher volume, last 25 sessions). UPTREND / PRESSURE (5+ distribution days or below 50-day) / CORRECTION (below a falling 50-day).
- **Trend:** price above 50-day and 200-day; 50-day above 200-day.
- **Entry:** BREAKOUT = close above pivot (prior-year high excl. last 5 sessions) on ≥1.4× volume; PULLBACK = within ±3% of the 50-day; WATCH = within 5% below pivot.
- **EPS:** latest quarter ≥25% above the year-ago quarter; ⚠ warning if growth >100% (possible one-time item — check Finviz "EPS Q/Q").
- **Earnings:** no new buys within 14 days of a report.
- **Relative strength:** Mansfield RS + 3-month performance vs the S&P 500.
- **Stops:** max 8% below entry. Rule A2 "earn the trail": original stop until +1R → breakeven at +1R → at +2R trail = higher of breakeven and (high since entry − 3×ATR). Never lower a stop.

## Trades tab
- Column **C = Account**: T4k = Tony's 401(k) (Fidelity), P4k = Priscilla's 401(k) (Fidelity), Kids = Schwab Kids, Dad = Schwab Dad, IRA, Paper. Fill it in for every new trade — Position Review shows it (e.g. "LLY · T4k").
- Column **J = Original Stop** (never change), **K = Current Stop** (update when the app says raise). Changing Current Stop auto-writes a dated note in Notes. (Columns are found by header name, so moving them doesn't break anything.)
- Also update the stop order at the broker (all shares, GTC).

## Routine
- Scan → I BOUGHT IT / I PASSED (logged automatically).
- Position Review every few days on open trades; raise stops when told.
- If GitHub emails "workflow failed": nothing breaks — the app uses the last good files; the next night usually fixes it.
- If GitHub emails "scheduled workflow disabled": Actions tab → Enable workflow.

## History
- v2.7 SEC EPS check · v2.7.1 nightly eps.json · v2.7.2 big-jump warning · v2.8 rules-based market gate, RS, earnings calendar (comparison week vs Claude from Oct 10) · v2.8.1 logs SEC EPS when AI skipped · v2.8.2 no false entry-price warning · v2.8.3 logs breakout-day volume · v2.9 new sheet key, account codes, sheet connection shares no notes
- The sheet key in `index.html` must match `SECRET` in the sheet script. If it's ever changed, change both and publish a new script version.
