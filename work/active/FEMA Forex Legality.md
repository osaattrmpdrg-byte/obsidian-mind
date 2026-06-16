---
date: 2026-06-05
description: "Can EUR/USD and USD/CAD breakout signals be traded legally from India? The offshore-broker vs NSE-currency-derivatives distinction, CA consultation questions, and decision log."
tags:
  - work-note
  - trading
  - legal
status: active
quarter: Q2-2026
---

# FEMA Forex Legality

**The question:** Can I legally trade my [[Trading System|backtested]] EUR/USD (+0.131R, SIG train+test) and USD/CAD signals from India? These are currently **disabled** in the vault as a "FEMA grey area" — but that framing may conflate two very different things.

> [!success] Core legality VERIFIED (2026-06-05 research)
> Perplexity Sonar research confirmed against primary sources: **SEBI Circular CIR/MRD/DP/20/2016 (31 Mar 2016)** permits EUR/USD, GBP/USD, USD/JPY futures + options on NSE — still in force, no rescinding circular. EUR/USD futures = 1,000 EUR lot, INR-settled, ~3% margin (~₹2,000-3,000/lot). Offshore brokers confirmed illegal under LRS Schedule III. CA consultation now narrows to **tax + personal application**, not the legality question itself.

> [!warning] Not legal advice
> Regulatory structure is now `[VERIFIED]` from research. But your *personal* tax treatment, audit thresholds, and reporting still need a CA's read on your specific situation. Do not skip the CA — just walk in already knowing the legality answer.

