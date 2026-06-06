---
date: 2026-06-05
description: "Spec for the daily strategy-discovery system — Daily Watch (monitor the one proven edge) + Weekly Hunt (disciplined candidate vetting gated by lockbox + cross-instrument confirmation). Replaces the rejected 'daily strategy generator' idea."
tags:
  - work-note
  - trading
status: active
quarter: Q2-2026
---

# Daily Watch, Weekly Hunt

The disciplined replacement for "run a daily sweep to find strategies." Designed in a [[grill-me]] session on 2026-06-05 that exposed the original idea as a curve-fitting machine.

## The Reframe (why the original idea was wrong)

The first ask was: *generate new strategies daily + backtest them.* The vault contradicted it:

- [[Trading System]] shows **one** validated edge (20-bar breakout + EMA regime), found after [[What Didn't Work|rejecting ~10 variations]].
- Hard rules: *"No complexity before the simple version is validated"*, *"frequency < 4 trades/year is unvalidatable."*
- The real bottleneck is **capital (₹5-6k) + execution (KYC, paper-trade gates, deploy)** — not a shortage of ideas. Trading returns ≈ 10.8%/yr; salary injection is the multiplier ([[North Star]]).

> [!danger] The trap this design avoids
> Mass-testing freely-generated strategies through a single-strategy gate (Wilson CI > 33.3% train+test) **manufactures false edges**. Test 100 candidates and several pass by pure luck — the multiple-comparisons / data-snooping problem. That "winner" then dies live. Testing more strategies does not find more edges; it finds more lucky noise.

## Component 1 — DAILY WATCH (automated, ~2-min read)

Monitors the **one proven edge**. Invents nothing. Cannot produce slop.

Each morning, surface three things:
1. **Regime state** — Has BTC EMA50 crossed above EMA200 yet? (Currently NO — EMA50 $76.8k < EMA200 $81.7k. The flip is the BTC go-live trigger.) Same check for [[XAU_USD|gold]].
2. **Signal fired?** — Yes/no, which instrument. (Deterministic — stays in the GitHub Actions scanner per the *"no LLM in the signal pipeline"* rule.)
3. **Macro context** — BTC/ETH/gold moves + anything regime-relevant, via the **CoinGecko MCP** (added to `.mcp.json` 2026-06-05, free/keyless data).

The deterministic regime+signal check is already built (`scanner.py`, GitHub Actions). Claude's daily add is reading that output + CoinGecko macro into a short brief.

## Component 2 — WEEKLY HUNT (one candidate at a time, never a firehose)

New strategy discovery — kept slow and gated. Candidate sources: **literature-mined** (`/research`, `/research-deep`, arXiv/SSRN) + **open brainstorm**. Novelty is allowed; the gauntlet is what keeps it honest.

### The gauntlet (every candidate, in order)
1. **Rationale first** — one-sentence economic/market-structure reason, logged *before* any backtest. No rationale → rejected. (This is *"state the edge in one sentence"* applied to generation.)
2. **Train backtest** — on training data only.
3. **Cross-instrument confirmation** — the *same* edge must appear on **3+ independent instruments** (e.g. BTC, gold, EUR/USD). Luck doesn't repeat across three markets; a real mechanism does.
4. **The Lockbox** — a held-out slice of history (recent ~2-3 yr, or one fully held-out instrument) the generator **never** sees. A candidate touches it **once**, and only after passing 1–3. The number of lockbox shots is capped.
5. **Trial-count penalty** — track N = total candidates ever tested. Raise the pass bar as N grows (deflated Sharpe / Bonferroni intuition). This counter is what stops 200 random ideas from sneaking a lucky winner through.

### Discipline
New strategies are a *"nice problem to have" — after* the proven edge is earning. Until BTC flips and gold/EUR-USD are live + paper-trade-gated, the Hunt stays weekly and small.

## Open / To Build

- [ ] Daily Watch brief format + where it lands (Telegram? daily note? vault brief?)
- [ ] Wire Daily Watch cadence (candidate: `/schedule` daily, or extend existing GitHub Actions)
- [ ] Implement the Lockbox: carve a held-out data slice in `D:\crypto_trading` / `D:\trading_system` that backtests never touch — via `/plan` → `/code-review`
- [ ] Implement the trial-count register (N + bar-raising rule)
- [ ] Define cross-instrument confirmation harness (run candidate on BTC + XAU + EUR/USD)
- [ ] First Hunt candidate: pull from [[Research Queue]] Run 1 (broad strategy scan)

## Related

- [[Trading System]] — the proven edge this protects and extends
- [[What Didn't Work]] — the rejection log that justified the reframe
- [[Research Queue]] — source of literature-mined Hunt candidates
- [[North Star]] — the ₹7-8L goal; capital + execution is the real bottleneck
- [[Streams]] — trading is Stream 2
- [[Signal Matrix]] — live-decision confidence matrix
