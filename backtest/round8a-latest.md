# Round 8 · session 1 — do the three fixes hold beyond the S&P 500? (2026-11-06)

**Data:** private EODHD all-US download (not in this repo). 6,139 US stocks were ever tradable (≥ $5, ≥ $20M/day); 456 files too damaged to repair were left out; **5,671 tested, 2,856 of them later delisted or acquired** (no survivorship bias). A stock can be bought only on days it was eligible *then* (price, 50-day dollar volume, one year of history).

**Rules:** today's price rules (trend, breakout on 1.4× volume, market gate, earnings timing not available → price rules only; fundamentals come in session 3). Idle money in SPY. **Costs:** 0.07%/side plus extra slippage for thinner stocks (+0.15%/side under $50M/day, +0.05% at $50–100M).

**Tune 2005–16 chooses · judge 2017–25 only checks.** Benchmarks: SPY 7.5%/yr tune, 14.9%/yr judge (max DD -33.7%) · RSP (equal-weight S&P, the 'average stock') 8.6% / 11.1%.

**Statistics (colleague review):** median of random same-day orders; judge bootstrap vs SPY; trade-level mean R after costs with a 95% interval **clustered by stock and by entry month** (shown next to the naive interval); results split by market regime (SPY vs its 200-day: bull / bear / sideways; high volatility = 20-day SPY volatility above 25%).

## 1. Verdicts on the three fixes (each judged on: statistically real · worth it after costs · consistent across regimes)

| Fix | All US, judge 2017–25 | S&P 500 / non-S&P | Regimes | Verdict |
| --- | --- | --- | --- | --- |
| **Original stop instead of A2 trail** | -11.9 → **-5.2** pts/yr vs SPY; mean R 0.093 [0.007, 0.18] → **0.634 [0.41, 0.858]** | better in all 3 universes, both periods (S&P -10.5 → +0.1) | positive in every regime (A2 negative in bear/sideways) | ✅ **Confirmed — strong** |
| **Breakouts only** (no pullback buys) | -6.2 → **-5.2** pts/yr; mean R 0.517 → 0.634 (intervals overlap) | S&P -6.6 → +0.1; non-S&P -6.7 → -7.7 | mixed | 🟡 **Supported, not proven** — keep (already live) |
| **Stronger market rule** (SPY > 200-day, or half size) | live gate -5.2 · half size -5.1 · SPY>200 -5.5; max DD -37.1 → -33.9% | tune: SPY>200 cost -2.8 pts/yr | — | ❌ **Not confirmed** — small drawdown help, no return gain; keep today's gate |

## 2. Where it works: big companies, not small ones

