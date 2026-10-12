"""Turn the newest round2-<date>.json into backtest/round2-latest.md."""
import glob, json, os, sys

out = sys.argv[1] if len(sys.argv) > 1 else "../../backtest"
r = json.load(open(sorted(glob.glob(os.path.join(out, "round2-*.json")))[-1]))
b = r["benchmarks"]
P = ["full", "2017-21", "2022-26", "2017-25 (no 2026)", "2026 so far"]
L = [f"# Round 2 — short-term pullbacks and a momentum stress test ({r['asOf']})", "",
     "Main universe: stocks only while they were in the S&P 500 (point-in-time membership), which is fairer than today's list.", "",
     "## Benchmarks (CAGR / max drawdown)", "", "| | " + " | ".join(P) + " |", "| --- |" + " --- |" * len(P)]
for k in ("SPY", "RSP (equal-weight S&P)"):
    L.append(f"| {k} | " + " | ".join(f"{b[p][k].get('cagr_%')}% / {b[p][k].get('max_dd_%')}%" for p in P) + " |")
L += ["", "## (a) Short-term pullback (mean reversion)", "",
      "Buy a sharp 2–3 day dip (RSI(2) under 10) in a stock above its 200-day; sell on the bounce. "
      "Portfolio: 10 slots of 10%, max 3 per sector, 0.1% cost per side unless noted. "
      "CAGR is the median of 10 runs with random tie-breaking among same-day buys (range in brackets).", "",
      "| Universe | Variant | Trades | Win % | Avg trade | Avg win / loss | Days held | CAGR full (range) | Max DD | CAGR 2017–21 | CAGR 2022–26 |",
      "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for x in r["mean_reversion"]:
    f = x["periods"]["full"]
    L.append(f"| {x['universe']} | {x['label']} | {f['trades']:,} | {f['win_%']} | {f['avg_ret_%']}% | {f['avg_win_%']}% / {f['avg_loss_%']}% | "
             f"{f['avg_days']} | {f['mc_cagr'][0]}% ({f['mc_cagr'][1]} to {f['mc_cagr'][2]}) | {f['mc_dd_median']}% | "
             f"{x['periods']['2017-21']['mc_cagr'][0]}% | {x['periods']['2022-26']['mc_cagr'][0]}% |")
L += ["", "## (b) Momentum rotation stress test", "",
      "Each month, hold the 10 S&P 500 members with the best 12-month return (skipping the last month) that are above their 200-day. "
      "\"Beat SPY in 3-yr windows\" = the share of rolling 3-year periods in which it finished ahead of SPY.", "",
      "| Variant | " + " | ".join(f"CAGR {p}" for p in P) + " | Max DD | Beat SPY in 3-yr windows | Beat RSP in 3-yr windows |",
      "| --- |" + " --- |" * (len(P) + 3)]
for x in r["momentum"]:
    p = x["periods"]
    L.append(f"| {x['label']} | " + " | ".join(f"{p[k].get('cagr_%')}%" for k in P) +
             f" | {p['full'].get('max_dd_%')}% | {x['beat_spy_3y_windows_%']}% | {x['beat_rsp_3y_windows_%']}% |")
yrs = sorted(r["spy_yearly"])
L += ["", "## Year by year (%)", "", "| | " + " | ".join(yrs) + " |", "| --- |" + " --- |" * len(yrs),
      "| SPY | " + " | ".join(str(r["spy_yearly"][y]) for y in yrs) + " |",
      "| RSP | " + " | ".join(str(r["rsp_yearly"].get(y, "")) for y in yrs) + " |"]
for x in r["momentum"][:1]:
    L.append("| momentum base | " + " | ".join(str(x["yearly"].get(y, "")) for y in yrs) + " |")
for x in r["mean_reversion"]:
    if x["universe"] == "sp500" and ("limit" in x["label"] or "RSI(2) < 5 + low cost" in x["label"]):
        L.append(f"| pullback: {x['label']} | " + " | ".join(str(x["yearly"].get(y, "")) for y in yrs) + " |")
picks = r["momentum"][0].get("recent_picks") or []
if picks:
    L += ["", "## Momentum: most recent monthly picks", ""] + [f"- {d}: {', '.join(p)}" for d, p in picks]
open(os.path.join(out, "round2-latest.md"), "w").write("\n".join(L) + "\n")
print("wrote", os.path.join(out, "round2-latest.md"))
