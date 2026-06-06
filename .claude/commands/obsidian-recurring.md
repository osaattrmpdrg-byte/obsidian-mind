---
description: Track a repeating obligation with cadence and next-due date - logs each completion, advances the next-due on check-off
category: vault
triggers_en: ["recurring task", "repeating obligation", "track this monthly", "set up recurring"]
---

Execute `/obsidian-recurring [task description]`:

Creates or updates a recurring task note that tracks a repeating obligation — monthly reviews, weekly standups, quarterly payments, etc.

1. Parse the task from the argument, or pull from conversation context.

2. Infer or ask for:
   - **Cadence**: e.g., "monthly day 20", "every quarter", "weekly Monday", "every 2 weeks"
   - **Owner**: who is responsible
   - **Blocker**: who or what gates completion (optional)
   - **Amount**: if it's a payment or measurable deliverable (optional)
   - **Next due**: computed from cadence + today

3. Search `work/active/` for an existing recurring note matching this task (fuzzy match). If found, update it instead of creating a duplicate.

4. Create or update `work/active/Recurring - <Task Name>.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Recurring task — <task name> — <cadence>
   type: recurring-task
   tags: [work-note, recurring]
   status: active
   quarter: <Q#-YYYY>
   cadence: <cadence string>
   owner: <owner>
   blocker: "[[org/people/<Name>]]"
   next-due: YYYY-MM-DD
   amount: <optional>
   ---
   ```

5. Body sections:
   - `## For future Claude` — what this recurring task is, why it exists, who it involves.
   - `## Next Steps` — what needs to happen before the next-due date.
   - `## History` — log of every completion: `- YYYY-MM-DD — completed by <owner>. Notes: <any context>.`

6. When a recurring task is checked off (user says "done" or "completed"):
   - Append a History entry with today's date and any context.
   - Advance `next-due` by the cadence.
   - Update `status: active` (it's never truly "completed" — it just advances).

7. Link the recurring note from `work/Index.md` under Active Projects.

**Anti-fabrication:** Never invent cadence or deadlines not stated by the user. If cadence is ambiguous, ask.
