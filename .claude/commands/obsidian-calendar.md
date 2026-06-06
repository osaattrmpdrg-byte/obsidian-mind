---
description: Reconcile the vault against your Google Calendar - flag deadlines and commitments implied by notes that are not on the calendar. Flag only, never adds events
category: vault
exclude: [codex-cli, gemini-cli, opencode]
triggers_en: ["calendar check", "reconcile calendar", "what's not on my calendar", "am I missing anything on my calendar"]
---

Execute `/obsidian-calendar [window]`:

Catch the gap between what the vault knows you need to do and what is actually scheduled. The optional argument is a window (`today`, `this week`, `this month`); default: this week.

Requires Google Calendar MCP tools (`mcp__claude_ai_Google_Calendar__list_calendars`, `mcp__claude_ai_Google_Calendar__list_events`). If not connected, say so and stop.

1. **Pull the calendar** for the window: find the primary calendar, list events with times.

2. **Gather what the vault implies** for the same window — by listing and grepping, never from memory:
   - Active project deadlines and `next_action`s in `work/active/` notes.
   - Open tasks mentioned in recent `work/1-1/` and `work/active/` notes.
   - Commitments mentioned in recent work notes (appointments, calls, deliverables, review deadlines).
   - Recurring items from any `work/active/recurring/` notes.

3. **Reconcile and report in two directions:**
   - **Vault-implied, not on the calendar** — the headline output. For each: state the item, its source note (`[[wikilink]]`), and the date/urgency.
   - **On the calendar, no vault context** (lighter) — events that might warrant a prep note.

4. **Flag only — never add, move, or change calendar events.** This is a hard boundary. For each gap, propose what you could do ("add a hold?", "needs a prep note?") but do not touch the calendar.

5. Offer to record the reconciliation summary in today's work note or create action items for gaps the user wants to act on.

**Anti-fabrication:** Only flag commitments that actually appear in the vault or calendar. Never invent a deadline. Before claiming a calendar event has no vault context, search exhaustively by event name, attendees, and related topics.
