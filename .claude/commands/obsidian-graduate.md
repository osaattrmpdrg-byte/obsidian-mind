---
description: Promote an idea or brain note into a full active project spec with tasks, goals, and open questions in work/active/
category: thinking
triggers_en: ["promote idea", "graduate this to project", "make a project from this", "elevate idea"]
---

Execute `/obsidian-graduate [idea title or keyword]`:

The optional argument is the idea title or keyword. If not provided, scan `brain/` for notes tagged `idea` or `thinking` and present them for selection.

1. Find the idea to graduate:
   - If argument given: search `brain/`, `work/archive/`, and recent `work/active/` for a matching idea (fuzzy match).
   - If no argument: list recent thinking/idea notes and ask the user to pick one.

2. Read the full idea note and any linked notes for context.

3. Research the vault for related content:
   - Existing projects in `work/active/` that overlap.
   - People in `org/people/` mentioned in connection with this idea.
   - Past decisions in `brain/Key Decisions.md` that relate.
   - Similar ideas that were previously explored (to avoid reinventing).

4. Generate a full project spec and create `work/active/<Project Name>.md`:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: <Project name> — <one-line summary of what and why>
   tags: [work-note]
   status: active
   quarter: <Q#-YYYY>
   ---
   ```
   Body sections: Context (what prompted this), Goals (3-5 concrete outcomes), Key Tasks (broken into phases with priorities), Open Questions (what still needs answering), Related (links to source idea, people, decisions).

5. Update `work/Index.md` — add the new project to Active Projects.

6. Update the original idea note in `brain/`:
   - Note that it was graduated with a `[[wikilink]]` to the new project note.

7. Report: what was created, what was linked, what needs the user's input.

The idea doesn't die — it evolves. The original note stays as the origin story, the project note becomes the execution plan.

**Anti-fabrication:** Search exhaustively before claiming related projects or decisions don't exist. Never invent goals or tasks not grounded in the idea note.
