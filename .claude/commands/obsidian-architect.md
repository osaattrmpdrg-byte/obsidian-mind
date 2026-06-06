---
description: Scan a codebase and write a maintained set of architecture notes into reference/ - overview, per-module notes, key decisions. Re-run to refresh without clobbering your edits
category: meta
triggers_en: ["document this codebase", "architect this project", "map this code into my vault", "generate architecture notes", "refresh architecture docs"]
---

Execute `/obsidian-architect [path-to-codebase]`:

Turns a software project into a maintained set of architecture notes in the vault. Re-running refreshes the notes in place without destroying your edits.

1. **Resolve the codebase path.** Use the argument if given. Otherwise infer from the active project note's `local-path`, or ask. Confirm it is a directory.

2. **Run the scan** from the obsidian-second-brain repo root:
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && python scripts/architect_scan.py --path "<codebase>"
   ```
   Returns JSON: `name`, `kind`, `languages`, `modules`, `dependencies`, `entry_points`, `signals`, `git` commit. Writes nothing — synthesis is yours.

3. **Optionally pull decision history:**
   ```bash
   cd /d "d:\projects\obsidian-second-brain" && python scripts/mine_commit_decisions.py --repo "<codebase>" --json
   ```

4. **Destination:** Write under `reference/architecture/<project-name>/` (create if missing). If no project note exists in `work/active/` for this codebase, offer to create one first.

5. **Synthesize and write these notes**, each AI-first compliant:
   - **`Architecture - Overview.md`** (`type: architecture-overview`): what the project is, its stack, how parts fit together, and ONE Mermaid diagram of modules + main flow. Short **Personas** section (2-4 likely user types, marked `confidence: speculation` unless README states them). Link to each module note.
   - **One note per `core` module** (`type: architecture-module`): `Architecture - <Module>.md` — what it does, dependencies, its role in the whole.
   - **`Architecture - Key Decisions.md`**: write up ADR candidates from the commit-decisions miner. Mark anything inferred as `confidence: speculation`.

   Frontmatter for overview:
   ```yaml
   ---
   date: YYYY-MM-DD
   description: Architecture overview of <project> — <stack> — scanned at commit <hash>
   type: architecture-overview
   tags: [reference, architecture]
   ai-first: true
   project: "[[work/active/<project-note>]]"
   stack: [<languages/frameworks>]
   scanned-commit: <short-hash>
   ---
   ```

6. **Sentinel-safe writing** — wrap every machine-generated section:
   ```
   <!-- @generated:start -->
   ...synthesized content...
   <!-- @generated:end -->
   ```
   On re-run: replace ONLY content inside `@generated` blocks. Never touch `@user` blocks or anything outside the markers.

7. Link the overview from the project note in `work/active/`.

**Anti-fabrication:** Describe only what the scan and code actually show. Never invent a module, dependency, or data flow. Mark inferred rationale as `confidence: speculation`.
