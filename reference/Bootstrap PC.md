---
date: 2026-07-02
description: "Self-contained PC setup instructions for Claude Code — clone all repos, install deps, configure Obsidian and global CLAUDE.md from scratch"
tags:
  - reference
  - tooling
---

# Bootstrap — Dileep's PC Setup

> **For Claude Code:** Read this entire file first, then execute every numbered step in order. This is a one-time machine setup. Do not skip steps. Do not push to any remote unless Dileep explicitly says "OK to push."

---

## Who You Are Working With

You are Claude Code, acting as Dileep Raj's engineering and analytical brain. Before starting the setup, internalize the following — this is your operating manual for every session with Dileep:

```
Name: Dileep Raj | osaattrmpdrg@gmail.com

Governing Principles (no exceptions):
1. Edge Before Action — nothing gets acted on without a provable, verifiable reason.
   If the edge cannot be stated in one sentence, it hasn't been found yet.
2. Asymmetric Thinking — map downside before upside. Ask: "What's the worst realistic
   outcome, and can I survive it?" Never frame opportunities without framing failure modes.
3. First Principles Over Consensus — consensus = no edge. Reason from fundamentals.

How Dileep thinks:
- Shares high-level goal → expects critical analysis before building, not immediate execution
- Prove the edge first, add complexity only after validation
- Pushes back on over-engineering — respect this every time
- Does not want to be told what he already knows — surface what's non-obvious
- Genuine honesty over flattery, every session
- Give the axis, not a blunt verdict

Hard Rules (non-negotiable):
- Never over-engineer Phase 1 — prove it works simply first
- Always use /plan before implementing anything non-trivial
- Prefer editing existing files over creating new ones
- No comments in code unless the WHY is non-obvious
- No half-finished work — complete or don't start
- Never present more than 3 actionable recommendations at once
- NEVER read .env files — secrets live there
- NEVER push to any remote without explicit "OK" from Dileep

Verification tags on every insight:
[VERIFIED] = backed by known facts / data
[HYPOTHESIS] = logically sound but needs confirmation
[BROWSE NEEDED] = requires current data before acting
```

---

## Prerequisites — Install These First (manual, before running Claude Code)

| Tool | Install | Check |
|------|---------|-------|
| Git | https://git-scm.com | `git --version` |
| Python 3.11+ | https://python.org (check "Add to PATH") | `python --version` |
| Node.js 20+ | https://nodejs.org | `node --version` |
| Obsidian | https://obsidian.md | Open app |
| Claude Code | `npm install -g @anthropic-ai/claude-code` | `claude --version` |

**GitHub Personal Access Token** — needed to clone the private repo:
- Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- New token → select `repo` scope → generate → copy it somewhere safe
- When git prompts for password during clone, paste this token

---

## Step 1 — Create the Directory Structure

```powershell
# Create base drive structure matching the laptop
New-Item -ItemType Directory -Force D:\projectsobsidian-mind
New-Item -ItemType Directory -Force D:\life-os
New-Item -ItemType Directory -Force D:\trading_system
```

---

## Step 2 — Clone All Repos

```powershell
# Vault (public)
git clone https://github.com/osaattrmpdrg-byte/obsidian-mind.git D:\projectsobsidian-mind

# Life-OS / crypto trading (public)
git clone https://github.com/osaattrmpdrg-byte/life-os.git D:\life-os

# Trading system (PRIVATE — will prompt for GitHub username + PAT)
git clone https://github.com/osaattrmpdrg-byte/trading-system.git D:\trading_system
```

---

## Step 3 — Install Global CLAUDE.md

This is Dileep's global operating manual. Claude Code reads it at every session start.

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude"
Copy-Item "D:\projectsobsidian-mind\reference\global-claude.md" "$env:USERPROFILE\.claude\CLAUDE.md"
```

Verify:
```powershell
Get-Content "$env:USERPROFILE\.claude\CLAUDE.md" | Select-Object -First 3
# Should show: # Claude — Core Brain: Dileep Raj
```

---

## Step 4 — Create `.env` Files (Manual — Ask Dileep for Values)

**Never commit these files.** They are in `.gitignore` on every repo.

### `D:\life-os\crypto_trading\.env`
```
COINDCX_API_KEY=
COINDCX_API_SECRET=
TELEGRAM_TOKEN=
TELEGRAM_CHAT=
LIVE_TRADING=0
LIVE_RISK_PCT=0.01
```

### `D:\trading_system\.env`
```
ANGEL_API_KEY=
ANGEL_CLIENT_ID=
ANGEL_PASSWORD=
ANGEL_TOTP_SECRET=
TELEGRAM_TOKEN=
TELEGRAM_CHAT=
PERPLEXITY_API_KEY=
```

### `D:\projectsobsidian-mind\.env` (if any MCP servers need keys)
Ask Dileep — check what's in the laptop's vault root `.env`.

Create each file using PowerShell (replace `<path>` and values):
```powershell
# Example for crypto_trading
New-Item -ItemType File -Path "D:\life-os\crypto_trading\.env" -Force
# Then open in Notepad and fill values:
notepad "D:\life-os\crypto_trading\.env"
```

---

## Step 5 — Install Python Dependencies

```powershell
# trading_system
cd D:\trading_system
pip install -r requirements.txt

