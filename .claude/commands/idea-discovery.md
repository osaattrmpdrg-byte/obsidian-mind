---
description: Surface 3-5 next-direction candidates by reading unformed brain notes, open project questions, and orphan research - what is worth working on next
category: thinking
triggers_en: ["what should I work on next", "idea discovery", "surface next directions", "what's worth pursuing"]
---

Execute `/idea-discovery`:

Answers "what is worth doing next" from material already in the vault. Distinct from `/obsidian-emerge` (which names unstated patterns) and `/obsidian-graduate` (which promotes one chosen idea into a project) — this ranks several candidate directions so you can pick one.

1. Gather candidate signals — search and list exhaustively, never from memory:
   - `brain/` notes tagged `idea` or `thinking` with no corresponding project in `work/active/`.
   - Open questions in `work/active/` project notes (Open Questions sections, unresolved decisions).
   - Orphan `reference/research/` notes that no `work/` or `brain/` note links to.
   - Recurring topics in `brain/Patterns.md` that have no active project driving them.

2. Rank the top 3-5 candidates by a stated heuristic: **recency** (touched recently), **pull** (how many notes reference or point toward it), **momentum** (does anything already build toward it). State the heuristic in the output so the ranking is auditable.

3. For each candidate, present: what it is, why now, the `[[source notes]]`, and the smallest next step that would move it forward.

4. Suggest next actions per candidate:
   - Run `/research [topic]` to pull external signal before committing.
   - Run `/obsidian-graduate` to promote one into a full project.
   - Run `/vault-deep-synthesis [topic]` to see everything the vault already knows about it.

5. Save the shortlist to `brain/Idea Discovery YYYY-MM-DD.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Idea discovery — top <N> next-direction candidates as of <date>
   type: synthesis
   tags: [brain, thinking, idea-discovery]
   ai-first: true
   sources: [<wikilinks to source notes for each candidate>]
   ---
   ```
   Body starts with `## For future Claude` preamble. Do NOT auto-graduate anything — this command only surfaces and ranks.

**Anti-fabrication:** Rank only real candidates found in the vault. Enumerate `brain/`, `work/active/` open questions, and orphan research exhaustively rather than sampling.
