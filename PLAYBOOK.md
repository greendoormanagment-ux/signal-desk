# Signal Desk Playbook

_The one page Claude reads before analyzing any stock or position for Tony. Rules decide; evidence ranks; lessons accumulate._
_Last updated: Oct 20, 2026 · app v2.12 · 30-day live test 9/29 → 10/29 (rules frozen)_

## 1. How to analyze a stock (every time, in this order)
1. **Market regime first.** SPY/QQQ vs 50-day + distribution days (app's gate: UPTREND / PRESSURE / CORRECTION). Also note: S&P vs its 200-day; failed index breakout (closed back under a high it just broke); leaders vs average stock (SPY vs RSP). PRESSURE or worse → new buys are **paper only**.
2. **Leadership.** Is it a leader? RS vs S&P (Mansfield + 3-month in the app; 12-month-skip-1 is the best-proven measure), distance from 52-week high (want ≤ 25%, ideally ≤ 15%), Minervini Trend Template (§3).
3. **Fundamentals.** Latest-quarter EPS ≥ +25% vs year-ago (SEC data; if > 100%, check for one-time items); sales growth; next earnings date (no new buys within 14 days).
4. **Setup.** Breakout (close above pivot on ≥ 1.4× volume, ≤ 5% extended) is the strongest-evidence entry. Pullback-to-50-day is the weakest — apply the §5 lessons. Before 4 PM ET volume is partial → treat as WATCH; rescan after the close (24-hour rule).
5. **Risk.** 1% of account per trade; stop ≤ 8% below entry, placed on fill, never lowered. Stop rule A2: original stop until +1R → breakeven → at +2R trail = max(breakeven, high since entry − 3×ATR).
6. **Crowding.** Same sector AND same theme (e.g. AI infrastructure spans Technology + Industrials + Utilities). Flag 3+ positions in one theme.
7. **Lessons check.** Compare with §5 and the mistake tally (§12) — does this look like a past mistake? Check the calendar (§10) and, for holdings, the sell (§7) and earnings (§8) playbooks.
8. **Straight take.** Buy real / buy paper / watch / pass / hold / trim / sell — with the one or two reasons that matter most. No financial-advisor disclaimers (Tony decides).
9. **Log the call** in the scorecard (§13) with a confidence level, so it can be graded later.

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

## 7. Sell playbook (for holdings — guidance now; candidates for the November backtest)
The hard rules stay: stop ≤ 8% below entry, never lowered; stop rule A2; SCALE_OUT at +20%. On top of those, watch for these warning signs (O'Neil, Minervini, Weinstein):

| Signal | What it looks like | Take |
|---|---|---|
| **Failed breakout** | Closes back below the pivot within a few days of breaking out, especially on volume | Biggest early warning. Cut or tighten to just under the breakout-day low |
| **Heavy-volume break of the 50-day** | First close below the 50-day on above-average volume after a run | Sell at least half; leaders often bounce off the 50-day, they rarely slice through it on volume |
| **Climax run** | Late in a long move: the biggest weekly gain of the run, several up days in a row, a gap up on huge volume | Take profit into strength — climax tops are where leaders peak |
| **Worst day of the move** | Largest one-day % drop since the breakout, on the heaviest volume | Treat as distribution; tighten stop or trim |
| **Distribution cluster** | 3+ down days on rising volume within ~2 weeks; footprints read flips to DISTRIBUTION | Tighten stop; no adding |
| **Stage change** (Weinstein) | 30-week (≈150-day) line flattens and price drops under it | Stage 3/4 — exit what's left |
| **Market turns** | Gate goes UPTREND → PRESSURE → CORRECTION | Tighten stops; no new real buys (v3 Layer 4) |

Process: decide the sell rule **before** the trade, write it in the Trades notes, and grade "did I follow it?" separately from "did it make money?"

## 8. Earnings playbook
Earnings are the biggest single-day risk for a holding. Gaps can jump straight past the stop.

**Before the report (holding):**

- Find the **expected move**: the options market's at-the-money straddle ÷ price (Barchart / broker "implied move"). Also look at the last 4 reports' moves.
- **Cushion test:** if the gain since entry > the expected move → OK to hold the full position. If the cushion is smaller → trim to half (or less) before the report. If the position is at a loss → don't hold a full position through it.
- Never add in the 14 days before a report (frozen rule).

**After the report:**

- **Gap up on heavy volume (≥ 2× normal) that holds the gap-day low** for 1–3 days = post-earnings drift setup, one of the better-documented edges (Bernard & Thomas 1989). Can add/buy on a hold of that low; stop under it.
- **Gap down through the stop** = sell at the open. No "waiting for a bounce."
- **Gap down but stop holds** = re-run Position Review after the close; a close below the 50-day on volume → sell (§7).
- Guidance matters more than the quarter: a beat with a guidance cut often fails.

Upcoming: KNSA 10/27, FCX 10/27 (FOMC 10/27–28 — same days, double event risk).

## 9. Setup library (exact definitions)
Pivot = the price the stock must close above to start a move (usually the top of the base/handle, + a few cents). Volume on the breakout ≥ 1.4× (frozen rule; O'Neil prefers ≥ 1.5×).

| Setup | Definition (O'Neil / Minervini) | Notes |
|---|---|---|
| **Cup with handle** | 7–65 weeks; cup 12–33% deep (up to ~50% in bad markets); handle in the upper half, drifts down ≤ 8–12% on light volume; pivot = handle high | The classic; a handle in the lower half or a "V" with no rest is weaker |
| **Flat base** | ≥ 5 weeks, ≤ 15% deep, usually after a prior breakout | Often a 2nd-stage base — good |
| **Volatility contraction (VCP)** | 2–4 pullbacks, each shallower (e.g. 25% → 12% → 6%), volume drying up on the last one; pivot = top of the last contraction | Footprints "volume dry-up" < 75% fits this |
| **High tight flag** | Up 100%+ in 4–8 weeks, then a 10–25% pullback over 3–5 weeks | Rare, powerful, volatile — size small |
| **Pullback to 50-day** | Orderly decline to the 50-day on lighter volume in an uptrend | Weakest evidence (§2, §5). Not after a −4% day / −10% week; not > 15–20% off the high |

**Base count:** count bases since the stock's last major low. **1st–2nd stage bases work best; 3rd–4th stage bases fail far more often** (the move is late, everyone owns it). A deep correction (> ~50%) resets the count. Note the base count on every BUY.
Extended = > 5% past the pivot → don't chase (frozen rule).

## 10. Market calendar check
Before a new real buy, check: **FOMC** decision days, **CPI**, the **jobs report** (usually the first Friday), and the stock's own earnings. These days bring large index moves; a breakout the day before can be undone the next morning. Not a rule — a "wait one day" nudge.
2026: FOMC Oct 27–28, Dec 8–9 (verify on federalreserve.gov). CPI and jobs dates: bls.gov release calendar.

## 11. Reading the institutional footprints panel (v2.12, info only)

| Signal | Evidence | How to read |
|---|---|---|
| Insider open-market **buys**, especially 2+ insiders ("cluster") | **Strong** — Lakonishok & Lee 2001; Cohen, Malloy & Pomorski 2012 | Real conviction: insiders sell for many reasons, buy for one. Sales are weak signals (often planned/routine) |
| **Estimate revisions** (rising analyst EPS estimates) | **Strong** — Chan, Jegadeesh & Lakonishok 1996 | Rising + price strength = good. Ignore anything flagged "suspect" (data change) |
| **Short interest** (days to cover ≥ 8) | **Moderate** — Asquith, Pathak & Ritter 2005 (high short interest predicts weak returns) | Pros betting against it. Also squeeze fuel — but don't buy *because* of a squeeze |
| **Up/down volume, accumulation/distribution days, pocket pivot, closing strength, dry-up** | **Practitioner** (O'Neil, Morales & Kacher) — little academic testing | Useful context; confirm a breakout, warn on a holding. Being tested in the day-30 review and November |

Overall read: ACCUMULATION / leaning / neutral / leaning distribution / DISTRIBUTION. Biggest weight: a DISTRIBUTION read on a holding = tighten stop (§7).

## 12. Mistake tally (tag every lesson in §5; fix the costliest first)

| Tag | Count | Examples |
|---|---|---|
| Deep or sharp "pullback" bought (really a correction / selling) | 3 | MRVL 10/15 (−26% from high), DDOG & PLTR 10/16 (−7% days) |
| Theme crowding | 1 | MRVL + PWR 10/17 (AI capex) |
| Buying into a weak / rotating market | 1 | 10/17 leader rotation |
| Earnings timing | 1 | PWR 10/15 |
| Missing / lagging data | 2 | CVE foreign filer 10/15; KNSA SEC lag 10/20 |
| Logging bug | 1 | Entry Price leak (v2.10.1) |
| Chased extended | 0 | — |

At each review: add the money result per tag (from Trades/Outcomes) — the tag that cost the most gets the next fix.

## 13. Scorecard — Claude's calls (graded at each review)
Every straight take gets a row. Confidence = how sure (50% = coin flip, 80% = strong). Grade at 5 / 10 / 20 trading days vs SPY; "right" = the stock beat SPY for buy/hold calls, lagged it for pass/sell/trim calls. Goal: calls marked 70%+ should be right ~70%+ of the time. If not, I'm overconfident.

| Date | Ticker | Call | Conf. | Price | Why (short) | 5d | 10d | 20d |
|---|---|---|---|---|---|---|---|---|
| 10/20 | KNSA | Hold into 10/27 earnings, stop unchanged | 60% | $83.02 | RS +37, ACCUMULATION footprints, pocket pivot 10/19; Q2 EPS +30%, revenue +55% | | | |

## 14. Open questions for the 10/29 review
- Do pullback BUYs after sharp drops (Day Change ≤ −4%) do worse? (Scans: Day Change %, 5D Change %, Volume Pace)
- Did Holding Health scores ≤ 3/5 come before losses?
- Did BUYs beat DON'T BUYs on 5/10/20-day returns vs SPY (Outcomes tab)?
- Breakout vs pullback results; UPTREND vs PRESSURE results.
- Did ACCUMULATION vs DISTRIBUTION footprint reads predict 5/10-day returns?
- When Claude's market read disagreed with the rules gate (e.g. 10/20: Claude UPTREND, rules PRESSURE), who was right?
- Scorecard (§13): hit rate by confidence level.

## 15. Where things are
App: https://greendoormanagment-ux.github.io/signal-desk/ · Handbook + v3 roadmap: `README.md` · Backtest: `scripts/backtest/`, reports in `backtest/` · Decision Log: Google Sheet "Signal_Desk_Decision_Log" (Scans, Trades, Outcomes, What's Working, Fix List).
_This file is public — never put account values, keys, or personal details here._
