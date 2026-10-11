"""Run the Signal Desk backtest: the live rules (base) plus one-change-at-a-time variants.

Usage: python run.py PRICE_CACHE SEC_CACHE OUT_DIR
Writes OUT_DIR/backtest-<date>.json (all numbers) and OUT_DIR/backtest-<date>.md (readable report).
"""
import datetime as dt, json, os, sys, time
import numpy as np, pandas as pd
import engine as E
from fetch_prices import WATCH as E_WATCH

PERIODS = {"in-sample 2017-2021": ("2017-10-15", "2021-12-31"),
           "out-of-sample 2022-2026": ("2022-01-01", "2026-12-31")}
FULL = ("2017-10-15", "2026-12-31")

VARIANTS = [
    dict(),                                                         # base = live rules
    dict(name="block buys in PRESSURE (#53)", block_pressure=True),
    dict(name="require RS pass", need_rs=True),
    dict(name="pullback: 0 to +3% above a RISING 50-day (#31)", pb_lo=0.0, pb_need_rising=True),
    dict(name="pullback: also needs below-avg volume", pb_need_low_vol=True),
    dict(name="breakouts only", breakout_only=True),
    dict(name="pullbacks only", pullback_only=True),
    dict(name="breakout volume 1.0x", vol_need=1.0),
    dict(name="breakout volume 2.0x", vol_need=2.0),
    dict(name="EPS growth >= 15%", eps_min=15.0),
    dict(name="EPS growth >= 40%", eps_min=40.0),
    dict(name="EPS >= 25% AND sales >= 15%", rev_min=15.0),
    dict(name="earnings block 7 days", earn_days=7),
    dict(name="no earnings block", earn_days=-1),
    dict(name="stop: original only (no trail)", stop="fixed"),
    dict(name="stop: breakeven at +1R, no trail", stop="be1R"),
    dict(name="stop: 3xATR trail from day 1", stop="chand"),
    dict(name="stop: A2 with 2xATR trail", atr_mult=2.0),
    dict(name="stop: A2 with 4xATR trail", atr_mult=4.0),
    dict(name="exit: close 2% under 50-day", stop="ma50"),
    dict(name="RS rank >= 80 (IBD-style, vs all stocks)", min_rsrank=80),
    dict(name="RS rank >= 90", min_rsrank=90),
    dict(name="Minervini trend template", trend_template=True),
    dict(name="market gate: SPY above 200-day only", mkt_mode="spy200"),
]
MC = 10   # random same-day orderings per portfolio test


def trade_stats(tr):
    if not tr:
        return {"trades": 0}
    r = np.array([t["ret"] for t in tr]); R = np.array([t["R"] for t in tr])
    win = r > 0
    pf = r[win].sum() / -r[~win].sum() if (~win).any() and r[~win].sum() < 0 else float("inf")
    return {"trades": len(tr), "win_%": round(win.mean() * 100, 1), "avg_ret_%": round(r.mean(), 2),
            "avg_R": round(R.mean(), 2), "avg_win_%": round(r[win].mean(), 1) if win.any() else 0,
            "avg_loss_%": round(r[~win].mean(), 1) if (~win).any() else 0, "profit_factor": round(pf, 2),
            "avg_days": round(np.mean([t["days"] for t in tr]), 1),
            "big_winners_%": round((R >= 3).mean() * 100, 1)}


