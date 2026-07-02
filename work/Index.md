---
date: 2026-06-05
description: "Central map of all work notes — active projects, completed work by quarter, decisions log"
tags:
  - index
  - moc
---

# Work Notes

Central map of content. All work notes and decisions link back here. For quick navigation, use [[Home]], the [[Work Board]] kanban, or `bases/Work Dashboard.base`.

**Folder structure**: `active/` = current projects, `archive/` = completed (by year), `incidents/` = incident docs, `1-1/` = meetings.

## Incidents

Incident docs live in `work/incidents/`. See `Incidents.base` for overview.

-

## Active Projects

- **[[Telegram Trading Bot]]** — Approval + validation + execution layer for XAU/USD live trading. Bot built (`D:/trading_system/bot/`). Angel One account created — next: SmartAPI key + segments, Perplexity key in trading .env, Cloud Run deploy. See [[Trading System]].
- **[[CoinDCX Execution Layer]]** — BTC/USDT live execution layer. **Phase 2 complete (2026-07-01): full SL/TP bracket automation, CoinDCX order polling in monitor, 38 tests green.** Panel-reviewed, all fatals fixed. Next: push `life-os` 3 commits to origin/main when deploying.
- **[[Agentic Trading Stack (Tauric + Paperclip + ODP)]]** — 3-layer agentic research stack (TauricResearch/TradingAgents signals, Paperclip orchestration, OpenBB ODP data), paper-only, separate repo (`D:\agentic-trading-stack`) from the live system. **Stage 1 built + live-verified; gate clock restarted 2026-06-29** after discovering the task never fired in its first 4 days (machine asleep at 6am — fixed with WakeToRun). Weekly check: `python review_health.py`. Paperclip (Stage 2) only after the gate clears.
- **[[Daily Watch Weekly Hunt]]** — strategy-discovery system: daily monitor the proven edge + weekly disciplined candidate vetting. **Fully operational (2026-07-02)**: Daily Watch brief + cadence live via GitHub Actions (07:00/18:00 IST). Gauntlet complete: lockbox + registry + cross-instrument harness built + tested (30 green, commit `9d270b7`). Next: first Hunt candidate from Research Queue.
- **[[Defence Career Strategy]]** — ⚡ **major trajectory fork (2026-06-15):** considering an armed-forces career (NCC Special Entry / Navy SSC Exec / AFCAT Flying primary). [[Vision]]-level decision; the income path becomes the no-pension backbone if it proceeds. **Next: eye exam (first gate) + a [[panel]] on the "why defence" core assumption.** Status: considering, not resolved.
- **[[AFCAT 2026 Prep Plan]]** — 7-week written exam prep (AFCAT 2/2026, exam 8 Aug 2026). Cold diagnostic not yet taken as of 2026-06-29. **Next: Cold Diagnostic Test 1 before any further prep.** Due 2026-07-02.
- **[[Multi-LLM Orchestration]]** — 🅿️ **PARKED, ready (2026-06-16):** verified you already own ~85% (`/research-deep`, `/panel`, `/council`, subagents). Only two keepers: cross-*model* critic diversity + a cheap DeepSeek-V4 batch lane for agri-scenario planning. Edge-gated phased plan written; build on signal.
- **[[Content Niche]]** — Stream 3 niche hypothesis (2026-06-14): AI-engineering build-in-public with the real-money trading system as proof (Framing C, "not trading-advice"). First artifact drafted ([[2026-06-13-lockbox-post-draft]]); 8-piece calendar. Blocked on: confirm the constraint revision → publish piece #1. Spawned from [[AI Tooling Workflow Patterns]] research.
- **[[SUI Reverse-Engineer]]** — ✅ **RESOLVED 2026-06-29**: no real entry edge found (rigorous permutation test refuted the initial timing-hypothesis). 16 tests green. Status: completed, thread closed. See work note for full result.
- **[[Cognify-Lite]]** — free SessionEnd capture hook, built instead of installing cognee ($3-30/mo, no caching). **Phase 1 shipped 2026-06-29** (suggest-only, 85 tests green). Phase 2 (auto-apply) designed but deliberately paused until Phase 1 has real-session signal.
- **[[RTK-Lite]]** — free Bash output-compression hook, built instead of trusting RTK's third-party binary (Defender flagged it 6x). **Shipped 2026-06-30**, default-off, opt-in per session via a SessionStart prompt.
- **[[Date Ideas App]]** — couples date-idea decision app for India (Bangalore v1). Stack locked (Next.js + Supabase + Vercel). Full plan at `C:\Users\drajg\.claude\plans\merry-snacking-marble.md`. **Blocked on manual setup**: Supabase project + Google Places API key + Vercel account. Resume with "let's build" once done.

