---
date: 2026-06-05
description: "Central map of all work notes — active projects, completed work by quarter, decisions log"
tags:
  - index
  - moc
---

# Work Notes

Central map of content. All work notes and decisions link back here. For quick navigation, use [[Home]] or open `bases/Work Dashboard.base`.

**Folder structure**: `active/` = current projects, `archive/` = completed (by year), `incidents/` = incident docs, `1-1/` = meetings.

## Incidents

Incident docs live in `work/incidents/`. See `Incidents.base` for overview.

-

## Active Projects

- **Telegram Trading Bot** — Approval + validation + execution layer for XAU/USD live trading. Bot built (`D:/trading_system/bot/`). Angel One account created — next: SmartAPI key + segments, Perplexity key in trading .env, Cloud Run deploy. See [[Trading System]].
- **[[CoinDCX Execution Layer]]** — One-tap BTC/USDT REST API trade placement. **Phase 1 client built + tested (TDD, 13 green) 2026-06-06.** Next: user generates API key → smoke test → Phase 2 Telegram wiring.
- **[[Edge Generalization Sweep]]** — GCP-credit compute burst: does the breakout edge generalize (max-breadth, Hybrid methodology) + go-live shortlist. Design approved; build paused at design-review. See [[GCP Credits Strategy]].
- **[[Trading Research Queue]]** — A1-A3 done, B1-B4 done. All research complete: build gaps filled, forex dead-ends closed, EUR/USD reopened.
- **[[FEMA Forex Legality]]** — EUR/USD legality VERIFIED + GO + **EXECUTED 2026-06-12**: scanner re-enabled, NSE sizing on alerts, brief memory fixed. Remaining: currency segment activation (user) → paper → live.
- **[[Daily Watch Weekly Hunt]]** — strategy-discovery system: daily monitor the proven edge + weekly disciplined candidate vetting. **Lockbox + trial-count registry BUILT 2026-06-12** (TDD, 18 green, `D:\trading_system\hunt\`). Remaining: cross-instrument harness, Daily Watch brief format + cadence.

## Review Prep

-

## Recently Completed

-

## Completed

### Current Quarter
-

### Previous Quarters
-

## Reference

### Trading System
- [[Trading System]] — proven signals, current status, pending build tasks
- [[What Didn't Work]] — rejected signals with patterns and learnings
- [[Streams]] — four income streams toward early retirement
- [[FEMA Forex Legality]] — EUR/USD legal via NSE; offshore brokers illegal
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

## Open Questions

-

## Archive

-
