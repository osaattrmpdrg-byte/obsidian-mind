---
date: 2026-06-16
description: "Design spec for backtesting the VWAP + volume-S/R strategy on BTC daily via a pre-registered ablation ladder — engine reuse, entry logic, variants, and anti-curve-fit validation discipline."
tags:
  - thinking
  - trading
  - spec
status: tested-rejected
---

> [!failure] TESTED 2026-06-17 — NO EDGE. See Results at the bottom and [[What Didn't Work]].

# VWAP + Volume-S/R Strategy — Backtest Design

**Goal:** Settle empirically whether the VWAP-vs-S/R idea has a backtestable edge on BTC, via a **pre-registered ablation ladder** — not a free parameter sweep. Each layer of the original strategy is added one rung at a time so we can measure what each actually contributes (and prove what's noise).

> Source idea: multi-timeframe VWAP + volume-correlated support/resistance, with a 6x-leverage 2hr execution layer and BTC CME-gap / ETF-flow correlators. This spec tests the **daily core only**; the intraday/leverage/correlator layers are explicitly deferred (see §7).

---

## 1. Instrument & Data

- **BTC/USD daily**, yfinance `BTC-USD` (~4,000 bars, real volume, longest clean history — strongest known venue per [[Trading System]]).
- Reuse `get_crypto()` from `D:\trading_system\validate_crypto.py`.
- **Deferred:** alts (SUI etc.), 2hr intraday, CME futures gap, ETF flows — short history / hard-to-source / idiosyncratic risk. Not admitted until the daily core earns it.

## 2. Entry Logic

Resolves the original (internally contradictory) lines into one coherent rule:

- **Long** when price **> VWAP** *and* within proximity of a **support** level → TP at next **resistance** band, hard SL below.
- **Short** when price **< VWAP** *and* within proximity of a **resistance** level → TP at next **support** band, hard SL above.
- **Proximity** = within `0.5 × ATR(14)` of the level (default).
- ⚠️ Short side is **backtest-only** — no clean India-legal crypto short vehicle. Flagged, not assumed tradeable.

## 3. Ablation Ladder (the ONLY variants run — no sweeping inside a rung)

| Rung | VWAP | S/R | Volume filter | What it isolates |
|---|---|---|---|---|
| **0 — Floor** | rolling-20 | rolling high/low channel | none | does *any* VWAP+S/R logic beat noise |
| **1 — Core** | rolling-20 | volume-confirmed swing pivots | none | does volume-confirmed S/R add value over the dumb channel |
| **1b — VWAP swap** | anchored (weekly open) | volume-confirmed pivots | none | does anchored VWAP beat rolling |
| **2 — +Volume** | best of above | best of above | entry requires `vol > N × avg` | does the volume-confluence trigger earn its place |

Each rung = one backtest with **fixed** parameters.

### Default parameters (fixed per rung)

| Param | Default | Notes |
|---|---|---|
| Rolling VWAP window | 20 | volume-weighted MA |
| Anchored VWAP anchor | weekly open (Mon 00:00 UTC) | matches "weekly chart" framing |
| Swing pivot half-width `k` | 5 bars each side | fractal pivot |
| Pivot volume confirmation | `vol > 1.5 × 20-bar avg` at pivot bar | the "volume correlation" |
| Rolling channel `N` | 20 | Donchian floor |
| Proximity to level | `0.5 × ATR(14)` | "near support/resistance" |
| Hard SL | `1.5 × ATR(14)` | matches existing engine |
| Entry-volume multiple `N` (rung 2) | 5 × 20-bar avg | from the original "5x volume" idea |

## 4. Exit

- **Primary:** TP at opposing band + hard SL at `1.5 × ATR` — as the original strategy literally states ("take profit at resistance / support").
- **Secondary comparison:** the validated **5-bar trailing stop, no TP** from `backtest/trail_engine.py`. Prior FX work found fixed TP *hurts* momentum (see [[What Didn't Work]] — "Fixed 2:1 R:R Take Profit"); this re-checks whether "TP at the band" actually beats letting winners run on crypto.

## 5. Validation Discipline (anti-curve-fit guard)

Reuse `wilson_ci` + `summarize` from `trail_engine.py`. A rung **passes only if** all hold:

1. **Train/holdout split** — older **70%** train, newer **30%** holdout. Wilson-lo > break-even WR in **BOTH**. (Break-even depends on realized R:R, not assumed 1:2 — compute from the rung's own avg win/loss, per the panel's correction in [[Trading System]].)
2. **Trial-count penalty** — ~5 variants run → raise the significance bar (Šidák: effective `z` for `α = 1 − (1 − 0.05)^(1/5)`). More variants tested = higher bar, by design.
3. **Robustness reports** (already in the crypto harness): temporal-era splits, tail-fragility (drop top-k winners), cost-sensitivity (sweep fee assumption).
4. **No look-ahead** — proven via a shifted-data assertion in tests (signal at bar `i` uses only data ≤ `i`; entry at `open[i+1]`).
5. **Non-overlapping trades only** — research-mode overlap inflates results (72–81%, per [[What Didn't Work]]).

## 6. Code Plan

- **New file:** `D:\trading_system\validate_vwap_sr.py` — drives the ladder, reuses `summarize` / `wilson_ci` / `get_crypto`.
- **New functions in `signals/indicators.py`** (built **TDD**, real-data tests, no look-ahead): `rolling_vwap`, `anchored_vwap`, `volume_pivots`, `vwap_sr_signals`.
- **Tests first:** each indicator gets a red→green test before use; a dedicated look-ahead test shifts input and asserts no signal change in the past.

## 7. Explicitly Deferred (not in this spec)

- 2hr intraday timeframe + multi-timeframe alignment (weekly S/R → daily volume → 2hr entry)
- 6x leverage + 8–9% TP / 5–7% SL sizing scheme (account-blowing risk at current capital — see [[Trading System]] position sizing rules)
- BTC CME futures gap-fill correlator
- BTC ETF inflow/outflow signal
- Oil inverse correlation
- Alt selection (SUI and other high-beta-to-BTC coins)

Each is admitted **only if** the daily core passes — and then through its own spec → plan → test cycle.

---

## Open Flags for Review

- **(a)** BTC-only daily, full intraday/leverage/correlator stack deferred — adjust if you want the full stack sooner despite the data cost.
- **(b)** Short side is in the backtest but has no clean execution path — kept for completeness, not tradeable as-is.
- **(c)** Variant count (~5) is the main curve-fit risk; the trial penalty + holdout are the mitigation. Adding more variants raises the bar for all.

## Results (2026-06-17)

Ran `D:\trading_system\validate_vwap_sr.py` on BTC/USD daily, 4,000 bars (2015-07 → 2026-06), 0% zero-vol bars.

| Rung | Exit | n | adjR (full) | Holdout adjR | Verdict |
|---|---|---|---|---|---|
| 0 — FLOOR (rolling/channel) | TP@band | **0** | — | — | never triggers |
| 1 — CORE (rolling/pivots) | TP@band | 83 | −0.051 | −0.236 | no edge |
| 1b — VWAP (anchored/pivots) | TP@band | 100 | −0.069 | −0.301 | no edge |
| 2 — +VOL (anchored/pivots/5×) | TP@band | **0** | — | — | never triggers |
| 1 — CORE (rolling/pivots) | 5-bar trail | 101 | +0.016 | +0.188 | ~breakeven, not sig |

**Verdict: REJECTED — no edge survives the gates.**
- Every TP@band config is negative full-sample **and** negative in the 30% holdout.
- Long-only shows a positive *point* estimate (+0.08 to +0.21R) but **Wilson-lo never clears break-even WR** → not significant; and it's **entirely tail-dependent** — dropping the single best winner turns it negative.
- The only strongly-positive era is **2015–2017 (n=7, +2.09R)** — early illiquid BTC, a relic. 2018→ negative.
- **5-bar trailing beats TP@band** (re-confirms "fixed TP hurts" from [[What Didn't Work]]) — flips full-sample to ~breakeven and holdout mildly positive — but still not significant, still tail-fragile.
- The **"5× volume"** entry filter and the **Donchian floor** each fire **0 trades** on daily bars.

**Implication:** does not beat the existing breakout edge (BTC +1.686R, tail-robust). Deferred 2hr/leverage/CME/ETF layers not pursued — the daily core fails OOS, and 6× leverage on ≤0R/trade expectancy only accelerates ruin. Full detail in [[What Didn't Work#VWAP + Volume-S/R (BTC daily) (2026-06-17)]].

## Related

- [[Trading System]] — proven signals, gates, position sizing
- [[What Didn't Work]] — fixed-TP and subjective-TA rejections this spec re-tests / avoids
- [[Daily Watch Weekly Hunt]] — the lockbox/trial-penalty discipline reused here