## Review Prep

-

## Recently Completed

-

## Completed

### Current Quarter
- [[Edge Generalization Sweep]] — 56-instrument sweep, 0/56 passed, write-up done (archived 2026-07-01)
- [[Trading Research Queue]] — A1-A3, B1-B4 all done; build gaps filled, forex dead-ends closed
- [[FEMA Forex Legality]] — killed 2026-06-16, NSE EUR/USD illiquid
- [[Panel - Why Defence (2026-06-22)]] — verdict delivered, feeds [[Defence Career Strategy]]

### Previous Quarters
-

## Reference

### Visibility
- [[Work Board]] — kanban, glance-only state (Active/Stale/Blocked/Done, domain by tag color)
- `bases/Work Dashboard.base` — sortable table, staleness + `next_step` detail

### Trading System
- [[Trading System]] — proven signals, current status, pending build tasks
- [[What Didn't Work]] — rejected signals with patterns and learnings
- [[Streams]] — four income streams toward early retirement
- [[FEMA Forex Legality]] — EUR/USD legal via NSE but **killed 2026-06-16** (illiquid); offshore brokers illegal
- [[Chief Analyst]] — disruptor opportunity identification framework
- [[Tech Watch]] — technology intelligence
- [[Geopolitics]] — macro context layer
- [[Health]] | [[Spirit]] — supporting domains

### Instruments
- [[BTC_USD]] | [[XAU_USD]] | [[ETH_USD]]

### Trading Journal
- [[trade-log]] | [[trade-stats]] | [[dashboard|Trading Dashboard]]
- [[Signal Matrix]] — confidence matrix for live signal decisions

## Decisions Log

| Date | Decision | Status | Link |
|------|----------|--------|------|
| 2026-06-05 | Angel One SmartAPI over Zerodha Kite Connect for MCX (free vs ₹2k/mo) | Accepted | [[XAU_USD]] |
| 2026-06-05 | EUR/USD GO via NSE futures — legal verified, CA waived at current scale | Accepted | [[FEMA Forex Legality]] |
| 2026-06-05 | Forex pair expansion closed (EUR/JPY, GBP/JPY, NZD/USD rejected) | Accepted | [[What Didn't Work]] |
| 2026-06-05 | EMA50 rejection short deferred to Phase 2 (no edge, no India-legal short) | Accepted | [[Trading Research Queue]] |
| 2026-06-06 | GCP credits = trial-bursts + Always-Free-persistent; spend on edge-discovery, not hosting | Accepted | [[GCP Credits Strategy]] |
| 2026-06-06 | Edge Generalization Sweep — Hybrid methodology, max-breadth, correlation-aware | Accepted | [[Edge Generalization Sweep]] |
| 2026-06-05 | "Daily Watch, Weekly Hunt" over a daily strategy generator (anti curve-fitting) | Accepted | [[Daily Watch Weekly Hunt]] |
| 2026-06-05 | CoinGecko MCP added; CoinDCX MCP rejected (duplicates self-built client) | Accepted | [[Daily Watch Weekly Hunt]] |
| 2026-06-17 | Reverse-Engineer Before Apply — all externally-sourced strategies are hypotheses until reverse-engineered + validated | Accepted | [[Reverse-Engineer Before Apply]] |
| 2026-06-17 | VWAP + volume-S/R strategy REJECTED — no edge on BTC/stocks/currencies, fails OOS | Accepted | [[What Didn't Work]] |
| 2026-06-29 | Built free cognify-lite (Gemini free tier) instead of installing cognee (est. $3-30/mo, no caching, opaque graph DB) | Accepted | [[Cognify-Lite]] |

## Open Questions

- **Wire a general-purpose Gemini agent** (2026-06-24) — Gemini API key already active (free tier, in `obsidian-second-brain/.env`) but only reachable via `/notebooklm`, which is hardcoded to vault-grounded File Search. Need a small new script/skill for open-ended Gemini reasoning (e.g. second-opinion review, same role a Claude subagent played for [[Agentic Trading Stack (Tauric + Paperclip + ODP)]]'s ODP↔Tauric wiring decision). Deferred until the trading-stack plan is done.

## Archive

-
