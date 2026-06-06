---
description: Vault-first deep research - scans the vault with QMD, fills gaps (Perplexity + Grok when keyed, free key-less sources otherwise), synthesizes a delta, then propagates updates across work notes, people, and brain/
category: research
triggers_en: ["deep research", "thorough research", "vault-first research", "research gaps"]
---

Execute `/research-deep [topic]`:

1. Resolve the topic from the user's argument. If no topic, ask: "What topic for deep research?"

2. Run from the obsidian-second-brain repo root:
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && uv run -m scripts.research.research_deep "<topic>"
   ```
   Auto-selects mode: if `PERPLEXITY_API_KEY` is set → paid pipeline; otherwise → free key-less sources. `OBSIDIAN_VAULT_PATH` must be set to `d:\projectsobsidian-mind` for Phase 1 vault scan.

3. **Paid mode** — script runs a 4-phase pipeline:
   - Phase 1: vault scan — finds existing notes mentioning the topic (baseline).
   - Phase 2: gap analysis — Perplexity sonar-pro identifies what's missing/stale, emits 3-5 targeted queries.
   - Phase 3: gap-fill — runs each query via Perplexity (web) or Grok+Live Search (X discourse).
   - Phase 4: synthesis — Perplexity produces a delta report, saves to `reference/research/deep/YYYY-MM-DD - <slug>.md`, then emits a JSON propagation payload.

   Show the synthesis verbatim, then do the propagation step (step 5).

4. **Free mode** — script does Phase 1 vault scan + free-source aggregation and prints JSON. YOU synthesize:
   - Read the baseline excerpts and source results. Flag thin coverage in Open Questions — do not pad.
   - Produce a delta with: What's New Since Vault Baseline, What's Confirmed, Contradictions / Updates Needed (name the `[[vault path]]`), Synthesis, Recommended Vault Updates, Open Questions. Every external claim carries a recency marker and source domain. Every vault reference uses `[[wikilinks]]`.
   - Save to `reference/research/deep/YYYY-MM-DD - <slug>.md` with frontmatter:
     ```yaml
     ---
     date: YYYY-MM-DD
     description: Deep research delta on <topic>
     type: research-deep
     tags: [research, deep]
     ai-first: true
     vault-baseline-notes: [<paths of notes found in Phase 1>]
     sources: [<every result URL verbatim>]
     ---
     ```
   - Then do the propagation step (step 5).

5. **Propagation (both modes):**
   - Treat the synthesis as input to vault updates.
   - For each "Recommended Vault Update" bullet: find the relevant note in `work/`, `org/`, or `brain/` and append the new finding with a recency marker and `[[wikilink]]` to the research note.
   - Update `brain/` topic notes if the research touches patterns, gotchas, or decisions.
   - Report back: "Updated [[X]], created [[Y]], linked [[Z]]."

6. Cost note: paid mode $0.20-$0.80 depending on topic depth. Free mode costs nothing.

**AI-first rule:** Every note MUST have `## For future Claude` preamble, `ai-first: true`, recency markers, mandatory `[[wikilinks]]`, sources verbatim.

**Anti-fabrication:** Enumerate vault matches exhaustively — do not sample. Never invent a claim, contradiction, or source.
