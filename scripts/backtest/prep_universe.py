"""Round 8 prep: load the all-US EODHD files, keep stocks that were ever tradable (>= $5 and >= $20M/day avg
dollar volume, 300+ bars), repair them with data_clean, save one pickle (the UNIVERSE_PKL every run_round8*.py takes).
The data is private (EODHD licence) — never commit the files or the pickle; only this code is in the repo.

Usage (from scripts/backtest): python prep_universe.py DATA_DIR OUT_PKL
DATA_DIR holds prices/<SYMBOL>.csv.gz and etfs/<SYMBOL>.csv.gz (columns date,o,h,l,c,v) and universe_meta.json."""
import os, sys, gzip, json, time, pickle
import numpy as np, pandas as pd
import data_clean as DC
U, OUT = sys.argv[1], sys.argv[2]; t0 = time.time()
meta = json.load(open(f"{U}/universe_meta.json"))
keep, n_all = {}, 0
for f in sorted(os.listdir(f"{U}/prices")):
    n_all += 1
    df = pd.read_csv(f"{U}/prices/{f}")
    df = df[(df.c > 0) & (df.h >= df.l)].drop_duplicates("date").sort_values("date").reset_index(drop=True)
    if len(df) < 300: continue
    dv = (df.v.rolling(50, min_periods=50).mean().shift(1) * df.c) / 1e6
    if not ((df.c >= 5) & (dv >= 20) & (df.date >= "2004-01-01")).any(): continue
    for k in ("o", "h", "l", "c", "v"): df[k] = df[k].astype(float)
    keep[f[:-7]] = df
print("files", n_all, "ever tradable", len(keep), f"{time.time()-t0:.0f}s", flush=True)
clean, notes, dropped = DC.clean_all(keep)
print("after clean", len(clean), "repaired", len(notes), "dropped", len(dropped), f"{time.time()-t0:.0f}s", flush=True)
etf = {}
for f in os.listdir(f"{U}/etfs"):
    df = pd.read_csv(f"{U}/etfs/{f}").sort_values("date").reset_index(drop=True)
    for k in ("o", "h", "l", "c", "v"): df[k] = df[k].astype(float)
    etf[f[:-7]] = df
status = {s: meta.get(s, {}).get("status", "?") for s in clean}
pickle.dump({"prices": clean, "etf": etf, "status": status, "notes": notes, "dropped": dropped, "n_files": n_all, "n_tradable": len(keep)},
            open(OUT, "wb"))
print("saved", f"{time.time()-t0:.0f}s", "active", sum(v == "active" for v in status.values()), "delisted", sum(v != "active" for v in status.values()))
