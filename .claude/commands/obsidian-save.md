---
description: Save everything worth keeping from this conversation to the vault - decisions, tasks, people, projects, ideas - via parallel subagents
category: vault
triggers_en: ["save this", "save the conversation", "save to vault", "obsidian save"]
---

Execute `/obsidian-save`:

Scans the entire conversation and saves all vault-worthy items in parallel. More powerful than `/om-dump` — handles multiple note types simultaneously.

1. Scan the entire conversation and identify all vault-worthy items:
   - Decisions made
   - Tasks and commitments
   - People mentioned
   - Projects started or updated
   - Ideas and insights
   - Research findings
   - Learnings and patterns

2. Group items by type. Spawn parallel subagents — one per group — so all note types are handled simultaneously:

   - **People agent**: Search `org/people/` for each person mentioned. Create stubs for unknowns. Log interactions to existing person notes.

   - **Projects agent**: Search `work/active/` for each project mentioned. Update existing project notes' Recent Activity sections. Create new work notes for untracked projects.

   - **Decisions agent**: Find relevant `work/active/` notes. Append to Key Decisions sections. For architectural decisions, offer to create a Decision Record in `work/`.

   - **Ideas agent**: Search `brain/` for related topic notes. Create or append. For standalone new ideas, save to `brain/` with appropriate tags.

   - **Patterns/Learnings agent**: Check `brain/Patterns.md` and `brain/Gotchas.md`. Append any new patterns, lessons, or gotchas surfaced in the conversation.

3. After all agents complete: update `work/Index.md` if new work notes were created. Report back a clean list of what was saved and where.

**Rules:**
- Search before creating anything — duplicate notes are vault rot.
- Every new note must link to at least one existing note (no orphans).
- Never overwrite existing user content — only append to existing sections.
- Follow obsidian-mind frontmatter conventions (date, description, tags, status, quarter).

**Anti-fabrication:** Only save what was actually said in the conversation. Never invent context, decisions, or tasks that weren't explicitly mentioned.
