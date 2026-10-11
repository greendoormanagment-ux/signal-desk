"""Turn the newest backtest-<date>.json into backtest/latest.md (plain-English tables)."""
import glob, json, os, sys

out = sys.argv[1] if len(sys.argv) > 1 else "../../backtest"
src = sorted(glob.glob(os.path.join(out, "backtest-*.json")))[-1]
r = json.load(open(src))
FULL, IS, OOS = "full 2017-2026", "in-sample 2017-2021", "out-of-sample 2022-2026"
L = [f"# Signal Desk backtest — {r['asOf']}", "",
     f"Live entry rules (v2.9.7) + stop rule A2 replayed on {r['stocks']:,} stocks ({r['with_sec']:,} with SEC EPS history), "
     f"Oct 2017 – today. Buys fill at the next day's open. Universe: {r['universe']}.", "",
     "**Read with care:** the universe is today's stocks, so companies that failed or were delisted are missing "
     "(survivorship bias, Fix List #69). That flatters every variant, most of all the ones that hold winners longer. "
     "Portfolio figures are the median of 10 runs with random tie-breaking among same-day buys; the range shows how much luck matters.", "",
     "## Benchmarks", "", "| Period | SPY buy-and-hold CAGR | max drawdown | SPY 200-day rule CAGR | max drawdown |", "| --- | --- | --- | --- | --- |"]
for p, b in r["benchmarks"].items():
    a, s = b["SPY buy-and-hold"], b["SPY 200-day rule"]
    L.append(f"| {p} | {a['cagr_%']}% | {a['max_dd_%']}% | {s['cagr_%']}% | {s['max_dd_%']}% |")
L += ["", "## Variants (one change at a time vs the live rules)", "",
      "Avg R = average result per trade in units of the initial risk (0.10 = earns 10% of what it risks). "
      "Portfolio = $100k, 10 positions max, 1% risk per trade.", "",
      "| Variant | Trades | Win % | Avg R (in / out of sample) | Profit factor | Portfolio CAGR median (range), full | Out-of-sample CAGR median (range) |",
      "| --- | --- | --- | --- | --- | --- | --- |"]
for v in r["variants"]:
    f, i, o = v["periods"][FULL], v["periods"][IS], v["periods"][OOS]
    a = f["all_signals"]; m = f["portfolio_mc"]; mo = o["portfolio_mc"]
    L.append(f"| {v['name']} | {a['trades']:,} | {a['win_%']} | {i['all_signals']['avg_R']} / {o['all_signals']['avg_R']} | "
             f"{a['profit_factor']} | {m['cagr_median_%']}% ({m['cagr_low_%']} to {m['cagr_high_%']}) | "
             f"{mo['cagr_median_%']}% ({mo['cagr_low_%']} to {mo['cagr_high_%']}) |")
L += ["", "## Do the ratings predict anything? (20 trading days, vs SPY)", "",
      "First-time signals and rating changes only.", "", "| Rating | Signals | Avg vs SPY, 20 days |", "| --- | --- | --- |"]
for k, v in sorted(r["ratings_vs_spy"].items()):
    L.append(f"| {k} | {v['rel20d']['n']:,} | {v['rel20d']['avg_vs_spy_%']:+.2f}% |")
L += ["", "## BUY signals broken down (20 days vs SPY)", "", "| Group | Signals | Avg | Median |", "| --- | --- | --- | --- |"]
for key, label in (("buy_by_setup", "setup"), ("buy_by_market", "market"), ("buy_by_rs", "rs"), ("buy_by_rsrank", "b")):
    for x in r[key]:
        L.append(f"| {key.replace('buy_by_', '')}: {x[label]} | {x['count']:,} | {x['mean']:+.2f}% | {x['median']:+.2f}% |")
L += ["", "## Base trades: exits and years", "", "| Exit reason | Trades | Avg return | Avg R |", "| --- | --- | --- | --- |"]
for x in r["base_exit_reasons"]:
    L.append(f"| {x['why']} | {x['n']:,} | {x['avg_ret']:+.2f}% | {x['avg_R']:+.2f} |")
L += ["", "| Year | Trades | Win % | Avg R |", "| --- | --- | --- | --- |"]
for x in r["base_by_year"]:
    L.append(f"| {x['y']} | {x['n']:,} | {x['win']} | {x['avg_R']:+.2f} |")
mm = r["base_mae_mfe"]
L += ["", f"Average best point reached (MFE): {mm['avg_MFE_R_all']}R · average worst point (MAE): {mm['avg_MAE_R_all']}R · "
      f"losing trades that were up at least +1R first: {mm['losers_that_first_reached_+1R_%']}%.", ""]
open(os.path.join(out, "latest.md"), "w").write("\n".join(L))
print("wrote", os.path.join(out, "latest.md"))
