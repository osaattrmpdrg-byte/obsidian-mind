---
date: 2026-06-05
description: Prioritized research runs ordered by ROI to the ₹7-8L passive income goal — trading first, AgriTech second, content third
tags: [brain, research, trading]
---

## For future Claude
This is the ordered research queue. Run in sequence — each run builds on the last. Before running any query, check if the vault already has the answer via `/trading-research`. Only run if there's a genuine gap. See [[api-decision-framework]] for when to use API vs vault.

---

## Trading Strategies Queue (Run First)

These 4 runs build the strategic knowledge base for trading. Run via `/research-deep` (Perplexity paid mode + vault scan).

- [ ] **Run 1 — Broad strategy scan**
  Query: `"quantitative trading strategies commodities forex edge backtested 2024 2025"`
  Goal: Map the landscape of what actually works across instruments
  Save to: `reference/research/deep/`

- [ ] **Run 2 — India-specific angle**
  Query: `"mean reversion momentum regime detection strategies India NSE MCX 2024 2025"`
  Goal: Filter for what applies to Indian markets and MCX specifically
  Save to: `reference/research/deep/`

- [ ] **Run 3 — F&O retail edge**
  Query: `"futures options F&O quantitative strategies retail trader India backtested 2024 2025"`
  Goal: Find F&O-specific approaches available to a retail trader
  Save to: `reference/research/deep/`

- [ ] **Run 4 — XAU instrument deep dive**
  Query: `"XAU USD gold regime classification signal strategy quantitative 2024 2025"`
  Goal: Circle back to the live instrument with full context from runs 1-3
  Save to: `reference/research/deep/`

**After all 4 complete:** Run `/notebooklm "trading strategy synthesis"` to produce one master note from all 4 (Gemini, near-free). This becomes the anchor for `/trading-research`.

---

## AgriTech Inspiration Queue (Run After First Live Trade)

2 calls max. Goal: find the spark for a product idea, not deep domain expertise.

- [ ] **Run 1 — Market scan**
  Query: `"Indian AgriTech startup problems gaps opportunities 2024 2025 founder"`
  Goal: What problems exist, what's being built, what's missing

- [ ] **Run 2 — Success patterns**
  Query: `"successful AgriTech products India case studies unit economics farmers"`
  Goal: What's actually working and why

**After both:** Run `/obsidian-connect "AgriTech" "trading"` (free) to find an angle that intersects with skills you already have.

---

## Content Queue (Run Last)

- [ ] **Run 1 — Positioning scan**
  Query: `"finance trading content creator India audience 2024 2025 what works"`
  Goal: Find where there's an underserved audience for your specific knowledge

---

## Tactical Research (No Queue — Run On Demand)

These are never queued. Run immediately when needed before a trade:
- Pre-trade macro context for any live position
- Current regime assessment for active instrument
- Breaking news affecting open positions

See [[api-decision-framework]] — Tier 1, always spend.

---

## Parked — Phase 2 (do NOT run until the simple version is live)

- [ ] **Multi-indicator confidence scoring** *(parked 2026-06-13)*
  Idea: require N-of-M confirming indicators above a confidence threshold before a trade qualifies, and grade conviction for position sizing.
  **Why parked, not rejected:** the *naive* form is a known trap — see [[What Didn't Work#Daily Strategy Generator (2026-06-06)]]. Most TA indicators are derived from the same price + moving averages, so "5 indicators agreeing" is one signal wearing five hats (correlated votes ≈ 1× confidence, not 5×), and inventing a "75%" threshold violates the hard rule *"never propose scoring weights without backtest calibration."*
  **The only honest path to un-park it:** test confirming filters **one at a time** through the [[Daily Watch Weekly Hunt]] rail — rationale-first → does it beat the bare breakout (adj R + Wilson CI, train AND test) *net of trades removed* → never-touched lockbox → trial-count penalty. A filter earns a place in the [[Signal Matrix]] confidence score only after surviving that gate.
  **Un-park trigger:** simple version live (paper gate cleared, see [[Trading System#Path to Live]]) AND a confirming filter has a one-sentence edge worth testing.
  **First scan run (2026-06-13):** tested 4 filters one-at-a-time on EUR/USD + XAU (overextension guard, higher-TF alignment, ADX>25, volume). Result: most failed (overextension *destroyed* XAU test, −0.557R; HTF/volume mixed); ADX>25 looked best under a fixed-TP exit but **the whole experiment hit a wall** — the bare baseline doesn't reproduce the vault's proven numbers under the live exit (see [[Gotchas#Backtest reproducibility]]), so no filter can be honestly judged yet. **The indicator question is blocked on baseline reconciliation, not on filter choice.**
