---
date: 2026-07-01
description: "Step-by-step setup instructions for Claude Code on the PC — clone all repos, create .env files, install deps, configure Obsidian and QMD"
tags:
  - reference
  - tooling
---

# PC Setup — Full Environment

**Read this first, then execute top-to-bottom.** This sets up the full development environment on the PC so it mirrors the laptop exactly.

> [!important] For Claude Code on the PC
> Read this file, then execute every step in order. When in doubt, ask before doing. Do NOT push to any remote unless Dileep explicitly says "OK to push."

---

## 0. Prerequisites

Install these manually before starting:

- **Git** — https://git-scm.com
- **Python 3.11+** — https://python.org (check "Add to PATH" on install)
- **Node.js 20+** — https://nodejs.org (for QMD vault search)
- **Obsidian** — https://obsidian.md
- **Claude Code** — `npm install -g @anthropic-ai/claude-code` (after Node.js)
- **VS Code** (optional, for editing)

Verify installs:
```powershell
git --version
python --version
node --version
```

---

## 1. Clone All Repos

```powershell
# Pick a drive/location — D:\ is convention from laptop
cd D:\

git clone https://github.com/osaattrmpdrg-byte/obsidian-mind.git projectsobsidian-mind
git clone https://github.com/osaattrmpdrg-byte/life-os.git life-os
git clone https://github.com/osaattrmpdrg-byte/trading-system.git trading_system
```

> [!note] `trading_system` is private — GitHub will prompt for credentials. Use a Personal Access Token (Settings → Developer settings → PAT → classic → `repo` scope).

---

## 2. Create `.env` Files

**Never commit these.** They are in `.gitignore`. Create each file manually using the credentials from the laptop (or your password manager).

### `D:\life-os\crypto_trading\.env`

```
COINDCX_API_KEY=
COINDCX_API_SECRET=
TELEGRAM_TOKEN=
TELEGRAM_CHAT=
# Set to 1 only when ready for live capital
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

### `D:\projectsobsidian-mind\.env` (if present on laptop)

Check the laptop's vault root for an `.env` — copy keys for any MCP servers that need them (Perplexity, Gemini, etc.).

---

## 3. Install Python Dependencies

```powershell
# trading_system
cd D:\trading_system
pip install -r requirements.txt

# crypto_trading (no requirements.txt — install manually)
pip install requests yfinance python-dotenv
```

---

## 4. Set Up Obsidian

1. Open Obsidian → **Open folder as vault** → select `D:\projectsobsidian-mind`
2. Obsidian will detect community plugins — click **Trust and enable plugins**
3. `obsidian-git` is already configured:
   - Go to Settings → Community Plugins → obsidian-git → Options
   - Set **Vault backup interval** to 10–15 minutes
   - Set **Pull on startup** to ON
   - Authenticate with GitHub when prompted (PAT or GitHub Desktop)

All vault content — including `thinking/` scratchpads and `brain/` notes — syncs automatically from this point.

---

## 5. Bootstrap QMD (Vault Search)

QMD powers semantic search across the vault. Run once after cloning:

```powershell
cd D:\projectsobsidian-mind
node --experimental-strip-types scripts/qmd-bootstrap.ts
```

This builds the local SQLite index. Claude Code will use it automatically via MCP on subsequent sessions.

---

## 6. Install Global CLAUDE.md

Claude Code reads `~/.claude/CLAUDE.md` at every session start — it contains your identity, governing principles, and hard rules. This file is not synced by git automatically, so copy it from the vault:

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude"
Copy-Item "D:\projectsobsidian-mind\reference\global-claude.md" "$env:USERPROFILE\.claude\CLAUDE.md"
```

Verify: `cat "$env:USERPROFILE\.claude\CLAUDE.md"` — should show "Claude — Core Brain: Dileep Raj".

> [!note] Keeping it in sync
> If you update the global CLAUDE.md on one machine, update `reference/global-claude.md` in the vault too so the PC stays in sync. Run the Copy-Item command again on the PC after pulling.

---

## 8. Configure `.mcp.json`

The vault's `.mcp.json` wires up MCP servers (QMD, Obsidian, CoinGecko, etc.). It should be present in the cloned vault already. If any server needs an API key that isn't in a `.env`:

```powershell
cat D:\projectsobsidian-mind\.mcp.json
```

Add missing keys to the appropriate `.env` and verify Claude Code picks them up on next session start.

---

## 9. Verify Claude Code Reads Context Correctly

In `D:\projectsobsidian-mind`, start Claude Code:

```powershell
cd D:\projectsobsidian-mind
claude
```

Claude Code will auto-load:
- `~/.claude/CLAUDE.md` (global operating manual — shared via git)
- `D:\projectsobsidian-mind\CLAUDE.md` (vault project instructions)
- SessionStart hook → injects [[North Star]], active work, tasks

> [!warning] `~/.claude/` memory files are NOT synced between machines
> The `MEMORY.md` index at `~/.claude/projects/.../memory/MEMORY.md` is machine-local. All durable knowledge lives in `D:\projectsobsidian-mind\brain\` (synced). On first session start on the PC, Claude will rebuild its memory pointers automatically over time.

---

## 10. Git Flow — Already Settled, Follow Exactly

| Repo | Remote | Rule |
|------|--------|------|
| `D:\projectsobsidian-mind` | ✅ GitHub | obsidian-git handles sync automatically |
| `D:\life-os` | ✅ GitHub | Push only when deploying, with explicit "OK" from Dileep |
| `D:\trading_system` | ✅ GitHub (private) | Commit locally freely; push to sync between machines |

**Never read `.env` files.** Verify commit health with `git log` only. See [[Patterns#Git flow — SETTLED, do not re-litigate (2026-06-16)]].

---

## 11. Quick Sanity Check

```powershell
# Vault
cd D:\projectsobsidian-mind; git log --oneline -3

# life-os / crypto_trading
cd D:\life-os; git log --oneline -3

# trading_system
cd D:\trading_system; git log --oneline -3

# Python deps
python -c "import yfinance, requests, dotenv; print('OK')"
```

All three repos should show recent commits. Python check should print `OK`.

---

## What Syncs Automatically vs. Manual

| Item | Sync method | Action needed |
|------|-------------|---------------|
| Vault notes + brain + thinking | obsidian-git (auto) | None |
| `life-os` code | git push/pull | Pull before starting, push when deploying |
| `trading_system` code | git push/pull | Pull before starting, push when done |
| `.env` files | **Never committed** | Manual copy (one-time) |
| `~/.claude/` memory | Not synced | Rebuilds from vault brain/ over time |
| `paper_trades.json` | gitignored | GitHub Actions owns the live state |

---

*Created 2026-07-01. Update this file if the repo list or env structure changes.*
