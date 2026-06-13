---
description: Compare stated intentions (North Star, Streams, action queues, open tasks) against what actually happened over the last 30-60 days. Surfaces what's being avoided or stalled, with the smallest next step to unstick each.
category: vault
triggers_en: ["am i drifting", "what am i avoiding", "intentions vs behaviour", "what have i been stalling on", "drift check"]
---

Execute `/drift [days]` (default window: 45 days):

Read-only accountability scan. Never edits money-path repos. Surfaces the gap between what Dileep *said* he'd do and what he *actually* did — and names what he's avoiding.

1. **Gather stated intentions** (what he committed to):
   - `brain/North Star.md` — current focus, goals
   - `brain/Streams.md` — each stream's "Next action" + Action Queue
   - `work/active/*.md` — each active project's open `- [ ]` tasks and "next" items
   - `brain/Research Queue.md` — queued runs
   - Any dated TODO / "pending" / "next session" markers across the vault (QMD or grep)

2. **Gather actual behaviour** (what happened in the window):
   - `git log --since="<days> days ago" --oneline` in the vault (and note any sibling repos mentioned, but do not cd into money-path repos to mutate — read-only `git log` only)
   - Recently modified notes (`thinking/session-logs/`, `work/`, `brain/`) in the window
   - Tasks flipped to `[x]` / notes marked done/✅ in the window

3. **Classify each intention** into:
   - ✅ **Done** — committed and completed in-window
   - 🔵 **Live** — committed and actively progressing (commits/notes touching it)
   - 🟠 **Drifting** — committed ≥ <days> ago, no movement since. **This is the signal.**

4. **For each 🟠 Drifting item**, output:
   - The item + how long it's been static
   - One honest line: *why* it might be getting avoided (hard? ambiguous? needs a gated external step? low-energy? fear?)
   - The **single smallest next step** to unstick it (5–15 min if possible)

5. **Output format** — terse, no padding:
   ```
   DRIFT CHECK · last <days>d

   ✅ Done (N)        — one line each
   🔵 Live (N)        — one line each
   🟠 Drifting (N)    — the focus

   For each 🟠:
     • <item>  (static <X>d)
       why: <one line>
       next: <smallest step>

   THE ONE THING: <the single highest-leverage drifting item to unstick this week, per North Star priority — trading first>
   ```

6. **Discipline:** Be direct, not gentle — this is the value. Don't manufacture drift; if something legitimately wasn't due yet, mark it Live or omit it. Rank 🟠 items by North Star ROI (trading > AgriTech > content > meta) so "THE ONE THING" is the highest-leverage unstick, not the easiest.

7. Optionally save the report to `thinking/YYYY-MM-DD-drift.md` only if the user asks to keep it; otherwise just print.

**Note:** Inspired by Vin's `/drift` command (see [[AI Tooling Workflow Patterns]]) — built because this vault's [[Streams|action queues]] accumulate pending items that need an avoidance check, not just a todo list.
