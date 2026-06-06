---
date: 2026-06-05
description: "Signals and approaches tested and rejected — with WHY and what each failure implies. Read before proposing anything new."
tags:
  - brain
  - trading
---

# What Didn't Work

Read this before proposing any new signal, strategy, or architecture. Each entry has the failure reason and what it implies for future directions. This is the learning layer — not just a rejection log.

---

## Trading Signals — Rejected

### RSI Recovery Signal
- **What:** RSI < 42 within 7 bars, entry on recovery
- **Result:** adj = -0.067R without strict regime. With strict regime: adj = +0.225R but only 1.6 trades/year
- **Why:** RSI recovery in downtrend = catching falling knives. Even with strict filter, frequency is too low to validate statistically
- **Implies:** Frequency < 4 trades/year is unvalidatable in a reasonable timeframe. RSI entries need strict regime filter at minimum.

### Fixed 2:1 R:R Take Profit (Breakout)
- **What:** Fixed TP at 2× SL distance instead of trailing stop
- **Result:** WR = 29.6% — too low
- **Why:** FX mean-reverts. Price often reaches TP area then pulls back. Fixed TP misses the full momentum burst.
- **Implies:** Trailing stop is structurally better for FX breakout entries. Never use fixed TP on FX momentum signals.

### Trailing Stop 10–30 Bars
- **What:** Held trailing stop longer (10-30 bars) vs 5-bar
- **Result:** avg_win = 0.83–1.45R — lower than 5-bar
- **Why:** Momentum bursts exhaust quickly in FX. Holding longer gives back gains.
- **Implies:** 5-bar trail is the optimum. Shorter = too tight (stopped out early), longer = gives back too much.

### USD/JPY (Any Direction)
- **What:** Same 20-bar breakout on USD/JPY
- **Result:** Signal unreliable across all tests
- **Why:** BOJ interventions create violent, unpredictable reversals that destroy any momentum signal
- **Implies:** All JPY crosses are structurally incompatible with trend-following. Avoid permanently.

### AUD/USD
- **What:** Same 20-bar breakout on AUD/USD (both directions)
- **Result:** adj negative across all tests
- **Why:** No consistent edge — commodity-currency dynamics don't trend cleanly
- **Implies:** AUD/USD off the instrument list permanently.

### GBP/USD
- **What:** Same 20-bar breakout on GBP/USD
- **Result:** Training period SIG, test period (2018-2026) negative
- **Why:** Brexit (2016-2019) + Truss mini-budget crash (2022) = structural breaks that destroy out-of-sample edge
- **Implies:** May work again in a calmer regime but can't be trusted until 5+ post-Truss years of data accumulate.

### EUR/JPY + GBP/JPY (2026-06-05, B1 research)
- **What:** 20-bar breakout on JPY crosses as instrument expansion
- **Result:** REJECTED — BoJ/MoF interventions (¥5.6T Oct 2022, April-May 2024) cause 5% intraday reversals + gap risk that whipsaw daily breakouts
- **Why:** Same structural problem as USD/JPY — policy interventions are circuit breakers that truncate trends. Diversification vs EUR/USD also spikes to 1.0 in crises (defeats the purpose).
- **Implies:** ALL JPY crosses confirmed off the list permanently.

### NZD/USD (2026-06-05, B2 research)
- **What:** 20-bar breakout on NZD/USD as diversification candidate
- **Result:** REJECTED despite passing trend mechanics
- **Why:** (1) 0.7-0.9 correlation with already-rejected AUD/USD — it's the same trade. (2) Forex spot has no India-legal execution path (same FEMA block as disabled EUR/USD).
- **Implies:** Forex *expansion to new pairs* is closed (JPY crosses, NZD/USD, AUD/USD all rejected). BUT — see correction below. Tradeable universe = India-legal: MCX commodities (XAU) + crypto (BTC/ETH on CoinDCX) + **NSE currency derivatives (EUR/USD)**.

> [!success] CORRECTION (2026-06-05): EUR/USD is NOT blocked
> The original "FEMA grey area" framing was wrong. **EUR/USD is legal via NSE exchange-traded futures** (SEBI 2016 circular, verified). What's illegal is *offshore* forex brokers, not the currency pair. EUR/USD (+0.131R, SIG train+test) is now **GO** — see [[FEMA Forex Legality]]. The lesson that holds: it's not "is forex legal?" but "WHERE are you trading it?" — Indian exchange = legal, offshore app = FEMA violation. **USD/CAD stays dead** (not listed on NSE). Don't re-propose *offshore* forex or new exotic pairs — but EUR/USD on NSE is live.

