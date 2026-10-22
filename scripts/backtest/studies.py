"""Round 7 · thinkorswim-style studies and Fibonacci retracements as BUY signals (daily bars).

Every study uses thinkorswim's default settings — no tuning — so a good result can't come from fitting parameters.
signals(df) returns {name: (signal bool array, stop price array)}: a signal on day t means "buy at the next open".
A "state" study (e.g. RSI(2) < 10) only fires on the FIRST day of the state. Stops default to 8% under the
signal close (the Playbook's maximum); Fibonacci entries use their own stop just past the next level down.

Fibonacci, mechanised (how a trader draws it):
  swing   = the highest high of the last 64 sessions (at least 3 sessions old, nothing higher since) and the lowest
            low before it in that window; the move must be at least +20%.
  depth   = how far the pullback since the high has retraced the move (0 = at the high, 1 = back at the low).
  signal  = the pullback's low lands in a level's band (level ± 3% of the move), that low is at most 5 sessions
            old, and today closes above yesterday's high (the turn) while still below the swing high.
  stop    = level + 8% of the move deeper (just past the next Fibonacci level), never more than 15% under the close.
  The same rules run at MADE-UP levels (30%, 44%, 56%, 70%) — if those do as well, the Fibonacci numbers add nothing.
"""
import numpy as np, pandas as pd
from numpy.lib.stride_tricks import sliding_window_view as swv

FIB_LEVELS = {"fib 38.2%": 0.382, "fib 50%": 0.5, "fib 61.8%": 0.618, "fib 78.6%": 0.786}
FAKE_LEVELS = {"fake 30%": 0.30, "fake 44%": 0.44, "fake 56%": 0.56, "fake 70%": 0.70}
BAND, SWING_N, MIN_MOVE = 0.03, 64, 0.20


def _wilder(x, n):
    x = np.asarray(x, float); out = np.full(len(x), np.nan)
    ok = np.where(~np.isnan(x))[0]
    if len(ok) <= n:
        return out
    s = ok[0]
    a = np.nanmean(x[s:s + n]); out[s + n - 1] = a
    for i in range(s + n, len(x)):
        a = (a * (n - 1) + (x[i] if x[i] == x[i] else a)) / n
        out[i] = a
    return out


def _ema(x, n):
    return pd.Series(x).ewm(span=n, adjust=False).mean().to_numpy()


def _sma(x, n):
    return pd.Series(x).rolling(n).mean().to_numpy()


def _lag(x, k=1, fill=np.nan):
    x = np.asarray(x, float); out = np.full(len(x), fill)
    out[k:] = x[:-k]
    return out


def cross_up(a, b):
    a, b = np.asarray(a, float), np.broadcast_to(np.asarray(b, float), np.shape(a))
    return (a > b) & (_lag(a) <= _lag(b))


def first(cond):
    cond = np.asarray(cond, bool)
    return cond & ~np.r_[False, cond[:-1]]


def rsi(c, n=14):
    d = np.diff(c, prepend=np.nan)
    g, l = _wilder(np.where(d > 0, d, 0.0), n), _wilder(np.where(d < 0, -d, 0.0), n)
    g[0] = l[0] = np.nan
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(l == 0, 100.0, 100 - 100 / (1 + g / l))


def atr(h, l, c, n=14):
    pc = _lag(c)
    tr = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    return _wilder(tr, n)


def psar(h, l, step=0.02, mx=0.2):
    n = len(h); out = np.full(n, np.nan); up = np.zeros(n, bool)
    if n < 3:
        return out, up
    bull, af, ep, sar = True, step, h[0], l[0]
    for i in range(1, n):
        sar = sar + af * (ep - sar)
        if bull:
            sar = min(sar, l[i - 1], l[i - 2] if i > 1 else l[i - 1])
            if l[i] < sar:
                bull, sar, ep, af = False, ep, l[i], step
            elif h[i] > ep:
                ep, af = h[i], min(af + step, mx)
        else:
            sar = max(sar, h[i - 1], h[i - 2] if i > 1 else h[i - 1])
            if h[i] > sar:
                bull, sar, ep, af = True, ep, h[i], step
            elif l[i] < ep:
                ep, af = l[i], min(af + step, mx)
        out[i], up[i] = sar, bull
    return out, up


