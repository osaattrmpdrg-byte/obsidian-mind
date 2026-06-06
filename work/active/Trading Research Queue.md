---
date: 2026-06-05
description: "Ordered queue of trading research questions to run via /trading-research. A1 complete, A2-A3 and B1-B4 pending."
tags:
  - work-note
  - trading
  - research
status: active
quarter: Q2-2026
---

# Trading Research Queue

Run via `/trading-research [question]` → routes to Perplexity Sonar (paid, ~$0.005/query).
Results auto-saved to `Research\Web\` in vault.

> [!tip] How to run
> Open Claude Code in this vault → type `/trading-research` → paste the question below verbatim.

---

## Option A — Build Gaps (run first)

- [x] **A1 — CoinDCX API mechanics** ✅ Done 2026-06-05 → [[CoinDCX Execution Layer]]
  > Source: [[2026-06-05 - coindcx rest api order placement for btcusdt - authentication endpoints rate lim]]
- [x] **A2 — Zerodha MCX Gold execution mechanics** ✅ Done 2026-06-05 → [[XAU_USD]]
  > Sources: [[2026-06-05 - complete execution mechanics for mcx gold mini on zerodha kite - lot size margin]], [[2026-06-05 - angel one smartapi mcx commodity order placement for gold mini - authentication]]
  > "What are the complete execution mechanics for MCX Gold Mini on Zerodha Kite? Cover: lot size (10g), margin requirements at current gold price, order types available (market/limit/SL-M), trading hours, settlement process, and whether Kite Connect API supports MCX commodity order placement programmatically."

- [x] **A3 — Position sizing for small capital (₹5-6k)** ✅ Done 2026-06-05 → [[Trading System#Position Sizing Rules]]
  > "What is the optimal position sizing strategy for a swing trader starting with ₹5-6k capital using a system with ~18 trades/year and +0.3R average expectancy? Cover: minimum viable capital per risk percentage, brokerage and spread impact at small position sizes, quarter-Kelly application, and compounding math from ₹5k to ₹50k over 3 years."
  > Source: [[2026-06-05 - optimal position sizing strategy for swing trader starting with 5000-6000 inr ca]]

---

## Option B — Strategy Gaps (run after A complete)

- [x] **B1 — EUR/JPY and GBP/JPY for instrument expansion** ❌ REJECTED 2026-06-05 
  > BoJ/MoF interventions (¥5.6T Oct 2022, April-May 2024) cause 5% intraday reversals that whipsaw daily breakout systems. Moderate diversification vs EUR/USD but correlations spike in crises. Structural incompatibility confirmed — same as USD/JPY. Do not pursue.
  > Source: [[2026-06-05 - how do eurjpy and gbpjpy behave under a 20-bar breakout plus ema50 over ema200 t]]

- [x] **B2 — NZD/USD candidacy** ❌ REJECTED 2026-06-05
  > Trend mechanics pass (45-55% bullish regime, 20-60 day legs), BUT: (1) 0.7-0.9 correlation with already-rejected AUD/USD — same trade, (2) forex spot = same FEMA/India-legal execution block as disabled EUR/USD. Two independent reasons. Forex expansion is a dead end — tradeable universe is India-legal only (MCX commodities + crypto).
  > Source: [[2026-06-05 - what are nzdusd trend characteristics for a 20-bar breakout momentum system on d]]

- [x] **B3 — BTC regime flip conditions** ✅ Done 2026-06-05 → [[BTC_USD]]
  > Golden cross is LAGGING confirmation, not predictive trigger — validates "wait for flip" approach. Precedes: accumulation after bear bottom, macro liquidity easing, MVRV recovering from <1.0, NUPL capitulation→hope, exchange netflows turning to outflows, ETF inflows. Crosses appear 12-24mo after halving bottom (2024 halving → 2025-26 expected window). Watch MVRV + netflow as secondary confirmation the flip has real accumulation. Contrarian flag: ETF era may break the 4-year pattern.
  > Source: [[2026-06-05 - what macro and on-chain conditions historically precede a btc ema50 over ema200]]

- [x] **B4 — EMA50 rejection short signal** ❌ REJECTED (Phase 1) 2026-06-05
  > No asset-specific backtest exists. Three blockers: (1) no India-legal short execution path at ₹5-6k (can't short BTC spot/MCX gold easily), (2) same family as already-rejected XAU short (-0.061R) and RSI recovery — counter-trend knife-catching, (3) zero published edge = fails Wilson CI bar by default, unvalidated complexity before core system has one live trade. Park for Phase 2 after 20+ live long trades.
  > Source: [[2026-06-05 - what is the historical performance of an ema50 rejection short entry signal in d]]

---

## Related

- [[CoinDCX Execution Layer]] — A1 findings feed directly into this build
- [[Trading System]] — signals this research expands
- [[What Didn't Work]] — cross-check every B-series finding here before acting
- [[XAU_USD]] — A2 directly unblocks live XAU paper trade execution
