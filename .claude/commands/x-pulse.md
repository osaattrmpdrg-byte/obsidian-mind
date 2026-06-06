---
description: Scan X for what's trending in a topic - themes, voices, hooks, and post ideas powered by Grok + Live Search
category: research
triggers_en: ["x pulse", "what is trending on twitter", "scan x for", "twitter pulse"]
---

Execute `/x-pulse [topic]`:

Requires `GROK_API_KEY` set in environment. If not set, say so clearly and stop.

1. Resolve the topic from the user's argument. Multi-word topics fine ("AI automation", "vibe coding"). If no topic, ask: "What topic should I scan X for?"

2. Run from the obsidian-second-brain repo root:
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && uv run -m scripts.research.x_pulse "<topic>"
   ```

3. The script returns a structured pulse: WHAT'S HOT (themes with rep posts + voices), WHAT'S UNDEREXPLORED (gaps), HOOKS THAT ARE WORKING, VOICE & TONE WORKING, POST IDEAS FOR YOU TODAY. Show the full output verbatim.

4. **Default save behavior: saves automatically.** Write AI-first note to `reference/research/x-pulse/YYYY-MM-DD - <slug>.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: X pulse on <topic> — trending themes and post ideas
   type: x-pulse
   tags: [research, x, twitter, pulse]
   ai-first: true
   topic: <topic>
   ---
   ```
   Body starts with `## For future Claude` preamble.

5. After printing, surface the file path the script saved to.

6. Plain English triggers: "what's hot on X about [topic]", "X pulse on [topic]", "what should I post about [topic] today", "scan X for [topic]".

7. If script reports "No active discourse found in last 72h on this topic" — offer to broaden the topic or try `/research [topic]` instead.

**AI-first rule:** Note MUST have `## For future Claude` preamble, `ai-first: true`, recency markers.

**Anti-fabrication:** Surface only what the script returned. Never invent trending posts or voices.