# crypto_trading (no requirements.txt)
pip install requests yfinance python-dotenv
```

---

## Step 6 — Set Up Obsidian

1. Open Obsidian
2. Click **Open folder as vault** → select `D:\projectsobsidian-mind`
3. Obsidian will detect community plugins → click **Trust and enable plugins**
4. Go to **Settings → Community Plugins → obsidian-git → Options**:
   - Pull on startup: **ON**
   - Vault backup interval: **10 minutes**
   - Authenticate with GitHub when prompted (use the same PAT from Step 2)

From this point the vault auto-syncs. All notes, brain files, thinking scratchpads, and decisions sync automatically.

---

## Step 7 — Bootstrap QMD (Vault Semantic Search)

QMD powers Claude Code's semantic search across vault notes. Run once:

```powershell
cd D:\projectsobsidian-mind
node --experimental-strip-types scripts/qmd-bootstrap.ts
```

---

## Step 8 — Configure `.mcp.json`

The vault's `.mcp.json` wires up MCP servers (QMD, Obsidian, CoinGecko, etc.). It cloned with the vault. If any server needs an API key not covered by a `.env` file, check with Dileep.

```powershell
# View what's configured
Get-Content D:\projectsobsidian-mind\.mcp.json
```

---

## Step 9 — Sanity Check

```powershell
# All three repos have recent commits
cd D:\projectsobsidian-mind; git log --oneline -3
cd D:\life-os; git log --oneline -3
cd D:\trading_system; git log --oneline -3

# Python deps work
python -c "import yfinance, requests, dotenv; print('Python OK')"

# Global CLAUDE.md is in place
Test-Path "$env:USERPROFILE\.claude\CLAUDE.md"
# Should print: True
```

---

## Step 10 — First Claude Code Session

```powershell
cd D:\projectsobsidian-mind
claude
```

Claude Code will auto-load:
- `~/.claude/CLAUDE.md` (global operating manual — just installed in Step 3)
- `D:\projectsobsidian-mind\CLAUDE.md` (vault project instructions)
- SessionStart hook → injects North Star, active work, tasks, QMD index

You're fully set up.

---

## Git Flow — Memorize This, Follow Always

| Repo | Remote | Rule |
|------|--------|------|
| `D:\projectsobsidian-mind` | GitHub | obsidian-git auto-syncs. Leave edits uncommitted — Dileep handles git sync. |
| `D:\life-os` | GitHub | Pull before working. Push ONLY with explicit "OK" from Dileep. |
| `D:\trading_system` | GitHub (private) | Commit locally freely. Push to sync between machines. |

**Never read `.env` files. Never push life-os without "OK". Never force-push anywhere.**

---

## What Syncs Automatically vs. Manual

| Item | How | Action |
|------|-----|--------|
| Vault notes, brain, thinking scratchpads | obsidian-git (auto every 10 min) | None after Step 6 |
| `life-os` / `crypto_trading` code | git push/pull | Pull before working |
| `trading_system` code | git push/pull | Pull before working |
| `.env` files | Never committed | Manual — Step 4 (one-time) |
| `~/.claude/CLAUDE.md` | Copied from vault | Re-run Step 3 if vault updates it |
| `~/.claude/` memory | Not synced | Rebuilds from `brain/` over time |
| `paper_trades.json` | gitignored | GitHub Actions owns live state |

---

*Bootstrap file — created 2026-07-02. Update `reference/global-claude.md` in the vault if the global CLAUDE.md changes. See also [[PC Setup]] for post-bootstrap maintenance and [[Patterns#Git flow — SETTLED, do not re-litigate (2026-06-16)]] for the full git flow rationale.*
