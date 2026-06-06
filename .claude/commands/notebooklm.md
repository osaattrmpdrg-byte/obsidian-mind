---
description: Vault-first source-grounded research via Gemini File Search. Grounds synthesis in your own vault notes. The grounded parallel to /research-deep (which is open-web via Perplexity).
category: research
triggers_en: ["notebooklm", "research grounded", "ground research in vault", "ask my notebook", "source-grounded research"]
---

Execute `/notebooklm [topic]`:

Requires `GEMINI_API_KEY` in the obsidian-second-brain `.env` file. Get one free at aistudio.google.com/apikey.

1. Resolve the topic from the user's argument. If no topic, ask.

2. Run from the obsidian-second-brain repo root:
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && uv run -m scripts.research.notebooklm --topic "<topic>"
   ```

3. The script does the whole flow end-to-end:
   - Scans the vault for the top 12 relevant notes.
   - Uploads them to a fresh Gemini File Search store.
   - Asks Gemini (default `gemini-2.5-pro`) for a synthesis grounded against those sources.
   - Writes the AI-first synthesis to `reference/research/notebooklm/YYYY-MM-DD - <slug>.md`.
   - Deletes the File Search store (nothing left behind).
   - Emits a propagation payload.

4. **After save, propagate:**
   - For each "Recommended next reads or angles" bullet that maps to a `work/`, `org/`, or `brain/` note: update that note with the new finding + `[[wikilink]]` to the synthesis.
   - Report back: "Saved [[YYYY-MM-DD - <slug>]]. Updated [[X]], created [[Y]]."

5. **When to choose `/notebooklm` vs `/research-deep`:**
   - `/research-deep` (Perplexity + Grok): open-web + X-discourse coverage. Cost: $0.20-$0.80.
   - `/notebooklm` (Gemini File Search): answers grounded in YOUR vault notes. Cost: ~$0.01-$0.05.
   - Run both for high-value topics — the contradictions between web view and vault view are where the insight is.

Frontmatter for saved note:
```yaml
---
date: YYYY-MM-DD
description: Vault-grounded synthesis on <topic> via Gemini File Search
type: research
tags: [research, notebooklm, grounded]
ai-first: true
vault-baseline-notes: [<paths of top 12 notes used>]
---
```
Body starts with `## For future Claude` preamble.

**Anti-fabrication:** Never invent sources. Only cite notes that were actually in the top-12 bundle sent to Gemini.
