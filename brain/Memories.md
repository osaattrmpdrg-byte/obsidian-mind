---
date: 2026-06-05
description: "Index of memory topics — key decisions, patterns, gotchas, people context"
tags:
  - brain
  - index
---

# Memories

Persistent context and knowledge retained across sessions. Each topic lives in its own note — follow the links.

- [[Working With Me]] — **read first, every session** — the standing operating agreement for how to engage with Dileep
- [[Key Decisions]] — architectural and workflow decisions worth recalling
- [[Patterns]] — recurring patterns and conventions discovered across work
- [[Gotchas]] — things that have bitten before and will bite again
- [[People & Context]] — org structure, teams, review history, dynamics
- [[North Star]] — living goals document, read at session start
- [[Vision]] — the life the financial goal serves (health, nature, off-grid, entrepreneurship) — the deeper why
- [[Skills]] — custom slash commands and workflows
- [[Binding Constraint First]] — the right question for any money idea: find the false link in the chain and prove it first
- [[Reverse-Engineer Before Apply]] — standing research protocol: any externally-sourced strategy (web/YouTube/influencer/friend) is a hypothesis until reverse-engineered, mechanized, OOS-backtested, and forward-validated

- [[Trading System]] — proven signals, current instrument status, what's built, pending tasks
- [[What Didn't Work]] — rejected signals and architecture decisions with WHY and learnings
- [[Streams]] — four income streams: job, trading, content, AgriTech — status and next action
- [[GCP Credits Strategy]] — two-assets model (trial bursts vs Always Free), self-sustaining rule, direction
- [[Edge Generalization Sweep]] — designed compute burst: is the breakout edge real + which instruments to trade
- [[Claude Subscription Billing]] — two token pools (interactive vs Agent SDK credit); Pro = $20/mo autonomous, read before designing scheduled/headless work
- [[Defence Career Strategy]] — ⚡ **open trajectory fork**: considering an armed-forces career (Vision-level, not resolved). Read before any North Star / streams advice.

## Recent Context

*(Trimmed 2026-06-18 — full history lives in `thinking/session-logs/`. 2026-06-05/06/12 settled entries on Obsidian MCP setup, Angel One go-live, CoinDCX Phase 1 build, GCP credits, and the original Lockbox build were folded out; see [[Key Decisions]] and [[CoinDCX Execution Layer]] for the durable record.)*

- 2026-06-18: **VIC signup + Gmail MCP wired up.** Researched Value Investing Club before Dileep signed up — it's free (not paid as the friend's pitch implied), 45-day-delayed email tier vs application-gated real-time tier. Data ([dschonholtz scrape](https://github.com/dschonholtz/ValueInvestorsClub)) shows long-idea returns concentrate in the first 1-2 weeks, so the delayed tier has near-zero tradeable edge — signed up anyway for thesis-structure study, not signals. Set up a **Gmail MCP server** (`@gongrzhe/server-gmail-autoauth-mcp`) for `osaattrmpdrg@gmail.com` so future sessions can read VIC emails directly — registered + Connected (`claude mcp list`), tools expected live next session. See [[Key Decisions]] → Vault & Tooling Infrastructure, [[Gotchas]] → Claude Code CLI (PowerShell `--` separator gotcha hit during setup).
- 2026-06-17/18: **Friend's SUI strategy → reverse-engineer project + a new standing principle.** A friend (Rakshith) claimed ~85% win rate on SUI futures; his **full CoinDCX ledger overturned it** — ~85 trades, **76% win but NET NEGATIVE after fees** (avg win +2.0 / avg loss −5.1, one −67 SUI trade erased a good year, fees > gross profit; ETH was his only profitable coin). Coined **[[Reverse-Engineer Before Apply]]** — every externally-sourced strategy (web/YouTube/influencer/friend) is a hypothesis until reverse-engineered from labeled evidence, mechanized, OOS-backtested, forward-validated. Launched [[SUI Reverse-Engineer]] as its first application: Phase-1 **data foundation + blind harness** built (`D:\trading_system\sui_re\`, 15 tests green) — sealed blind set (50 real incl. all 9 losses + 50 decoys). **Next: Part 3 blind prediction + scoring.** Also: **VWAP + volume-S/R strategy REJECTED** (no edge, fails OOS — [[What Didn't Work]]).
- 2026-06-16/17: **Trading thesis re-grounded — BTC is the edge, not FX.** Full validation battery (8 scripts): EUR +0.131R **dies under realistic fills** → KILL current impl; execution path solved (resting −1R SL + at-close trailing, +0.150R); **NSE EUR/USD future untradeable** (~92 lots/day) — legal ≠ liquid; **BTC = strongest edge (+1.686R)**, only blocker is a CoinDCX 400 now confirmed account-side. EUR/USD scanner disabled. New principle: **[[Binding Constraint First]]** — find the false link in the chain and prove it first; wired into [[North Star]] + [[Key Decisions]].
- 2026-06-16: **Telegram brief drift closed.** The deployed brief (`life-os/scripts/brief.py`) was a 3rd, missed copy still saying EUR/USD "DISABLED" for 4 days while the scanner fired live paper trades. Fixed the stale block + added `_active_scanner_pairs()` so the brief **parses scanner.py's `PAIRS` live**, closing the silent-drift class for good. See [[Gotchas#Daily brief status drift (two/three sources of truth)]].
- 2026-06-15: **⚡ Trajectory fork open: considering an armed-forces career.** [[Defence Career Strategy]] is a [[Vision]]-level decision that would deprioritize ₹7-8L-by-27 as primary; the automated trading system is the one stream that survives a service life. **Next: eye exam + a [[panel]] on the "why defence" core assumption.** Status: CONSIDERING, not resolved.
- 2026-06-15: **Standing efficiency mandate + tool authority granted** ([[Working With Me#Efficiency mandate standing — Dileep 2026-06-15|Working With Me]]). Claude may pick the best tool/skill/research method by its own judgment; optimize efficiency AND quality, never trade off; be brutally honest about better external tools even against self-interest.
- 2026-06-14: **Multi-agent stance corrected + working-style captured.** Real axis is *interactive multi-agent (adopt, ≈free, decision-quality)* vs *autonomous swarm (skip on Pro)* — independence/diverse-lenses is the make-or-break, not multi-agent yes/no. "How Dileep engages" captured in [[Key Decisions]] — probes distinctions not conclusions, active co-investigator, reflective/meta, system-over-flash.
- 2026-06-13: **Claude billing constraint logged** ([[Claude Subscription Billing]]) — interactive quota and the Agent SDK credit (`claude -p`, `/schedule`, GitHub Actions) are *separate* pools; idle interactive quota can't feed overnight agents. Pro = $20/mo Agent SDK credit (~3–4 agentic experiments).
