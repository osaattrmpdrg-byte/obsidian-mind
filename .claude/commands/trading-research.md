---
description: Answers trading strategy questions from accumulated vault research — routes to Perplexity only when vault has a genuine gap or the question is tactical/real-time
category: research
triggers_en: ["trading research", "strategy research", "what do I know about", "trading question", "should I use this strategy"]
---

Execute `/trading-research [question]`:

The smart routing layer between vault knowledge and paid APIs. Never calls Perplexity for what the vault already knows. Never uses stale vault knowledge for live trade decisions.

## Step 1 — Classify the question

**Is this Tactical (real-time, trade-critical)?**

Tactical signals: "right now", "today", "should I enter", "current regime", "what's happening with", "pre-trade", "before I place".

→ If tactical: skip the vault entirely. Run immediately:
```
/research "[instrument] current market conditions [today's date]"
```
Then synthesize the result for the trade decision. Do not delay. Do not check vault first.

**Is this Strategic (stable knowledge, not time-sensitive)?**

Strategy signals: "what strategies", "how does", "which approach", "what works for", "parameters for", "explain".

→ Proceed to Step 2.

---

## Step 2 — Search vault exhaustively (Strategic questions only)

Search in order:
1. QMD semantic search: `mcp__qmd__query` with the question
2. Search `reference/research/deep/` for relevant research notes
3. Search `reference/research/notebooklm/` for synthesis notes
4. Search `reference/trading/` (Chief Trader, Signal Matrix, instruments)
5. Read `brain/Trading System.md` and `brain/What Didn't Work.md`

Enumerate ALL matching notes — do not sample.

---

## Step 3 — Synthesize from vault

If vault has relevant content:
- Synthesize the answer with citations to `[[vault notes]]`
- Note the date of each source (recency marker) — flag if older than 6 months
- Cross-reference `brain/What Didn't Work.md` — if the strategy was tested and rejected, say so immediately

If vault answer is complete → deliver it. No API call.

---

## Step 4 — Gap detection

If the vault does not have a satisfying answer:

1. State clearly what the vault knows and what is missing
2. Classify the gap:
   - **New domain** (never researched): Suggest adding to [[Research Queue]], run via `/research-deep`
   - **Stale knowledge** (vault note older than 6 months on a regime-sensitive topic): Suggest a targeted refresh
   - **Tactical gap** (realised mid-synthesis that current data is needed): Switch to tactical mode, run `/research` immediately

3. Provide the exact suggested query:
   ```
   Suggested: /research-deep "[precise query to fill this gap]"
   ```

4. Estimated cost: "~$0.20-0.80 for deep research, ~$0.02-0.05 for single query"

---

## The ROI Rule

Before every suggested API call, state the ROI case:
- Strategic: "This fills a permanent knowledge gap. One spend, reused indefinitely."
- Tactical: "This is pre-trade intelligence. Cost of bad trade >> cost of this call."
- Decline: "Vault already covers this. No API needed."

---

## Anti-fabrication

Never invent trading strategies, backtested results, or performance claims. If the vault doesn't have it and no API call is warranted, say "I don't have current data on this — add to Research Queue or run `/research`." A confident wrong answer on a trading question costs real money.
