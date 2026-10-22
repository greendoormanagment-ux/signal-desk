"""Clean EODHD bars before backtesting (found in Round 7: 61 of 985 files have impossible jumps).

Three kinds of damage:
  0. unadjusted splits — a calm day where open and close both sit at an exact split ratio (½, ⅓, ¼, ⅔, 2x, 3x…) of the
     prior close, with a narrow day range (real crashes have wide ranges) → earlier bars are rescaled;
  1. one-day spikes — a single bar 3x+ away from both neighbours (bad print) → the bar is dropped;
  2. splices — a re-used ticker glues two companies together (e.g. GDW 2014: $0.005 → $40), or a bad adjustment
     shifts the whole history → the series is cut at every 3x+ jump and only the piece that overlaps the stock's
     S&P 500 membership the most is kept.
No real S&P 500 stock moves 3x in one session (AIG's worst 2008 day was about -60%, i.e. 2.5x), so 3x is safe.
"""
import numpy as np

JUMP = 3.0


def _ratio(a, b):
    with np.errstate(divide="ignore", invalid="ignore"):
        r = a / b
    return np.maximum(r, 1 / r)


SPLITS = (2, 3, 4, 5, 10, 1.5, 2.5, 4 / 3)


def fix_splits(df):
    df = df.reset_index(drop=True).copy()
    for col in ("o", "h", "l", "c", "v"):
        df[col] = df[col].astype(float)
    c, o, h, l = (df[k].to_numpy(float) for k in ("c", "o", "h", "l"))
    n_fix = 0
    for i in range(1, len(c)):
        r, ro = c[i] / c[i - 1], o[i] / c[i - 1]
        if not (h[i] / l[i] < 1.12):
            continue
        for k in SPLITS:
            for f in (1 / k, k):
                if abs(r / f - 1) < 0.03 and abs(ro / f - 1) < 0.04:
                    for col in ("o", "h", "l", "c"):
                        df.loc[: i - 1, col] *= f
                    df.loc[: i - 1, "v"] /= f
                    c, o, h, l = (df[k2].to_numpy(float) for k2 in ("c", "o", "h", "l"))
                    n_fix += 1
                    break
            else:
                continue
            break
    return df, n_fix


def clean(df, spans=None):
    """Return (clean df, note) for one stock. spans = [(start, end), ...] membership dates (optional)."""
    df, nf = fix_splits(df)
    note = [f"rescaled {nf} unadjusted split(s)"] if nf else []
    for _ in range(20):                                   # 1. single-bar spikes
        c = df.c.to_numpy(float)
        if len(c) < 3:
            break
        prev, nxt = _ratio(c[1:-1], c[:-2]), _ratio(c[1:-1], c[2:])
        bad = np.where((prev > JUMP) & (nxt > JUMP))[0] + 1
        if not len(bad):
            break
        note.append(f"dropped {len(bad)} spike bar(s)")
        df = df.drop(index=bad).reset_index(drop=True)
    c, o, h, l = (df[k].to_numpy(float) for k in ("c", "o", "h", "l"))
    j = np.zeros(len(c), bool)
    j[1:] = (_ratio(c[1:], c[:-1]) > JUMP) | (_ratio(o[1:], c[:-1]) > JUMP)
    cuts = np.where(j)[0]
    if len(cuts):
        edges = [0] + list(cuts) + [len(df)]
        segs = [(edges[k], edges[k + 1]) for k in range(len(edges) - 1) if edges[k + 1] > edges[k]]
        d = df.date.to_numpy()

        def overlap(a, b):
            if not spans:
                return b - a
            lo, hi = d[a], d[b - 1]
            return sum(max(0, (min(hi, e) > max(lo, s0))) * ((d[a:b] >= s0) & (d[a:b] <= e)).sum() for s0, e in spans)
        a, b = max(segs, key=lambda s: overlap(*s))
        note.append(f"cut at {len(cuts)} jump(s); kept {d[a]}..{d[b - 1]}")
        df = df.iloc[a:b].reset_index(drop=True)
    return df, "; ".join(note)


def still_dirty(df, max_fix=5, n_fix=0):
    """A file is beyond repair if it needed many split fixes or still has a calm-day 1.8x+ jump (a real crash has a
    wide day range; a glitch doesn't)."""
    if n_fix > max_fix:
        return True
    c, h, l = (df[k].to_numpy(float) for k in ("c", "h", "l"))
    r = _ratio(c[1:], c[:-1])
    return bool(((r >= 1.8) & (h[1:] / l[1:] < 1.15)).any())


def clean_all(prices, members=None, keep=("SPY", "QQQ", "RSP")):
    """Returns (clean prices, notes, dropped): dropped = files too broken to trust (listed in the report)."""
    out, notes, dropped = {}, {}, []
    for s, df in prices.items():
        if s in keep:
            out[s] = df; continue
        cdf, n = clean(df, (members or {}).get(s))
        nf = int(n.split("rescaled ")[1].split()[0]) if "rescaled " in n else 0
        if n:
            notes[s] = n
        if still_dirty(cdf, n_fix=nf):
            dropped.append(s); continue
        if len(cdf) >= 300:
            out[s] = cdf
    return out, notes, sorted(dropped)
