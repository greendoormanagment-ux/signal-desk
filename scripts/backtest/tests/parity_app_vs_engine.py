"""Does the APP (index.html) rate a stock the same way the BACKTEST engine does?

Feeds identical daily bars to both: the app's own JavaScript (computeIndicators + runRuleEngine + the market read) and
engine.py (indicators + evaluate + market_status), with the live settings (breakouts only, 1.4x volume, 5% extension).
Fundamentals and the earnings date are set to "pass" on both sides, so this isolates the price rules.
Compares: rating, setup, stop, pivot, 50/200-day averages, ATR, RSI, and the market reading.

Usage (from scripts/backtest):  python tests/parity_app_vs_engine.py [UNIVERSE_PKL]
Without a pickle it uses synthetic random-walk stocks (enough to catch logic drift; real data is a stronger check).
"""
import json, os, pickle, subprocess, sys, tempfile
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import engine as E

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def synth(seed, n=700):
    r = np.random.default_rng(seed)
    c = 40 * np.exp(np.cumsum(r.normal(0.0012, 0.022, n))); o = c * (1 + r.normal(0, .004, n))
    h = np.maximum(c, o) * (1 + abs(r.normal(0, .008, n))); l = np.minimum(c, o) * (1 - abs(r.normal(0, .008, n)))
    v = r.lognormal(14, .45, n)
    for k in r.integers(260, n, 12): v[k] *= 3
    return pd.DataFrame({"date": [d.date().isoformat() for d in pd.bdate_range("2019-01-01", periods=n)], "o": o, "h": h, "l": l, "c": c, "v": v})


def main():
    if len(sys.argv) > 1:
        U = pickle.load(open(sys.argv[1], "rb")); spy, qqq = U["etf"]["SPY"], U["etf"]["QQQ"]
        stocks = dict(list(U["prices"].items())[:120]); src = "real data"
    else:
        spy, qqq = synth(1), synth(2); stocks = {f"S{i}": synth(10 + i) for i in range(60)}; src = "synthetic data"
    mkt = E.market_status(spy, qqq); live = mkt["live"]; spy_close = dict(zip(spy.date, spy.c))
    P = dict(E.BASE); P.update(nosec_pass=True, breakout_only=True, mkt_mode="live")
    cases, want = [], {}
    rng = np.random.default_rng(0)
    for s, df in stocks.items():
        df = df.reset_index(drop=True)
        if len(df) < 330:
            continue
        ind = E.indicators(df); ev = E.evaluate(s, df, ind, None, mkt, spy_close, P); E._PIT.pop(s, None)
        buys = [i for i in np.where(ev.rating.to_numpy() == "BUY")[0] if i >= 320]
        idx = set(rng.choice(np.arange(320, len(df)), size=min(25, len(df) - 320), replace=False).tolist()) | set(buys[:15])
        for i in sorted(idx):
            m = live.get(df.date.iat[i])
            if m is None or ev.rating.iat[i] == "NA":
                continue
            w = df.iloc[i - 319:i + 1]
            cid = f"{s}|{df.date.iat[i]}"
            cases.append({"id": cid, "kind": "stock", "market": m,
                          "bars": [{"date": a, "o": float(b), "h": float(c), "l": float(d), "c": float(e), "v": float(f)} for a, b, c, d, e, f in zip(w.date, w.o, w.h, w.l, w.c, w.v)]})
            want[cid] = {"rating": ev.rating.iat[i], "setup": ev.setup.iat[i], "stop": float(ev.stop.iat[i]) if ev.rating.iat[i] == "BUY" else None,
                         "pivot": float(ind["pivot"][i]), "sma50": float(ind["sma50"][i]), "sma200": float(ind["sma200"][i]),
                         "atr": float(ind["atr"][i]), "rsi": float(ind["rsi"][i])}
    j = spy.merge(qqq, on="date", suffixes=("_s", "_q")).reset_index(drop=True)
    for i in rng.choice(np.arange(120, len(j)), size=min(300, len(j) - 120), replace=False):
        d = j.date.iat[i]
        if d not in live:
            continue
        w = j.iloc[i - 99:i + 1]
        cases.append({"id": "MKT|" + d, "kind": "market", "spy": [{"c": float(a), "v": float(b)} for a, b in zip(w.c_s, w.v_s)],
                      "qqq": [{"c": float(a), "v": float(b)} for a, b in zip(w.c_q, w.v_q)]})
        want["MKT|" + d] = {"market": live[d]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(cases, f); path = f.name
    got = {r["id"]: r for r in json.loads(subprocess.run(["node", os.path.join(HERE, "parity_app.js"), os.path.join(ROOT, "index.html"), path],
                                                        capture_output=True, text=True, check=True).stdout)}
    os.unlink(path)
    SETUP = {"PULLBACK_FILTERED": "PULLBACK"}                       # engine label for the app's info-only pullback
    bad = {}; n = {"stock": 0, "market": 0, "buy": 0}
    for cid, w in want.items():
        g = got[cid]
        if "market" in w:
            n["market"] += 1
            if g["market"] != w["market"]: bad.setdefault("market", []).append((cid, w["market"], g["market"]))
            continue
        n["stock"] += 1; n["buy"] += w["rating"] == "BUY"
        # A pullback is "WATCH" (info) in the app and "DONT_BUY" in the engine: neither buys, so only the label differs.
        label_only = w["setup"] == "PULLBACK_FILTERED" and {g["rating"], w["rating"]} == {"WATCH", "DONT_BUY"}
        if g["rating"] != w["rating"] and not label_only: bad.setdefault("rating", []).append((cid, w["rating"], g["rating"], w["setup"], g["setup"]))
        if label_only: n["label"] = n.get("label", 0) + 1
        if SETUP.get(w["setup"], w["setup"]) != g["setup"]: bad.setdefault("setup", []).append((cid, w["setup"], g["setup"]))
        for k in ("pivot", "sma50", "sma200"):
            if abs(g[k] - w[k]) > 1e-6 * max(1, abs(w[k])): bad.setdefault(k, []).append((cid, w[k], g[k]))
        if w["stop"] is not None and (g["stop"] is None or abs(g["stop"] - w["stop"]) > 1e-6 * w["stop"]): bad.setdefault("stop", []).append((cid, w["stop"], g["stop"]))
        for k in ("atr", "rsi"):                                    # Wilder smoothing depends on how much history is fed in
            if abs(g[k] - w[k]) > 0.02 * max(1, abs(w[k])): bad.setdefault(k, []).append((cid, round(w[k], 4), round(g[k], 4)))
    print(f"{src}: {n['stock']} stock-days ({n['buy']} BUYs) and {n['market']} market days compared")
    if n.get("label"): print(f"  note: {n['label']} pullback days are labeled WATCH in the app and DONT_BUY in the engine (no buy either way)")
    for k, v in bad.items():
        print(f"  MISMATCH {k}: {len(v)} · e.g. {v[:4]}")
    if bad:
        sys.exit(1)
    print("  app and backtest agree on every case")


if __name__ == "__main__":
    main()
