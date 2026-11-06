# Signal Desk — Footprint Test Constitution

**LOCKED · November 6, 2026 · agreed with the colleague reviewer before any Session 2 footprint result was run or examined.**
Code and definitions frozen at repo commit `9cd4d99` (index.html `footprints()`, app v2.16).
Nothing here changes the frozen live rules before January 29, 2027.

## Locked thresholds

| Item | Value |
| --- | --- |
| Minimum incremental expectancy per trade (after costs) | **+0.15R** |
| Family-wise statistical confidence | **99%, two-sided, Holm-adjusted** |
| Materially negative regime effect | estimated effect **below −0.10R** |
| Maximum permitted additional drawdown | **3 percentage points** deeper than the comparator |
| Minimum trades WITH the footprint | **300** |
| Minimum trades WITHOUT the footprint | **300** |
| Primary analysis | All US stocks pooled |
| Consistency analysis | S&P 500 · non-S&P · four regimes (bull, bear, sideways, high volatility) |
| Clustering | Two-way: stock and entry month |
| Periods | 2005–2016 development · 2017–2025 validation |

## The pre-registered family (6 primary tests)

Each footprint is measured on the signal day from completed daily bars, exactly as Signal Desk's `footprints()` calculates it. **"With the footprint" = the app's ✓ reading; "without" = every other qualified trade.**

| # | Footprint | Calculation (frozen) | "With" means |
| --- | --- | --- | --- |
| 1 | Up/down volume | volume on up days ÷ volume on down days, 50 sessions | ratio **≥ 1.1** |
| 2 | Accumulation/distribution | days up ≥ 0.2% / down ≥ 0.2% on above-50-day-average volume, 25 sessions | accumulation days **>** distribution days |
| 3 | Closing strength | average (close − low) ÷ (high − low), 10 sessions | **≥ 0.60** |
| 4 | Pocket pivot | up-day volume > every down day's volume in the prior 10 sessions, close ≥ 99% of the 10-day average | present in the **last 3 sessions** |
| 5 | Volume dry-up | 10-day ÷ 50-day average volume | **< 0.75** |
| 6 | Biggest-volume day | largest-volume day of the last 50 sessions | an **up** day at **≥ 2×** average volume |

Holm correction applies across exactly these six tests.
The 21-day moving average, 12-1 momentum and earnings-gap drift form a **separate family** with their own Holm correction. Any combination tests form their **own pre-registered family** with their own correction.

## The rules — a footprint passes only if ALL are met

1. **Incremental value.** At least +0.15R per trade after costs versus otherwise-qualified trades without that footprint — same entry, exit, stop, market gate, position sizing, period and universe. The test is whether it adds information beyond the existing rules, not whether such stocks do better in general. Report the difference in R, its confidence interval, trade counts and effect size.
2. **Statistical confidence.** The difference is positive under the 99% two-sided family-wise standard (Holm-adjusted p-values or equivalent adjusted intervals), clustered by stock and entry month, and the estimate is at least +0.15R.
3. **Out-of-sample.** Development (2005–16): meets rules 1–2. Validation (2017–25): positive incremental effect, no material deterioration. Nothing is selected, modified or tuned on the validation years. If a footprint is later modified, a new holdout period is required.
4. **Consistency.** Positive estimated effect in both S&P 500 and non-S&P stocks, and in at least 3 of 4 regimes; no regime below −0.10R. Subgroups do not each need significance; report the sample size and interval for every subgroup. The S&P vs non-S&P difference is tested directly (clustered), not inferred from one subgroup being significant and the other not.
5. **Adequate evidence and portfolio value.** At least 300 trades with and 300 without. The portfolio's return vs SPY must improve after costs, with identical starting capital, sizing, exposure limits, costs and construction, and maximum drawdown no more than 3 pp deeper than the rules-only portfolio. Report annual return, maximum drawdown, turnover and SPY-relative return.
6. **Combinations.** Must beat the best individual footprint by at least +0.15R per trade, meet the same adjusted statistical standard within their own family, be positive in validation, improve the portfolio after costs, and not worsen subgroup consistency. Drawdown is compared with the best individual footprint's portfolio. Matching the best single footprint is a fail.
7. **Frozen methodology.** After testing begins, no changes to definitions, lookbacks, thresholds, entry/exit rules, sample minimums or statistical methods. A result that suggests a better threshold becomes a future hypothesis, tested separately.
8. **Complete reporting.** Every test is reported as **Pass** (meets every requirement), **Fail** (evidence shows it does not meet the economic or statistical requirements) or **Inconclusive** (too few observations, wide intervals or conflicting evidence). Nothing is omitted.

**An inconclusive result is not permission to lower the standard.**

_No footprint earns authority because it looks convincing. It earns authority only by passing the rules established before we see the results._
