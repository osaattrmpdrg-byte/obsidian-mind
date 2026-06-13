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

## Queued — money-path adopt (C3, supervised only)

- **Model isolation in the trading bot:** when the bot moves to continuous cron operation, route cron/monitor tasks to Sonnet and keep interactive/decision steps on Opus. Surfaces when scaling the bot; do it in a supervised session — touches `D:\trading_system`. Tracked in [[AI Tooling Workflow Patterns#Vault-adoption roadmap B4 C1 mapping|the adoption roadmap]].
