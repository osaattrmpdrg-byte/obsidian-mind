---
date: 2026-06-13
description: Design for an autonomous AI-tooling intelligence system — weekly scan of how people use Claude/OpenClaw/Obsidian/AI tooling, queue-driven nightly cloud experiments, gated adoption, delivered to a dedicated Telegram channel + vault. Gives Tech Watch a heartbeat.
tags:
  - work-note
  - thinking
  - automation
status: proposed
quarter: Q2-2026
---

# Tooling Intelligence Scan — Design

Designed in a `/grill-me` session on 2026-06-12/13. Gives [[Tech Watch]] a heartbeat: automates the AI & LLMs domain it already defines as highest-priority, focused on the AI-tooling slice (Claude Code, OpenClaw, Obsidian, MCP, agent patterns).

## The edge (one sentence)

Idle overnight subscription quota — which expires unused on days Dileep doesn't touch the laptop — is converted into evidence-backed verdicts on which AI tools/workflows would actually speed up active work, so the morning decision collapses from "evaluate" to "accept/reject."

## Purpose (in priority order)

1. **Primary — sharpen Dileep's own build workflow.** Findings must name an active project or standing workflow they would speed up ([[CoinDCX Execution Layer]], the Hunt harness, vault automation, research pipeline) and end in a verdict: *try / queue / ignore*.
2. **Secondary — awareness.** Anything that can't be tied to active work is demoted to an FYI awareness line, kept but not acted on.

This is **not** trade-setup-only. Scope is AI tooling itself — Claude Code features, OpenClaw setups, Obsidian plugins/workflows, MCP servers, agent patterns — whatever HN/Reddit/X is buzzing about. Trading enters only in two roles: as one of the active projects a finding can claim to speed up, and as the **forbidden zone** for unsupervised changes.

## What already exists (reuse, don't rebuild)

| Asset | Location | Role here |
|---|---|---|
| GitHub Actions cron rail | `life-os` repo (`github.com/osaattrmpdrg-byte/life-os`), `.github/workflows/morning-brief.yml` etc. | Proven autonomous, machine-off-friendly rail. Runs `scripts/brief.py` on cron. |
| Telegram bot | `@DileepLifeOSBot` + Groq synthesis | Delivery. A **new chat_id** (dedicated channel) keeps tooling noise out of the trading approval bot. |
| Brief tech section | `scripts/brief.py` already emits "📱 TECH — TOP 3" | The awareness layer is half-built; this formalizes and deepens it. |
| `/research` | shells to `d:\projects\obsidian-second-brain`, Perplexity when keyed, free HN/Reddit/arXiv otherwise | Source engine for the scan. Free sources first per [[api-decision-framework]]. |
| `/youtube`, `/podcast`, `defuddle` | this vault | Deep-read individual sources the scan surfaces. |
| `/notebooklm` (Gemini) | this vault | Monthly synthesis of accumulated tooling notes into one master note (near-free). |
| `/schedule` cloud routines | Claude Code | Phase 2 nightly experiment agent. **Mechanics unverified — see Phase 0.** |

## Architecture — two rails

Each rail does what it is good at; they are not interchangeable.

| Rail | Executes on | Strength | Limitation |
|---|---|---|---|
| **GitHub Actions (life-os)** | GitHub servers, cron | Deterministic API calls + Telegram delivery, runs with laptop off | Not agentic — cannot clone/install/try tools |
| **Cloud Claude agent (`/schedule`)** | Cloud sandbox | Agentic experiments — clone repo, install tool, try workflow, report | Mechanics (billing, secrets, sandbox scope) need a 1-run verify |

> [!important] Why not `CronCreate`
> `CronCreate` jobs are session-only — they die when the Claude REPL exits, so they cannot run overnight when no session is open. Overnight autonomy requires either GitHub Actions (rail 1) or a persistent `/schedule` cloud routine (rail 2). `CronCreate` is unsuitable and is not used.

## Data flow

```
SUNDAY NIGHT  ── weekly scan (rail 1 or cloud agent) ──► ranked QUEUE (vault file)
                  sources: free HN/Reddit/arXiv first, Perplexity gap-fill,
                           YouTube for demos. (Grok/X pending — ~30% blind spot.)
                  each item: {title, source, which active project it speeds up,
                              A-filter verdict: try | queue | ignore}

EACH NIGHT    ── pop top item IF it clears the A-filter "try" bar (else NO RUN) ──►
                  cloud agent experiments in sandbox:
                    clone vault repo copy, install/try the tool against it,
                    record what worked + where it broke
                  ──► verdict: adopt | skip
                  ──► writes vault note (evidence) + Telegram one-liner (dedicated channel)

MORNING       ── Dileep reads: digest + experiment evidence + adopt/skip verdict.
                  Adopting a winner into the REAL environment = daytime, supervised step.

MONTHLY       ── /notebooklm synthesis of the month's tooling notes → one master note.
```

## The A-filter (what makes an item "try"-worthy)

