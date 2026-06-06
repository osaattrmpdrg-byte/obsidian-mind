---
description: Deep cross-reference of everything the vault knows about one topic - agreements, contradictions, stale claims, and coverage gaps. Pure vault, no network
category: thinking
triggers_en: ["synthesize what I know about", "deep synthesis on", "cross-reference my notes on", "what does my vault say about"]
---

Execute `/vault-deep-synthesis [topic]`:

A focused, topic-driven cross-reference of the existing vault. Takes a topic you name and reads every note touching it to produce one consolidated view. Pure vault: no network, no API keys needed.

1. Resolve the topic from the argument. If none, ask what to synthesize.

2. Find every note that references the topic — search exhaustively across `work/`, `reference/research/`, `brain/`, `org/`, `perf/` using QMD semantic search first (`mcp__qmd__query`), then grep for every plausible name, alias, and variation. Do not sample — enumerate all matches.

3. Read the matching notes and cross-reference them into:
   - **What the vault agrees on** — claims multiple notes corroborate, with `[[wikilinks]]` to each.
   - **Contradictions** — where notes disagree; name both `[[notes]]` and the specific conflict. Surface only — do not resolve here.
   - **Stale claims** — dated facts that may no longer hold (cite the note and the date).
   - **Coverage gaps** — questions the topic raises that the vault does not answer. For each gap, suggest `/research [topic]` to fill it from the web.

4. Write the synthesis to `brain/YYYY-MM-DD - synthesis - <topic-slug>.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Vault synthesis on <topic> — agreements, contradictions, gaps
   type: synthesis
   tags: [brain, thinking, vault-deep-synthesis]
   ai-first: true
   sources: [<paths of every note read>]
   ---
   ```
   Body starts with `## For future Claude` preamble. Sections: What the Vault Agrees On, Contradictions, Stale Claims, Coverage Gaps.

5. Do NOT modify source notes — this command only reads and synthesizes.

6. After saving, update `brain/Memories.md` index if the synthesis produces a new durable topic.

**Anti-fabrication:** Enumerate matching notes exhaustively — a partial scan reported as complete produces confident wrong answers. Never invent a claim, contradiction, or source. If the vault is thin, say so.
