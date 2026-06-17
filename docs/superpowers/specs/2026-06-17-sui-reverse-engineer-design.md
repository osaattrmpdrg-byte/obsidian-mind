---
date: 2026-06-17
description: "Design spec — reverse-engineer a friend's crypto-futures entries to test (blind) whether his 75%-win-but-net-losing record hides a real entry edge or is pure exit-artifact. Understand → encode → validate, market as judge."
tags:
  - thinking
  - trading
  - spec
status: proposed
---

# SUI Reverse-Engineer — Design

Governed by [[Reverse-Engineer Before Apply]]. This is its first full application.

## Corrected premise (read first)

The original goal — "clone the friend's method to achieve similar results" — **is dead.** His full 1-year ledger (CoinDCX futures export, 100 closed trades, Apr 2025–Mar 2026) is **net −6.5 USDT after fees** with a **75% win rate** (not 85%): avg win **+2.0**, avg loss **−5.1**, worst **−67** (~3× his account). The high win rate is likely *manufactured by exit behaviour* (small TPs, held losers), not entry skill. He also traded multiple coins (SUI, ETH, BTC, MOODENG, KAITO, ETHFI), not just SUI.

**So the question is not "how do we copy him." It is:**

> Do his **winning** entries look different from his **losing** entries and from **random** moments — i.e. is there ANY real directional edge in his *entries*, or is the 75% win rate purely an artifact of how he exits?

If yes → his entry read + **our** risk management is a candidate. If no → confirmed no edge, we walk away having spent only research, not capital.

## What "reverse engineer" means here (grilled 2026-06-17)

**Both, in sequence:** Phase 1 understand the logic (I form independent blind reads and we cross-verify) → Phase 2 encode the understood logic as deterministic rules → Phase 3 validate OOS + forward paper. Understanding generates the hypothesis; statistics stop us fooling ourselves.

## Data layer

- **Price:** Binance public data (`data-api.binance.vision`, no auth, no geo-block) — confirmed to have 15m/2h/1d/1w history back through his trade dates, real volume. CoinDCX futures are Binance-mirrored, so this *is* the price he traded.
- **Coins:** all pairs in his ledger (SUI primary; ETH, BTC, MOODENG, KAITO, ETHFI). Plus BTCUSDT for cross-asset context.
- **Trades:** his 100 closed trades from the Excel — timestamp, pair, side, entry/exit, gross/net P&L, fees.

## Phase 1 — Blind entry test (the core)

**Blind set** = his **winning** entries + his **losing** entries + **random decoy timestamps** he didn't trade — all *shuffled and unlabeled*. (Decoys force me to *reject* non-setups; losses in the mix expose whether his bad entries looked different. Without both, "is this a setup" leaks.)

**Truncation (structural blindness):** for each item, the harness renders the chart and computes numbers **only up to the last closed bar before the entry timestamp.** All future bars, his trade details, and the outcome are stripped from the artifact. The future is never in my context at prediction time — blindness is structural, **not** "trust me to not peek" (explicitly rejected: an LLM cannot ignore data already in its context).

**What I analyse:** rendered multi-timeframe candlestick charts (W/D/2h/15m, with VWAP + volume) **and** the exact numeric context (VWAP distance, nearest S/R, volume ratio, BTC state). Pattern read backed by levels.

**What I commit (per item, before any reveal):** `{ is_setup: bool, direction, entry_zone, target, stop, confidence 1–5, rationale }`. The rationale is the raw material for Phase 2.

**Scoring — market is the judge:**
- **Primary:** simulate *my* committed calls (entry/target/stop) on the forward bars → expectancy. Is **my** independent read +EV?
- **Diagnostic (secondary):** agreement with his actual entries — am I converging on his logic? Not the target; matching a net-losing trader is worthless.

**The four outcomes and what each means:**

| My read +EV? | Distinguishes his W from L / decoys? | Verdict |
|---|---|---|
| Yes | Yes | Real entry edge — proceed to Phase 2 with his entry + our exits |
| Yes | No | *I* found an edge his entries don't have — keep mine, drop him |
| No | Yes | His entries differ but aren't profitable — no tradable edge |
| No | No | **Win rate was pure exit-artifact — walk away** (most likely given the ledger) |

## Phase 2 — Encode (only if an entry edge survives Phase 1)

Turn the understood logic (from rationales + what separated W/L/decoys) into a **small (2–4 condition) deterministic rule**. No discretion, no LLM in the signal path (per [[Trading System]] hard rules).

## Phase 3 — Validate (gate before any capital)

OOS backtest (Wilson-gated, trial-count penalty, base-rate contrast) on SUI dates outside his trades + forward paper-trade as a scanner alert. Only then "incorporate" — and "incorporate" = **his entry read + our disciplined trailing exit + our position sizing**, de-levered, paper → small live. Never his 6×-full-account sizing.

## Guardrails

- **n and asymmetry:** even 100 trades is thin once split W/L/decoy; treat every extracted rule as hypothesis until Phase 3.
- **Exit-artifact trap:** the whole point — a high win rate can exist with zero entry edge. Phase 1 is designed to detect exactly this.
- **The read may not be in OHLCV:** if W, L, and decoys are indistinguishable to me, the honest conclusion is "no mechanizable entry edge," and we stop.
- **No imported conclusions:** web/influencer claims (and even my own beta measurements) are kept OUT of this spec — I form conclusions blind from the data, then we cross-verify. (Per Dileep, 2026-06-17.)

## Related

- [[Reverse-Engineer Before Apply]] — the governing protocol
- [[Trading System]] — where a validated rule would land; hard rules
- [[What Didn't Work]] — the overfitting / survivorship traps this guards against
- [[Binding Constraint First]] — the binding constraint is integrity of the read