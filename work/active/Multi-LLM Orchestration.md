---
date: 2026-06-16
description: "Parked-but-ready plan for a multi-LLM capability — verified 2026 model landscape, what you already own vs the two genuinely new keepers, and the edge-gated phased build path. Implement on signal."
tags:
  - work-note
status: proposed
quarter: Q2-2026
---

# Multi-LLM Orchestration

> [!info] Status — PARKED, ready to build on signal
> Verified and scoped 2026-06-16. Not started. Implement when Dileep asks. The edge is gated: Phase 1 must prove it before Phase 2 builds it.

## The core finding

The original idea (a Python/OpenRouter orchestrator that routes tasks by model strength) is **~85% a re-implementation of infrastructure already running**: `/research-deep` (multi-provider research), `/panel` + `/council` (the "two agents talking" critic loop), `/ceo` (task routing), Claude Code subagents + Workflow (parallel agents). Building that from scratch adds cost + a dependency for no edge.

**Only two pieces have non-redundant value** — and both require going *outside* Claude Code to get, which is why they're real:

1. **Cross-*model* adversarial diversity.** `/panel`/`/council` spawn *Claude* instances — correlated errors, shared blind spots. A loop where Claude's output is attacked by **Gemini 3.1 Pro + DeepSeek V4** gives *uncorrelated* critique. Real edge on high-stakes calls (a thesis, an agri-capital decision).
2. **A cheap high-volume batch lane.** No frontier-cheap tier exists in the current stack. DeepSeek V4 Flash economics make batch generation/scoring of hundreds of variants trivial — wrong for interactive Claude Code, right for [[Streams|agri-scenario planning]].

## Verified 2026 model landscape (2026-06-16, web-checked)

| Provider | Reality | Routing call |
|---|---|---|
| **Gemini 3.1 Pro** | Real, reasoning-first, 1M context, PDFs | Research / big-context — `[VERIFIED]` |
| **DeepSeek V4 Flash** | $0.14/M in, $0.28/M out; cache hits 1/10; ~18–36× cheaper than frontier | Cheap batch — `[VERIFIED]` |
| **Claude Opus 4.8** | Leads SWE-bench Pro, ahead of GPT-5 | **Coding + synthesis** (NOT Grok) — `[VERIFIED]` |
| **Grok** | Grok 5 not shipped; flagship 4.20 beta; coding model unproven | Realtime/X niche only, and still **unkeyed** ([[grok_api_pending]]) — `[VERIFIED]` |

Corrections to the original plan: route **coding to Claude, not Grok** (biggest factual error); model ID `claude-opus-4-6` → `claude-opus-4-8`; "Grok leads SWE-bench" is false.

## The build path (edge-gated)

- **Phase 0 — substrate (~15 min):** one OpenRouter key + ~$5–10 credit. One key + one ledger across all four providers; fits [[api-usage]] Tier discipline; enables both keepers.
- **Phase 1 — prove each keeper on ONE real task (the edge gate):**
  - *Test A — cross-model critic:* Claude draft → Gemini + DeepSeek "find the flaw." Edge = do they catch what a Claude-only `/panel` structurally couldn't? If they only echo Claude → kill it.
  - *Test B — cheap batch:* ~50 agri-scenario variants via DeepSeek V4 Flash; check quality + cost. Recommended first — ties to [[Streams]], economics already verified.
- **Phase 2 — build only the winner, as a thin addition (not a parallel system):** cross-model critic → a `/panel` variant calling other providers; batch lane → a small standalone script. State the one-sentence edge before writing it.

## Autonomy requirement (2026-06-16)

Dileep's constraint: **the capability must be runnable autonomously, not just interactively.** This decides the run surface via [[Patterns#Automation routing — who drives, what's the token pool|the automation-routing pattern]]:

- **Cheap batch lane (Test B)** → the natural autonomous fit. Build it as a **headless script** invoked by **`/schedule` (cloud cron)** or a GitHub Actions cron — fire-and-forget scenario generation/scoring, results land in the vault. Burns the Agent-SDK pool, not the interactive one.
- **Cross-model critic (Test A)** → mostly on-demand/interactive (you invoke it on a specific decision), but can be wrapped headless for batch critique runs.
- **⛔ NOT Claude Cowork** — it needs the desktop app open, so it can't run truly unattended. Rules it out for the autonomous path.

Implication for Phase 2: design the batch lane as a **standalone, parameterized, headless script from day one** (not an interactive notebook), so `/schedule` or Actions can drive it without a human in the loop.

## Hard guardrails

- **Research / planning only — never the trading signal or money path.** No LLM in the execution pipeline ([[Patterns]], [[Gotchas]]).
- **Cost isolation:** batch/critic calls → cheap tier; reserve Opus for synthesis ([[Claude Subscription Billing]]).

## Related

- [[Streams]] — the agri-scenario batch lane feeds this directly
- [[Patterns]] — Automation routing (who drives, which token pool); model-isolation-by-cost
- [[Claude Subscription Billing]] — token-pool tradeoffs
- [[grok_api_pending]] — Grok lane is aspirational until keyed