An item earns a "try" verdict only if it can name a specific active project or standing workflow it would speed up. Generic "people like tool X" with no attachment point → demoted to awareness FYI. This is the falsifiable gate: it forces every experiment candidate to have a stated payoff before any quota is spent on it. Max throughput is the queue, not a fixed count — but a "try" with no attachment point cannot exist by construction.

## Safety boundary (non-negotiable)

The cloud sandbox is fed by content scraped from Reddit/X/HN — an untrusted input channel (prompt-injection-via-blog-post is a real pattern). Therefore:

- **Cloud env holds research keys only:** Perplexity, YouTube, Gemini. Worst case if compromised = wasted research credits.
- **Exchange keys NEVER enter the cloud.** `D:\crypto_trading\.env` (live CoinDCX key that can place orders), Angel One, and anything in `D:\trading_system` / `D:\crypto_trading` stay local. This extends the existing *"no LLM in the signal pipeline"* rule to *"no unsupervised tooling changes in the money path."*
- **Experiments are sandboxed and disposable.** Clone a copy, break it freely, throw it away. Nothing installed globally, no real config touched.
- **Adoption is human-gated and daytime.** The agent recommends; Dileep, present, runs the adoption into the real environment (via `/prototype` for anything non-trivial).

## Delivery

- **Vault note per cycle:** `reference/research/tooling/YYYY-MM-DD <topic>.md`, AI-first format (`## For future Claude` preamble, `ai-first: true`, sources verbatim, wikilinks to affected work notes). Git-tracked evidence that compounds.
- **Telegram one-liner** to a **dedicated channel** (new chat_id, same `@DileepLifeOSBot`, NOT the trading approval bot): e.g. `Tonight's experiment: <tool> — verdict: adopt/skip. Details in vault.`
- A "rejected tooling" ledger compounds like [[What Didn't Work]] — no tool gets evaluated twice.

## Kill criterion (pre-committed)

Track **adoptions** per cycle — findings that actually changed the stack or a workflow.

- After **4 weeks**: if adoptions = 0, the experiment layer (Phase 2) dies. The near-free awareness scan (Phase 1) survives.
- After **8 weeks**: review whether nightly cadence earns its queue depth or should drop to 2–3 nights/week.
- **Self-throttling:** empty queue → no night run → zero waste. The system shrinks naturally when the ecosystem is quiet.

## Phasing (Edge Before Action)

> [!note] The one decision to confirm
> Per CLAUDE.md *"never over-engineer Phase 1 — prove it works simply first."* The experiment layer is the expensive, risky, mechanics-unverified part; the scan is cheap and rides a proven rail. Recommended split below. Confirm or veto before the plan is written.

### Phase 0 — Verify cloud-agent mechanics (1 run, ~15 min)
Before committing to Phase 2, confirm with one test `/schedule` cloud run:
1. **Billing:** does it draw from the subscription quota (the whole premise) or bill API per-token? Check `/usage` after the run.
2. **Secrets:** can the cloud env hold Perplexity/Telegram credentials?
3. **Sandbox scope:** can it clone a repo, install a tool, run it, and commit a report back?

If billing turns out to be per-token API, Phase 2 collapses to weekly-chained on the GitHub Actions rail instead of nightly.

### Phase 1 — Awareness scan (build now, proven rail)
Weekly scan → ranked queue + digest with A-filter verdicts → dedicated Telegram channel + vault note. Reuses the `life-os` GitHub Actions + Telegram rail. Proves the edge cheaply: *does the scan surface adoptable items?* Run 2 weeks before Phase 2.

### Phase 2 — Nightly experiments (build after Phase 1 shows queue signal)
Queue-driven nightly cloud-agent experiments with the safety boundary above. This is where idle quota gets used hard — justified only once the queue is proven to feed real candidates.

## Open mechanics flagged for build-time verification

- `/schedule` cloud-agent billing model, secret storage, and sandbox capabilities (Phase 0 resolves).
- Whether the cloud agent can write back to the `obsidian-mind` vault repo (PAT + checkout), or whether delivery must go vault-note-via-life-os-Action instead.
- New Telegram channel creation + chat_id wiring for `@DileepLifeOSBot`.
- Grok/X remains on the pending list ([[grok_api_pending]] in memory) — accept a ~30% blind spot on X discourse until added; HN+Reddit covers the rest.

## Related

- [[Tech Watch]] — the framework this automates (AI & LLMs domain, 🔴/🟡/🟢 priority, signal format)
- [[Daily Watch Weekly Hunt]] — shares the "wire cadence via /schedule or GitHub Actions" open task; same rail decision
- [[api-decision-framework]] — free sources first, paid only when it translates to value
- [[Research Queue]] — the compounding research-once-reuse-forever pattern this mirrors
- [[North Star]] — primary purpose (build velocity) serves the ₹7-8L goal indirectly via hours saved
- [[What Didn't Work]] — model for the "rejected tooling" ledger
