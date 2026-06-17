---
date: 2026-06-17
description: "Implementation plan — Phase 1 Part 2 of the SUI reverse-engineer project: build the blind-artifact harness (indicators, numeric context, decoy sampler, chart renderer, blind-set builder with structural answer-key split). TDD."
tags:
  - thinking
  - trading
  - plan
status: proposed
---

# SUI Reverse-Engineer — Phase 1 Part 2: Blind Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Turn `labeled_trades.csv` into a shuffled, unlabeled **blind set** — his wins + losses + random decoys — where each item is a multi-timeframe chart + numeric context **truncated at the bar before T**, with the answer key written to a *separate* path never read at prediction time.

**Architecture:** Five focused modules. `indicators.py` (look-ahead-safe VWAP/ATR/volume-pivots), `context.py` (numeric features at T), `decoys.py` (random non-trade timestamps), `render.py` (truncated candlestick PNGs), `blindset.py` (assemble + shuffle + split blind artifacts vs answer key). Consumes Part 1's `binance_data` + `labeled_trades.csv`.

**Tech Stack:** Python, pandas, numpy, mplfinance + matplotlib (charts). Lives in `D:\trading_system\sui_re\`.

**Spec:** `obsidian-mind/docs/superpowers/specs/2026-06-17-sui-reverse-engineer-design.md`. Governed by [[Reverse-Engineer Before Apply]]. Blind-set = wins+losses+decoys shuffled (grilled). Structural blindness, not "trust me."

---

### Task 1: Indicators (look-ahead-safe)

**Files:**
- Create: `D:\trading_system\sui_re\indicators.py`
- Test: `D:\trading_system\sui_re\tests\test_indicators.py`

- [ ] **Step 1: Write the failing test**

```python
import numpy as np, pandas as pd
from sui_re.indicators import rolling_vwap, atr, volume_pivots

def _df():
    idx = pd.date_range("2025-01-01", periods=60, freq="D")
    base = pd.Series(np.linspace(1.0, 2.0, 60), index=idx)
    return pd.DataFrame({"open": base, "high": base*1.01, "low": base*0.99,
                         "close": base, "volume": np.arange(1, 61.0)}, index=idx)

def test_rolling_vwap_between_low_and_high():
    v = rolling_vwap(_df(), 20)
    d = _df()
    assert (v.dropna() <= d["high"].max()) and (v.dropna() >= d["low"].min()).all()
    assert v.iloc[:19].isna().all()         # needs full window -> no look-ahead leak

def test_volume_pivots_returns_levels_arrays():
    sup, res = volume_pivots(_df(), k=3, vol_mult=0.5)
    assert len(sup) == len(res) == 60
```

- [ ] **Step 2: Run to verify fail** — `python -m pytest sui_re/tests/test_indicators.py -v` → ModuleNotFoundError.

- [ ] **Step 3: Implement** (ported from the validated `validate_vwap_sr.py`)

```python
"""Look-ahead-safe indicators for the SUI blind harness (ported from validate_vwap_sr)."""
import numpy as np
import pandas as pd

def typical_price(df): return (df["high"] + df["low"] + df["close"]) / 3.0

def rolling_vwap(df, window=20):
    tp = typical_price(df)
    pv = (tp * df["volume"]).rolling(window, min_periods=window).sum()
    v = df["volume"].rolling(window, min_periods=window).sum()
    return pv / v

def anchored_vwap(df, freq="W"):
    tp = typical_price(df)
    grp = df.index.to_period(freq)
    return (tp * df["volume"]).groupby(grp).cumsum() / df["volume"].groupby(grp).cumsum()

def atr(df, period=14):
    pc = df["close"].shift(1)
    tr = pd.concat([df["high"]-df["low"], (df["high"]-pc).abs(), (df["low"]-pc).abs()],
                   axis=1).max(axis=1)
    return tr.ewm(com=period-1, adjust=False).mean()

