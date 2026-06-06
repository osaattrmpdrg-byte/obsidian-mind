---
description: Bridge two unrelated domains using your vault's link graph - forces creative friction to spark new ideas
category: thinking
triggers_en: ["connect domains", "cross-pollinate", "bridge ideas", "find an unexpected link"]
---

Execute `/obsidian-connect [domain A] [domain B]`:

Two arguments required: the two topics, domains, or note names to connect. If only one given or none, ask for both.

1. Parse the two domains from arguments (e.g., `/obsidian-connect "distributed systems" "team dynamics"`).

2. For each domain, search the vault exhaustively using QMD semantic search (`mcp__qmd__query`) + grep for every plausible name and alias:
   - Find all notes related to that domain (by title, tags, content).
   - Map their wikilinks to build a local cluster.

3. Find the bridge:
   - Look for shared links, shared tags, or shared people between the two clusters.
   - If a direct path exists in the link graph, trace it and explain each hop.
   - If no direct path exists, find the closest semantic overlap — concepts, metaphors, or structural similarities.

4. Generate creative connections:
   - **Structural analogy**: how a pattern in domain A maps to domain B.
   - **Transfer opportunities**: what works in A that could be applied to B.
   - **Collision ideas**: new concepts that only exist at the intersection of both.

5. Present 3-5 specific, actionable connections — not vague analogies but concrete ideas you could act on.

6. Offer to save the best connections to `brain/Connection - <A> x <B> YYYY-MM-DD.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Connection between <domain A> and <domain B> — <N> bridges found
   type: synthesis
   tags: [brain, thinking, connections]
   ai-first: true
   sources: [<wikilinks to source notes from both clusters>]
   ---
   ```

The value is in unexpected links. If the connection is obvious, dig deeper. The best output makes you say "I never thought of it that way."

**Anti-fabrication:** Only draw connections grounded in actual vault notes. Cite every analogy with `[[wikilinks]]` to the source notes. Never invent connections.