def fib_signals(h, l, c, levels):
    """Signal + stop arrays for each named retracement level (see module docstring)."""
    n = len(c); res = {k: (np.zeros(n, bool), np.full(n, np.nan)) for k in levels}
    if n < SWING_N + 2:
        return res
    W = SWING_N
    hw, lw = swv(h, W), swv(l, W)                       # row r covers days r .. r+W-1 (today = r+W-1)
    t = np.arange(W - 1, n)
    ih = hw.argmax(axis=1)
    H = hw[np.arange(len(t)), ih]
    pos = np.arange(W)[None, :]
    L = np.where(pos <= ih[:, None], lw, np.inf).min(axis=1)
    after = np.where(pos > ih[:, None], lw, np.inf)
    mlow = after.min(axis=1); imin = after.argmin(axis=1)
    ok = (ih <= W - 4) & (H >= L * (1 + MIN_MOVE)) & np.isfinite(mlow) & (imin >= W - 6)
    rng = H - L
    with np.errstate(divide="ignore", invalid="ignore"):
        depth = (H - mlow) / rng
    turn = (c[t] > h[t - 1]) & (c[t] < H)
    for k, x in levels.items():
        sig = ok & turn & (np.abs(depth - x) <= BAND)
        stop = H - (x + 0.08) * rng
        stop = np.maximum(stop, c[t] * 0.85)
        s, st = res[k]
        s[t] = sig; st[t] = np.where(sig, stop, np.nan)
        res[k] = (first(s), st)
    return res


