---
date: 2026-06-13
description: "How Claude usage is billed on Dileep's Pro plan — two separate token pools (interactive vs Agent SDK credit) and what that means for automation spend decisions. Read before designing any autonomous/scheduled Claude work."
tags:
  - brain
  - reference
aliases:
  - Token Budget
  - Agent SDK Credit
---

# Claude Subscription Billing

> [!important] Read this before designing any autonomous, scheduled, or headless Claude work
> The two pools below are **separate**. Idle interactive quota cannot be redirected to autonomous agents — it just expires. Plan token spend accordingly.

## The two pools (as of 2026-06-15)

[VERIFIED 2026-06-13 — [Claude Agent SDK with your plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan), [Claude Code Pricing 2026](https://www.morphllm.com/claude-code-pricing)]

1. **Interactive quota** — the 5-hour rolling session limits. Covers interactive Claude Code, Claude Cowork, and claude.ai chat. **Reserved for interactive use** — autonomous agents cannot draw from it. Unused = expires. (Reduced weekdays 5–11 AM PT.)
2. **Agent SDK credit** — a *separate monthly* allowance for all **non-interactive** usage: `claude -p` headless runs, Agent SDK projects, scheduled/cloud routines (`/schedule`), and GitHub Actions that authenticate with the subscription.
   - **Pro = $20/mo · Max 5x = $100/mo · Max 20x = $200/mo.**
   - **Does not roll over** — unused, it expires every month.
   - When exhausted: usage **stops**, unless overflow to API rates is explicitly enabled (off by default → safe failure mode is "stops," not "surprise bill").

**Dileep is on Pro → $20/month Agent SDK credit.**

## What this means for spend decisions

- **The "recycle idle overnight tokens" idea does not work.** Interactive quota that goes unused overnight cannot feed an overnight agent. The genuinely use-it-or-lose-it autonomous budget is the **$20 Agent SDK credit**, not the interactive pool.
- **$20/mo ≈ 3–4 agentic experiments.** A clone→install→try→report agentic run costs ~$5–8 on Opus / ~$2–5 on Sonnet (API-equivalent rates the credit is denominated in). So nightly autonomous agentic work is **not affordable on Pro**.
- **Route work to the cheapest rail that does the job:**
  - Heavy autonomous experiments → interactive, daytime, you-present (draws the abundant interactive pool, which is otherwise reserved/wasted anyway).
  - Cheap autonomous fetch/synthesis → GitHub Actions + Groq/Perplexity keys, which **do not touch the Claude Agent SDK credit at all** (separate API keys). This is how [[Tooling Intelligence Scan — Design|the tooling scan]] and the `brief.py` rail stay near-free.
- **If/when upgrading to Max**, the overnight-autonomous-agent patterns (e.g. the deferred Phase 2 cloud experiment layer) become affordable — revisit then.

## Claude Code on the web — which pool? [VERIFIED 2026-06-14]

**Claude Code on the web draws from the interactive session + weekly limits — NOT the $20 Agent SDK credit.** All Claude surfaces (claude.ai chat, desktop, Claude Code on web) share one interactive budget. The June 15 2026 Agent SDK split applies only to *programmatic* non-interactive use (Agent SDK, `claude -p`, GitHub Actions, third-party apps); human-in-the-loop Claude Code is explicitly unaffected.

[VERIFIED 2026-06-14 — corroborated across [ccforeveryone.com (Jun 2026)](https://ccforeveryone.com/guides/claude-code-limits-and-pricing) ("Typing into Claude Code in your terminal is unaffected"; all surfaces share one budget) and [morphllm Claude Code usage limits](https://www.morphllm.com/claude-code-usage-limits) (Pro/Max usage is one pool across chat + Claude Code).]

**Implication:** CC-on-web is effectively *free within the Pro interactive quota you already pay for and otherwise waste* — the right rail for offloading mechanical `trading_system` chores (test scaffolding, refactors, doc passes). It is NOT charged to the scarce $20 autonomous credit. The only real ceiling is the shared 5-hour/weekly session cap (doubled May 6 2026), which competes with your interactive chat/CLI time, not your money.

> [!note] Optional sanity check
> Not required (verified above), but if you ever want to confirm on your own account: kick off one web task, then watch whether your 5-hour session usage moves (it should) rather than any separate credit. Pure confirmation, not a blocker.

## Related

- [[api-decision-framework]] — the spend-vs-vault governing rule; this note is the subscription-side constraint that sits underneath it
- [[GCP Credits Strategy]] — sibling "don't build a cost cliff" thinking for GCP credits
- [[North Star]] — Edge Before Action; this constraint is why the tooling scan dropped its autonomous experiment layer