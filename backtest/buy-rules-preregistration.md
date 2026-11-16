# Buy-rules test (Round 8 · session 3) — pre-registration (LOCKED 2026-11-16, before any result was run)

**Why.** Five things on the buy side of the live app were never tested on their own: the EPS-growth block, the 14-day earnings block, the breakout definition (1.4× volume, max 5% above the pivot), the 24-hour rule, and an earnings gap as its own entry. Rule register policy: every rule is tested or labeled untested.

## Base (same for all five tests)
Breakouts only, live market gate (no buys in CORRECTION), all US stocks incl. delisted, point-in-time eligibility (≥ $5, ≥ $20M/day, one year of history), buy at the next open, costs 0.07%/side plus liquidity slippage — exactly as Round 8 sessions 1–2. Two stop bases: **A2 trail (live) = primary**, **original stop = secondary (report only)**. Development 2005–16 decides; validation 2017–25 checks; **2026 is not touched**. Statistics: mean R per trade after costs, two-way clustered by stock × entry month. Portfolio figures: 10 slots, 1% risk, idle money in SPY, median of 10 random same-day orders.

**SEC data limits (T1, T2, T5).** EPS, sales and operating income come from SEC XBRL filings (public from about 2009–11), earnings dates from 8-K Item 2.02 filings; both exist only for companies still registered with the SEC today (about 2,800 of 5,671 stocks). So these three tests run on the covered trades only; coverage is reported. Every number is used only from its filing date on (point in time), a quarter older than 135 days counts as "no reading". Both sides of each comparison share the same coverage limit.

## T1 — Fundamentals block (one Holm family of three)
Among base trades with a usable SEC reading on the signal day, "pass" vs "fail":

| | Measure | Pass (same math as the app's EPS rule) |
| --- | --- | --- |
| E1 | **Official EPS growth ≥ 25%** (the live rule) | latest quarter vs the same quarter a year ago ≥ +25%, or loss → profit; unprofitable = fail |
| E2 | Sales growth ≥ 25% | latest quarter's revenue vs a year ago ≥ +25% |
| E3 | Operating income growth ≥ 25% | same math as E1 on operating income (leaves out one-time items below the operating line) |

Reported, no verdict: mean R by EPS-growth bucket (unprofitable / below 0 / 0–25 / 25–50 / 50–100 / over 100 / loss → profit); trades where official EPS fails but operating income passes (the Berkshire question); portfolio with the E1 block vs without it, on covered stocks. The AI-adjusted EPS override cannot be backtested (no history) and stays labeled untested.

## T2 — No buys within 14 days of earnings
Among base trades whose next SEC earnings date is known: "outside" (next report more than 14 calendar days after the signal) vs "inside" (0–14 days). The live rule blocks "inside". Reported, no verdict: windows of 7 and 21 days; buckets 0–3 / 4–7 / 8–14 / 15–30 / 31+ days; portfolio with vs without the block.

## Verdict for E1, E2, E3 and T2 (two-sided p-values, Holm across the four)
- **EARNS ITS PLACE:** development difference (pass − fail, or outside − inside) > 0 with the Holm-adjusted 95% interval above 0, **and** validation difference > 0, with 300+ trades on each side in each period.
- **HURTS:** development difference < 0 with its interval below 0, **and** validation < 0.
- **INCONCLUSIVE** otherwise. For a live rule (E1, T2) that means: not proven — a candidate to become information only in the next version (simpler wins when close). For E2/E3 it means: not added.

## T3 — Breakout definition
Grid: breakout-day volume ≥ **1.2 / 1.4 / 1.6 / 2.0×** the 50-day average × close no more than **3 / 5 / 8%** above the pivot = 12 cells. Champion = 1.4× and 5%. The stop formula is unchanged in every cell.
- **A challenger replaces the champion** only if, in **both** periods, its portfolio CAGR is at least **+1.0 pt/yr** higher, its max drawdown is no more than **2 pts** deeper, **and** its mean R per trade is not lower. If several qualify: the one with the highest development CAGR.
- Otherwise **the champion stays**. Reported: all 12 cells (trades, mean R with interval, CAGR, drawdown) and mean R by volume and by extension bucket.

## T4 — 24-hour rule
W0 = buy at the next open after the first BUY close (every backtest so far). W1 = the app's rule: the stock must rate BUY again at the next day's close, then buy at the following open (stop from the second day's signal).
- **EARNS ITS PLACE:** mean R per trade W1 − W0 > 0 with a 95% clustered interval above 0 in development, > 0 in validation, **and** W1's portfolio CAGR no more than 0.5 pt/yr below W0's in both periods.
- **HURTS:** the difference < 0 with its interval below 0 in development and < 0 in validation, **or** W1's portfolio CAGR at least 1.0 pt/yr below W0's in both periods.
- **INCONCLUSIVE** otherwise → optional, not an instruction, in the next version.
- Reported: share of signals still BUY the next day; R of the signals that W1 skips.

## T5 — Earnings gap as its own entry (a challenger setup, not a filter)
Signal day G (all must hold at the close of G): an SEC earnings date on G or the trading day before; open ≥ **4%** above the prior close; volume ≥ **2×** the 50-day average; close in the upper half of the day's range; close above the 50-day and the 200-day average; market gate not CORRECTION; eligible. **No pivot breakout needed.** Buy the next open. Stop = the low of G, never more than 8% below G's close. Exits as in the base.
- **CANDIDATE SETUP:** 300+ trades in each period, development mean R > 0 with a 95% clustered interval above 0, validation mean R > 0, **and** a portfolio of breakouts + earnings gaps beats breakouts alone (covered stocks) by at least **+1.0 pt/yr** CAGR in both periods with max drawdown no more than 2 pts deeper.
- **NO:** development mean R ≤ 0, or the pooled portfolio is at least 1.0 pt/yr worse in both periods.
- **INCONCLUSIVE** otherwise → not added.
- Reported: mean R next to the base breakouts on the same stocks and years; how many gap entries are also breakouts.

## Guardrails
No changes after results. Results that show no effect are reported. Nothing changes in the live test (Nov 2, 2026 → Jan 29, 2027) except by a dated amendment decided by Tony. Investor-style inputs (Graham / Buffett / Lynch) need balance-sheet data and move to the ranking test as a written amendment before it runs (Nov 23).
