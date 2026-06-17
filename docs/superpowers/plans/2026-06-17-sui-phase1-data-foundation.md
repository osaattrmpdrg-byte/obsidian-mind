---
date: 2026-06-17
description: "Implementation plan — Phase 1 Part 1 of the SUI reverse-engineer project: Binance data layer + parse the friend's CoinDCX exports into a direction-labeled trade dataset, TDD, validated against a known short."
tags:
  - thinking
  - trading
  - plan
status: proposed
---

# SUI Reverse-Engineer — Phase 1 Part 1: Data Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the friend's CoinDCX Excel exports + Binance price history into a clean, direction-labeled dataset of his entries (`labeled_trades.csv`) — the foundation every later Phase-1 step consumes.

**Architecture:** Two focused modules. `binance_data.py` fetches and caches Binance public OHLCV (no auth) and answers "price at time T." `trades.py` parses the futures sheet, pairs opens→closes into positions, and *derives* each trade's long/short direction from the P&L sign vs the price move (the export has no side column). A thin builder joins them into the labeled dataset. Validated against a trade whose direction we already know (23 Apr 2026 SUI short).

**Tech Stack:** Python 3.x, pandas, numpy, openpyxl (Excel), urllib (stdlib, for Binance). Lives in `D:\trading_system\sui_re\` (shares the trading_system env; local git, no remote).

**Spec:** `obsidian-mind/docs/superpowers/specs/2026-06-17-sui-reverse-engineer-design.md`. Governed by `[[Reverse-Engineer Before Apply]]`.

---

### Task 1: Binance data layer — fetch + cache OHLCV

**Files:**
- Create: `D:\trading_system\sui_re\__init__.py` (empty)
- Create: `D:\trading_system\sui_re\binance_data.py`
- Test: `D:\trading_system\sui_re\tests\test_binance_data.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_binance_data.py
import pandas as pd
from sui_re.binance_data import load_ohlcv, price_at

def test_load_ohlcv_real_sui_daily():
    df = load_ohlcv("SUIUSDT", "1d", "2025-09-10", "2025-09-20")
    assert {"open","high","low","close","volume"} <= set(df.columns)
    assert df.index.is_monotonic_increasing
    assert (df["volume"] > 0).all()          # real traded volume
    assert len(df) >= 8                       # ~10 daily bars in range

def test_price_at_returns_last_close_before_ts():
    df = load_ohlcv("SUIUSDT", "1d", "2025-09-10", "2025-09-20")
    p = price_at(df, pd.Timestamp("2025-09-15 12:00"))
    assert 1.0 < p < 10.0                      # SUI ~3.7 in Sep 2025; sanity band
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_binance_data.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'sui_re.binance_data'`

- [ ] **Step 3: Write minimal implementation**

```python
# sui_re/binance_data.py
"""Binance public OHLCV (data-api.binance.vision — no auth, no geo-block).
CoinDCX USDT-M futures are Binance-mirrored, so this is the price actually traded."""
import json, time, urllib.request
from pathlib import Path
import pandas as pd

BASE = "https://data-api.binance.vision/api/v3/klines"
CACHE = Path(__file__).parent / ".cache"
CACHE.mkdir(exist_ok=True)

def _ms(ts) -> int:
    return int(pd.Timestamp(ts).tz_localize("UTC").timestamp() * 1000)

def fetch_klines(symbol, interval, start_ms, end_ms):
    """Paginated raw kline fetch (1000/call)."""
    out, cur = [], start_ms
    while cur < end_ms:
        url = f"{BASE}?symbol={symbol}&interval={interval}&startTime={cur}&endTime={end_ms}&limit=1000"
        rows = json.load(urllib.request.urlopen(url, timeout=30))
        if not rows:
            break
        out.extend(rows)
        nxt = int(rows[-1][0]) + 1
        if nxt <= cur:
            break
        cur = nxt
        if len(rows) < 1000:
            break
        time.sleep(0.1)
    return out

