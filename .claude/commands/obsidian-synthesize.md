---
description: Automatic vault synthesis - scans for unnamed patterns across unrelated sources and writes synthesis notes to brain/
category: thinking
triggers_en: ["synthesize", "auto-synthesis", "make synthesis notes", "find unnamed patterns"]
---

Execute `/obsidian-synthesize`:

Thinks for you. Scans the whole vault and writes synthesis notes for patterns it finds across unrelated sources. Can run manually or be scheduled.

1. Spawn parallel subagents to scan for synthesis opportunities:

   - **Cross-source agent**: Read all notes in `reference/research/` created in the last 7 days. Find concepts that appear in 2+ unrelated sources (web research + YouTube + podcast + X). If the same idea shows up across unrelated sources — that's a synthesis candidate.

   - **Entity convergence agent**: Scan `org/people/` for people who appear together in multiple `work/` contexts but have no explicit connection note. If two people keep showing up in the same projects — write a connection note.

   - **Concept evolution agent**: Scan `brain/` for topic notes that have been updated 3+ times. Track how the concept evolved — write a "Concept Evolution" section showing the timeline.

   - **Orphan rescue agent**: Find notes in `reference/research/` and `work/` with no incoming wikilinks that contain claims which SHOULD be linked to existing brain/ or work/ notes. Create the missing links and explain why.

2. For each synthesis found, create `brain/Synthesis — <Title>.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Auto-synthesis — <what pattern was found>
   type: synthesis
   tags: [brain, thinking, synthesis]
   ai-first: true
   auto_generated: true
   sources: [<wikilinks to source notes>]
   ---
   ```
   Body starts with `## For future Claude` preamble. Document: what pattern was found, which notes it came from (with `[[wikilinks]]`), what it means, and a suggested action.

3. Link the synthesis note FROM all source notes it references.

4. Update `brain/Memories.md` index with any new synthesis topics.

5. Report: X synthesis notes created, Y orphans rescued, Z connections found.

**Anti-fabrication:** Only create synthesis from patterns actually found in the vault. Never invent a pattern to fill the output. If no patterns emerge, say so.
