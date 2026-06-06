---
date: 2026-06-05
description: "ETH/USD instrument reference — Phase 2, deferred until BTC validates. Borderline test results, high BTC correlation."
tags:
  - reference
  - trading
  - instrument
---

# ETH/USD — Instrument Reference

## Backtest Results (20-bar breakout, LONG ONLY)

| Period | n | WR | Adj R | Verdict |
|---|---|---|---|---|
| Full 9yr | 57 | 47.4% | +0.321R | SIG |
| Train 2017-2021 | 33 | 54.5% | +0.536R | SIG |
| Test 2022-today | 24 | 37.5% | +0.025R | NOT SIG |

**Frequency:** 6.7 completed trades/year
**Status: Phase 2 — add only after 20 BTC paper trades validate**

## Why Deferred

- Test period n=24 — too small to confirm edge
- adj_R in test = +0.025R — borderline, doesn't clear the Wilson CI bar
- BTC/ETH correlation ~0.85 — limited diversification until BTC validates first

## Execution (when activated)

- Exchange: CoinDCX (ETH/USDT)
- Same signal logic as [[BTC_USD]]

## Related

- [[BTC_USD]] — validate this first before activating ETH
- [[Trading System]] — full system context
