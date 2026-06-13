---
date: 2026-06-05
description: When to hit a paid API vs use Claude's knowledge — governing rule for all API credit decisions across trading, AgriTech, and content
tags: [reference, research, framework]
---

## For future Claude
This is the governing framework for API credit decisions. Read this before deciding whether to call Perplexity, Gemini, or use vault knowledge. The core rule: never be cheap on information that is in the critical path of a trade. Every other API call should be scrutinized.

> [!tip] Operational layer
> This note is the *source of truth* for the tier logic. The `api-usage` skill operationalizes it — it gates each call against these tiers, logs the decision to `brain/api-ledger.jsonl`, and audits spend + ROI drift. See [[Skills#Operational Skills (Skill tool, not slash commands)]].

---

## The Governing Rule

**API spend should translate to money.** Every credit spent is an investment. The question before every call: "Does this information directly improve a decision that has financial consequences?"

- If yes → spend without hesitation
- If no → check vault first

A bad trade from stale data costs 100x more than one Perplexity call. Never optimize the wrong thing.

> [!info] Subscription-side constraint
> This framework governs *external API* spend (Perplexity, Gemini, etc.). For *Claude's own* token economics — the separate interactive vs Agent SDK credit pools, and why autonomous Claude work has its own monthly ceiling — see [[Claude Subscription Billing]]. Pro = $20/mo for all non-interactive Claude usage.

---

## Tier 1 — Tactical (Always Hit API, No Compromise)

These questions are in the critical path of a live trade decision. Stale information here costs real money.

**Use Perplexity (`/research`) immediately:**
- Current market regime — "Is XAU trending or ranging this week?"
- Pre-trade macro context — "What is driving gold right now before I enter?"
- Breaking developments — "What just happened with Fed/RBI/crude that affects my position?"
- Instrument-specific current data — "What are current XAU options flows/sentiment?"

**Use `/x-pulse` (when Grok added):**
- Real-time discourse on an instrument — "What are traders saying about gold right now?"

**Rule:** Never delay a tactical query to save credits. The cost asymmetry is always in favor of spending.

---

## Tier 2 — Strategic (Research Once, Reuse Forever)

These questions have answers that are stable for months. Research once, save to vault, reuse via `/trading-research`.

**Research once via `/research-deep`, then use vault:**
- Strategy fundamentals — "What mean reversion parameters work on commodities?"
- Instrument structure — "What are the key macro drivers of XAU long-term?"
- Domain landscape — "What are the F&O strategies that work for retail traders in India?"
- Market structure — "What does regime detection look like in practice?"

**Research once via `/research`, then use vault:**
- AgriTech market landscape (2 calls max before having a hypothesis)
- Content strategy landscape (1 call max)

**Rule:** Before running a strategic query, always check the vault first via `/trading-research` or QMD search. If the vault has it, don't call the API.

---

## Tier 3 — Claude Only (Never Call API)

Claude's training covers these completely. No API needed.

- Definitions — "What is mean reversion?" "How does RSI work?"
- Math and statistics — "How do I calculate Sharpe ratio?"
- Code implementation — "Write a backtest for this strategy"
- Vault operations — organizing notes, writing summaries, creating links
- Reasoning over information already in the vault

**Rule:** If the question could be answered by a textbook, don't call an API.

---

## Decision Tree (Quick Reference)

```
Is this question in the critical path of a live trade?
    YES → Hit Perplexity immediately. No compromise.
    NO  → Is the answer time-sensitive (changes week to week)?
              YES → Check vault first. If stale or missing → hit Perplexity.
              NO  → Is it in the vault already?
                        YES → Use vault (free).
                        NO  → Is it a foundational concept?
                                  YES → Claude knows it. No API.
                                  NO  → Add to Research Queue. Run when ready.
```

---

## The Compounding Pattern

```
Week 1:  4x Perplexity runs (strategic research queue) → 4 vault notes
Week 2:  1x Gemini /notebooklm synthesis → 1 master synthesis note (near-free)
Week 3+: /trading-research answers questions from vault → $0 per query
Month 2: Only NEW gaps get a Perplexity call — vault handles the rest
```

Each Perplexity credit buys permanent knowledge. Over time, the vault answers more and Perplexity is called less — except for Tier 1 tactical queries, which never go stale.

---

## Research Queue Priority

See [[Research Queue]] for the ordered list of strategic research to run.
Current status of each stream:
- Trading: 4 queries queued (commodities/forex/F&O strategies + XAU specific)
- AgriTech: 2 queries queued (run after trading is live)
- Content: 1 query queued (run last)