def signals(df):
    """All single studies for one stock. Returns {name: (bool array, stop array)}."""
    o, h, l, c, v = (df[k].to_numpy(float) for k in ("o", "h", "l", "c", "v"))
    n = len(c); pc = _lag(c)
    s20, s50, s200 = _sma(c, 20), _sma(c, 50), _sma(c, 200)
    avgv = _lag(_sma(v, 50))
    out = {}
    r14, r2 = rsi(c, 14), rsi(c, 2)
    out["RSI(14) crosses up 30"] = cross_up(r14, 30)
    out["RSI(14) crosses up 50"] = cross_up(r14, 50)
    out["RSI(2) under 10"] = first(r2 < 10)
    m = _ema(c, 12) - _ema(c, 26); sg = _ema(m, 9)
    out["MACD crosses signal"] = cross_up(m, sg)
    out["MACD crosses zero"] = cross_up(m, 0)
    ll, hh = pd.Series(l).rolling(14).min().to_numpy(), pd.Series(h).rolling(14).max().to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        fk = 100 * (c - ll) / (hh - ll)
    k = _sma(fk, 3); d = _sma(k, 3)
    out["Stochastic %K crosses %D under 20"] = cross_up(k, d) & (k < 20)
    sd = pd.Series(c).rolling(20).std(ddof=0).to_numpy()
    bu, bl = s20 + 2 * sd, s20 - 2 * sd
    out["Bollinger: back above lower band"] = cross_up(c, bl)
    out["Bollinger: close above upper band"] = cross_up(c, bu)
    e20, a20 = _ema(c, 20), atr(h, l, c, 20)
    ku, kl = e20 + 1.5 * a20, e20 - 1.5 * a20
    out["Keltner: close above upper channel"] = cross_up(c, ku)
    squeeze = (bu < ku) & (bl > kl)
    donch_mid = (pd.Series(h).rolling(20).max().to_numpy() + pd.Series(l).rolling(20).min().to_numpy()) / 2
    mom = c - (donch_mid + s20) / 2
    out["TTM Squeeze fires up"] = _lag(squeeze, fill=0).astype(bool) & ~squeeze & (mom > 0) & (mom > _lag(mom))
    up_m, dn_m = h - _lag(h), _lag(l) - l
    pdm = np.where((up_m > dn_m) & (up_m > 0), up_m, 0.0); mdm = np.where((dn_m > up_m) & (dn_m > 0), dn_m, 0.0)
    a14 = atr(h, l, c, 14)
    with np.errstate(divide="ignore", invalid="ignore"):
        pdi, mdi = 100 * _wilder(pdm, 14) / a14, 100 * _wilder(mdm, 14) / a14
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)
    adx = _wilder(dx, 14)
    out["DMI: +DI crosses -DI with ADX > 20"] = cross_up(pdi, mdi) & (adx > 20)
    out["Golden cross (50 over 200)"] = cross_up(s50, s200)
    out["Close crosses above 50-day"] = cross_up(c, s50)
    out["EMA 8 crosses EMA 21"] = cross_up(_ema(c, 8), _ema(c, 21))
    out["Donchian 20-day breakout"] = first(c > _lag(pd.Series(h).rolling(20).max().to_numpy()))
    out["New 52-week high"] = first(c > _lag(pd.Series(h).rolling(252).max().to_numpy()))
    _, bull = psar(h, l)
    out["Parabolic SAR flips up"] = bull & ~np.r_[True, bull[:-1]]
    tp = (h + l + c) / 3
    md = pd.Series(tp).rolling(14).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True).to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        cci = (tp - _sma(tp, 14)) / (0.015 * md)
    out["CCI crosses up -100"] = cross_up(cci, -100)
    with np.errstate(divide="ignore", invalid="ignore"):
        wr = -100 * (hh - c) / (hh - ll)
    out["Williams %R crosses up -80"] = cross_up(wr, -80)
    obv = np.cumsum(np.where(c > pc, v, np.where(c < pc, -v, 0.0)))
    out["OBV new 50-day high"] = first(obv > _lag(pd.Series(obv).rolling(50).max().to_numpy()))
    with np.errstate(divide="ignore", invalid="ignore"):
        mfm = np.where(h > l, ((c - l) - (h - c)) / (h - l), 0.0)
        cmf = pd.Series(mfm * v).rolling(21).sum().to_numpy() / pd.Series(v).rolling(21).sum().to_numpy()
    out["Chaikin Money Flow crosses 0"] = cross_up(cmf, 0)
    rmf = tp * v; ptp = _lag(tp)
    pos_f = pd.Series(np.where(tp > ptp, rmf, 0.0)).rolling(14).sum().to_numpy()
    neg_f = pd.Series(np.where(tp < ptp, rmf, 0.0)).rolling(14).sum().to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        mfi = np.where(neg_f == 0, 100.0, 100 - 100 / (1 + pos_f / neg_f))
    out["MFI crosses up 20"] = cross_up(mfi, 20)
    out["Rate of Change(14) crosses 0"] = cross_up(c / _lag(c, 14) - 1, 0)
    rng_ = h - l
    with np.errstate(divide="ignore", invalid="ignore"):
        out["Volume surge up day (2x vol, +2%)"] = (v >= 2 * avgv) & (c >= pc * 1.02) & ((c - l) >= 0.5 * rng_)
        out["Gap up 3%+ on 1.5x volume"] = (o >= pc * 1.03) & (v >= 1.5 * avgv) & (c > o)
    conv = (pd.Series(h).rolling(9).max() + pd.Series(l).rolling(9).min()).to_numpy() / 2
    base = (pd.Series(h).rolling(26).max() + pd.Series(l).rolling(26).min()).to_numpy() / 2
    spanb = (pd.Series(h).rolling(52).max() + pd.Series(l).rolling(52).min()).to_numpy() / 2
    cloud = np.fmax(_lag((conv + base) / 2, 26), _lag(spanb, 26))
    out["Ichimoku: close above the cloud"] = cross_up(c, cloud)
    nr7 = rng_ <= pd.Series(rng_).rolling(7).min().to_numpy()
    out["NR7 then close above its high"] = _lag(nr7, fill=0).astype(bool) & (c > _lag(h))
    inside = (h < _lag(h)) & (l > _lag(l))
    out["Inside day then close above its high"] = _lag(inside, fill=0).astype(bool) & (c > _lag(h))
    dvol = pd.Series(np.where(c < pc, v, 0.0)).rolling(10).max().shift(1).to_numpy()
    out["Pocket pivot (vol > any down day in 10)"] = (c > pc) & (v > dvol) & (c > s50) & (_lag(c) > _lag(s50) * 0.98)
    stop8 = c * 0.92
    res = {k: (np.nan_to_num(np.asarray(x, float)).astype(bool), stop8) for k, x in out.items()}
    for k, (s, st) in fib_signals(h, l, c, {**FIB_LEVELS, **FAKE_LEVELS}).items():
        res[k] = (s, st)
    return res


def uptrend(df):
    """Trend filter used as an optional add-on to every study: close > 200-day and 50-day > 200-day."""
    c = df.c.to_numpy(float)
    s50, s200 = _sma(c, 50), _sma(c, 200)
    return (c > s200) & (s50 > s200)
