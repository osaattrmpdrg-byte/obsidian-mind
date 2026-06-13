---
date: 2026-06-13
description: Design for an autonomous AI-tooling intelligence scan — a daily, deduped scan of how people use Claude/OpenClaw/Obsidian/AI tooling, delivered to a dedicated Telegram channel + vault. Gives Tech Watch a heartbeat. Scoped to Claude Pro economics.
tags:
  - work-note
  - thinking
  - automation
status: proposed
quarter: Q2-2026
aliases:
  - Tooling Intelligence Scan
  - Tooling Intelligence Scan — Design
---

# Tooling Intelligence Scan — Design

Designed in a `/grill-me` session on 2026-06-12/13. Gives [[Tech Watch]] a heartbeat: automates the AI & LLMs domain it already defines as highest-priority, focused on the AI-tooling slice (Claude Code, OpenClaw, Obsidian, MCP, agent patterns).

## The edge (one sentence)

A daily deduped scan of how practitioners are actually using AI tools surfaces — at near-zero cost — the specific workflow/tool changes that would speed up Dileep's active build work, so awareness arrives as a short morning verdict instead of being something he has to remember to go looking for.

## Purpose (in priority order)

1. **Primary — sharpen Dileep's own build workflow.** Findings must name an active project or standing workflow they would speed up ([[CoinDCX Execution Layer]], the Hunt harness, vault automation, research pipeline) and end in a verdict: *try / queue / ignore*.
2. **Secondary — awareness.** Anything that can't be tied to active work is demoted to an FYI awareness line, kept but not acted on.

Scope is AI tooling itself — Claude Code features, OpenClaw setups, Obsidian plugins/workflows, MCP servers, agent patterns — whatever HN/Reddit/arXiv is buzzing about. Not trade-setup-only.

## The cost finding that shaped this design

