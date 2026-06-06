---
description: Deep-read an X (Twitter) post via Grok + Live Search - verbatim post, thread, TL;DR, claims, reply sentiment, voices to watch
category: research
triggers_en: ["read this x post", "deep read this tweet", "analyze this tweet", "read this thread"]
---

Execute `/x-read [url]`:

Requires `GROK_API_KEY` set in environment. If not set, say so clearly and stop.

1. Resolve the URL from the user's argument. If no URL, ask: "Which X post URL?" Accept any URL containing `x.com/` or `twitter.com/`.

2. Run from the obsidian-second-brain repo root:
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && uv run -m scripts.research.x_read "<url>"
   ```

3. The script prints a structured analysis: ORIGINAL POST, THREAD, TL;DR, KEY CLAIMS, REPLY SENTIMENT, NOTABLE COUNTER-ARGUMENTS, VOICES TO WATCH. Show the analysis verbatim — don't paraphrase or summarize.

4. **Default save behavior: chat only.** Do NOT save automatically. The user must ask explicitly ("save this", "save to vault") for it to be archived.

5. If the user asks to save: write AI-first note to `reference/research/x-reads/YYYY-MM-DD - <slug>.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   time: HH:MM
   description: X post analysis — <topic or author>
   type: x-read
   tags: [research, x, twitter]
   ai-first: true
   post-url: <url>
   post-author: <handle if known>
   key-claims: [<list>]
   related-people: [<[[wikilinks]] for handles that map to known people in org/people/>]
   ---
   ```
   Body starts with `## For future Claude` preamble.

6. If script fails (missing key, network), surface error verbatim. Auto-retry on transient errors is handled inside the script.

**AI-first rule:** Note MUST have `## For future Claude` preamble, `ai-first: true`, sources verbatim.

**Anti-fabrication:** Show only what the script actually returned. Never invent post content or thread replies.
