---
date: 2026-06-05
description: "BTC/USD instrument reference — backtest results, signal logic, current regime, and execution details."
tags:
  - reference
  - trading
  - instrument
---

# BTC/USD — Instrument Reference

## Backtest Results (20-bar breakout, LONG ONLY)

| Period | n | WR | Adj R | Verdict |
|---|---|---|---|---|
| Full 12yr | 116 | 51.7% | +0.452R | SIG |
| Train 2017-2021 | 81 | 56.8% | +0.604R | SIG |
| Test 2022-today | 35 | 40.0% | +0.100R | Borderline |

**Frequency:** 9.9 completed trades/year
**Kelly (quarter):** 6.3% of equity

> [!warning] Test Period Borderline
> Test period n=35 and adj=+0.100R is borderline. BTC/ETH correlation ~0.85 — validate BTC fully before adding ETH.

## Signal Logic

- **Entry:** close > prior 20-bar high
- **Regime:** EMA50 > EMA200 AND close > EMA50
- **ATR filter:** skip if ATR > 2× its 50-day average
- **SL:** 1.5× ATR | **TP:** 3.0× ATR | **Max hold:** 20 bars

## Current Regime (last updated 2026-05-22)

- EMA50: $76,780 | EMA200: $81,690
- **Status: NONE — EMA50 < EMA200. Waiting for regime flip.**
- Close at last check: $77,539

### Regime Flip Conditions (B3 research, 2026-06-05)

The golden cross (EMA50 > EMA200) is a **lagging confirmation, not a predictive trigger** — you can't reliably front-run it. The cross IS the signal. But these secondary indicators confirm a flip has real accumulation behind it (vs a fakeout):

| Signal | Bullish flip condition |
|--------|----------------------|
| MVRV | Recovering from <1.0 toward long-term mean |
| NUPL | Moving capitulation → hope/optimism (not yet euphoria) |
| Exchange netflow | Turning from inflows (sell pressure) → outflows (accumulation) |
| Institutional | ETF / CME futures inflows turning net-positive |
| Macro | Falling real yields, weaker dollar |

**Halving timing:** crosses historically appear 12-24 months after a halving-cycle bottom. 2024 halving → 2025-26 is the expected expansion window.

> [!warning] Contrarian flag
> As BTC becomes ETF/institution-dominated, the clean 4-year halving pattern may break down — macro liquidity could dominate supply effects. Don't treat the halving cycle as destiny.

## Execution

- Exchange: CoinDCX (BTC/USDT or BTC/INR)
- Phase: Paper trading (target 20 trades before live)
- Scanner: GitHub Actions, 00:30 UTC daily, Telegram alert on signal
- **Execution layer not built yet** — one-tap CoinDCX REST API is the next build task

## Trade Journal

- [[trade-log]]

## Related

- [[Trading System]] — full system context
- [[ETH_USD]] — Phase 2 instrument (correlated, deferred until BTC validates)
- [[What Didn't Work]] — signals tested and rejected on BTC
