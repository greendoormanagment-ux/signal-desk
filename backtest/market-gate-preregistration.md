# Market gate test — pre-registration (LOCKED 2026-11-11, before any result was run)

**Question.** The live app allows real-money buys only when the market gate reads UPTREND (PRESSURE = paper only). Every backtest allowed buys in PRESSURE and blocked only CORRECTION. Which is better?

**Setup.** Breakouts only, all US stocks, point-in-time eligibility, costs 0.07%/side plus liquidity slippage (as in Round 8). Two stop bases: A2 trail (live) = primary; original stop = secondary (report only). Portfolio: 10 slots, 1% risk, idle money in SPY; **median of 10 random same-day orders**. Development 2005–16 decides; validation 2017–25 checks.

| Variant | Buys allowed when the gate reads |
| --- | --- |
| G0 | UPTREND or PRESSURE (what the backtests did) |
| G1 | UPTREND only (the live app rule) |

**Measured:** portfolio CAGR, excess vs SPY, max drawdown, Sharpe; trade level: mean R of PRESSURE-entry trades vs UPTREND-entry trades (two-way clustered by stock × entry month); share of PRESSURE days.

**Verdict (decided on development, checked on validation):**
- **ALLOW PRESSURE (G0)** if G0's CAGR is at least **+1.0 pt/yr** higher than G1's in **both** periods **and** PRESSURE-entry trades have a positive mean R with a 95% clustered interval above 0 in development and a positive mean in validation.
- **KEEP UPTREND-ONLY (G1)** if G1's CAGR is within **0.5 pt/yr** of G0's (or higher) in both periods **and** its max drawdown is at least **2 pts** shallower in both.
- **INCONCLUSIVE** otherwise → the current live rule stays (it is the more cautious one), marked 🟡 in the rule register.

No changes after results. A verdict that changes the live rule is applied as a dated amendment by Tony's decision, as with v2.16.3.
