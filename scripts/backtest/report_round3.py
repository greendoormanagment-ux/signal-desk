"""Write backtest/round3-latest.md: Gate 1 (data + engine audit) and Gate 2 (realistic re-test).
Usage: python report_round3.py AUDIT_DIR RESULTS_DIR OUT_MD [TEST_RESULT_LINE]"""
import glob, json, os, sys
import pandas as pd

audit_dir, res_dir, out_md = sys.argv[1:4]
test_line = sys.argv[4] if len(sys.argv) > 4 else "see tests/test_backtest.py"
a = json.load(open(os.path.join(audit_dir, "audit-summary.json")))
r = json.load(open(sorted(glob.glob(os.path.join(res_dir, "round3-*.json")))[-1]))
ev = pd.read_csv(os.path.join(audit_dir, "extreme_moves.csv"))
cov = pd.read_csv(os.path.join(audit_dir, "sp500_coverage.csv"))
pct = lambda x: "–" if x is None else f"{x}%"
spy, spytr = r["spy"]["eval"], r.get("spy_total_return") or {}
L = [f"# Round 3 — audit first, then a realistic re-test ({r['asOf']})", "",
     "Live Signal Desk rules were not changed. No strategy was required to beat SPY; \"no robust edge\" is an allowed result.", "",
     "## Gate 1 — data and engine integrity", "",
     f"**Data snapshot:** {a['files']:,} price files, combined SHA-256 `{a['combined_sha256'][:16]}…` (full list in `data-manifest.json`).", "",
     "### Extreme daily moves (close-to-close over 60%)", "",
     f"{a['extreme_moves']} moves in {a['stocks_with_extreme_moves']} stocks. Each was checked against Yahoo split records, an independent "
     "price source (Nasdaq historical quotes) and the next day's price. The cached prices were never edited; any correction would go in "
     "`corrections.json` and be applied in memory, with a line in `corrections_log.csv`.", "",
     "| Classification | Count | Rule |", "| --- | --- | --- |"]
rules = {"genuine": "independent source shows the same move (within 5%, log terms)",
         "unresolved": "no second source for that date, or sources disagree without a clear error pattern",
         "data error: split not adjusted": "split record within 2 sessions and the move matches its ratio",
         "data error: one-day bad bar": "second source disagrees and the move reverses the next day"}
for k, v in ev.classification.value_counts().items():
    L.append(f"| {k} | {v} | {rules.get(k, '')} |")
L += ["", f"Corrections applied: **{a['corrections']}**. None of the unresolved moves fall on a day the stock was in the S&P 500, "
      "so they cannot affect the S&P 500 tests below; Gate 2 also reran momentum without those stocks (identical result). "
      "Stocks with unresolved moves: " + ", ".join(a["stocks_with_unresolved"]) + ".", "",
      "Not detectable with these sources: spin-offs and special cash dividends (prices are not adjusted for them; KDP's 2018 "
      "special dividend is one of the unresolved items, before it joined the S&P 500).", "",
      "### Gaps and coverage", "",
      f"- Missing sessions inside a stock's own history: {a['total_missing_sessions']} (in {a['stocks_with_missing_sessions']} stock). Bad or duplicate rows: {a['bad_rows_dropped']} / {a['duplicate_rows']}.",
      f"- Stocks with at least one zero-volume day: {a['stocks_with_zero_volume_days']} (mostly thin non-S&P names; the $20M/day liquidity rule screens them out).",
      f"- Stocks whose history starts after 2016 (IPOs, spin-offs, listings): {a['stocks_starting_after_2016']}. They become eligible only after 252 sessions.", "",
      "| Year | S&P 500 members that year | With price data | Missing (mostly bought out / delisted) |", "| --- | --- | --- | --- |"]
for _, c in cov.iterrows():
    L.append(f"| {c.year} | {c.members_during_year} | {c.with_price_data} | {c.missing} ({c.missing_pct}%) |")
