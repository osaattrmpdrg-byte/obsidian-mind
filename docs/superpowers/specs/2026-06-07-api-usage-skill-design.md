---
date: 2026-06-07
description: "Design spec for the api-usage skill — a full-lifecycle gate + audit for paid API spend (Perplexity/Gemini/Grok), sharing one ledger and the Tier 1/2/3 framework"
tags:
  - thinking
  - spec
status: accepted
---

# Design: `api-usage` skill

**Date:** 2026-06-07
**Status:** Approved (design)
**Author:** Dileep + Claude

## Problem

Paid API spend (Perplexity, Gemini, Grok-pending) needs discipline in two
directions:

1. **Before a call** — was this call worth it, or could the vault / Claude
   answer it for free? The rules already exist in
   `reference/research/api-decision-framework.md` (Tier 1/2/3 decision tree),
   but nothing operationalizes them — they're prose, easy to skip.
2. **After the fact** — how much got spent, and did it translate to value?
   Today there is no record of calls and no way to review ROI.

The governing rule (from the framework): **API spend should translate to
money.** Never be cheap on Tier-1 tactical calls; scrutinize everything else.

## Goal

One skill, `api-usage`, covering the full lifecycle: a **gate** on the way out
and an **audit** on the way back, sharing one append-only ledger.

Non-goals (YAGNI):
- Hard, unbypassable enforcement (would need a PreToolUse hook — defer until the
  skill-as-nudge proves insufficient).
- Real-time billing integration with provider dashboards.
- Duplicating the Tier 1/2/3 logic — the framework note stays the single source
  of truth; the skill references it.

## Architecture

A vault skill at `.claude/skills/api-usage/`:

| Component | Responsibility |
|---|---|
| `SKILL.md` | Skill instructions + trigger description. Holds the gate decision flow (referencing the framework) and the audit invocation. |
| `scripts/audit.py` | Stdlib-only. Reads ledger + globs vault artifacts, computes counts/cost/drift, prints report. |
| `brain/api-ledger.jsonl` | Append-only decision log. Created on first gate decision. Data, not a note — JSONL not Markdown. |

Single source of truth for the tier logic remains
`reference/research/api-decision-framework.md`. The skill links to it.

## Gate mode (default)

Triggers before any paid API call (Perplexity / Gemini / Grok). The SKILL.md
description is written so Claude's skill-discovery loads it automatically when
about to call a paid provider.

Flow:

```
Query about to be sent + provider
  -> classify against api-decision-framework.md tiers
       Tier 1 (tactical / pre-trade / real-time) -> PAY (no friction)
       Tier 2 (strategic)                         -> VAULT-FIRST
                                                       (QMD-check; if missing/
                                                        stale -> PAY, else use vault)
       Tier 3 (foundational / definitional)       -> CLAUDE-ONLY (no call)
  -> emit verdict + one-line reason
  -> on PAY or VAULT-FIRST: append one line to brain/api-ledger.jsonl
```

Verdict vocabulary: **PAY** / **VAULT-FIRST** / **CLAUDE-ONLY**.

## Audit mode (on demand)

Invoked explicitly ("audit api usage", weekly cadence). Read-only over the
ledger; writes only the report note.

Flow:

```
Read brain/api-ledger.jsonl
Glob vault artifacts: Research/Web/, reference/research/
Cross-check drift:
  - ledger PAY entry with no matching artifact  -> WASTED SPEND
  - artifact with no matching ledger entry      -> UNTRACKED CALL
Report:
  - calls + est. cost per provider (period + lifetime)
  - ROI signal: did spend produce a note / decision?
  - drift flags
Save a dated audit note (brain/api-audits/API Audit YYYY-MM-DD.md) for trend tracking
```

Audit notes go in `brain/api-audits/` (operational review artifacts, not
performance-review evidence), one per run, linking back to
`[[api-decision-framework]]`.

Matching ledger<->artifact: by query-text similarity and date proximity
(same-day, fuzzy). Exact linkage is best-effort; drift detection is the point.

## Ledger format

`brain/api-ledger.jsonl`, one JSON object per line:

```json
{"ts":"2026-06-07T10:00","provider":"perplexity","mode":"research-deep","query":"...","verdict":"pay","tier":1,"est_cost_usd":0.005}
```

JSONL chosen for append-safety (no merge conflicts), machine-parseability, and
clean growth. Human-readable output is the audit note, not the ledger.

## Cost table (seed values)

| Provider | Unit cost | Notes |
|---|---|---|
| Perplexity Sonar | ~$0.005 / query | paid |
| Gemini | $0 | free tier |
| YouTube Data API | $0 | free quota |
| Grok | TBD | pending — `[[grok-api-pending]]` |

Costs live as a small dict in `audit.py`, easy to update.

## Error handling

- Ledger missing -> audit reports "no ledger yet," still counts vault artifacts.
- Malformed ledger line -> skip + warn, don't crash.
- Gate with framework file absent -> fall back to an inline tier summary.

## Testing

- `audit.py`: TDD unit tests against a fixture ledger + fixture vault dir.
  Assert per-provider counts, cost sums, and both drift directions
  (wasted spend, untracked call). Malformed-line handling covered.
- Gate mode (prose): validated with worked example scenarios embedded in
  `SKILL.md` (one per tier).

## Future enhancement (out of scope now)

If Claude skips the gate in practice, add a PreToolUse hook (Approach C) that
fires on the research commands / MCP calls for unbypassable enforcement.
