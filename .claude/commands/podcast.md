---
description: Extract metadata, transcript, and summary from a podcast episode - saved as an AI-first note in reference/research/podcasts/
category: research
triggers_en: ["summarize this podcast", "podcast episode summary", "extract podcast", "what's in this episode"]
---

Execute `/podcast [url]`:

1. Resolve the podcast URL from the user's argument. Accept:
   - Apple Podcasts episode URL (`https://podcasts.apple.com/.../id<show>?i=<episode>`)
   - Direct RSS feed URL (uses latest episode unless `?episode=<guid>` selector is appended)
   Spotify URLs are NOT supported (DRM blocks access). If pasted, say so clearly.

   If no input, ask: "Which podcast episode? Paste the Apple Podcasts link or RSS feed URL."

2. Run from the obsidian-second-brain repo root:
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && uv run -m scripts.research.podcast_extract "<url>"
   ```

3. The script:
   - Resolves Apple Podcasts URLs to RSS via iTunes Lookup API (free, no key).
   - Parses RSS feed, extracts episode metadata (title, show, host, published, duration, audio URL, show notes).
   - Tries to obtain transcript in order:
     1. `<podcast:transcript>` tag in RSS (free, fast, high fidelity).
     2. Whisper API transcription if `OPENAI_API_KEY` is set (~$0.006/min).
     3. Show-notes-only fallback (quality drops; Notable Quotes will be empty).
   - Returns: TL;DR, Key Points, Notable Quotes, Themes & Topics, Guests & People Mentioned, Worth Following Up On.

4. Show the script output verbatim.

5. **Default save behavior: saves automatically.** Write AI-first note to `reference/research/podcasts/YYYY-MM-DD - <episode-title-slug>.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Podcast summary — <show>: <episode title>
   type: podcast
   tags: [research, podcast]
   ai-first: true
   show: <show name>
   host: <host name>
   episode-title: <title>
   episode-url: <url>
   feed-url: <RSS URL>
   published: <date string from RSS>
   transcript-source: rss-transcript-tag | whisper-api | show-notes
   ---
   ```
   Body starts with `## For future Claude` preamble.

6. Plain English triggers: "summarize this podcast", "what's in this episode", pasting an Apple Podcasts URL.

7. If the user asks to research someone mentioned in "Guests & People Mentioned", route to `/research [name]` or check `org/people/` for an existing person note.

**AI-first rule:** Note MUST have `## For future Claude` preamble, `ai-first: true`, sources verbatim.

**Anti-fabrication:** Never invent episode content. If transcript is unavailable and no API key set, surface the error clearly.
