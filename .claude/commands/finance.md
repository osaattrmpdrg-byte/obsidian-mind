---
description: Pre-trade brief via Perplexity Finance Search -- live level, macro catalysts, technical context, and risk flags for an instrument. Tier-1 tactical; self-logs to the api-usage ledger.
category: research
triggers_en: ["finance brief", "pre-trade brief", "what's moving", "market context for", "before I trade", "/finance"]
---

Execute `/finance [instrument-or-question]`:

The qualitative CONTEXT layer ahead of a trade. Pulls live quotes, fundamentals,
earnings, FX, and cited news via Perplexity's `finance_search` tool, then saves
an AI-first pre-trade brief to `Research/Finance/`.

This is NOT an execution price source -- broker feeds (Angel One, CoinDCX,
CoinGecko MCP) are authoritative for the price you trade on. Use `/finance` for
the macro/news/catalyst context those feeds do not carry.

## Step 1 -- Gate (api-decision-framework)

A pre-trade brief is **Tier 1 (tactical, real-time, trade-critical)**. The rule:
never be cheap on critical-path-of-a-trade information. Verdict is always **PAY**
-- run immediately, do not check the vault first. The cost of a bad trade dwarfs
the ~$0.005 call.

The script self-logs the call to `brain/api-ledger.jsonl`, so you do NOT need to
run `audit.py record` separately for `/finance`. (See the `api-usage` skill.)

## Step 2 -- Run

```bash
cd /d "d:\projects\obsidian-second-brain" && uv run -m scripts.research.finance "<instrument-or-question>"
```

Examples:
- `/finance XAU/USD gold` -- gold pre-trade context
- `/finance BTC/USD` -- crypto macro/catalyst read
- `/finance NVDA earnings setup` -- equity event brief

The script prints the brief, saves the note, logs the call, and prints save links.

## Step 3 -- Use it for the decision

Surface the brief tied to the trade at hand. Cross-reference [[Signal Matrix]]
and [[Daily Watch Weekly Hunt]]. If the brief contradicts a fired signal (e.g. a
high-impact event inside the holding window), say so before the user acts.

## Anti-fabrication

The brief is sourced market data with recency markers -- treat every figure as a
snapshot and flag anything stale. Never invent levels, catalysts, or earnings
dates. If `finance_search` returns thin data, say so plainly rather than padding.

## Related

- `/trading-research` -- routes STRATEGY questions to vault-first knowledge; use that for "what works", this for "what's happening right now".
- `/research` -- general web dossier when the question is not finance-specific.
