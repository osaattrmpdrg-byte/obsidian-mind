---
date: 2026-06-05
description: "Recurring patterns and conventions discovered across work — architecture, naming, tooling, and implementation patterns"
tags:
  - brain
---

# Patterns

Recurring patterns discovered across work.

## Convergent agent-OS patterns (validated 2026-06-13)

Cross-validated across four independent practitioners (Max Mitcham, Vin, Sajal Sharma, Context Studios) in the [[AI Tooling Workflow Patterns]] deep-dive. Most confirm rules this vault already follows — adopt/reinforce, don't rebuild.

- **Deterministic code for critical state, never the LLM.** Read/unread flags, dedup, signal logic, money decisions → plain code. Independently learned the hard way by Sajal ("some logic just needs to be deterministic code"); already this vault's rule as [[Trading System|"no LLM in the signal pipeline"]]. **Reinforced.**
- **Memory tiering + aggressive pruning.** Identity/long-term/raw-daily as separate layers; "daily files are cheap, the curated index is precious — prune aggressively" (Context Studios). Apply to [[Memories]] + `MEMORY.md`: keep the index lean, prune stale Recent Context entries.
- **Silent-unless-needed monitoring.** Batched heartbeat checks that message only on signal, stay quiet otherwise. Already the design of the [[Tooling Intelligence Scan — Design|tooling scan]] and the Telegram brief. **Confirmed direction.**
- **Model isolation by cost.** Sonnet for autonomous/cron, Opus for interactive — matches the [[Claude Subscription Billing|Pro $20 Agent SDK ceiling]]. Default autonomous work to the cheaper model.
- **`confidence:` frontmatter convention** on synthesis notes — formalizes the existing `[VERIFIED]`/`[HYPOTHESIS]` tags into a queryable property.
- **Start minimal, earn complexity.** Every source's contrarian warns against heavy stacks (OpenClaw/Hermes) before a workflow needs them — the [[North Star|Edge Before Action]] rule. The ROI gut-check: *"is the setup time worth the payoff?"*

## Gotcha — agent supply-chain & permission risk

(security pattern from Context Studios) Broad-permission agents (shell/browser) can touch files unintentionally; third-party skills/MCP servers are a supply-chain risk ("a malicious skill could contain harmful tool definitions"). **Vet skills before installing; use tool + user allowlists; never give an agent the money path unsupervised.** Reinforces the [[Claude Subscription Billing|cloud-sandbox-gets-research-keys-only]] boundary.

## Git flow — SETTLED, do not re-litigate (2026-06-16)

Dileep's explicit instruction: the git flow across the three repos is **fixed — stop proposing changes to it each session.** Claude follows it silently; never reconfigure, never re-pitch.

- **`D:\trading_system`** — LOCAL git repo, **no remote** (by design). Commit trading scripts/analysis here locally so they can't vanish (the [[Gotchas#Backtest reproducibility & live-exit divergence|"recovered script was never under git"]] lesson). No push — there's nothing to push to.
- **`/d/life-os`** (GitHub `osaattrmpdrg-byte/life-os`) — has the remote; the **live GitHub Actions monitor deploys from `origin/main`**. Push here only when deploying, with explicit OK.
- **Vault** (`d:\projectsobsidian-mind`) — git-tracked; **Dileep handles sync**. Make note edits, leave them uncommitted unless asked to commit.
- **Never read `.env` files** in any repo — secrets live there. Verify commit health with local `git log` only (no auth, no credential exposure). A `gho_…` token leaked to a log once ([[Gotchas]]) — that class of mistake is why this rule is hard.

**Why:** repeatedly re-deciding the git setup wastes the session and risks touching credentials. It works; leave it.

## Queued — money-path adopt (C3, supervised only)

- **Model isolation in the trading bot:** when the bot moves to continuous cron operation, route cron/monitor tasks to Sonnet and keep interactive/decision steps on Opus. Surfaces when scaling the bot; do it in a supervised session — touches `D:\trading_system`. Tracked in [[AI Tooling Workflow Patterns#Vault-adoption roadmap B4 C1 mapping|the adoption roadmap]].

## Automation routing — who drives, what's the token pool (2026-06-16)

Three ways to run agentic/automated work. The decision axis is **two questions: how much do I sit in the loop, and which token pool does it burn.** Don't reach for the shiny one — match the task to the surface.

| Surface | Autonomy | Runs when machine off? | Token pool | Best for |
|---|---|---|---|---|
| **GitHub Actions** (live monitor) | None — fixed deterministic script | Yes (cloud cron) | None (own infra) | 24/7 monitoring, money-path heartbeat. The life-os deploy. |
| **`/schedule` cloud agents** | Agentic, headless, recurring | Yes (cloud) | Agent SDK ceiling ([[Claude Subscription Billing]]) | Scheduled agentic work — research sweeps on a cron, weekly synthesis. |
| **Claude Cowork** | Agentic, **attended-but-async** — kick off, walk away, course-correct mid-stream | **No** — desktop app must stay open | **Interactive Pro pool** (competes with hands-on Claude Code) | One-off exploratory multi-step tasks too messy for a cron, too long to babysit: vault reorgs, refactors on `D:\trading_system`. |

**The trap:** Cowork's marketing ("autonomous cloud agent") implies it replaces a 24/7 monitor. It does not — the desktop-open requirement rules out anything headless, and it eats the *interactive* pool, not the isolated Agent-SDK budget. For Dileep on Pro, that's the binding constraint.

**Rule:** truly headless / 24-7 → GitHub Actions or `/schedule`. Attended-but-async exploration → Cowork. Never route the trading live-monitor to Cowork.

**Why:** without this written down, the Cowork-vs-`/schedule` distinction gets re-derived every time a new "autonomous agent" feature ships, and the token-pool tradeoff ([[Claude Subscription Billing]]) gets forgotten until a Pro allocation runs dry mid-session.