> [!tip] CAN we make EUR run? Vehicle = YES (EUR/INR), edge = marginal (2026-06-16)
> "Make EUR/USD run" hunt. **The vehicle problem is solvable: trade EUR exposure via EUR/INR**, which is legal AND liquid — NSE near-month **EUR/INR = 2,799 lots/day, GBP/INR = 5,198, both 0 flat days** (vs EUR/USD-direct 92 lots, flat half the days; JPY/INR dead at 18). ~1-3 paise spread (~0.04R) fits the headroom.
> **BUT the edge on EUR/INR is weak + fragile**, so the vehicle being fixed doesn't make it worth trading: EUR/INR breakout adjR full **+0.066** / recent 2021-26 **+0.140**, but **tail-fragile — drop the top 1 winner → +0.014, top 2 → NEGATIVE** (rests on ~1-2 trades of 124). GBP/INR weaker. Both confounded by ~3%/yr INR-depreciation drift. The 2-leg synthetic EUR/USD was **−0.126 (dead)**. Script: `D:\trading_system\validate_inr_vehicle.py`.
> **Verdict:** *we can make it run, but shouldn't* — EUR/INR is a marginal, fragile, drift-confounded edge, not worth real capital next to **BTC's robust +1.686R** ([[Trading System#CRYPTO REVALIDATION]]). If ever pursued, EUR/INR must earn its OWN gate + drift control first (it does not inherit EUR/USD's numbers — it's a different, INR-blended edge).

> [!failure] LEGAL ≠ LIQUID — the decisive correction (2026-06-16, `[VERIFIED]` from real Angel One data)
> EUR/USD is legal on NSE, but the **NSE EUR/USD cross-currency future is effectively untradeable**: real Angel SmartAPI data shows the near-month (peak liquidity) trades **~92 lots/day with flat single-print OHLC on half the days**, diverging **11–36 pips from spot** — more than the edge's entire 21-pip slippage headroom. Control: **USD/INR = 312,614 lots/day** (~3,400× more). All NSE cross-currency futures (EUR/USD, USD/JPY, GBP/USD) are equally thin; only **USD/INR** has real depth. **So the FEMA "GO" was correct on legality but moot on tradeability — there is no liquid vehicle for the EUR/USD edge.** The only liquid+legal NSE FX future (USD/INR) has no *working* edge in the current regime. See [[Trading System#GATE 2b]]. Action: disable the EUR/USD scanner; this note's "execute" conclusion is superseded for EUR/USD.

---

## The Core Distinction (what most people get wrong)

Two completely different activities both get called "forex trading" — and they have opposite legal status:

| Route | Legal status | Why |
|-------|-------------|-----|
| **Offshore forex broker** (OANDA, IC Markets, Exness, etc.) | ❌ **Illegal** for Indian residents | Funding an overseas margin forex account is a *prohibited* use of the LRS |
| **NSE currency derivatives** (Indian exchange, SEBI broker) | ✅ **Legal** | Exchange-traded, INR-settled, explicitly permitted by RBI |

`[HYPOTHESIS]` The vault's "grey area" label probably came from the (correct) knowledge that *offshore* forex trading is illegal — and wrongly concluded that EUR/USD is *untradeable*. But EUR/USD is available as an exchange-traded derivative on the NSE.

---

## Why offshore brokers are illegal

`[HYPOTHESIS — confirm with CA]`

- The **Liberalised Remittance Scheme (LRS)** lets a resident remit up to **$250,000/year** abroad — but only for *permitted* purposes.
- **Schedule III of FEMA** explicitly **prohibits** remittance for *"margin or margin calls to overseas exchanges / overseas counterparties"* and for trading foreign exchange abroad.
- So you legally **cannot** fund an OANDA/Exness-type account for margin forex trading. RBI has also publicly flagged unauthorized electronic trading platforms (ETPs).
- This is the part that is genuinely illegal — and it's what gives "forex trading in India" its bad reputation.

---

## Why NSE currency derivatives are legal

`[HYPOTHESIS — confirm with CA]`

- In **2015**, RBI/SEBI permitted **cross-currency futures and options** on Indian exchanges: **EUR/USD, GBP/USD, USD/JPY** (in addition to the INR pairs: USD/INR, EUR/INR, GBP/INR, JPY/INR).
- These are **SEBI-regulated, exchange-traded, and settled in INR** based on the RBI reference rate — no money leaves the country, no overseas margin.
- Traded through a normal Indian broker's **currency segment** — including **[[XAU_USD|Angel One]]**, which already supports it.

**Implication:** If this still stands (needs current-date confirmation), EUR/USD comes back online as a tradeable signal — through the *same broker* you're already setting up for MCX gold.

---

## What this means for my specific signals

| Signal | Backtest | NSE availability | Verdict if confirmed |
|--------|----------|------------------|---------------------|
| **EUR/USD long** | +0.131R, SIG train+test (best forex signal) | ✅ EUR/USD futures on NSE | **Unlocked** — re-enable |
| **USD/CAD short** | +0.054R, SIG train+test | ❌ Not on NSE cross-currency list | Stays blocked |
| GBP/USD | Rejected (Brexit/Truss) | ✅ Available | Irrelevant — signal failed |
| USD/JPY | Rejected (BoJ) | ✅ Available | Irrelevant — signal failed |

So the realistic unlock is **EUR/USD only** — but that's your single best-validated forex edge, so it matters.

---

## Margin math (does it fit ₹5-6k?)

`[HYPOTHESIS — confirm exact contract specs with CA / Angel One]`

- NSE EUR/USD futures contract size: **1,000 EUR**
- At ~1.08 → ~$1,080 → **~₹90,000 notional** per lot
- Currency futures margin ~**3%** → **~₹2,700 per lot**
- **Verdict:** one lot is fundable at ₹5-6k capital. Far more accessible than [[XAU_USD|MCX Gold]] (~₹70k/lot).

This makes EUR/USD potentially the **most capital-accessible live instrument** of everything in the system.

---

## Execution fit with the existing system

- Scanner already fires on daily EUR/USD **spot** close — NSE EUR/USD futures track spot, so the signal translates directly.
- NSE currency derivatives hours: **9:00 AM – 5:00 PM IST**, Mon-Fri → place the order the morning after the signal fires.
- Same Angel One SmartAPI execution path being built for gold — just the currency segment instead of MCX.

---

## Questions for the CA

1. **Is the 2015 cross-currency derivatives permission still in force?** Can a resident individual trade EUR/USD futures/options on NSE today?
2. **Confirm offshore is out:** Is funding an overseas forex broker via LRS still prohibited under Schedule III? (Sanity check the hard boundary.)
3. **Tax treatment:** How are gains on NSE currency derivatives taxed — speculative business income, non-speculative business income, or capital gains? STT applicability?
4. **Any per-individual limits** on currency derivative positions for residents?
5. **Reporting:** Anything I need to disclose (ITR schedules, etc.) for currency derivative trading?
6. **USD/CAD:** Confirmed not available on any Indian exchange? Any legal route at all, or permanently blocked?

---

## Decision Log

| Date | Status | Note |
|------|--------|------|
| 2026-06-05 | Note created | Reasoning hypothesis-stage. |
| 2026-06-05 | **Legality VERIFIED** | Research confirmed SEBI 2016 circular still in force. EUR/USD legal on NSE. |
| 2026-06-05 | **GO — CA waived** | Decision: proceed with EUR/USD. CA consultation waived as disproportionate at current scale (1 lot, ~18 trades/yr, tiny tax stakes, legality already verified). Downside of skipping = small/known/reversible (worst case: file ITR-3, report broker P&L; far below 44AB audit threshold). **Revisit CA when scaling up** (multiple lots / salary converted / new instruments). EUR/USD moves DISABLED → PENDING (paper-trade gate still required before live). |
| 2026-06-12 | **EXECUTED** | Scanner re-enabled for EUR/USD (PAIRS in `scanner.py`), NSE futures sizing block added to alerts, FX callback precision fixed, brief memory de-staled. Committed in life-os repo — push pending user. See [[Trading System]] for the remaining path (segment activation → paper → live). |

> [!info] CA revisit trigger
> Re-book the CA when trading materially bigger — multiple lots, post-salary-conversion capital, or adding instruments. At that point the business-income tax mechanics (audit threshold, ITR-3 bookkeeping, salary interaction) start to matter. Not now.

---

## Related

- [[2026-06-05 - is it legal in 2026 for a resident individual in india to trade eurusd gbpusd us]] — source research this verdict rests on
- [[Trading System]] — EUR/USD + USD/CAD currently disabled here; update if CA confirms
- [[What Didn't Work]] — forex "category closed" conclusion is conditional on this note's outcome
- [[XAU_USD]] — same Angel One execution path; currency segment vs MCX
- [[Streams]] — Stream 2 (trading); unlocking EUR/USD adds a capital-accessible instrument
- [[North Star]] — re-enabling the best-validated signal moves toward the goal
