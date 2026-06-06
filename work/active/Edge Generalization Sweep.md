---
date: 2026-06-06
description: "One-time GCP compute burst that tests the breakout edge across a max-breadth instrument universe — real-edge verdict (Phase 1) + go-live shortlist (Phase 2). Design approved, build pending."
tags:
  - work-note
  - trading
status: active
quarter: Q2-2026
---

# Edge Generalization Sweep

> [!abstract] Status — design approved, build paused
> Brainstorm paused mid design-review on 2026-06-06 (focus lost). Methodology and universe are decided; resume at the **To-Do** below. This is sub-project 1 of the "[[GCP Credits Strategy]] → unblock stuck streams" direction.

## What & Why

The blocker this kills: *"Which instruments do we actually go live on — and is the breakout edge even real, or just curve-fit to crypto?"* Funded by the **$300 GCP trial credits** as a one-time compute burst (see [[GCP Credits Strategy]]). Nothing persists → zero cost after the 2026-09-04 cliff.

## Approved Design

**Universe — maximum breadth.** Every liquid instrument across asset classes, each tagged `asset_class`, `correlation_group`, `tradeable_venue`:
- Crypto (~100 `-USD`) → tradeable = CoinDCX-listed
- FX majors + minors (`EURUSD=X`…) → tradeable = NSE cross-currency
- Commodities (`GC=F`, `CL=F`, `SI=F`…) → tradeable = MCX (gold)
- Index futures (`ES=F`, `NQ=F`…) → tradeable = No
- Sector ETFs → diversity panel, tradeable = No

**Methodology — Hybrid (C).**
- **Phase 1 — Lock-and-Apply (truth test):** the *fixed* BTC-winning params (lookback 20, SL 1.5·ATR, TP 1:2, EMA50>EMA200 regime) applied **unchanged** to every instrument. One backtest each. **Correlation-aware aggregation** — pass-rate per asset class / cluster, so crypto's correlated mass can't fake the verdict. Headline: does the edge stay positive on *uncorrelated* classes (FX, commodities, indices)? → verdict: real & universal / crypto-only / not real.
- **Phase 2 — Walk-forward + bootstrap (go-live numbers):** only on instruments that pass Phase 1 **AND** are tradeable. Rolling walk-forward + 10k bootstrap on out-of-sample trades → CIs on expectancy **and worst-case drawdown**. → ranked go-live shortlist.

**Infra.** Spot VM (preemptible) on Compute Engine; `yfinance` (single free cross-asset daily source, fetch-once + parquet cache); results → Cloud Storage bucket + vault; VM **auto-deletes** after run. Budget alert $50.

**Scope / YAGNI.** Long-only, daily bars only, breakout edge only (the 4-family `strategy_sweep` is a separate question). Builds on the existing `D:\crypto_trading\backtest_parallel.py` engine — refactor, not rewrite.

## To-Do (resume here)

- [ ] **Resume the brainstorm** — confirm/adjust 3 open items: final universe size, Phase-1 fixed params, results note location. Then continue to spec.
- [ ] Write the spec doc (brainstorming → `writing-plans`)
- [ ] Refactor `backtest_parallel.py` engine into a reusable module, **TDD**: `wilson_ci`, `run_backtest`, walk-forward splitter (prove **no look-ahead**), bootstrap CI
- [ ] Build the tagged instrument-universe list
- [ ] Phase 1 runner + correlation-aware aggregation
- [ ] Phase 2 runner (walk-forward + bootstrap, tradeable survivors only)
- [ ] **Local regression run on BTC/ETH — reproduce existing results before spending on the VM**
- [ ] GCP: set budget alert → provision Spot VM → run → results to bucket + vault → auto-delete VM
- [ ] Write `reference/trading/Edge Generalization Sweep Results.md`, link from [[Trading System]] + [[Signal Matrix]]

## Also pending (separate specs)

- **Content Niche Discovery Engine** — sub-project 2 of [[GCP Credits Strategy]]. Own spec, not started. Flag: more API+analysis than heavy compute.

## Related

- [[GCP Credits Strategy]] — the parent strategy and why this is funded by credits
- [[Trading System]] — the edge being tested, current instrument status
- [[Signal Matrix]] — confidence gate the shortlist feeds
- [[What Didn't Work]] — overfitting traps this design is built to avoid
- [[Streams]] — Stream 2 (Trading)
- [[CoinDCX Execution Layer]] — where validated crypto instruments get executed