L += ["", "### Point-in-time rules now enforced", "",
      "- **Universe:** a stock counts only on days it was in the S&P 500, traded at $5+, averaged $20M+/day over the prior 50 days, and had 252 sessions of history.",
      "- **RS ranking:** each day ranks only the stocks eligible that day (previously: against today's whole list).",
      "- **Earnings data:** a quarter is used only from its SEC filing date; later restatements don't leak backwards (planted test 5).",
      "- **Execution:** a signal from a close trades no earlier than the next session — next open, or a next-day limit order. "
      "The round-2 \"buy at the signal close\" version was dropped. A stop crossed by an opening gap fills at the open.",
      f"- **Costs:** {r['costs_per_side']['base']*100:.2f}% per side ($0 commission + ~0.05% slippage + ~0.02% half-spread), stress test at {r['costs_per_side']['stress']*100:.2f}%.",
      "- **Sector/theme caps** use today's sector and industry labels (historical classifications aren't available free).",
      f"- **Dividends:** prices exclude dividends. SPY returned {spy.get('cagr_%')}%/yr on price but {spytr.get('cagr_%')}%/yr with dividends over the same window, "
      "so price-only comparisons flatter the strategies by roughly 1–2%/yr.", "",
      "### Planted tests", "", f"`python tests/test_backtest.py` → **{test_line}**. Synthetic stocks with hand-worked answers: "
      "next-open entry, stop gapped at the open, A2 breakeven and trail, 7.5% rule, partial exit maths, portfolio sizing and costs, "
      "momentum next-open execution, point-in-time EPS with a restatement, RS eligibility, and the move classifier.", "",
      "**Gate 1 verdict:** passes for S&P 500-based tests, with the limits above documented. It does **not** pass for a broad "
      "growth-stock universe: delisted small and mid caps are absent, so those tests must wait for a dataset that includes them.", "",
      "## Gate 2 — momentum and pullback, realistic execution", "",
      f"Evaluation window {r['eval_window'][0]} to {r['eval_window'][1]} (2026 shown separately). Benchmark SPY: {spy.get('cagr_%')}%/yr "
      f"price-only ({spytr.get('cagr_%')}% with dividends), max drawdown {spy.get('max_dd_%')}%, volatility {spy.get('vol_%')}%.", "",
      "### Momentum rotation (S&P 500, next-open execution)", "",
      "| Variant | Return/yr | vs SPY | Max DD | Volatility | Sharpe | Turnover/yr | 2026 so far |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
for m in r["momentum"]:
    e = m["eval"]
    L.append(f"| {m['label']} | {pct(e.get('cagr_%'))} | {e.get('excess_cagr_%'):+} pts | {pct(e.get('max_dd_%'))} | {pct(e.get('vol_%'))} | {e.get('sharpe')} | "
             f"{m['turnover_per_year']}× | {pct(m['2026'].get('cagr_%'))} |")
base = r["momentum"][0]
L += ["", "Non-overlapping two-year periods (base version):", "", "| Period | Momentum | SPY | Difference | Momentum max DD |", "| --- | --- | --- | --- | --- |"]
for b in base["blocks"]:
    L.append(f"| {b['period']} | {pct(b['cagr_%'])} | {pct(b['spy_cagr_%'])} | {b['excess_%']:+} pts | {pct(b['max_dd_%'])} |")
bs = base["bootstrap"]
L += ["", f"**Resampling (replaces the round-2 \"3-year windows\" figure):** {bs.get('months')} monthly differences vs SPY, resampled "
      f"{bs.get('resamples'):,} times in {bs.get('block_months')}-month blocks. Annual difference vs SPY: 5th percentile {bs.get('excess_p5_%')} pts, "
      f"median {bs.get('excess_median_%')} pts, 95th percentile {bs.get('excess_p95_%')} pts; {bs.get('share_above_zero_%'):.0f}% of resamples above zero. "
      "This describes uncertainty about the PAST average only — it is not a probability of beating SPY in the future.", "",
      "### Short-term pullback — control (S&P 500, next-session execution only)", "",
      "| Variant | Trades | Win % after costs | Avg trade after costs | Avg win / loss | Days held | Return/yr (range) | vs SPY | Max DD | Volatility |",
      "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for p in r["pullback"]:
    e = p["eval"]
    L.append(f"| {p['label']} | {p['trades_taken']:,} ({p['trades_per_year']:.0f}/yr) | {p['win_after_costs_%']} | {p['expectancy_after_costs_%']}% | "
             f"{p['avg_win_%']}% / {p['avg_loss_%']}% | {p['avg_days']} | {pct(e.get('cagr_%'))} ({p['mc_cagr_range'][0]} to {p['mc_cagr_range'][1]}) | "
             f"{e.get('excess_cagr_%'):+} pts | {pct(e.get('max_dd_%'))} | {pct(e.get('vol_%'))} |")
best = max(r["pullback"], key=lambda p: p["eval"].get("cagr_%", -99))
rd = [base["eval"]["excess_cagr_%"]] + [m["eval"]["excess_cagr_%"] for m in r["momentum"] if m["label"].startswith("rebalance on")]
L += ["", f"Best pullback version by period ({best['label']}):", "", "| Period | Pullback | SPY | Difference | Pullback max DD |", "| --- | --- | --- | --- | --- |"]
for b in best["blocks"]:
    L.append(f"| {b['period']} | {pct(b['cagr_%'])} | {pct(b['spy_cagr_%'])} | {b['excess_%']:+} pts | {pct(b['max_dd_%'])} |")
bb = best["bootstrap"]
L += ["", f"Resampled annual difference vs SPY: 5th {bb.get('excess_p5_%')} / median {bb.get('excess_median_%')} / 95th {bb.get('excess_p95_%')} pts; "
      f"{bb.get('share_above_zero_%'):.0f}% of resamples above zero.", "",
      "**Gate 2 verdict:** neither system shows a robust advantage over SPY once execution is realistic and 2026 is excluded. "
      f"Momentum: across the five rebalance days the difference vs SPY ranges from {min(rd):+} to {max(rd):+} points a year "
      f"({sum(1 for x in rd if x < 0)} of 5 behind), and every cost, cap and size variant is behind. "
      f"Pullback: the best version earns {best['expectancy_after_costs_%']}% per trade after costs with lower volatility and drawdown than SPY, "
      f"but returns {best['eval'].get('excess_cagr_%'):+} points a year vs SPY and most of the edge disappears at the stress cost.", "",
      "## Gate 3 — external data", "", "Not started. Before paying for any dataset, confirm on a free tier that it actually contains the missing "
      "S&P 500 members listed in `sp500_coverage.csv` and delisted small/mid caps. The purpose would be testing the leader-breakout idea on a broad "
      "growth universe — not rescuing these two systems.", "",
      "## Reproduce", "", "```", "cd scripts/backtest",
      "python tests/test_backtest.py",
      "SEC_DIR=<sec cache> python audit.py <prices> <prices-sp> <sp500_ticker_start_end.csv> <audit out>",
      "python run_round3.py <prices> <sec cache> <results out> <prices-sp> <sp500_ticker_start_end.csv> <audit out>",
      "python report_round3.py <audit out> <results out> ../../backtest/round3-latest.md", "```",
      "Results depend on the data snapshot; compare the combined SHA-256 above before comparing numbers."]
open(out_md, "w").write("\n".join(L) + "\n")
print("wrote", out_md)
