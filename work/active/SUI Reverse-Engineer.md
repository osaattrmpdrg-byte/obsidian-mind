---
date: 2026-06-18
description: "Reverse-engineer a friend's SUI/crypto-futures entries to test (blind) whether his 75%-win-but-net-losing record hides a real entry edge or is pure exit-artifact. Phase 1 harness built; Part 3 (blind prediction) pending."
tags:
  - work-note
  - trading
status: active
quarter: Q2-2026
---

# SUI Reverse-Engineer

> [!abstract] Status (2026-06-18) — Phase 1 data + harness BUILT; Part 3 (blind prediction) pending
> 15 tests green in `D:\trading_system\sui_re\` (local git). The blind set is generated and sealed. Next session: run the blind reads + scoring.

First full application of [[Reverse-Engineer Before Apply]].

## What & Why

A friend (Rakshith) trades SUI futures with a claimed ~85% win rate. The goal mutated as evidence arrived:
1. Started as "clone his method to achieve similar results."
2. His **full 1-year ledger overturned the highlight reel**: ~85 trades, **76% win rate but NET NEGATIVE (~−6 USDT) after fees** — avg win +2.0 / avg loss −5.1, one −67 SUI trade erased a good year, fees (30 USDT) > gross profit (24). Multi-coin (ETH was his only profitable coin), not "SUI only." So *"similar results" = a net loss* → cloning is off the table.
3. **Corrected premise:** does his *entry* hold any real directional edge, or is the high win rate purely an **exit-artifact** (small TPs, held losers)? Built a blind test to settle it.

## The method (grilled 2026-06-17)

Reverse-engineer = **understand → encode → validate**, in sequence. Spec: `docs/superpowers/specs/2026-06-17-sui-reverse-engineer-design.md`.

- **Phase 1 (built):** reconstruct the chart at each of his entries from Binance data → a **blind set** of his wins + losses + random decoys, shuffled & unlabeled, each = truncated multi-timeframe charts + numeric context. **Structural blindness** (no "trust me"): blind artifacts carry no labels; the answer key is sealed separately.
- **Part 3 (next):** I read each item blind, commit a prediction (setup? direction? entry/target/stop?), then unseal the key. Judge = **my read's forward profitability**; diagnostic = win/loss/decoy discrimination. Friend = teacher, market = judge.

## Built so far (`D:\trading_system\sui_re\`, local git)

- **Part 1 — Data foundation:** Binance OHLCV layer, Excel parser, LIFO open→close pairing, direction derivation → `labeled_trades.csv` (85 trades, 47 short / 38 long, validated vs the known 23 Apr short). Plan: `docs/superpowers/plans/2026-06-17-sui-phase1-data-foundation.md`.
- **Part 2 — Blind harness:** indicators, numeric context, decoy sampler, truncated chart renderer (OOM-fixed), blind-set builder. Plan: `docs/superpowers/plans/2026-06-17-sui-phase1-blind-harness.md`.
- **Output:** `blind_run/` = 100 items (50 real incl. all 9 losses + 50 decoys) + sealed answer key.

## Next session

1. **Part 3** — write the predict-loop + scorer plan, run blind reads (decide scale: sample vs full ~100 items / ~400 charts), score → the four-cell verdict.
2. If an entry edge survives: Phase 2 encode → Phase 3 OOS + forward paper, then "incorporate" = **his entry read + our risk management** (de-levered), never his 6× full-account sizing.

## Related

- [[Reverse-Engineer Before Apply]] — the governing protocol this pilots
- [[Trading System]] — where a validated rule would land; hard rules
- [[What Didn't Work]] — the VWAP/S-R mechanical version (no edge) + the survivorship/overfitting traps this guards against
- [[Binding Constraint First]] — the binding constraint here is integrity of the read
