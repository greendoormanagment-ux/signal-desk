# Signal Desk — Signal Ranking Test · pre-registration

**LOCKED · November 11, 2026 · agreed with the colleague reviewer (his five clarifications resolved below) before any ranking result was run.**
Nothing here changes the frozen live rules before January 29, 2027.

**Question.** When there are more valid breakouts than open slots, does a ranking fixed in advance, using only information available on the signal day, allocate the 10 slots better than the current method?

## 1. Fixed setup (not tuned)
- Signals: breakouts only, **original stop** (baseline), live market gate. All US stocks, point-in-time eligibility (≥ $5, ≥ $20M/day, one year of history).
- Portfolio: 10 slots, 1% risk per trade, max 20% per position, idle money in SPY. Costs 0.07%/side plus liquidity slippage (as in Round 8).
- Ranking decides the order among signals competing on the same day; everything else in portfolio construction is identical for every method.
- Development 2005–16 builds; validation 2017–25 judges once.

## 2. Candidate inputs (signal day, completed bars, no look-ahead) — six groups

| Group | Inputs |
| --- | --- |
| A. Strength | 3-month return vs SPY · 12-1 momentum percentile among eligible US stocks |
| B. Position | % above the pivot · % above the 50-day · % above the 200-day |
| C. Breakout quality | breakout-day volume ÷ 50-day average (excluding that day) · prior-20-day high–low range % |
| D. Risk | ATR(14) % of price · stop distance % |
| E. Size / liquidity | log 50-day dollar volume · S&P 500 member on the signal date (0/1) |
| F. Footprints — **EXPERIMENTAL, UNVALIDATED** | up/down volume ratio · accumulation − distribution days · closing strength · volume dry-up ratio · biggest-volume-day multiple, signed (+ up / − down) |

Group F failed as yes/no filters in session 2. It is included only to test a different question (ranking). **Its inclusion is not evidence of predictive value.** Every report shows the result with and without group F (without F = sensitivity, not used for pass/fail).

Fundamentals (EPS / sales growth) may be added only by a written amendment after Round 8 session 3, before any ranking run.

**Scaling.** Each input is converted to a percentile using cut-offs from the development-period distribution of all signals (fixed, never re-estimated on validation).

## 3. Methods (exactly four; no others)
- **M0 — current method:** the engine's existing order (best score first on the same day).
- **RANDOM — control:** 2,000 random same-day orders with identical portfolio construction, sizing, costs and cash treatment.
- **M1 — simple composite:** each input gets a direction (+1 / −1 / 0) from development data (§4). Inputs are averaged **within their group**, then the six group scores are averaged with **equal weight per group** (each group 1/6, so footprints are at most 1/6 of the score).
- **M2 — big-winner model:** L2-regularized logistic regression of P(+3R), all inputs standardized from development statistics.

**+3R outcome (M2 target).** 1 if the daily high reaches entry + 3 × (entry − original stop) **before** the daily low touches the original stop, within **252 trading days** after entry. If both happen on the same day: counted as the stop (conservative). Neither within 252 days: 0. Labels use prices up to **2016-12-31 only**; a development trade not resolved by then is left out of fitting.

## 4. Chronological cross-validation (development only)
Expanding folds: train 2005–08 → test 2009–10 · train 2005–10 → test 2011–12 · train 2005–12 → test 2013–14 · train 2005–14 → test 2015–16.
- **M1 directions:** the sign of the development-period Spearman correlation between the input and R (resolved trades only). An input keeps its sign only if that sign holds in at least 3 of the 4 test folds; otherwise its direction is 0 (left out).
- **M2 setting:** L2 strength chosen from {0.001, 0.01, 0.1, 1} by mean out-of-fold log-loss; then refit on all resolved development trades.
- Both models are then **frozen** — directions, coefficients, scaling cut-offs — and committed to GitHub before validation is run. Validation data is not touched until then.

## 5. Pass rules (validation 2017–25, once)
A ranking passes only if **all** hold:
1. **CAGR at least +2.0 percentage points per year above M0's CAGR** (equivalently, excess CAGR vs SPY at least +2.0 points above M0's), both computed the same way from daily equity over 2017–25.
2. Beats at least **95% of the 2,000 random orderings** on CAGR.
3. Maximum drawdown no more than **3 percentage points deeper** than M0's.
4. Beats M0 in **both halves** of validation (2017–21 and 2022–25).
5. Trades it actually takes average higher R than M0's, with the difference's 95% interval (two-way clustered, stock × entry month) above zero.

If both M1 and M2 pass, M1 (simpler) is chosen. Every result is reported as PASS, FAIL or INCONCLUSIVE.

## 6. Always reported
- **Top-5% winner capture:** of the eventual top 5% of validation signals by R, how many each method took vs missed (key measure).
- Turnover, top-10-stock concentration, missed opportunities, results by year and regime, rank correlation between score and R (clustered intervals), and every method with and without group F.

## 7. Guardrails
- No changes to inputs, outcome definition, models, settings or thresholds after any result is seen. New ideas become new hypotheses judged on new data (2026 onward, the live test).
- Nothing is promoted to the live app before January 29, 2027. A passing ranking becomes a next-version candidate only.
- **An inconclusive result is not permission to lower the standard.**
