---
date: 2026-06-05
description: "Plan for extending the Telegram daily brief to cover all four income streams with stream nudges and BTC/XAU market data."
tags:
  - thinking
  - plan
---

# Plan: Telegram Brief — Four-Stream Expansion

## Goal

Extend `life-os/scripts/brief.py` so the morning and evening Telegram briefs cover all four income streams (trading regime, content nudge, AgriTech nudge, job status) in addition to the existing tech and geopolitics sections.

---

## Files Affected

| File | Action |
|------|--------|
| `C:\Users\drajg\life-os\scripts\brief.py` | Modify — add BTC/USD to market data, add STREAMS_CONTEXT constant, update both prompts with stream section |

No workflow files need to change — the existing `.github/workflows/morning-brief.yml` and `evening-brief.yml` already run `python scripts/brief.py morning|evening`. No new GitHub Secrets needed.

---

## Step-by-Step Changes

### Step 1 — Add BTC/USD to market data fetch

In `_fetch_market_data()`, add `"BTC/USD": "BTC-USD"` to the `tickers` dict.
Also add `"XAU/USD (MCX)": "GC=F"` context (already present as `XAU/USD`).

EUR/USD and USD/CAD stay in the fetch — useful to monitor even when scanner is disabled.

**Output:** Brief now shows BTC/USD regime status (critical — scanner fires when BTC flips).

---

### Step 2 — Add STREAMS_CONTEXT constant

Add a module-level constant that embeds current stream status. This is manually maintained when stream status changes (stream activates, niche defined, paper trade fires, etc.).

```python
STREAMS_CONTEXT = """
STREAM STATUS (as of 2026-06-05):

Job (Stackbox):
  Status: Intern → converting to full-time. Offer letter expected end of June 2026.
  Capital: ₹5-6k/month investable. More after conversion.

Trading:
  BTC/USD: Regime NONE (EMA50 < EMA200). Waiting for flip. Scanner: GitHub Actions 00:30 UTC.
  XAU/USD: Scanner live 22:30 UTC. Zerodha MCX activation pending. No trades fired yet.
  EUR/USD + USD/CAD: DISABLED — no India-legal execution path.
  Gap: Execution layer (one-tap CoinDCX) not built yet.

Content:
  Status: Idea only. Niche not defined. Constraints: faceless, no voice, views-based.
  Next step: Define one niche hypothesis.

AgriTech:
  Status: Idea only. Family owns agricultural land.
  Next step: Assess what the land currently does and what problem is worth solving.
"""
```

**Why constant, not file fetch:** Stream status changes slowly (weeks, not days). Manual update on change is acceptable and avoids adding a GitHub PAT fetch dependency. Upgrade to dynamic fetching when streams become more active.

---

### Step 3 — Update MORNING_PROMPT

Add a `🔀 STREAMS` section after `📊 MARKETS`:

```
🔀 STREAMS
Trading → [one line: BTC/XAU regime from LIVE DATA + any signal building]
Content → [one specific action for today — "niche not defined" → suggest one angle to explore]
AgriTech → [one specific action for today — "land not assessed" → suggest one question to answer]
Job → [only if relevant: offer letter timing, conversion milestone]
```

Also update the `📊 MARKETS` section header to `📊 MARKETS (all instruments, scanner active on BTC + XAU)`.

---

### Step 4 — Update EVENING_PROMPT

Add `🔀 STREAMS` section after `📊 WATCH TOMORROW`:

```
🔀 STREAMS — TODAY'S PROGRESS
Trading → [BTC/XAU regime end of day from LIVE DATA]
Content → [one honest question: "Did you spend 15 min on the niche today?"]
AgriTech → [nudge for tomorrow if not touched today]
```

---

### Step 5 — Update CHART_FOOTER

Add BTC chart link, remove EUR/USD and USD/CAD as primary links (they're disabled in scanner):

```python
CHART_FOOTER = """
━━━━━━━━━━━━━━━━━━━━━
🔗 CHARTS
BTC/USD → https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT
XAU/USD → https://www.tradingview.com/chart/?symbol=TVC:GOLD
MCX     → https://www.mcxindia.com/market-data/spot-market-rates
EUR/USD → https://www.tradingview.com/chart/?symbol=FX:EURUSD
Calendar→ https://www.forexfactory.com/calendar
━━━━━━━━━━━━━━━━━━━━━"""
```

---

### Step 6 — Push to GitHub and trigger test

```bash
git -C "C:\Users\drajg\life-os" add scripts/brief.py
git -C "C:\Users\drajg\life-os" commit -m "feat: expand brief to cover all four income streams"
git -C "C:\Users\drajg\life-os" push
```

Then trigger manually from GitHub Actions to verify Telegram receives the updated brief.

---

## Why This Approach

**Alternatives considered:**

| Approach | Verdict |
|---|---|
| Read `brain/Streams.md` from obsidian-mind GitHub repo via raw URL | Adds PAT fetch + URL dependency. Unnecessary when stream status changes slowly. Upgrade path when streams become active. |
| Read from obsidian-mind repo via git clone in workflow | Heavyweight, adds checkout step, two-repo dependency. Overkill for v1. |
| New separate workflow for stream nudges | Extra complexity. One brief covering all streams is simpler and more useful. |
| Hardcode nudges without Groq | Groq can personalize the stream nudge based on current market context (e.g., "BTC regime may be flipping — check scanner output before opening content work"). |

**Chosen approach:** Single file change, no new infrastructure, manually maintained context, Groq generates stream nudges contextually.

---

## Risks

1. **PAT exposure in git remote URL:** The remote URL contains the PAT in plaintext. This is an existing issue, not introduced by this change.
2. **STREAMS_CONTEXT staleness:** If stream status changes and the constant isn't updated, nudges become stale. Mitigation: update brief.py whenever a stream status changes (BTC regime flips, trade fires, niche defined, etc.).
3. **Token length:** Adding streams section increases prompt length. At 900 max_tokens for the response, need to verify the brief doesn't get truncated. Mitigation: keep stream nudges to one line each.
4. **Groq model behavior:** `llama-3.3-70b-versatile` may not follow the format exactly. The existing brief already has this risk — acceptable for now.

---

## Verification

1. Push to GitHub
2. Go to `github.com/osaattrmpdrg-byte/life-os` → Actions → `morning-brief` → "Run workflow"
3. Wait ~60 seconds
4. Check Telegram `@DileepLifeOSBot` — brief should show `🔀 STREAMS` section with all four streams
5. Confirm BTC/USD regime appears in `📊 MARKETS`

**Expected morning brief shape:**
```
🌅 MORNING BRIEF · 05 Jun 2026
📱 TECH — TOP 3
📊 MARKETS (BTC/USD, XAU/USD, EUR/USD, USD/CAD)
🔀 STREAMS
  Trading → BTC regime NONE, waiting for flip
  Content → [one niche angle to explore today]
  AgriTech → [one question to ask about the land]
  Job → Offer letter expected end of June
🌍 GEOPOLITICS
💪 TODAY'S EDGE
🪞 MORNING QUESTION
```