def volume_pivots(df, k=5, vol_mult=1.5, vol_window=20):
    """Volume-confirmed swing pivots -> nearest support below / resistance above.
    A pivot at i is usable only from i+k (no look-ahead)."""
    high, low, vol, close = (df["high"].values, df["low"].values,
                             df["volume"].values, df["close"].values)
    n = len(df)
    avg = pd.Series(vol).rolling(vol_window, min_periods=vol_window).mean().values
    ph, pl = [], []
    for i in range(k, n-k):
        if np.isnan(avg[i]) or vol[i] <= vol_mult*avg[i]:
            continue
        if high[i] == high[i-k:i+k+1].max(): ph.append((i+k, high[i]))
        if low[i] == low[i-k:i+k+1].min():  pl.append((i+k, low[i]))
    ph.sort(); pl.sort()
    sup = np.full(n, np.nan); res = np.full(n, np.nan)
    ah, al, hi, li = [], [], 0, 0
    for t in range(n):
        while hi < len(ph) and ph[hi][0] <= t: ah.append(ph[hi][1]); hi += 1
        while li < len(pl) and pl[li][0] <= t: al.append(pl[li][1]); li += 1
        above = [x for x in ah if x >= close[t]]; below = [x for x in al if x <= close[t]]
        if above: res[t] = min(above)
        if below: sup[t] = max(below)
    return sup, res
```

- [ ] **Step 4: Run to verify pass** — `python -m pytest sui_re/tests/test_indicators.py -v` → 2 passed.
- [ ] **Step 5: Commit** — `git add sui_re/indicators.py sui_re/tests/test_indicators.py && git commit -m "feat(sui_re): look-ahead-safe indicators (vwap/atr/pivots)"`

---

### Task 2: Numeric context at T (truncated)

**Files:**
- Create: `D:\trading_system\sui_re\context.py`
- Test: `D:\trading_system\sui_re\tests\test_context.py`

- [ ] **Step 1: Write the failing test**

```python
import pandas as pd
from sui_re.context import context_at

def test_context_at_is_truncated_and_complete():
    T = pd.Timestamp("2026-04-23 01:00")
    ctx = context_at("SUI", T)
    assert {"price","vwap20_dist_pct","nearest_res","nearest_sup",
            "vol_ratio","atr_pct","daily_trend"} <= set(ctx)
    assert ctx["asof"] < T                  # last CLOSED bar strictly before T (no look-ahead)
    assert ctx["price"] > 0
```

- [ ] **Step 2: Run to verify fail** → ModuleNotFoundError.

- [ ] **Step 3: Implement**

```python
"""Numeric market context at timestamp T, computed only from bars strictly before T."""
import numpy as np
import pandas as pd
from sui_re.binance_data import load_ohlcv
from sui_re.indicators import rolling_vwap, atr, volume_pivots

def _window(pair, interval, T, bars, lookback_days):
    df = load_ohlcv(f"{pair}USDT", interval, T - pd.Timedelta(days=lookback_days),
                    T + pd.Timedelta(days=1))
    df = df[df.index < T]                    # strictly before entry -> no look-ahead
    return df.tail(bars)

def context_at(pair, T) -> dict:
    T = pd.Timestamp(T)
    m15 = _window(pair, "15m", T, 200, 7)
    d1 = _window(pair, "1d", T, 120, 200)
    px = float(m15["close"].iloc[-1])
    vwap = rolling_vwap(m15, 20).iloc[-1]
    a = atr(m15, 14).iloc[-1]
    sup, res = volume_pivots(m15, k=5, vol_mult=1.5)
    avgvol = m15["volume"].rolling(20).mean().iloc[-1]
    d_ema = d1["close"].ewm(span=20, adjust=False).mean()
    return {
        "asof": m15.index[-1], "price": px,
        "vwap20_dist_pct": round((px - vwap)/vwap*100, 2) if vwap else None,
        "nearest_res": None if np.isnan(res[-1]) else round(float(res[-1]), 4),
        "nearest_sup": None if np.isnan(sup[-1]) else round(float(sup[-1]), 4),
        "vol_ratio": round(float(m15["volume"].iloc[-1]/avgvol), 2) if avgvol else None,
        "atr_pct": round(float(a/px*100), 2),
        "daily_trend": "up" if d1["close"].iloc[-1] > d_ema.iloc[-1] else "down",
    }
```

- [ ] **Step 4: Run to verify pass** → 1 passed.
- [ ] **Step 5: Commit** — `feat(sui_re): numeric context at T (look-ahead-safe)`

---

### Task 3: Decoy sampler

**Files:**
- Create: `D:\trading_system\sui_re\decoys.py`
- Test: `D:\trading_system\sui_re\tests\test_decoys.py`

- [ ] **Step 1: Write the failing test**

```python
import pandas as pd
from sui_re.decoys import sample_decoys

