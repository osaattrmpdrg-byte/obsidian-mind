---
description: Surface unnamed patterns from your recent notes - recurring themes, hidden connections, and conclusions you haven't explicitly stated yet
category: thinking
triggers_en: ["find patterns", "what is emerging", "surface themes", "unnamed patterns"]
---

Execute `/obsidian-emerge [timeframe]`:

The optional argument is a timeframe (e.g., "2 weeks", "this month"). Default: last 30 days.

1. Determine the date range from the argument.

2. Spawn parallel subagents to read vault content from the period:

   - **Work notes agent**: Read all `work/active/` and recent `work/archive/YYYY/` notes in the date range. Extract recurring topics, blockers, decisions, energy patterns.

   - **1-1 agent**: Read all `work/1-1/` notes in the range. Extract recurring themes in conversations, feedback patterns, relationship signals.

   - **Research agent**: Read all `reference/research/` notes created in the range. Extract recurring concepts and emerging interests.

   - **Brain agent**: Read recent updates to `brain/` topic notes. Look for directional trends and ideas being actively developed.

3. Merge results and identify:
   - **Recurring themes**: topics that appeared 3+ times without being named as a priority.
   - **Emotional patterns**: what energizes vs. drains (based on language and context in work/1-1 notes).
   - **Unnamed conclusions**: things the notes imply but never state outright (e.g., "you've mentioned a recurring coordination problem in 4 different notes — this is a systemic issue, not a one-off").
   - **Emerging directions**: where the vault suggests you are heading, even if you haven't committed to it.

4. Present findings as a structured Pattern Report — each pattern gets: the evidence (cited `[[wikilinks]]`), the interpretation, and a suggested action.

5. Offer to save the pattern report to `brain/Emerging Patterns YYYY-MM-DD.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Emerging patterns from the last <timeframe> — <N> patterns surfaced
   type: synthesis
   tags: [brain, thinking, patterns]
   ai-first: true
   ---
   ```

The goal is insight the user cannot see themselves. Do not restate what they already know — surface what they haven't named yet.

**Anti-fabrication:** Only surface patterns actually grounded in vault notes. Cite every claim with a `[[wikilink]]`. Never invent a pattern.
