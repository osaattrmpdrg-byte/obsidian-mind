---
description: Web research with citations - Perplexity Sonar when PERPLEXITY_API_KEY is set, free key-less sources (Wikipedia, HackerNews, arXiv, Reddit) otherwise. Deep dossier with summary, facts, timeline, players, contrarian views, open questions
category: research
triggers_en: ["research this", "look up", "find information about", "perplexity research"]
---

Execute `/research [topic]`:

1. Resolve the topic from the user's argument. Multi-word topics fine. If no topic, ask: "What topic should I research?"

2. Run from the obsidian-second-brain repo root:
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && uv run -m scripts.research.research "<topic>"
   ```
   Auto-selects mode: if `PERPLEXITY_API_KEY` is set → Perplexity Sonar (paid); otherwise → free key-less sources. Pass `--free` to force free mode, `--academic` to restrict to scholarly sources (arXiv, Semantic Scholar, OpenAlex, CrossRef).

3. Handle output by mode:
   - **Paid mode** — script prints a finished dossier (Summary, Key Facts with recency markers, Timeline, Key Players, Contrarian Views, Further Reading, Open Questions, Sources) and saves the AI-first note itself. Show the dossier verbatim, then surface the saved file path. Nothing else to do.
   - **Free mode** — script prints a JSON block. YOU synthesize the dossier from it:
     a. Read the JSON. If fewer than 3 sources returned results, say so plainly — do not pad.
     b. Write a dossier with the same structure as paid mode. Every Key Fact carries a recency marker and the source domain/URL it came from. Never invent facts.
     c. Save it as an AI-first note at `reference/research/web/YYYY-MM-DD - <slug>.md` with frontmatter:
        ```yaml
        ---
        date: YYYY-MM-DD
        description: Research dossier on <topic> — <one-line summary>
        type: research
        tags: [research, web]
        ai-first: true
        sources: [<every result URL verbatim>]
        ---
        ```
        Body starts with `## For future Claude` preamble (2-3 sentences: what was researched, when, confidence caveat).
     d. Show the dossier to the user and surface the saved path.

4. If the user wants X discourse on the same topic, suggest `/x-pulse [topic]`. For vault-aware synthesis, suggest `/research-deep [topic]`.

**AI-first rule:** Every note MUST have `## For future Claude` preamble, `ai-first: true`, recency markers per external claim, mandatory `[[wikilinks]]` for every person/project/concept referenced, sources verbatim with URLs.

**Anti-fabrication:** Never invent facts, entities, or dates. Mark unknowns as `TBD`. False absence is the most common failure mode — search exhaustively before claiming something doesn't exist.
