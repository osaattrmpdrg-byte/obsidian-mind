---
description: Extract transcript, metadata, and top comments from a YouTube video - summarized and saved to reference/research/youtube/
category: research
triggers_en: ["summarize youtube", "youtube transcript", "extract video", "youtube to vault"]
---

Execute `/youtube [url]`:

1. Resolve the YouTube URL or video ID from the user's argument. Accept: full URL (`https://www.youtube.com/watch?v=...`), `https://youtu.be/...`, `https://www.youtube.com/shorts/...`, or just the 11-character video ID. If no input, ask: "Which YouTube video?"

2. Run from the obsidian-second-brain repo root:
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && uv run -m scripts.research.youtube_extract "<url-or-id>"
   ```

3. The script:
   - Extracts the transcript via `youtube-transcript-api` (free, no API key).
   - If `YOUTUBE_API_KEY` is set, also fetches title, channel, view/like counts, top comments. Otherwise skips metadata silently.
   - Sends the transcript (and optional comments) to Grok for AI-first summarization.
   - Returns: TL;DR, Key Points, Notable Quotes, Themes & Topics, Comment Sentiment, Worth Following Up On.

4. Show the script output verbatim to the user.

5. **Default save behavior: saves automatically.** Write AI-first note to `reference/research/youtube/YYYY-MM-DD - <video-title-slug>.md` with frontmatter:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: YouTube summary — <video title>
   type: youtube
   tags: [research, youtube]
   ai-first: true
   video-id: <id>
   channel: <channel name>
   source-url: <full YouTube URL>
   ---
   ```
   Body starts with `## For future Claude` preamble (what the video is about, why it was saved, staleness caveat).

6. Plain English triggers: "summarize this YouTube video", "what's in this video", "extract this YouTube link", or pasting a YouTube URL.

7. If no captions AND no API key, the script will fail with a clear message — surface it.

8. If the user asks to research something mentioned in "Worth Following Up On", route to `/research [topic]`.

**AI-first rule:** Note MUST have `## For future Claude` preamble, `ai-first: true`, recency markers, sources verbatim.

**Anti-fabrication:** Never summarize content not actually in the transcript. If the script fails, say so — don't invent content.
