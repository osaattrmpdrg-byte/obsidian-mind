---
description: Review vault learnings, prune stale ones, surface active patterns, identify lessons worth promoting to permanent brain/ rules
category: thinking
triggers_en: ["review learnings", "what have I learned", "show lessons", "prune learnings"]
---

Execute `/obsidian-learn [scope]`:

The optional argument is a scope: `recent` (last 30 days, default), `all` (entire vault), or a topic name.

1. Spawn parallel subagents to gather learnings:

   - **Lessons agent**: Scan `work/active/`, `work/archive/`, and `work/1-1/` notes for "Lesson learned" sections, "What didn't work", retrospective insights, and outcome notes.

   - **Decisions agent**: Read decision records in `work/` — extract the rationale and whether the decision held up.

   - **Patterns agent**: Read `brain/Patterns.md` and `brain/Gotchas.md` — classify each as still active or superseded by newer evidence.

   - **Mistakes agent**: Scan `work/incidents/`, `work/1-1/`, and `work/archive/` for "what didn't work", "wasted time on", "next time", "lesson" — phrases indicating learning from failure.

   - **Wins agent**: Scan `perf/brag/` and `work/` for patterns that worked — "this saved time", "this approach worked", recurring success patterns.

2. For each learning found, classify:
   - **Active**: still relevant, recurring, reinforced by recent activity.
   - **Stale**: 6+ months old with no recent reinforcement, or contradicted by newer evidence.
   - **Superseded**: explicitly replaced by a newer decision or pattern.
   - **Promoted**: appeared 3+ times — should become a permanent rule in `brain/Patterns.md` or `brain/Gotchas.md`.

3. Generate the Learnings Report with sections: Active Learnings, Stale Learnings, Superseded Learnings, Promotion Candidates (appeared 3+ times), Top 5 Lessons of the Period.

4. Save to `brain/Learnings Review YYYY-MM-DD.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Learnings review covering <scope> — <N> active, <N> stale, <N> promotion candidates
   type: synthesis
   tags: [brain, thinking, learnings]
   ai-first: true
   ---
   ```

5. Offer to:
   - Promote candidates to `brain/Patterns.md` or `brain/Gotchas.md` (with user confirmation).
   - Archive stale learnings (with user confirmation).

Lessons that aren't reviewed don't compound. This command turns scattered work notes into a living rulebook.

**Anti-fabrication:** Only surface learnings actually found in the vault. Never invent lessons to pad the report.