def load_ohlcv(symbol, interval, start, end, refresh=False) -> pd.DataFrame:
    cache = CACHE / f"{symbol}_{interval}_{pd.Timestamp(start).date()}_{pd.Timestamp(end).date()}.parquet"
    if cache.exists() and not refresh:
        return pd.read_parquet(cache)
    raw = fetch_klines(symbol, interval, _ms(start), _ms(end))
    df = pd.DataFrame(raw, columns=["t","open","high","low","close","volume",
                                    "ct","qv","n","tb","tq","ig"])
    df = df[["t","open","high","low","close","volume"]].astype(
        {"open":float,"high":float,"low":float,"close":float,"volume":float})
    df["time"] = pd.to_datetime(df["t"], unit="ms")
    df = df.drop(columns="t").set_index("time").sort_index()
    df.to_parquet(cache)
    return df

def price_at(df, ts) -> float:
    """Close of the last bar at or before ts (look-ahead-safe)."""
    ts = pd.Timestamp(ts)
    sub = df.loc[:ts]
    if sub.empty:
        raise ValueError(f"no bars at/before {ts}")
    return float(sub["close"].iloc[-1])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_binance_data.py -v`
Expected: PASS (2 passed). If parquet engine missing: `pip install pyarrow`.

- [ ] **Step 5: Commit**

```bash
cd /d D:\trading_system
git add sui_re/__init__.py sui_re/binance_data.py sui_re/tests/test_binance_data.py
git commit -m "feat(sui_re): Binance OHLCV data layer with cache + price_at"
```

---

### Task 2: Parse the futures sheet into clean rows

**Files:**
- Create: `D:\trading_system\sui_re\trades.py`
- Test: `D:\trading_system\sui_re\tests\test_trades.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_trades.py
from pathlib import Path
from sui_re.trades import load_futures_rows

XLSX = list(Path(r"D:\DRG\afcat").glob("RakshithG_*qhqi9l*.xlsx"))[0]  # FY26, 100 trades

def test_load_futures_rows_shape_and_columns():
    rows = load_futures_rows(XLSX)
    assert set(["pair","time","type","gross","fees"]) <= set(rows.columns)
    assert len(rows) > 150                      # ~195 order+funding rows
    assert rows["time"].notna().all()
    assert rows["pair"].str.contains("SUI").any()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_trades.py -v`
Expected: FAIL with `ImportError: cannot import name 'load_futures_rows'`

- [ ] **Step 3: Write minimal implementation**

```python
# sui_re/trades.py
"""Parse CoinDCX USDT-M futures export into labeled, direction-derived entries."""
import pandas as pd

