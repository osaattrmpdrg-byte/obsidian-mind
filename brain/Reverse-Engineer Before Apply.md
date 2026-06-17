---
date: 2026-06-17
description: "Standing research protocol — any externally-sourced strategy (web, YouTube, influencer, a friend's record) is a HYPOTHESIS until reverse-engineered from evidence, mechanized, backtested out-of-sample, and validated forward. Never apply on the claim."
tags:
  - brain
  - trading
  - method
aliases:
  - Strategy Research Protocol
  - Reverse-Engineer Backtest Apply
  - Reverse-Engineer Before Believe
---

# Reverse-Engineer Before Apply

> [!important] The rule
> **No externally-sourced strategy gets applied on the strength of its claim.** A YouTube video, a web article, an influencer's calls, a friend's track record, a "this works" — all of it is a **hypothesis**, never an edge, until it has been reverse-engineered from *evidence*, mechanized into deterministic rules, backtested out-of-sample, and validated forward. The highlight reel is not the expectancy. See [[North Star]] — Edge Before Action.

This is **the** way to handle strategy research — especially web/YouTube sourcing, where the signal-to-hype ratio is worst and where Claude's capability is needed most. Don't summarize the claim; *interrogate it against data*.

## The Protocol

1. **Source the claim** — capture exactly what is asserted (entry, exit, instrument, the "why"). Strip the narrative down to a testable statement.
2. **Gather labeled evidence, not the story** — actual trades, timestamps, examples, screenshots, a track record. A claim with no evidence to reverse-engineer stops here as unfalsifiable.
3. **Reconstruct the situation** — rebuild the chart/market state at each example moment from real data (OHLCV, indicators, cross-asset context). Extract a deterministic feature vector: "what was true when it fired."
4. **Find the common signal against the BASE RATE** — a feature only counts if it's far more frequent at the real entries than at random times. Without the base-rate contrast you "discover" things that are always true. Keep the resulting rule **small** (2–4 conditions).
5. **Validate before believing** — out-of-sample backtest (Wilson-gated, trial-count penalty) **and** forward paper-trade. Both, or it stays a hypothesis.
6. **Only then apply** — and with de-levered sizing, paper → small live. Promote into the system ([[Trading System]] / Signal Matrix) only after it passes.

## Guardrails (where this goes wrong)

- **Tiny-n overfitting** — with few examples and many candidate features, *something* always "explains" them and dies forward. This is the data-snooping trap that killed the Daily Strategy Generator (see [[What Didn't Work]]).
- **Survivorship / positive-only** — wins-only records hide the *skips* and the *losses*, which is where the real filter lives. Demand the losers; they're the most informative labels.
- **The read may not be in the data** — if reconstruction can't separate real entries from random moments, the honest conclusion is "not mechanizable from price data," and that's a valid result, not a failure.
- **Influencer incentive** — content exists to attract, not to be correct. Treat track records as marketing until verified.

## Why

Consensus and influencer claims are, by definition, already priced in or unproven — no edge in repeating them ([[North Star]] — First Principles Over Consensus). The only durable advantage is converting a *claim* into a *measured expectancy*. This protocol is the [[Binding Constraint First]] discipline applied to research: the binding constraint is almost never "find more ideas," it's "prove the one in front of you."

## First application

The SUI reverse-engineering project (reconstruct a friend's actual trades → mechanize the setup → walk-forward + paper validate) is the template case — spec: `docs/superpowers/specs/2026-06-17-sui-reverse-engineer-design.md`.

## Related

- [[North Star]] — Edge Before Action, First Principles Over Consensus
- [[What Didn't Work]] — the data-snooping / overfitting failures this prevents
- [[Binding Constraint First]] — prove the one idea, don't chase more
- [[Trading System]] — where validated strategies land
- [[Research Queue]] — research runs this protocol governs