> [!important] Why there is no autonomous experiment layer
> [VERIFIED 2026-06-13] As of **June 15, 2026** Claude splits usage into two pools:
> 1. **Interactive quota** (5-hour session limits) — reserved for interactive use; autonomous agents cannot draw from it. The "idle overnight tokens" idea does not work — that quota simply expires.
> 2. **Agent SDK credit** — a separate monthly allowance for `claude -p`, scheduled cloud agents, and GitHub Actions authenticated with the subscription. **Pro = $20/month, does not roll over.**
>
> On Pro, a single agentic experiment (clone → install → try → report) costs ~$5–8 on Opus / ~$2–5 on Sonnet. $20/month buys **~3–4 experiments**, not nightly runs. So an autonomous overnight experiment agent is **not affordable on Pro** and is deliberately out of scope. Sources: [Claude Agent SDK with your plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan), [Claude Code Pricing 2026](https://www.morphllm.com/claude-code-pricing).

The economically rational split on Pro:

- **Autonomous = the cheap scan only.** It runs on the Perplexity/Groq + GitHub Actions rail (Dileep's proven `brief.py` rail), which uses **separate API keys, not the Claude Agent SDK credit** — so it costs Perplexity pennies (~₹10–40/month) and leaves the $20 credit untouched.
- **Experiments = interactive, daytime, you-present.** When a digest item earns "try," Dileep runs `/prototype` in a normal session, drawing the abundant *interactive* pool. This is also the safety boundary we want — experiments fed by scraped content never run unsupervised against a credentialed machine.

This is [[North Star|Edge Before Action]] enforced by the budget: prove the awareness edge cheaply; add the autonomous experiment layer only if/when a Max plan makes it affordable.

## What already exists (reuse, don't rebuild)

| Asset | Location | Role here |
|---|---|---|
| GitHub Actions cron rail | `life-os` repo (`github.com/osaattrmpdrg-byte/life-os`), `.github/workflows/*.yml` | Proven autonomous, machine-off rail. Runs `scripts/brief.py` on cron. |
| Telegram bot | `@DileepLifeOSBot` + Groq synthesis | Delivery. A **new chat_id** (dedicated channel) keeps tooling noise out of the trading approval bot. |
| Brief tech section | `scripts/brief.py` already emits "📱 TECH — TOP 3" | The awareness layer is half-built; this deepens and dedups it into its own stream. |
| Free research sources | HN (Algolia API), Reddit (JSON API), arXiv — all keyless | Primary scan sources per [[api-decision-framework]]. |
| Perplexity | `PERPLEXITY_API_KEY` | Gap-fill only — when free sources are thin on a topic. |

## Architecture — one rail

```
DAILY (cron, GitHub Actions on life-os, machine-off)
  scan: free HN/Reddit/arXiv for AI-tooling chatter
        → Perplexity gap-fill ONLY when free sources are thin
  dedup: drop anything already in tooling_seen.json (the "seen" ledger)
  classify each NEW item via the A-filter:
        which active project/workflow would it speed up?  → verdict: try | queue | ignore
  synthesize digest (Groq, already wired)
  deliver:
        → dedicated Telegram channel (new chat_id) — ONLY if there is new try/queue signal (else silent)
        → vault note committed to obsidian-mind: reference/research/tooling/YYYY-MM-DD <topic>.md
  commit updated tooling_seen.json back to life-os
```

Everything runs on the existing rail. No cloud agents, no new infrastructure class. `CronCreate`/`/schedule` cloud routines are **not** used — they would draw the scarce $20 Agent SDK credit; GitHub Actions on the Perplexity/Groq keys does not.

## Cadence — daily, deduped, self-throttling

Daily runs give fast awareness of new tools. The **seen-ledger dedup** is what makes daily frequency safe: each digest contains only items not surfaced before, so the same tool never re-appears morning after morning. When a day produces no new try/queue-worthy item, **no Telegram ping fires** — the system goes quiet on slow days instead of manufacturing noise. Cost stays at pennies because most days are served by free sources; Perplexity is touched only to fill genuine gaps.

## The A-filter (what makes an item "try"-worthy)

An item earns a "try" verdict only if it can name a specific active project or standing workflow it would speed up. Generic "people like tool X" with no attachment point → demoted to an awareness FYI line. This is the falsifiable gate: every actionable finding must state its payoff. Max one "try" highlighted per digest — the rest queue.

## Delivery

- **Vault note per run with new signal:** `reference/research/tooling/YYYY-MM-DD <topic>.md`, AI-first format (`## For future Claude` preamble, `ai-first: true`, sources verbatim, wikilinks to affected work notes / [[Tech Watch]]). Git-tracked evidence that compounds.
- **Telegram one-liner** to a **dedicated channel** (new chat_id, same `@DileepLifeOSBot`, NOT the trading approval bot): e.g. `Tooling scan: <tool> — try (speeds up <project>). Details in vault.` Silent on no-new-signal days.
- A "rejected tooling" section in the vault notes compounds like [[What Didn't Work]] — combined with the seen-ledger, no tool gets evaluated twice.

## Experiments (no autonomous layer — interactive only)

When a digest "try" item is compelling, Dileep runs it through `/prototype` in an interactive session: throwaway clone, try the tool against a copy, decide adopt/skip. Hard rule: never touches `D:\trading_system`, `D:\crypto_trading`, or exchange keys — the *"no LLM in the signal pipeline"* rule extends to *"no unvetted tooling in the money path."* Adoptions get logged to the relevant work note.

## Kill criterion (pre-committed)

Track **adoptions** — digest items that actually changed the stack or a workflow.

- After **4 weeks**: if adoptions = 0, the scan is adding noise, not edge — cut cadence to weekly or kill it.
- The scan is **self-throttling**: quiet ecosystem → no new items → no pings → near-zero cost, so an idle system shrinks on its own rather than nagging.

## Open mechanics flagged for build-time verification

- Whether `PERPLEXITY_API_KEY` already exists as a GitHub secret on `life-os` (brief.py uses Groq; Perplexity may need adding).
- New Telegram channel creation + `TOOLING_CHAT_ID` secret wiring for `@DileepLifeOSBot`.
- Cross-repo commit: the Action needs a PAT to commit the vault note into `obsidian-mind` (the PAT pattern already exists for the brief's repo pushes — reuse it).
- Free-source fetch is self-contained in the scan script (HN Algolia + Reddit JSON + arXiv) rather than depending on the local `obsidian-second-brain` `/research` script, which isn't available to a GitHub runner. Minor, focused duplication — accepted for rail independence.
- Grok/X stays on the pending list ([[grok_api_pending]] in memory) — accept a ~30% blind spot on X discourse until added; HN+Reddit covers the rest.

## Related

- [[Tech Watch]] — the framework this automates (AI & LLMs domain, 🔴/🟡/🟢 priority, signal format)
- [[Daily Watch Weekly Hunt]] — shares the "wire cadence via GitHub Actions" rail decision
- [[api-decision-framework]] — free sources first, paid only when it translates to value
- [[Research Queue]] — the compounding research-once-reuse-forever pattern this mirrors
- [[North Star]] — primary purpose (build velocity) serves the ₹7-8L goal via hours saved; Edge Before Action drove the no-experiment-layer scope
- [[What Didn't Work]] — model for the "rejected tooling" ledger
