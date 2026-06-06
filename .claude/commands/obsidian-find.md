---
description: Smart vault search - returns results with context, excerpts, and action prompts - not just filenames
category: vault
triggers_en: ["find in vault", "search my notes", "where is", "what did I write about"]
---

Execute `/obsidian-find [query]`:

Smart vault search that returns context you can act on, not just filenames.

1. If no query, ask: "What are you looking for?"

2. Search the vault in order of precision:
   - First: QMD semantic search (`mcp__qmd__query` with the query) — best for conceptual matches.
   - Then: grep for exact phrases, names, or keywords across all `.md` files.
   - Also try: synonyms and related terms if results are sparse.

3. For each result, return:
   - Note title and folder (with `[[wikilink]]`)
   - What type of note it is (work note, person, brain topic, research, etc.)
   - A relevant excerpt (2-4 lines around the match)
   - Last modified date

4. If results are ambiguous, group by type: people, work notes, brain topics, research, etc.

5. After showing results, offer concrete next actions:
   - "Open this note"
   - "Update this note with [context from conversation]"
   - "Link this note to [another note]"
   - "Run `/vault-deep-synthesis [topic]` for a full cross-reference"

6. If nothing found after exhaustive search: say so explicitly and suggest:
   - Running `/research [topic]` to find external information.
   - Creating a new note if the concept should exist in the vault.

**Anti-fabrication:** Before claiming a note doesn't exist, search by every plausible name, alias, and folder. False absence (saying "nothing found" when something exists) is the most common failure mode.