def load_futures_rows(xlsx_path) -> pd.DataFrame:
    """Read the 'Futures Orders (USDT-M)' sheet; header sits on file row 8."""
    df = pd.read_excel(xlsx_path, sheet_name="Futures Orders (USDT-M)", header=7)
    df.columns = ["txid","pair","base","time","type","gross","net_inr","fees"]
    df = df.dropna(subset=["time"]).copy()
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"])
    for c in ("gross","net_inr","fees"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["pair"] = (df["pair"].astype(str)
                  .str.replace("B-","",regex=False).str.replace("_USDT","",regex=False))
    return df.sort_values("time").reset_index(drop=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_trades.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
cd /d D:\trading_system
git add sui_re/trades.py sui_re/tests/test_trades.py
git commit -m "feat(sui_re): parse CoinDCX futures export rows"
```

---

### Task 3: Pair opens→closes into positions

**Files:**
- Modify: `D:\trading_system\sui_re\trades.py`
- Test: `D:\trading_system\sui_re\tests\test_trades.py`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_trades.py
from sui_re.trades import pair_trades

def test_pair_trades_produces_closed_positions():
    rows = load_futures_rows(XLSX)
    trades = pair_trades(rows)
    # each closed trade has an entry + exit time and a realized pnl
    assert {"open_time","close_time","pair","gross","fees"} <= set(trades.columns)
    assert (trades["close_time"] >= trades["open_time"]).all()
    assert len(trades) >= 90                     # ~100 realized closes in FY26
    assert (trades["gross"] != 0).all()          # closes carry the P&L, opens excluded
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_trades.py::test_pair_trades_produces_closed_positions -v`
Expected: FAIL with `ImportError: cannot import name 'pair_trades'`

- [ ] **Step 3: Write minimal implementation**

```python
# append to sui_re/trades.py
def pair_trades(rows) -> pd.DataFrame:
    """Pair each closing order (gross != 0) with the most recent prior opening
    order (gross == 0) on the same pair (FIFO). Funding rows ignored.
    NOTE: heuristic — CoinDCX export has no position id. Validated downstream
    against a known trade (23 Apr SUI short)."""
    orders = rows[rows["type"] == "By Order"].copy()
    open_q = {}                                   # pair -> list of open times (FIFO)
    trades = []
    for _, r in orders.iterrows():
        if r["gross"] == 0:                       # opening order (fee only)
            open_q.setdefault(r["pair"], []).append(r["time"])
        else:                                     # closing order (carries P&L)
            q = open_q.get(r["pair"], [])
            open_time = q.pop(0) if q else r["time"]
            trades.append({"open_time": open_time, "close_time": r["time"],
                           "pair": r["pair"], "gross": r["gross"], "fees": r["fees"]})
    return pd.DataFrame(trades)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_trades.py -v`
Expected: PASS (all)

- [ ] **Step 5: Commit**

```bash
cd /d D:\trading_system
git add sui_re/trades.py sui_re/tests/test_trades.py
git commit -m "feat(sui_re): pair opens to closes into positions (FIFO heuristic)"
```

---

### Task 4: Derive direction (long/short) from P&L vs price move

**Files:**
- Modify: `D:\trading_system\sui_re\trades.py`
- Test: `D:\trading_system\sui_re\tests\test_trades.py`

- [ ] **Step 1: Write the failing test** (pure unit + known-trade anchor)

```python
# append to tests/test_trades.py
from sui_re.trades import derive_direction

def test_derive_direction_pure():
    # 23 Apr SUI: entry 0.970 -> close 0.957 (price fell), P&L positive => SHORT
    assert derive_direction(+2.8, 0.970, 0.957) == "short"
    # price rose + positive pnl => long
    assert derive_direction(+1.0, 0.95, 0.97) == "long"
    # price rose + negative pnl => short (lost being short into a rally)
    assert derive_direction(-1.0, 0.95, 0.97) == "short"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_trades.py::test_derive_direction_pure -v`
Expected: FAIL with `ImportError: cannot import name 'derive_direction'`

- [ ] **Step 3: Write minimal implementation**

```python
# append to sui_re/trades.py
def derive_direction(gross_pnl, price_open, price_close) -> str:
    """Long profits when price rises; short profits when price falls.
    direction = long iff sign(pnl) agrees with sign(price move)."""
    price_up = price_close > price_open
    pnl_pos = gross_pnl > 0
    return "long" if (pnl_pos == price_up) else "short"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_trades.py::test_derive_direction_pure -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
cd /d D:\trading_system
git add sui_re/trades.py sui_re/tests/test_trades.py
git commit -m "feat(sui_re): derive long/short direction from pnl vs price move"
```

---

### Task 5: Build the labeled dataset (join trades + prices) and validate end-to-end

**Files:**
- Modify: `D:\trading_system\sui_re\trades.py`
- Create: `D:\trading_system\sui_re\build_dataset.py`
- Test: `D:\trading_system\sui_re\tests\test_trades.py`

- [ ] **Step 1: Write the failing test** (real Excel + real Binance prices; the 23 Apr trade MUST come out short)

```python
# append to tests/test_trades.py
from sui_re.trades import build_labeled_trades

def test_build_labeled_trades_known_short():
    df = build_labeled_trades(XLSX)
    assert {"entry_time","pair","direction","outcome","gross"} <= set(df.columns)
    assert df["outcome"].isin(["win","loss"]).all()
    # the 23 Apr 2026 ~01:04 SUI close is a known SHORT winner
    apr23 = df[(df.pair=="SUI") &
               (df.close_time.dt.strftime("%Y-%m-%d")=="2026-04-23")]
    assert len(apr23) >= 1
    assert (apr23["direction"] == "short").any()
```
*(Note: 23 Apr trade lives in the FY27 export; for this test point `XLSX` at the FY27 file `*yurf1q*.xlsx`, or run `build_labeled_trades` over both files. Keep one combined builder — see Step 3.)*

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_trades.py::test_build_labeled_trades_known_short -v`
Expected: FAIL with `ImportError: cannot import name 'build_labeled_trades'`

- [ ] **Step 3: Write minimal implementation**

```python
# append to sui_re/trades.py
from sui_re.binance_data import load_ohlcv, price_at

def _symbol(pair): return f"{pair}USDT"

def build_labeled_trades(*xlsx_paths) -> pd.DataFrame:
    """Full pipeline: parse -> pair -> derive direction (Binance prices) -> label outcome."""
    frames = [pair_trades(load_futures_rows(p)) for p in xlsx_paths]
    t = pd.concat(frames, ignore_index=True).sort_values("open_time")
    out = []
    for pair, grp in t.groupby("pair"):
        lo = grp["open_time"].min() - pd.Timedelta(days=2)
        hi = grp["close_time"].max() + pd.Timedelta(days=2)
        px = load_ohlcv(_symbol(pair), "15m", lo, hi)
        for _, r in grp.iterrows():
            p_open, p_close = price_at(px, r["open_time"]), price_at(px, r["close_time"])
            out.append({
                "entry_time": r["open_time"], "close_time": r["close_time"],
                "pair": pair,
                "direction": derive_direction(r["gross"], p_open, p_close),
                "outcome": "win" if r["gross"] > 0 else "loss",
                "gross": r["gross"], "fees": r["fees"],
            })
    return pd.DataFrame(out).sort_values("entry_time").reset_index(drop=True)
```

```python
# sui_re/build_dataset.py
"""Run the labeled-dataset build over both exports; write CSV + print summary."""
import sys, glob
import pandas as pd
from sui_re.trades import build_labeled_trades

sys.stdout.reconfigure(encoding="utf-8")
FILES = glob.glob(r"D:\DRG\afcat\RakshithG_*.xlsx")

def main():
    df = build_labeled_trades(*FILES)
    df.to_csv(r"D:\trading_system\sui_re\labeled_trades.csv", index=False)
    print(f"trades: {len(df)}  wins: {(df.outcome=='win').sum()}  losses: {(df.outcome=='loss').sum()}")
    print("direction split:\n", df["direction"].value_counts().to_string())
    print("by pair:\n", df.groupby("pair")["outcome"].value_counts().to_string())

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test + the build script**

Run: `cd /d D:\trading_system && python -m pytest sui_re/tests/test_trades.py -v && python -m sui_re.build_dataset`
Expected: tests PASS; script prints ~113 trades with a win/loss + direction split, and writes `labeled_trades.csv`. **Sanity-check the direction split is plausible (not 100% one side).**

- [ ] **Step 5: Commit**

```bash
cd /d D:\trading_system
git add sui_re/trades.py sui_re/build_dataset.py sui_re/tests/test_trades.py sui_re/labeled_trades.csv
git commit -m "feat(sui_re): build direction-labeled trade dataset (validated vs known short)"
```

---

## Self-Review

- **Spec coverage:** This plan covers the spec's "Data layer" + "Label set" requirements. The blind-set mix (wins+losses+decoys), truncated rendering, prediction schema, and scoring are **Parts 2–3** (separate plans) — see below.
- **Placeholder scan:** none — every step has runnable code/commands.
- **Type consistency:** `load_ohlcv`/`price_at` (Task 1) reused in Task 5; `load_futures_rows`→`pair_trades`→`derive_direction`→`build_labeled_trades` chain consistent.
- **Known risk flagged:** open→close pairing is a heuristic (no position id in the export). Task 5's known-short test is the guardrail; if the direction split looks degenerate, revisit pairing (try LIFO) before Part 2.

## Phase 1 — Parts 2 & 3 (next plans, outlined)

- **Part 2 — Blind artifacts:** at each `entry_time` (and for sampled decoy timestamps), render multi-timeframe candlestick charts (W/D/2h/15m + VWAP + volume) **truncated at the last closed bar before T**, plus a truncated numeric-context table. Build the shuffled, anonymized blind set (his wins + losses + decoys); write the answer key to a *separate* file never loaded at prediction time. Reuses indicators from `validate_vwap_sr.py`.
- **Part 3 — Predict + score:** I commit a blind read per item (`is_setup, direction, entry, target, stop, confidence, rationale`); the scorer simulates *my* calls on forward bars for expectancy (primary), and reports agreement-with-his-entries + win/loss/decoy discrimination (diagnostic). Outcome decides the four-cell verdict in the spec.