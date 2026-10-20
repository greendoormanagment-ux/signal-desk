# Signal Desk Playbook

_The one page Claude reads before analyzing any stock or position for Tony. Rules decide; evidence ranks; lessons accumulate._
_Last updated: Oct 21, 2026 · app v2.11 · 30-day live test 9/29 → 10/29 (rules frozen)_

## 1. How to analyze a stock (every time, in this order)
1. **Market regime first.** SPY/QQQ vs 50-day + distribution days (app's gate: UPTREND / PRESSURE / CORRECTION). Also note: S&P vs its 200-day; failed index breakout (closed back under a high it just broke); leaders vs average stock (SPY vs RSP). PRESSURE or worse → new buys are **paper only**.
2. **Leadership.** Is it a leader? RS vs S&P (Mansfield + 3-month in the app; 12-month-skip-1 is the best-proven measure), distance from 52-week high (want ≤ 25%, ideally ≤ 15%), Minervini Trend Template (§3).
3. **Fundamentals.** Latest-quarter EPS ≥ +25% vs year-ago (SEC data; if > 100%, check for one-time items); sales growth; next earnings date (no new buys within 14 days).
4. **Setup.** Breakout (close above pivot on ≥ 1.4× volume, ≤ 5% extended) is the strongest-evidence entry. Pullback-to-50-day is the weakest — apply the §5 lessons. Before 4 PM ET volume is partial → treat as WATCH; rescan after the close (24-hour rule).
5. **Risk.** 1% of account per trade; stop ≤ 8% below entry, placed on fill, never lowered. Stop rule A2: original stop until +1R → breakeven → at +2R trail = max(breakeven, high since entry − 3×ATR).
6. **Crowding.** Same sector AND same theme (e.g. AI infrastructure spans Technology + Industrials + Utilities). Flag 3+ positions in one theme.
7. **Lessons check.** Compare with §5 — does this look like a past mistake?
8. **Straight take.** Buy real / buy paper / watch / pass — with the one or two reasons that matter most. No financial-advisor disclaimers (Tony decides).

## 2. Evidence ranking of technical signals (academic + practitioner)
| Strength | Signal | Where it lives |
|---|---|---|
| Strong | Trend following / market regime (cuts drawdowns) | Market gate; v3 Layer 1 |
| Strong | Relative strength, 12-month-skip-1 momentum (beware momentum crashes) | RS check (10 pts today — underweighted) |
| Strong | Nearness to 52-week high | Pivot / breakout |
| Moderate | Post-earnings drift (earnings gaps) | Not in the app yet (v3) |
| Moderate | Volume confirmation | Breakout ≥ 1.4× |
| Weak-moderate | Short-term reversal (buying dips) — small edge, eaten by costs | Pullback entry |
| Weak | RSI, MACD, Fibonacci, candlesticks, most chart patterns | RSI = 10 pts (should be info only) |

Key sources: O'Neil *How to Make Money in Stocks*; Minervini *Trade Like a Stock Market Wizard*; Gray & Vogel *Quantitative Momentum*; Aronson *Evidence-Based Technical Analysis*; Bodie-Kane-Marcus *Investments*; Clenow *Stocks on the Move*; Jegadeesh & Titman 1993; George & Hwang 2004; Moskowitz-Ooi-Pedersen 2012; Daniel & Moskowitz 2016.

## 3. Author rules to test (exact, from public sources)
**Minervini Trend Template** — price > 150-day and 200-day · 150-day > 200-day · 200-day rising ≥ 1 month (ideally 4–5) · 50-day > 150-day and 200-day · price > 50-day · price ≥ 30% above 52-week low · price within 25% of 52-week high · (book) RS rating ≥ 70.
**Gray & Vogel Quantitative Momentum** — largest ~1,500 stocks, drop least-liquid 15% · rank by 12-month return skipping the last month · prefer "smooth" momentum (frog in the pan: many small up days beat a few big jumps; ID = sign(12-1 return) × (%down days − %up days), lower is better) · monthly rebalance · ~50 stocks equal weight.
**Clenow Stocks on the Move** — rank by 90-day exponential-regression slope (annualized) × R² · buy only when S&P > 200-day · stock > 100-day, no 15%+ gap in 90 days · size by ATR (volatility).
Status: queued for the November backtest. None changes live rules until it passes.

## 4. What the backtests have shown so far (Rounds 1–3, Oct 2026)
- Free price data hides failed/delisted companies → results look too good (survivorship bias). Fair tests need delisted stocks (EODHD, Gate 3).
- On S&P 500 stocks with realistic next-day fills and costs, 2017–2025: **momentum rotation ≈ 8%/yr vs SPY 12.7%** (−45% max drawdown); **pullback system ≈ 8%/yr**, 62% winners but tiny gains per trade. Neither showed a robust edge vs SPY.
- The live app's own leader-breakout rules have **not** had a fair test yet — that's the Gate 3 / November job.
- Pass bar for any change: tune on 2005–2016, judge on 2017–2025; higher average gain per trade after costs, drawdown no worse, works on unseen years. Beating SPY is not required. Add one change at a time.

## 5. Lessons learned (add after every review — newest first)
- **10/17 · Leader rotation.** S&P −2% while equal-weight RSP +0.5%; last spring's top-100 stocks −5%, bottom-100 +4% (DELL, HPE −20%+, PLTR −11%). When SPY lags RSP and the strongest stocks fall hardest, treat it as a momentum-crash warning: no new real buys, keep stops, don't add to the hot theme.
- **10/17 · Theme beats sector.** MRVL (Technology) and PWR (Industrials) fell together on AI-capex worries. Check themes, not just sector labels (Fix #90).
- **10/16 · Sharp drops aren't pullbacks.** DDOG and PLTR rated BUY after −7% days because the pullback rule only checks distance to the 50-day. A −4%+ day or −10% over 5 days on heavy volume = selling, not an orderly pullback (v2.11 warning; Fix #31a–e).
- **10/15 · Deep "pullbacks" are corrections.** MRVL was 26% below its 1-year high when rated BUY. Cap pullback depth (~15–20%; Trend Template says ≤ 25%).
- **10/15 · Earnings timing can flip tomorrow's rescan.** PWR was 15 days from earnings — the 24-hour rescan would fall inside the 14-day rule. Check the date before planning a "buy tomorrow."
- **10/15 · Foreign filers aren't in SEC EPS data.** CVE (Canada) showed fundamentals "not checked"; verify from the company's release. Growth > 100% usually includes one-time items.
- **10/20 · SEC's data feed can lag a company's filing** (KNSA Q2 filed 7/28, missing from SEC data). When EPS shows "not available," read the 8-K press release.
- **10/13 · Most test trades came through the weakest entry** (pullbacks). Judge Signal Desk's breakout idea separately from the pullback rule.
- **Process:** logging bugs distort reviews (stale Entry Price leaked into 95 rows; fixed v2.10.1). Check the data before trusting conclusions.

## 6. What the great stock pickers agree on (and how Signal Desk uses it)
Distilled from O'Neil, Minervini, Darvas, Livermore, Weinstein, Lynch, Druckenmiller, Paul Tudor Jones, the Turtles/Seykota and Schwager's *Market Wizards* interviews. Their common ground is **risk control and discipline, not prediction**.

| Principle | Who | In Signal Desk today? | Next step |
|---|---|---|---|
| Cut every loss small and fast (7–8% max) | O'Neil, Minervini, PTJ | ✓ 8% stop, never lowered | — |
| Never average down; only add to winners (pyramid) | Livermore, Darvas, O'Neil | Partly (no averaging down by habit) | Test: add ½ position once a breakout is +3–5% with the stop at breakeven |
| Respect the market trend — most stocks follow it | O'Neil, PTJ (200-day rule), Druckenmiller | ✓ market gate | v3 regime sizing; **follow-through day** to re-enter after a correction (O'Neil) — not in the app |
| Buy leaders in **leading industry groups** | O'Neil, Minervini | ✗ (stock RS only) | Test an industry-group RS gate (top 40% of groups) |
| Buy at new highs / proper pivots, not cheap-looking stocks | Darvas, O'Neil, Minervini | ✓ breakout entry | — |
| Only take trades with reward ≥ 2–3× risk | Minervini, PTJ (5:1) | ✗ | Fix #32 reward-vs-risk check (e.g. target = next resistance or +20%) |
| Take some profit into strength; let the rest run | O'Neil (+20–25%), Minervini | ✓ SCALE_OUT at +20% | Test O'Neil's 8-week hold: a stock up 20%+ within 3 weeks of a breakout is held 8 weeks |
| Size by risk; cut size after losses, grow it after wins (progressive exposure) | Minervini, Turtles, Seykota | Partly (1% risk) | Test: after 3 losses in a row → half size until a win |
| Know what you own — the story in two minutes | Lynch | ✗ | Add a one-line "why this company is growing" to BUY results (AI or 10-Q) |
| Liquidity and the Fed drive the market | Druckenmiller | Logged only (market.json: credit spreads, VIX, yield curve) | Test as a regime input in November |
| Have a written method and follow it; review every trade | All of *Market Wizards* | ✓ rules + Decision Log + this playbook | Keep adding Lessons learned |

**Where they disagree — and Signal Desk's choice:** concentration (Druckenmiller, Minervini concentrate in their best ideas) vs diversification (Turtles). Signal Desk uses 1% risk per trade with ≤ 8 positions — closer to the disciplined middle. Re-test concentration only after the system proves an edge.

## 7. Open questions for the 10/29 review
- Do pullback BUYs after sharp drops (Day Change ≤ −4%) do worse? (Scans: Day Change %, 5D Change %, Volume Pace)
- Did Holding Health scores ≤ 3/5 come before losses?
- Did BUYs beat DON'T BUYs on 5/10/20-day returns vs SPY (Outcomes tab)?
- Breakout vs pullback results; UPTREND vs PRESSURE results.

## 8. Where things are
App: https://greendoormanagment-ux.github.io/signal-desk/ · Handbook + v3 roadmap: `README.md` · Backtest: `scripts/backtest/`, reports in `backtest/` · Decision Log: Google Sheet "Signal_Desk_Decision_Log" (Scans, Trades, Outcomes, What's Working, Fix List).
_This file is public — never put account values, keys, or personal details here._
