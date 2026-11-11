# Market gate — real money only in UPTREND, or also in PRESSURE? (2026-11-11)

Pre-registered in `backtest/market-gate-preregistration.md` (locked before the run). Code: `scripts/backtest/run_round8e.py`. Breakouts only, all US stocks, costs as in Round 8, portfolio = median of 10 random same-day orders. The gate read PRESSURE on about half of all days (53% in 2005–16, 50% in 2017–25).

| Stop | Period | G0: UPTREND or PRESSURE | G1: UPTREND only (live rule) | G1 − G0 return |
| --- | --- | --- | --- | --- |
| A2 trail (live) | 2005–16 | 2.5%/yr · DD −62% | **3.9%/yr · DD −50%** | **+1.5 pts** |
| A2 trail (live) | 2017–25 | 3.0%/yr · DD −37% | **5.0%/yr · DD −38%** | **+2.0 pts** |
| Original stop | 2005–16 | 6.9%/yr · DD −58% | **7.6%/yr · DD −69%** | **+0.7 pts** |
| Original stop | 2017–25 | 9.7%/yr · DD −37% | **13.8%/yr · DD −36%** | **+4.1 pts** |

**Trade level (G0 trades, mean R, 95% clustered interval):** PRESSURE entries earn less than UPTREND entries in every case — original stop: +0.72R [0.46, 0.98] vs +1.15R in 2005–16; +0.57R [0.33, 0.80] vs +0.71R in 2017–25. With the A2 stop PRESSURE entries are near zero (+0.07R / +0.08R, intervals include 0).

**Verdict (pre-registered rule): INCONCLUSIVE → the live rule stays (UPTREND only).** UPTREND-only had the higher return in all four comparisons, but the "keep" rule also required a drawdown at least 2 pts shallower in both periods, and drawdowns were mixed. So the data leans clearly toward the live rule without meeting the full bar.

**What it means:** PRESSURE breakouts are still profitable on average (with the original stop), just less so — and they take slots that UPTREND breakouts use better. This reverses Round 4's S&P-only finding on the much larger all-US data. It also connects to the slot-ranking question: market condition on the signal day may be a useful ranking input.

**Limits:** price rules only; rules-based market reading; portfolio results depend on the 10-slot construction.