def test_decoys_avoid_real_entries():
    reals = pd.to_datetime(["2026-04-02 06:53","2026-04-18 04:49"])
    d = sample_decoys(reals, n=20, start="2026-04-01", end="2026-04-23", seed=1)
    assert len(d) == 20
    for ts in d:
        assert (abs((reals - ts).total_seconds()) > 6*3600).all()   # >6h from any real entry
```

- [ ] **Step 2: Run to verify fail** → ModuleNotFoundError.

- [ ] **Step 3: Implement**

```python
"""Sample random timestamps where he did NOT trade -- non-setup controls."""
import random
import pandas as pd

def sample_decoys(real_entries, n, start, end, seed=0, min_gap_h=6):
    rng = random.Random(seed)
    reals = pd.to_datetime(list(real_entries))
    lo, hi = pd.Timestamp(start), pd.Timestamp(end)
    span = int((hi - lo).total_seconds() // 900)        # 15-min slots
    out, guard = [], 0
    while len(out) < n and guard < n * 50:
        guard += 1
        ts = lo + pd.Timedelta(minutes=15 * rng.randint(0, span))
        if (abs((reals - ts).total_seconds()) > min_gap_h*3600).all():
            out.append(ts)
    return out
```

- [ ] **Step 4: Run to verify pass** → 1 passed.
- [ ] **Step 5: Commit** — `feat(sui_re): decoy timestamp sampler`

---

### Task 4: Chart renderer (truncated candlesticks)

**Files:**
- Create: `D:\trading_system\sui_re\render.py`
- Test: `D:\trading_system\sui_re\tests\test_render.py`

- [ ] **Step 1: Install dep** — `python -m pip install mplfinance --quiet`

- [ ] **Step 2: Write the failing test**

```python
import pandas as pd
from pathlib import Path
from sui_re.render import render_charts

def test_render_creates_truncated_charts(tmp_path):
    T = pd.Timestamp("2026-04-23 01:00")
    files = render_charts("SUI", T, tmp_path)
    assert len(files) == 4                       # weekly/daily/2h/15m
    for f in files:
        assert Path(f).exists() and Path(f).stat().st_size > 1000
```

- [ ] **Step 3: Run to verify fail** → ModuleNotFoundError.

- [ ] **Step 4: Implement**

```python
"""Render multi-timeframe candlestick charts truncated at T (no future bars)."""
import matplotlib
matplotlib.use("Agg")
import mplfinance as mpf
import pandas as pd
from sui_re.binance_data import load_ohlcv
from sui_re.indicators import rolling_vwap

TFS = [("1w", 60, 800), ("1d", 120, 250), ("2h", 120, 40), ("15m", 96, 7)]

def render_charts(pair, T, outdir):
    T = pd.Timestamp(T)
    files = []
    for interval, bars, lookback in TFS:
        df = load_ohlcv(f"{pair}USDT", interval,
                        T - pd.Timedelta(days=lookback), T + pd.Timedelta(days=1))
        df = df[df.index < T].tail(bars)          # strictly before entry
        if len(df) < 10:
            continue
        vwap = rolling_vwap(df, 20)
        ap = [mpf.make_addplot(vwap, color="orange", width=0.8)] if vwap.notna().any() else None
        path = f"{outdir}/{interval}.png"
        mpf.plot(df, type="candle", volume=True, style="charles",
                 addplot=ap, title=f"{pair} {interval}",
                 savefig=dict(fname=path, dpi=90, bbox_inches="tight"))
        files.append(path)
    return files
```

- [ ] **Step 5: Run to verify pass** → 1 passed.
- [ ] **Step 6: Commit** — `feat(sui_re): truncated multi-timeframe chart renderer`

---

### Task 5: Blind-set builder (artifacts + answer-key split)

**Files:**
- Create: `D:\trading_system\sui_re\blindset.py`
- Create: `D:\trading_system\sui_re\build_blind.py`
- Test: `D:\trading_system\sui_re\tests\test_blindset.py`

- [ ] **Step 1: Write the failing test**

```python
import json
from pathlib import Path
import pandas as pd
from sui_re.blindset import build_blind_set

def test_blind_artifacts_have_no_labels(tmp_path):
    trades = pd.DataFrame({
        "entry_time": pd.to_datetime(["2026-04-18 04:49","2026-04-02 06:53"]),
        "pair": ["SUI","SUI"], "direction": ["long","short"], "outcome": ["win","win"]})
    out = build_blind_set(trades, pair="SUI", n_decoys=2, root=tmp_path, seed=1)
    blind = Path(out)/"blind"; answers = Path(out)/"answers"/"answers.json"
    items = list(blind.iterdir())
    assert len(items) == 4                        # 2 real + 2 decoy, shuffled
    # blind context.json carries NO label/outcome/direction/is_real
    ctx = json.loads((items[0]/"context.json").read_text())
    assert not ({"outcome","direction","is_real","label"} & set(ctx))
    # answer key exists and is separate
    key = json.loads(answers.read_text())
    assert len(key) == 4 and all("is_real" in v for v in key.values())
```

- [ ] **Step 2: Run to verify fail** → ModuleNotFoundError.

- [ ] **Step 3: Implement**

```python
"""Assemble the shuffled blind set; split artifacts (no labels) from the answer key."""
import json
import random
from pathlib import Path
import pandas as pd
from sui_re.context import context_at
from sui_re.decoys import sample_decoys
from sui_re.render import render_charts

def build_blind_set(trades, pair, n_decoys, root, seed=0):
    root = Path(root); blind = root/"blind"; ans_dir = root/"answers"
    blind.mkdir(parents=True, exist_ok=True); ans_dir.mkdir(parents=True, exist_ok=True)
    sub = trades[trades["pair"] == pair].copy()
    items = [{"T": pd.Timestamp(r.entry_time), "is_real": True,
              "outcome": r.outcome, "direction": r.direction} for r in sub.itertuples()]
    decoys = sample_decoys(sub["entry_time"], n_decoys,
                           sub["entry_time"].min(), sub["entry_time"].max(), seed=seed)
    items += [{"T": ts, "is_real": False, "outcome": "decoy", "direction": None} for ts in decoys]
    random.Random(seed).shuffle(items)

    answers = {}
    for i, it in enumerate(items):
        iid = f"item_{i:03d}"
        idir = blind/iid; idir.mkdir(exist_ok=True)
        ctx = context_at(pair, it["T"])
        ctx_pub = {k: (str(v) if isinstance(v, pd.Timestamp) else v) for k, v in ctx.items()}
        (idir/"context.json").write_text(json.dumps({"id": iid, "pair": pair, **ctx_pub}, indent=2))
        render_charts(pair, it["T"], idir)
        answers[iid] = {"is_real": it["is_real"], "outcome": it["outcome"],
                        "direction": it["direction"], "entry_time": str(it["T"]), "pair": pair}
    (ans_dir/"answers.json").write_text(json.dumps(answers, indent=2))
    return str(root)
```

```python
# build_blind.py
"""Build the SUI blind set from labeled_trades.csv."""
import sys
import pandas as pd
from sui_re.blindset import build_blind_set

sys.stdout.reconfigure(encoding="utf-8")

def main():
    trades = pd.read_csv(r"D:\trading_system\sui_re\labeled_trades.csv",
                         parse_dates=["entry_time", "close_time"])
    sui = trades[trades.pair == "SUI"]
    out = build_blind_set(sui, pair="SUI", n_decoys=len(sui),
                          root=r"D:\trading_system\sui_re\blind_run", seed=7)
    print(f"blind set built at {out}: {len(sui)} real SUI + {len(sui)} decoys")

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run to verify pass + build** — `python -m pytest sui_re/tests/test_blindset.py -v && python -m sui_re.build_blind`
- [ ] **Step 5: Commit** — `feat(sui_re): blind-set builder with structural answer-key split`

---

## Self-Review

- **Spec coverage:** wins+losses+decoys shuffled ✓ (Task 5); truncated charts+numbers ✓ (Tasks 2,4); structural blindness — blind artifacts carry no label, answer key in separate dir never read at predict time ✓ (Task 5 test asserts it).
- **Placeholder scan:** none; runnable code throughout.
- **Type consistency:** `load_ohlcv` (Part 1) reused; `context_at`→dict used by `blindset`; `render_charts`/`sample_decoys` signatures consistent across tasks.
- **Integrity note:** Part 3 (predict) must read ONLY `blind_run/blind/<id>/`; `blind_run/answers/` stays unopened until scoring. This is the discipline that makes the blind real.

## Next (Part 3, separate plan)
Predict loop (I commit a read per item from blind artifacts only) + scorer (simulate my calls on forward bars for expectancy; agreement + win/loss/decoy discrimination as diagnostics) → the four-cell verdict.
