"""Write the Round 7 report from the newest round7-*.json.  Usage: python report_round7.py RESULTS_DIR OUT_MD"""
import glob, json, os, sys

src, out_md = sys.argv[1], sys.argv[2]
R = json.load(open(sorted(glob.glob(os.path.join(src, "round7-2*.json")))[-1]))
f = lambda x, s="": "–" if x is None else f"{x}{s}"
flt = lambda r: "uptrend only" if r["trend_filter"] else "any stock"
ru = R["rules"]
L = [f"# Round 7 — which thinkorswim studies and Fibonacci levels help? ({R['asOf']})", "",
     f"**Data:** EODHD · {R['stocks']} S&P 500 members since 2004 (point in time, failed companies included) · "
     f"TUNE {R['tune'][0][:4]}–{R['tune'][1][:4]} chooses · JUDGE {R['judge'][0][:4]}–{R['judge'][1][:4]} only checks.", "",
     f"**Data repair:** {R.get('data_repairs', 0)} files fixed (unadjusted splits, bad one-day prints, re-used tickers cut back to "
     f"the right company); {len(R.get('dropped_files', []))} files too broken to trust were left out: "
     f"{', '.join(R.get('dropped_files', [])) or 'none'}.", "",
     "**How each study was scored:** buy at the next open after the signal; compare the return over the next 20 and 60 "
     "sessions with a RANDOM eligible stock bought the same day (for 'uptrend only' rows: a random uptrend stock). "
     "**Edge** = the study's average minus the random pick's, in % points. t = Newey-West t-statistic (≥ 2 is "
     "usually 'real'; we required ≥ " + str(ru["t_min"]) + " because ~80 versions were tried). Thinkorswim default "
     "settings, no tuning.", "",
     f"**A study survives** if in TUNE it has ≥ {ru['n_min']} signals, positive 20- and 60-day edge, 60-day t ≥ {ru['t_min']}, "
     "and a positive 60-day edge in both halves (2005–10 and 2011–16). Judge columns were filled in after the choices were frozen.", ""]
st = R["studies"]
nsurv = sum(r["survives"] for r in st)
L += [f"**{nsurv} of {len(st)} study versions survived the tune screen.**", "",
      "## 1. Every study, ranked by tune t-statistic (60-day edge)", "",
      "| Study | Stocks | Signals | Edge 20d | Edge 60d | t (60d) | Halves 60d | Survives | Judge edge 60d | Judge t |",
      "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for r in sorted(st, key=lambda r: -(r["tune"].get("t60") or 0)):
    t, j = r["tune"], r["judge"]
    L.append(f"| {r['study']} | {flt(r)} | {t['signals']:,} | {f(t.get('edge20'))} | **{f(t.get('edge60'))}** | {f(t.get('t60'))} | "
             f"{' / '.join(f(x) for x in r['halves'])} | {'✅' if r['survives'] else '✗'} | {f(j.get('edge60'))} | {f(j.get('t60'))} |")
fib = [r for r in st if r["study"].startswith(("fib", "fake"))]
L += ["", "## 2. Fibonacci vs made-up levels", "",
      "Same swing, same turn-up rule, same stop logic — only the level differs. If the Fibonacci rows don't beat the "
      "made-up rows, the Fibonacci numbers carry no extra information.", "",
      "| Level | Stocks | Signals (tune) | Edge 60d tune | t | Edge 60d judge | t | Hit rate 60d (tune) |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
key = lambda r: (r["trend_filter"], float(r["study"].split()[-1].rstrip("%")))
for r in sorted(fib, key=key):
    t, j = r["tune"], r["judge"]
    L.append(f"| {'**' + r['study'] + '**' if r['study'].startswith('fib') else r['study']} | {flt(r)} | {t['signals']:,} | {f(t.get('edge60'))} | "
             f"{f(t.get('t60'))} | {f(j.get('edge60'))} | {f(j.get('t60'))} | {f(t.get('hit60'), '%')} |")
for tf in (False, True):
    a = [r for r in fib if r["trend_filter"] == tf]
    fa = [r["tune"].get("edge60") or 0 for r in a if r["study"].startswith("fib")]
    ka = [r["tune"].get("edge60") or 0 for r in a if r["study"].startswith("fake")]
    if fa and ka:
        L += ["", f"*{'Uptrend only' if tf else 'Any stock'}:* average tune 60-day edge — Fibonacci levels {sum(fa)/len(fa):+.2f} vs made-up levels {sum(ka)/len(ka):+.2f}."]
pr = R["pairs"]
if pr:
    L += ["", "## 3. Pairs of survivors (second study within 5 sessions)", "",
          "| Pair | Stocks | Signals | Edge 60d tune | t | Halves | Survives | Judge edge 60d | Judge t |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(pr, key=lambda r: -(r["tune"].get("t60") or 0)):
        t, j = r["tune"], r["judge"]
        L.append(f"| {r['study']} | {flt(r)} | {t['signals']:,} | {f(t.get('edge60'))} | {f(t.get('t60'))} | "
                 f"{' / '.join(f(x) for x in r['halves'])} | {'✅' if r['survives'] else '✗'} | {f(j.get('edge60'))} | {f(j.get('t60'))} |")
po = R["portfolio"]
if po:
    L += ["", "## 4. Portfolio test (10 slots, 1% risk, idle money in SPY, 0.07% cost per side)", "",
          f"SPY: tune {f(R['spy']['tune'].get('cagr_%'), '%')}/yr (max DD {f(R['spy']['tune'].get('max_dd_%'), '%')}), "
          f"judge {f(R['spy']['judge'].get('cagr_%'), '%')}/yr (max DD {f(R['spy']['judge'].get('max_dd_%'), '%')}). "
          "RANDOM = random uptrend stocks with the same exits — the bar a study must clear.", "",
          "| Entry | Stocks | Exit | S&P > 200-day gate | Tune CAGR | Tune vs SPY | Tune DD | Judge CAGR (vs SPY) | Bootstrap % | Judge DD | 2026 vs SPY | Passes |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in po:
        t, j, y = r["tune"], r.get("judge") or {}, r.get("2026") or {}
        L.append(f"| {r['study']} | {flt(r)} | {r['exit']} | {'yes' if r['spy200_gate'] else 'no'} | {f(t['cagr'], '%')} | {f(t['excess_median'])} | "
                 f"{f(t['max_dd'], '%')} | {f(j.get('cagr_median'), '%')} ({f(j.get('excess_median'))}) | "
                 f"{f((j.get('bootstrap') or {}).get('share_above_zero_%'))} | {f(j.get('max_dd'), '%')} | {f(y.get('excess_median'))} | "
                 f"{'' if 'passes_bar' not in r else ('✅' if r['passes_bar'] else '✗')} |")
L += ["", "_Edges are averages per signal over 20 / 60 trading days (≈ 1 / 3 months), not yearly returns. "
      "Generated by scripts/backtest/run_round7.py from privately held EODHD data (not in this repo)._"]
open(out_md, "w").write("\n".join(L) + "\n")
print("wrote", out_md)