### XAU/USD Short Direction
- **What:** Short breakout on XAU/USD (close < prior 20-bar low)
- **Result:** adj = -0.061R
- **Why:** Gold has a persistent long-side asymmetry — safe haven demand creates asymmetric momentum
- **Implies:** XAU/USD LONG only. Short direction rejected permanently.

### Fibonacci Levels (2026-05-23)
- **What:** Fibonacci retracement entries
- **Result:** REJECTED — not quantifiable in a deterministic system
- **Why:** Can't backtest "where price might bounce at Fibonacci level" without curve-fitting. Fails Phase 1 deterministic rule.
- **Implies:** No subjective TA. Everything must be rule-based, deterministic, and backtestable.

---

## Architecture Decisions — Rejected

### Research Mode for Signal Validation
- **What:** Using research-mode backtest results (overlapping trades allowed)
- **Result:** 72-81% overlap confirmed — inflates win rates and frequency artificially
- **Why:** Overlapping trades share the same price action — they're not independent. Statistical tests assume independence.
- **Implies:** Only trading-mode results (non-overlapping) trusted. Research mode = exploration only.

### 7-Agent Architecture (Phase 1)
- **What:** Original design with 7 AI agents in the signal pipeline
- **Result:** Rejected before build — user identified over-engineering
- **Why:** LLM agents add latency, cost, and hallucination risk before deterministic edge is validated
- **Implies:** Phase 1 = deterministic only. Agents considered for Phase 2 only after 20+ live trades.

### Prediction Markets (Polymarket / Kalshi)
- **What:** AI-powered prediction market trading
- **Result:** Rejected — three independent blockers: Polymarket geo-blocked in India, Kalshi US-regulated only, not passive
- **Implies:** Any strategy requiring non-Indian exchange access is blocked. Filter proposals for India-legal execution first.

### Daily Strategy Generator (2026-06-06)
- **What:** A daily automated sweep that *generates* new strategy candidates (open brainstorm + literature mining) and backtests them, accepting any that pass the gate
- **Result:** REJECTED in design ([[grill-me]] session) before any build
- **Why:** Mass-testing freely-generated candidates through a single-strategy gate (Wilson CI > 33.3% train+test) manufactures false edges. Test ~100/yr and several pass train AND test by pure luck (multiple-comparisons / data-snooping) — the "winner" then dies live. Testing more strategies doesn't find more edges; it finds more lucky noise. Also contradicts the hard rule "no complexity before the simple version is validated" — the real bottleneck is capital + execution, not idea count.
- **Implies:** Discovery must be slow and gated. Replaced with [[Daily Watch Weekly Hunt]]: daily = monitor the ONE proven edge; weekly = one candidate at a time through rationale-first → cross-instrument confirmation (3+ assets) → a never-seen lockbox (touched once) → a trial-count penalty that raises the bar as N grows.

### CCR Remote Routines for Telegram
- **What:** Claude.ai remote routines to push scanner alerts
- **Result:** CCR blocks api.telegram.org at infrastructure level — not user-configurable
- **Fix adopted:** GitHub Actions (free tier, full internet access)
- **Implies:** All Telegram automation must route through GitHub Actions.

### Gemini API for Brief Generation
- **What:** Groq alternative — Gemini free tier for daily brief generation
- **Result:** Free tier quota = 0 on billing-enabled project
- **Fix adopted:** Groq (llama-3.3-70b-versatile, genuinely free)
- **Implies:** Use Groq for any free-tier LLM automation. Gemini free tier is unreliable.

### Zerodha Kite Connect for MCX Gold API
- **What:** Kite Connect API for XAU/USD execution layer
- **Result:** ₹2,000/month subscription cost — 33-40% of investable capital just for API access
- **Fix adopted:** Angel One SmartAPI (free, supports MCX, same REST/WebSocket pattern)
- **Implies:** Always check API subscription cost before choosing a broker for algo trading. For small capital, free APIs are non-negotiable.

---

## Related

- [[Trading System]] — what's proven and currently active
- [[Chief Trader]] — hard rules that prevent re-proposing dead ends
- [[North Star]] — filter everything through the retirement goal