def main(pcache, scache, out):
    t0 = time.time()
    prices = E.load_prices(pcache)
    uni = json.load(open(os.path.join(pcache, "universe.json")))
    spy, qqq = prices.pop("SPY"), prices.pop("QQQ"); prices.pop("RSP", None)
    for etf in [k for k in prices if k not in uni["meta"] and k not in E_WATCH]:
        prices.pop(etf)                                                  # keep the stock universe only
    mkt = E.market_status(spy, qqq)
    spy_close = dict(zip(spy.date, spy.c))
    cal = list(spy.date)
    syms = sorted(prices)
    print(f"{len(syms)} stocks · loading SEC + indicators", flush=True)
    IND, SEC = {}, {}
    rk = E.rs_rank(prices, cal)
    for s in syms:
        IND[s] = E.indicators(prices[s]); SEC[s] = E.load_sec(scache, s)
        IND[s]["rsrank"] = rk[s].reindex(prices[s].date).to_numpy()
    del rk
    have_sec = sum(1 for s in syms if SEC[s] and SEC[s]["eps"])
    print(f"indicators done {time.time()-t0:.0f}s · SEC EPS history for {have_sec}", flush=True)

    # ── base: every rating, forward returns vs SPY (first-time signals and rating changes only)
    spy_c = spy.set_index("date").c
    rows = []
    results = {"asOf": dt.date.today().isoformat(), "stocks": len(syms), "with_sec": have_sec,
               "universe": f"US stocks >= ${uni.get('minCapB', 2)}B market cap today (survivorship-biased)", "variants": []}
    base_trades = None
    for vi, V in enumerate(VARIANTS):
        P = dict(E.BASE); P.update(V)
        trades = []
        for s in syms:
            sig = E.evaluate(s, prices[s], IND[s], SEC[s], mkt, spy_close, P)
            if vi == 0:
                rt = sig.rating.to_numpy(); chg = np.r_[True, rt[1:] != rt[:-1]]
                c = sig.close.to_numpy()
                d = sig[chg & (sig.date >= FULL[0]) & (sig.rating != "NA")].copy()
                idx = np.flatnonzero(chg & (sig.date.to_numpy() >= FULL[0]) & (sig.rating.to_numpy() != "NA"))
                for h in (5, 10, 20):
                    fwd = np.array([c[i + h] / c[i] - 1 if i + h < len(c) else np.nan for i in idx]) * 100
                    sd = sig.date.to_numpy()
                    spf = np.array([(spy_c.get(sd[i + h], np.nan) / spy_c.get(sd[i], np.nan) - 1) * 100 if i + h < len(c) else np.nan for i in idx])
                    d[f"rel{h}"] = fwd - spf
                rows.append(d[["sym", "date", "rating", "setup", "market", "fund", "earn", "rs", "rsrank", "eps_g", "rel5", "rel10", "rel20"]])
            trades += E.simulate_trades(s, prices[s], IND[s], sig, P, *FULL)
        closes = {s: prices[s].set_index("date").c for s in {t["sym"] for t in trades}}
        res = {"name": P["name"], "change": {k: v for k, v in V.items() if k != "name"}, "periods": {}}
        for pn, (a, b) in {"full 2017-2026": FULL, **PERIODS}.items():
            tr = [t for t in trades if a <= t["entry_date"] <= b]
            eq, taken = E.portfolio(tr, closes, cal, a, b)
            runs = [E.stats_equity(E.portfolio(tr, closes, cal, a, b, seed=k)[0]) for k in range(MC)]
            cg = np.array([r.get("cagr_%", 0) for r in runs]); dd = np.array([r.get("max_dd_%", 0) for r in runs])
            res["periods"][pn] = {"all_signals": trade_stats(tr), "portfolio_score_order": E.stats_equity(eq),
                                  "portfolio_mc": {"cagr_median_%": round(float(np.median(cg)), 1),
                                                   "cagr_low_%": round(float(cg.min()), 1), "cagr_high_%": round(float(cg.max()), 1),
                                                   "max_dd_median_%": round(float(np.median(dd)), 1)},
                                  "portfolio_trades": trade_stats(taken)}
        results["variants"].append(res)
        if vi == 0:
            base_trades = trades
        f = res["periods"]["full 2017-2026"]
        print(f"[{vi+1}/{len(VARIANTS)}] {P['name']}: n={f['all_signals'].get('trades')} avgR={f['all_signals'].get('avg_R')} "
              f"PF={f['all_signals'].get('profit_factor')} | MC {f['portfolio_mc']} ({time.time()-t0:.0f}s)", flush=True)
        os.makedirs(out, exist_ok=True)
        json.dump(results, open(os.path.join(out, "partial.json"), "w"), default=str)

    sig = pd.concat(rows)
    results["benchmarks"] = {pn: dict(zip(["SPY buy-and-hold", "SPY 200-day rule"], E.spy_benchmarks(spy, a, b)))
                             for pn, (a, b) in {"full 2017-2026": FULL, **PERIODS}.items()}
    g = sig.groupby("rating")[["rel5", "rel10", "rel20"]].agg(["count", "mean"]).round(2)
    results["ratings_vs_spy"] = {r: {f"{h}d": {"n": int(g.loc[r, (h, "count")]), "avg_vs_spy_%": float(g.loc[r, (h, "mean")])}
                                     for h in ("rel5", "rel10", "rel20")} for r in g.index}
    buys = sig[sig.rating == "BUY"]
    results["buy_by_setup"] = buys.groupby("setup").rel20.agg(["count", "mean", "median"]).round(2).reset_index().to_dict("records")
    results["buy_by_market"] = buys.groupby("market").rel20.agg(["count", "mean", "median"]).round(2).reset_index().to_dict("records")
    results["buy_by_rs"] = buys.groupby("rs").rel20.agg(["count", "mean", "median"]).round(2).reset_index().to_dict("records")
    results["buy_by_rsrank"] = buys.assign(b=pd.cut(buys.rsrank, [0, 50, 70, 80, 90, 100])).groupby("b", observed=True).rel20.agg(["count", "mean", "median"]).round(2).reset_index().astype({"b": str}).to_dict("records")
    bt = pd.DataFrame(base_trades)
    results["base_exit_reasons"] = bt.groupby("why").agg(n=("ret", "size"), avg_ret=("ret", "mean"), avg_R=("R", "mean")).round(2).reset_index().to_dict("records")
    results["base_by_year"] = bt.assign(y=bt.entry_date.str[:4]).groupby("y").agg(n=("ret", "size"), win=("ret", lambda x: round((x > 0).mean() * 100, 1)), avg_R=("R", "mean")).round(2).reset_index().to_dict("records")
    stopped = bt[bt.why.str.startswith("stop")]
    results["base_mae_mfe"] = {"avg_MFE_R_all": round(bt.mfe_R.mean(), 2), "avg_MAE_R_all": round(bt.mae_R.mean(), 2),
                               "losers_that_first_reached_+1R_%": round((bt[bt.R <= 0].mfe_R >= 1).mean() * 100, 1),
                               "stopped_trades": int(len(stopped))}
    os.makedirs(out, exist_ok=True)
    stamp = dt.date.today().isoformat()
    json.dump(results, open(os.path.join(out, f"backtest-{stamp}.json"), "w"), indent=1, default=str)
    bt.to_csv(os.path.join(out, f"trades-base-{stamp}.csv.gz"), index=False, compression="gzip")
    os.remove(os.path.join(out, "partial.json"))
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