Best version (breakouts only + original stop + today's gate), judge 2017–25:

| Universe | CAGR | vs SPY | vs RSP | Max DD | Sharpe | Sortino | Calmar | Trades | Mean R [clustered 95%] | Median R | Win % | Bootstrap > SPY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S&P 500 | 15.0% | +0.1 | +3.9 | -37.6% | 0.77 | 0.97 | 0.42 | 2,072 | 0.67 [0.351, 0.988] | -1.016 | 29.8% | 68.0% |
| all US | 9.65% | -5.2 | -1.4 | -37.1% | 0.54 | 0.69 | 0.28 | 7,752 | 0.634 [0.41, 0.858] | -1.019 | 25.2% | 7.0% |
| non-S&P | 7.25% | -7.7 | -3.9 | -42.8% | 0.42 | 0.55 | 0.18 | 5,680 | 0.621 [0.397, 0.844] | -1.022 | 23.5% | 2.0% |

- **S&P 500 stocks: matched SPY (+0.1 pts/yr) and beat the equal-weight average stock by ~4 pts/yr** in 2017–25, a mega-cap-led decade.
- **Non-S&P stocks lagged SPY by ~7–8 pts/yr** with similar per-trade results — smaller stocks are noisier and the 10 slots fill with weaker names. Signal Desk's rules fit larger companies better.
- **Shape of the edge:** median trade ≈ −1R and only 25–30% winners; the average is positive because a few winners are very large. Expect long losing streaks — that's normal for this system, not a sign it broke.

## 3. The colleague's statistics points, in numbers

- **Clustering matters:** the clustered interval is **1.4–4.3× wider** than the naive one (repeat trades in the same stock and month are not independent). Conclusions above use the clustered intervals.
- **Regimes:** the original-stop version stayed positive in bull, bear, sideways and high-volatility markets (all US); the A2 trail was negative in bear, sideways and high-volatility periods in 2017–25.

## 4. All 36 cells

| Universe | Setup | Exit | Market | Tune vs SPY | Judge vs SPY | Judge vs RSP | Judge DD | Judge mean R [clustered] | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all US | breakouts + pullbacks | A2 trail | live gate | -7.0 | -13.8 | -10.0 | -43.0% | 0.086 [0.01, 0.162] | 59,613 |
| S&P 500 | breakouts + pullbacks | A2 trail | live gate | -8.7 | -9.1 | -5.2 | -34.8% | 0.14 [0.051, 0.23] | 16,072 |
| non-S&P | breakouts + pullbacks | A2 trail | live gate | -13.0 | -14.2 | -10.4 | -50.1% | 0.066 [-0.01, 0.142] | 43,541 |
| all US | breakouts + pullbacks | original stop | live gate | -3.1 | -6.2 | -2.4 | -39.8% | 0.517 [0.309, 0.724] | 22,361 |
| S&P 500 | breakouts + pullbacks | original stop | live gate | -0.6 | -6.6 | -2.8 | -34.1% | 0.593 [0.351, 0.836] | 6,332 |
| non-S&P | breakouts + pullbacks | original stop | live gate | +0.1 | -6.7 | -2.9 | -39.85% | 0.486 [0.276, 0.697] | 16,029 |
| all US | breakouts + pullbacks | A2 trail | half size if not UPTREND | -4.5 | -11.3 | -7.5 | -38.35% | 0.086 [0.01, 0.162] | 59,613 |
| S&P 500 | breakouts + pullbacks | A2 trail | half size if not UPTREND | -6.4 | -7.1 | -3.3 | -33.3% | 0.14 [0.051, 0.23] | 16,072 |
| non-S&P | breakouts + pullbacks | A2 trail | half size if not UPTREND | -11.2 | -12.9 | -9.2 | -43.85% | 0.066 [-0.01, 0.142] | 43,541 |
| all US | breakouts + pullbacks | original stop | half size if not UPTREND | -0.3 | -5.2 | -1.4 | -37.3% | 0.517 [0.309, 0.724] | 22,361 |
| S&P 500 | breakouts + pullbacks | original stop | half size if not UPTREND | -0.5 | -6.7 | -2.9 | -34.3% | 0.593 [0.351, 0.836] | 6,332 |
| non-S&P | breakouts + pullbacks | original stop | half size if not UPTREND | -0.6 | -6.2 | -2.4 | -37.8% | 0.486 [0.276, 0.697] | 16,029 |
| all US | breakouts + pullbacks | A2 trail | SPY above 200-day | -8.2 | -8.3 | -4.5 | -40.4% | 0.073 [-0.009, 0.155] | 59,621 |
| S&P 500 | breakouts + pullbacks | A2 trail | SPY above 200-day | -7.3 | -6.3 | -2.5 | -34.0% | 0.122 [0.026, 0.218] | 16,078 |
| non-S&P | breakouts + pullbacks | A2 trail | SPY above 200-day | -7.8 | -10.9 | -7.1 | -39.65% | 0.055 [-0.027, 0.136] | 43,543 |
| all US | breakouts + pullbacks | original stop | SPY above 200-day | -0.9 | -5.8 | -2.0 | -38.2% | 0.486 [0.269, 0.703] | 22,226 |
| S&P 500 | breakouts + pullbacks | original stop | SPY above 200-day | -0.3 | -5.2 | -1.4 | -33.9% | 0.571 [0.327, 0.814] | 6,259 |
| non-S&P | breakouts + pullbacks | original stop | SPY above 200-day | -1.6 | -6.8 | -3.0 | -46.75% | 0.453 [0.232, 0.673] | 15,967 |
| all US | breakouts only | A2 trail | live gate | -4.6 | -11.9 | -8.1 | -37.1% | 0.093 [0.007, 0.18] | 12,293 |
| S&P 500 | breakouts only | A2 trail | live gate | -3.0 | -10.5 | -6.7 | -31.6% | 0.177 [0.06, 0.295] | 3,230 |
| non-S&P | breakouts only | A2 trail | live gate | -2.3 | -13.6 | -9.8 | -41.55% | 0.063 [-0.021, 0.147] | 9,063 |
| all US | breakouts only | original stop | live gate | +0.6 | -5.2 | -1.4 | -37.1% | 0.634 [0.41, 0.858] | 7,752 |
| S&P 500 | breakouts only | original stop | live gate | +2.0 | +0.1 | +3.9 | -37.6% | 0.67 [0.351, 0.988] | 2,072 |
| non-S&P | breakouts only | original stop | live gate | -1.7 | -7.7 | -3.9 | -42.8% | 0.621 [0.397, 0.844] | 5,680 |
| all US | breakouts only | A2 trail | half size if not UPTREND | -2.1 | -9.5 | -5.7 | -34.8% | 0.093 [0.007, 0.18] | 12,293 |
| S&P 500 | breakouts only | A2 trail | half size if not UPTREND | -2.6 | -8.1 | -4.2 | -32.55% | 0.177 [0.06, 0.295] | 3,230 |
| non-S&P | breakouts only | A2 trail | half size if not UPTREND | +0.0 | -12.6 | -8.8 | -36.35% | 0.063 [-0.021, 0.147] | 9,063 |
| all US | breakouts only | original stop | half size if not UPTREND | +0.1 | -5.1 | -1.3 | -37.4% | 0.634 [0.41, 0.858] | 7,752 |
| S&P 500 | breakouts only | original stop | half size if not UPTREND | +1.2 | -0.7 | +3.1 | -37.55% | 0.67 [0.351, 0.988] | 2,072 |
| non-S&P | breakouts only | original stop | half size if not UPTREND | +1.2 | -7.3 | -3.5 | -38.85% | 0.621 [0.397, 0.844] | 5,680 |
| all US | breakouts only | A2 trail | SPY above 200-day | -4.3 | -8.1 | -4.2 | -32.25% | 0.098 [0.009, 0.186] | 12,190 |
| S&P 500 | breakouts only | A2 trail | SPY above 200-day | -3.2 | -9.0 | -5.2 | -31.7% | 0.185 [0.068, 0.302] | 3,235 |
| non-S&P | breakouts only | A2 trail | SPY above 200-day | -4.9 | -9.2 | -5.5 | -35.5% | 0.066 [-0.021, 0.153] | 8,955 |
| all US | breakouts only | original stop | SPY above 200-day | -2.2 | -5.5 | -1.7 | -33.9% | 0.629 [0.401, 0.856] | 7,674 |
| S&P 500 | breakouts only | original stop | SPY above 200-day | +2.3 | -1.9 | +1.9 | -32.6% | 0.69 [0.368, 1.011] | 2,061 |
| non-S&P | breakouts only | original stop | SPY above 200-day | -1.8 | -8.7 | -4.9 | -37.2% | 0.606 [0.38, 0.832] | 5,613 |

**Limits:** price rules only (EPS/sales filter not applied — session 3); 456 damaged files (8%) left out; delisted stocks exit at their last traded price; one trade at a time per stock. Nothing here changes the live test (frozen until Jan 29, 2027) — findings go into the next version.

_Generated by scripts/backtest/run_round8a.py from privately held EODHD data (not in this repo)._
