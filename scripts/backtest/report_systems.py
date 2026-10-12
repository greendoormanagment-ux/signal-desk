"""Turn the newest systems-<date>.json into backtest/systems-latest.md."""
import glob, json, os, sys

out = sys.argv[1] if len(sys.argv) > 1 else "../../backtest"
r = json.load(open(sorted(glob.glob(os.path.join(out, "systems-*.json")))[-1]))
F, I, O = "full", "in-sample 2017-21", "out-of-sample 2022-26"
b = r["benchmarks"]
L = [f"# Candidate growth systems — round 1 ({r['asOf']})", "",
     f"{r['stocks']:,} stocks, Oct 2017 – today. Every system buys at the next day's open after a signal. "
     "Portfolio = $100k, 8 positions, 1% risk per trade, max 2 per sector, ranked by RS. "
     "\"Range\" = 10 runs with random tie-breaking (how much luck matters).", "",
     "**Two universes.** *broad* = stocks worth $2B+ today; it includes today's winners in the past, so it flatters "
     "everything (survivorship bias). *sp500* = a stock only counts while it was actually in the S&P 500, which is a fairer test. "
     "About 19% of past members have no free price history (mostly buyouts), so it is less biased, not bias-free.", "",
     "**Pass bar (set before the run):** at least 300 trades, at least +0.3R per trade in both halves, "
     "a smaller drawdown than SPY, and beating SPY in 2022–26.", "",
     "| Benchmark | Full CAGR | Max drawdown | 2022–26 CAGR |", "| --- | --- | --- | --- |"]
for k in ("SPY buy-and-hold", "SPY 200-day rule"):
    L.append(f"| {k} | {b[F][k]['cagr_%']}% | {b[F][k]['max_dd_%']}% | {b[O][k]['cagr_%']}% |")
for uni in ("broad", "sp500"):
    runs = [x for x in r["runs"] if x["universe"] == uni]
    if not runs:
        continue
    L += ["", f"## Universe: {uni}", "",
          "| System | Variant | Trades | Win % | Avg R (2017–21 / 2022–26) | Avg win / loss R | Portfolio CAGR, full (range) | Max DD | 2022–26 CAGR (range) | Pass? |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for x in runs:
        p = x["periods"]
        if x["system"] == "momentum_rotation":
            L.append(f"| momentum | {x['label']} | {p[F]['holdings']['holdings']:,} holdings | {p[F]['holdings']['win_%']} | – | – | "
                     f"{p[F]['portfolio']['cagr_%']}% | {p[F]['portfolio']['max_dd_%']}% | {p[O]['portfolio']['cagr_%']}% | – |")
            continue
        s, si, so = p[F]["signals"], p[I]["signals"], p[O]["signals"]
        ok = (s.get("trades", 0) >= 300 and si.get("avg_R", -9) >= 0.3 and so.get("avg_R", -9) >= 0.3
              and p[F]["mc_dd_median"] > b[F]["SPY buy-and-hold"]["max_dd_%"] and p[O]["mc_cagr"][0] > b[O]["SPY buy-and-hold"]["cagr_%"])
        L.append(f"| {x['system'].replace('_', ' ')} | {x['label']} | {s.get('trades', 0):,} | {s.get('win_%')} | {si.get('avg_R')} / {so.get('avg_R')} | "
                 f"{s.get('avg_win_R')} / {s.get('avg_loss_R')} | {p[F]['mc_cagr'][0]}% ({p[F]['mc_cagr'][1]} to {p[F]['mc_cagr'][2]}) | "
                 f"{p[F]['mc_dd_median']}% | {p[O]['mc_cagr'][0]}% ({p[O]['mc_cagr'][1]} to {p[O]['mc_cagr'][2]}) | {'yes' if ok else 'no'} |")
yrs = sorted(r["spy_yearly"])
L += ["", "## Year by year (portfolio return %)", "", "| | " + " | ".join(yrs) + " |", "| --- |" + " --- |" * len(yrs),
      "| SPY | " + " | ".join(str(r["spy_yearly"][y]) for y in yrs) + " |"]
for x in r["runs"]:
    if x["label"].startswith("base") and x["system"] == "combined" or x["label"] == "momentum top 10":
        yy = x["periods"][F].get("yearly", {})
        L.append(f"| {x['universe']} · {x['system'].replace('_', ' ')} | " + " | ".join(str(yy.get(y, "")) for y in yrs) + " |")
open(os.path.join(out, "systems-latest.md"), "w").write("\n".join(L) + "\n")
print("wrote", os.path.join(out, "systems-latest.md"))
