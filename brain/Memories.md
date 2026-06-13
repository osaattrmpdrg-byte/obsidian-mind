---
date: 2026-06-05
description: "Index of memory topics — key decisions, patterns, gotchas, people context"
tags:
  - brain
  - index
---

# Memories

Persistent context and knowledge retained across sessions. Each topic lives in its own note — follow the links.

- [[Key Decisions]] — architectural and workflow decisions worth recalling
- [[Patterns]] — recurring patterns and conventions discovered across work
- [[Gotchas]] — things that have bitten before and will bite again
- [[People & Context]] — org structure, teams, review history, dynamics
- [[North Star]] — living goals document, read at session start
- [[Vision]] — the life the financial goal serves (health, nature, off-grid, entrepreneurship) — the deeper why
- [[Skills]] — custom slash commands and workflows

- [[Trading System]] — proven signals, current instrument status, what's built, pending tasks
- [[What Didn't Work]] — rejected signals and architecture decisions with WHY and learnings
- [[Streams]] — four income streams: job, trading, content, AgriTech — status and next action
- [[GCP Credits Strategy]] — two-assets model (trial bursts vs Always Free), self-sustaining rule, direction
- [[Edge Generalization Sweep]] — designed compute burst: is the breakout edge real + which instruments to trade

## Recent Context

- 2026-06-05: Migrated life-os vault into obsidian-mind. Brain layer populated with trading context, goals, and stream tracking.
- 2026-06-05: Obsidian MCP wired up — Local REST API plugin v4.1.3 with built-in MCP, configured in `.mcp.json`. Certificate trusted in Windows CA store. See [[Key Decisions]] → Vault & Tooling Infrastructure.
- 2026-06-05: Trading research complete (A1-A3, B1-B4 via Perplexity Sonar). Key outcomes: Angel One SmartAPI chosen (free), position sizing rules set (1-2% at ₹5-6k), all forex pair expansion rejected, BTC golden cross is lagging confirmation, EMA50 short deferred. See [[Trading Research Queue]].
- 2026-06-05: **EUR/USD reopened** — "FEMA grey area" was a misunderstanding. EUR/USD is legal via NSE exchange-traded futures (SEBI 2016 circular, verified). Offshore brokers are the illegal part, not the pair. Marked GO. See [[FEMA Forex Legality]].
- 2026-06-05: Session capture now obsidian-mind-native — `/log-session` skill rewritten (writes `thinking/session-logs/`, updates Memories, routes to brain notes, no git auto-push), Stop hook points at it. See [[Key Decisions]] → Session Workflow.
- 2026-06-06: `/scout` audit (418 skills) + installed `indian-trading-skills` (10 NSE/F&O skills) and `skill-algotrader` (reference only). Added **CoinGecko MCP** to `.mcp.json` (free/keyless, activates on restart); rejected CoinDCX MCP. See [[Key Decisions]] → Vault & Tooling.
- 2026-06-06: Designed [[Daily Watch Weekly Hunt]] via grill-me — daily monitor the proven edge + weekly disciplined candidate vetting (lockbox + cross-instrument + trial-count penalty). Killed the naive "daily strategy generator" as a curve-fitting machine.
- 2026-06-06: Angel One **live** — login verified (`test_angel_login.py`), MCX (`mcx_fo`) + currency (`cde_fo`) segments both active. SmartAPI gotchas logged ([[Gotchas]]).
- 2026-06-06: **Plan of action approved** — paper test first (5-6 trade gate = pipeline validation, not edge), then calibrate → small live (EUR/USD first). 4-phase roadmap in [[Trading System#Path to Live (approved 2026-06-06 — prune after execution)|Trading System → Path to Live]]. Implementation plan written for Phase 1 (paper-trade logging). Prune the roadmap once executed.
- 2026-06-06: **CoinDCX execution layer built** (Phase 1) — `D:\crypto_trading\coindcx_client.py` + 13 offline tests (all green) + `smoke_coindcx.py` + `.env.example`, TDD. HMAC-SHA256 signs exact bytes (guards the 401 bug); dynamic min-size enforced before every order. Awaiting user: generate API key → run smoke → then Phase 2 Telegram wiring. See [[CoinDCX Execution Layer]].
- 2026-06-06: **GCP credits strategy set** — two-assets model (trial bursts vs Always Free, self-sustaining rule). Direction: edge-discovery bursts to unblock stuck streams. Designed [[Edge Generalization Sweep]] (max breadth + Hybrid methodology) — build paused at design-review. See [[GCP Credits Strategy]].
- 2026-06-06: Wrote [[The Story So Far]] — plain-language journey record for the user. Added [[Vision]] from Dileep's own "Vision for the Future" doc: the ₹7-8L goal is the *means*; the end is a balanced life (health, connection to nature, off-grid sustainable farming, entrepreneurship, creativity). **Stream 4 / AgriTech is the emotional core of the vision, not just an income stream.** Money decisions filter through the life, not just the number.
- 2026-06-12: **EUR/USD re-enabled in the live scanner** — root cause of the brief saying "scanner disabled" was a 3-way drift (stale brief-memory, dev scanner commented out, prod repo on old code). Re-enabled in `scanner.py` with an NSE EUR/USD futures sizing block on alerts; USD/CAD stays dead. Fixed a real bug along the way — `callback_data` 2-dp precision collapsed FX prices ([[Gotchas]]). Synced dev→life-os, committed + pushed (deploys tonight's 22:30 UTC Actions run). See [[FEMA Forex Legality]] decision log (EXECUTED).
- 2026-06-12: **Lockbox + trial-count registry built** (`D:\trading_system\hunt\`) — the Weekly Hunt's anti-curve-fitting enforcement. Held-out slice from 2024-01-01; one lockbox shot per candidate (6/yr cap); rationale required at registration; Bonferroni-raised Wilson bar as N grows; weak train results auto-reject and still count toward N. TDD, 18 tests green, `/plan` first. See [[Daily Watch Weekly Hunt]].
- 2026-06-12: **Both execution rails verified live.** Angel One: re-ran `test_angel_login.py` — MCX + currency segments both active, **existing key works, no new key needed**. CoinDCX: `smoke_coindcx.py` all green (auth/HMAC accepted, BTCUSDT min 1e-05, below-min guard) — funded (~0.00027 BTC, 0.031 ETH, 1.14 USDT). Added limit-order support to the client (`price_per_unit`, TDD, 16 tests) for zero-fill-risk order/cancel testing. **Pending (user back in ~2h): place the unfillable test limit buy → confirm in app → cancel via API** — closes the CoinDCX Phase 1 checklist. See [[CoinDCX Execution Layer]].
- 2026-06-12: End-to-end bot test passed — test signal → keyboard → Validate tap → circuit breakers → Perplexity → verdict. Returned **NO GO** on a fake $2,680 gold price (real ~$4,678) = validation working as designed. Perplexity key already set, Layer 2 live. **Standing reminder logged** (vault + brief memory): wire live order placement in `bot/execution.py` when the paper gate hits 5-6 trades.
