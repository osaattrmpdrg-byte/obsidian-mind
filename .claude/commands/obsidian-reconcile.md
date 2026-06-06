---
description: Resolve contradictions between vault notes - surfaces conflicts found by /om-vault-audit or /vault-deep-synthesis and proposes resolutions
category: vault
triggers_en: ["reconcile notes", "resolve contradiction", "notes conflict", "fix conflicting notes"]
---

Execute `/obsidian-reconcile [topic or note pair]`:

Where `/om-vault-audit` and `/vault-deep-synthesis` surface contradictions, this resolves them. Takes a topic (finds all conflicts) or two specific note names.

1. If a topic is given: run the equivalent of `/vault-deep-synthesis [topic]` but focus only on the Contradictions section. List all conflicting claims with `[[wikilinks]]` to both notes.

2. If two note names are given: read both notes fully and identify every point where they disagree.

3. For each contradiction, present:
   - **Note A claim** (with `[[wikilink]]`, date, confidence)
   - **Note B claim** (with `[[wikilink]]`, date, confidence)
   - **Which is more likely current**: based on recency and confidence markers
   - **Proposed resolution**: update Note A / update Note B / create a third note that supersedes both

4. For each proposed resolution, ask for explicit confirmation before touching any note. Never auto-resolve without user approval.

5. On approval, apply the resolution:
   - Update the stale note with a recency marker and link to the current note.
   - If the resolution creates a new understanding, offer to save it to the relevant `brain/` topic note.
   - Never delete content — only annotate and link.

6. After resolving, check if `brain/Key Decisions.md` should be updated to reflect the reconciled position.

**Anti-fabrication:** Only flag contradictions that actually exist in the notes. Never invent a conflict. When in doubt about which note is more current, present both and ask the user.
