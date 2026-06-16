---
date: 2026-06-05
description: "Four income streams toward ₹7-8L/month passive by age 27. Current status, next action, and what's blocking each. Read at session start."
tags:
  - brain
  - strategy
---

# Income Streams

**Goal:** ₹7-8L/month passive income by age 27 (currently 22 → 5-year window).
**Philosophy:** Each stream feeds the next. Job funds trading capital. Trading validates the edge. Content and AgriTech build asymmetric income.

> [!tip] How Claude should use this
> At session start, scan all four streams. Surface the one with the most actionable next step. Nudge toward small daily progress even when the main session focus is elsewhere.

> [!warning] Open trajectory fork (2026-06-15)
> Dileep is considering an **armed-forces career** ([[Defence Career Strategy]]) — a [[Vision]]-level decision that could reorder all four streams. If it proceeds, the **automated trading system is the one stream that survives a service life** (content + AgriTech don't), and the financial work becomes the no-pension backbone. Not decided — the streams below stand until it is.

---

## Stream 1 — Job (Stackbox)

**Status:** Active. Primary income source.
**Current:** Software engineering intern, converting to full-time
**Income:** ₹27k/month after deductions
**Investable:** ₹5-6k/month — serious allocation (committed despite small absolute size)
**Next unlock:** Offer letter end of June 2026 → full-time salary → more capital for Stream 2
**Constraint:** Job takes most daily energy — don't suggest anything requiring 2+ hours/day outside work hours

---

## Stream 2 — Trading (Systematic Swing)

**Status:** System built, Telegram approval bot built, Angel One account created (2026-06-05). Zero live trades.
**Active instruments:**
- BTC/USD — regime NONE (EMA50 < EMA200). Scanner 00:30 UTC. Waiting for flip.
- XAU/USD (MCX Gold) — scanner 22:30 UTC. No signals fired yet. Execution via Angel One SmartAPI.
- EUR/USD — **GO** (legal via NSE futures, verified 2026-06-05). Cheapest instrument (~₹2,700/lot). **Scanner re-enabled 2026-06-12** with NSE sizing block on alerts (deploy = push life-os). Execution still pending Angel One currency segment. See [[FEMA Forex Legality]].
**Disabled:** USD/CAD — not listed on NSE cross-currency, no India-legal route.
**Execution layer:** Telegram approval bot built (`D:/trading_system/bot/`). Sends inline keyboard on signal. Runs two-layer pre-trade validation (circuit breakers → Perplexity). Angel One SmartAPI stub ready — fills when key arrives.
**Broker for automation:** Angel One (free SmartAPI, better docs than Finvasia, ₹20/trade flat — beats KiteConnect at ₹2,000/month)
**Cloud hosting:** Google Cloud Run — $300 credits expire 2026-09-04. Deploy at `asia-south1`.
**Target:** Angel One key → first live XAU trade → Cloud Run deploy

**Pending actions:**
- Angel One: generate SmartAPI key + enable TOTP + activate MCX & currency segments (account created)
- Add `PERPLEXITY_API_KEY` to `D:\trading_system\.env`
- Deploy bot to Cloud Run (see `docs/deploy.md`)

---

## Stream 3 — Content (Faceless)

**Status:** Niche **hypothesis defined** 2026-06-13 — see [[Content Niche]].
**Constraints:** No face, no voice, views/algorithm-based — all satisfiable. **"Not trading-related" is in tension** with the proposed edge; proposed revision → *"not trading-**advice**; the trading **system** is fair game as engineering proof."* Pending user confirmation.
**Niche hypothesis (Framing C, recommended):** AI-engineering / personal-agent-OS build-in-public, with the real-money trading system as recurring credibility proof (engineering, never signals). Edge: *"I built the AI second-brain these creators teach, then pointed it at a live trading account with the risk discipline the hype skips."*
**Next action:** Confirm the constraint revision → ship ONE artifact (the drafted lockbox post) → measure traction over ~2 weeks (falsifiable test). See [[Content Niche]].
**Claude's role:** Keep it engineering-framed, not finance-advice (SEBI/advisory + liability). Don't drift to generic "trending topic" advice.

---

## Stream 4 — AgriTech

**Status:** Idea only. Not started.
**Context:** Family owns agricultural land. AgriTech is high-potential in India — precision farming, government schemes, supply chain tech.
**Next action:** Assess what the land currently does and what specific problem is worth solving first.
**Claude's role:** When this activates, bring geopolitical + tech context ([[Geopolitics]], [[Tech Watch]]). Flag India-specific government schemes relevant to the land size and crop type.

---

## System Reminders

- **2026-06-06:** Claude account migration — **first verify `osaattrmpdrg@gmail.com` is on the Max/Opus tier** (existing account), then `claude logout` → `claude login` with it. Switch is pure upside if the plan tier matches; no local data is affected.
- **2026-06-10:** Delete `C:\Xilinx` on C: drive — `Remove-Item C:\Xilinx -Recurse -Force` (Admin PowerShell)
- **2026-08-28:** GCP billing audit before the **2026-09-04** credit cliff — delete running VMs, confirm nothing flips to paid, verify budget alert is set. See [[GCP Credits Strategy]].

## Action Queue (start here next session)

### Trading — Immediate (in order)
1. ~~Add `PERPLEXITY_API_KEY`~~ ✅ done (2026-06-06)
2. Run `python -m bot.handler` locally → test full approval flow via Telegram
3. **CoinDCX:** generate API key (Settings → API) → add to `D:\crypto_trading\.env` → `python smoke_coindcx.py`. Client built + tested 2026-06-06; on all-PASS, wire Phase 2 (route BTC → `coindcx_client` in `bot/execution.py`). See [[CoinDCX Execution Layer]].
4. Angel One (account created, KYC done): get SmartAPI key from `smartapi.angelbroking.com`, enable TOTP, activate MCX + currency segments
5. Add `ANGEL_ONE_API_KEY` to `D:\trading_system\.env`, uncomment SmartConnect block in `bot/execution.py`
6. Deploy the bot — **prefer webhook / scale-to-zero (Always Free)** over `--min-instances 1` so it's ₹0 and survives the credit cliff. See [[GCP Credits Strategy]].

### Edge / Research compute (GCP credits)
7. **[[Edge Generalization Sweep]]** — designed, build paused at design-review. Resume → spec → build (TDD) → Spot-VM burst. Funded by trial credits.

### Research — Run these via `/research-deep`
6. Run Research Queue **Run 1**: `"quantitative trading strategies commodities forex edge backtested 2024 2025"` — see [[Research Queue]]

### System
7. Verify morning brief 4-stream section in Telegram history

---

## Related

- [[North Star]] — the goal all four streams feed
- [[Trading System]] — full Stream 2 context
- [[What Didn't Work]] — don't re-propose rejected paths
- [[Chief Analyst]] — opportunity identification for Streams 3 and 4
- [[Geopolitics]] — macro context especially for Stream 4 (AgriTech)
- [[Tech Watch]] — technology signals relevant to content and AgriTech
