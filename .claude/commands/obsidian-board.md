---
description: Create or manage a kanban board in the vault - add tasks, move cards, track progress visually using Obsidian's kanban plugin format
category: vault
triggers_en: ["create board", "kanban board", "add to board", "task board", "move card"]
---

Execute `/obsidian-board [action] [board name]`:

Create or manage kanban boards. Boards use Obsidian's kanban plugin format. Actions: `create`, `add`, `move`, `show`.

**Board format:**
```yaml
---
kanban-plugin: board
---
```
Columns as H2 headings. Items as task checkboxes.

**Standard columns:** `📥 Backlog` · `📋 This Week` · `🔨 In Progress` · `⏳ Waiting On` · `✅ Done`

**Item format (active):**
```markdown
- [ ] 🔴 **Task Title** · @{YYYY-MM-DD}
  One-line description. [[Related Work Note]] [[Person]]
```

**Priority:** 🔴 critical · 🟡 important · 🟢 low

**Item format (done — never delete, move to ✅ Done):**
```markdown
- [x] ~~🔴 **Task Title**~~ ✅ YYYY-MM-DD
```

**Actions:**
- `create [board name]`: Create a new board in `work/active/<Board Name>.md` with standard columns. Link from `work/Index.md`.
- `add [task] to [board]`: Find the board, add a card to the right column based on due date (This Week if due soon, Backlog otherwise). Infer priority from conversation context.
- `move [task] to [column]`: Find the card, move it to the specified column. For `Done`: strikethrough the title and add ✅ date.
- `show [board]`: Read and display the board's current state.

If no board is specified and multiple boards exist in `work/active/`, ask which one.

**Anti-fabrication:** Search for existing boards before creating a new one. Never create duplicate boards.
