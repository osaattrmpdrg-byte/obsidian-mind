---
date: 2026-06-05
description: "Complete trading system context — proven signals, current status, what's built, pending tasks, hard rules. Claude reads this at every trading session start."
tags:
  - brain
  - trading
---

# Trading System

**Core question every session:** *"Is there a backtested edge here?"*

Read by Claude at session start. Updated when signals are added, validated, or rejected. Never modify proven signals without new backtest evidence.

---

## Proven Signals

| Pair | Direction | WR | Adj R | n | Status |
|---|---|---|---|---|---|
| EUR/USD | Long | 54.3% (20yr) / 67.7% (test) | +0.131R | 92 | SIG train+test — **DISABLED** (India legal) |
| USD/CAD | Short | — | +0.054R | — | SIG train+test — **DISABLED** (India legal) |
| XAU/USD | Long | 46.6% | +0.278R | 206 | SIG train+test — **ACTIVE** (scanner live) |
| BTC/USD | Long | 51.7% full / 40% test | +0.452R | 116 | SIG full, borderline test — **PAPER TRADING** |
| EUR/USD | Long | 54.3% (20yr) / 67.7% (test) | +0.131R | 92 | SIG train+test — **GO via NSE futures** (legal cleared 2026-06-05, paper-trade gate pending) |
| ETH/USD | Long | 47.4% | +0.321R | 57 | NOT SIG in test — **PHASE 2, deferred** |

**Minimum bar:** Wilson CI lower bound > 33.3% (break-even for 1:2 R:R) in BOTH train AND test. Not just positive expectancy.

---

## Signal Logic (all instruments)

- **Entry:** close > prior 20-bar high
- **Regime:** EMA50 > EMA200 AND close > EMA50 (strict — both required)
- **ATR filter:** skip if ATR > 2× its 50-day average (no shock entries)
- **SL:** 1.5× ATR | **Exit forex:** 5-bar trailing low | **Exit crypto:** 3.0× ATR TP
- **Max hold:** 60 bars forex / 20 bars crypto

---

## Current Status (2026-06-05)

| Instrument | Regime | Scanner | Notes |
|---|---|---|---|
| BTC/USD | NONE — EMA50 $76.8k < EMA200 $81.7k | GitHub Actions 00:30 UTC | Waiting for flip |
| XAU/USD | Live | GitHub Actions 22:30 UTC | No signals fired yet. Execution via **Angel One SmartAPI** (account created 2026-06-05). |
| EUR/USD | — | **Re-enabling** | Legal via NSE EUR/USD futures (~₹2,700/lot, INR-settled). See [[FEMA Forex Legality]]. Build NSE execution path → paper trade → live. |
| USD/CAD | — | Disabled | Not listed on NSE cross-currency. Permanently blocked — no India-legal route. |

---

## Path to Live (approved 2026-06-06 — prune after execution)

The plan of action from system-built → live capital. **Paper test first.**

| Phase | What | Gate to next |
|-------|------|--------------|
| **1. Build** | Make the Telegram "Paper" tap actually log a structured trade. See plan: `D:\trading_system\docs\superpowers\plans\2026-06-06-paper-trade-logging.md` | Pipeline runs end-to-end, no errors |
| **2. Paper** | Scanner fires → Telegram → **Paper tap** → log + monitor. Accumulate **5-6 trades** (XAU / EUR-USD) | 5-6 trades logged |
| **3. Calibrate** | Compare live paper WR + adj R vs backtest (`calibrate.py`) | Tracks backtest → green-light. Diverges → diagnose |
| **4. Live (small)** | Wire real SmartAPI placement in `execution.py`. Start 1 lot, 1-2% risk. **EUR/USD first** (~₹2,700/lot) | — |

**The 5-6 gate validates the PIPELINE, not the edge.** Edge was validated in backtest (proper n). At ~18 trades/yr, waiting for 20 paper trades = a year — impractical. 5-6 proves the plumbing + sanity-checks fills; edge-confidence keeps building during early live trading at tiny size.

**Near-term loop while waiting on signals:** re-point scanner to add EUR/USD → let scanner watch → paper-trade what fires → build live `execution.py` in parallel.

## What's Built

| File | Purpose |
|---|---|
| `D:\trading_system\signals\scorer.py` | compute_breakout_features() + regime_filter() |
| `D:\trading_system\backtest\engine.py` | Research/trading mode backtest engine |
| `D:\trading_system\scanner.py` | Live scan, Telegram alerts with inline keyboard, MCX Gold conversion |
| `D:\trading_system\monitor_trades.py` | Paper trade monitoring via GitHub Actions |
| `D:\trading_system\position_size.py` | Quarter-Kelly position sizing |
| `D:\trading_system\log_trade.py` | Trade logging to trade_log.csv |
| `D:\trading_system\calibrate.py` | Brier score (run after 20 trades) |
| `D:\crypto_trading\backtest_parallel.py` | 54-combo param sweep via ProcessPoolExecutor |
| `D:\trading_system\bot\handler.py` | Telegram polling bot — routes Validate/Paper/Skip/Execute taps |
| `D:\trading_system\bot\validation.py` | Two-layer pre-trade check: circuit breakers → Perplexity |
| `D:\trading_system\bot\execution.py` | Angel One SmartAPI stub (fills when key arrives) |
| `D:\trading_system\Dockerfile` | Cloud Run deployment — always-on polling bot |

GitHub repo: `osaattrmpdrg-byte/life-os` (private) — scanner + monitor run via Actions.

---

## Pending Next Steps (priority order)

1. **Angel One API key** — account CREATED (2026-06-05). Next: generate SmartAPI key from smartapi.angelbroking.com (create a "Trading API" app), enable TOTP, activate MCX + currency segments. Add key to `D:\trading_system\.env` as `ANGEL_ONE_API_KEY`. Uncomment SmartConnect block in `bot/execution.py`. Free API.
2. **Add Perplexity key to trading_system .env** — `D:\trading_system\.env` has `PERPLEXITY_API_KEY=` placeholder. Fill it. Then `bot/validation.py` Layer 2 activates.
3. **Deploy bot to Cloud Run** — see `D:\trading_system\docs\deploy.md`. Run: `gcloud run deploy trading-bot --source . --region asia-south1 --min-instances 1`. $300 GCP credits expire 2026-09-04.
4. **Run the bot locally first** — `python -m bot.handler` + `python scanner.py` — verify keyboard appears in Telegram, Validate tap works.
5. **Bake breakout signal into scorer.py + engine.py** — currently validated separately in validate_breakout.py
3. **Position sizing calculator** — given capital + risk% → expected annual return output (research pending — see [[Trading Research Queue]] A3)
4. **short_agent.py** — EMA50 rejection logic (not RSI inversion — different entry)
5. ~~Instrument expansion — EUR/JPY, GBP/JPY, NZD/USD~~ ❌ All rejected (B1-B2, see [[What Didn't Work]]). Forex expansion closed except EUR/USD below.

### EUR/USD re-enablement (GO — legal cleared 2026-06-05)
1. Activate **currency derivatives segment** (not just MCX) — account created 2026-06-05
2. Verify scanner's EUR/USD daily-close source matches NSE futures behaviour (spot vs INR-settled futures, 9-5 IST hours) — cheap check, do before trusting fills
3. Re-point execution: NSE EUR/USD futures (1,000 EUR lot, ~₹2,700 margin) via Angel One currency segment
4. **Paper trade through live pipeline** before any real capital (own hard rule — backtest SIG ≠ live edge)
5. Then live. Most capital-accessible instrument in the system (~₹2,700/lot vs ₹70k gold).

---

## Code Workflow

1. `/plan` before touching any file
2. Implement
3. `/code-review` before committing any signal logic
4. `superpowers:verification-before-completion` before calling anything done

---

## Code Standards

- **Stack:** Python, stdlib + yfinance + pandas + numpy (Phase 1 only)
- **Tests:** Real data only — no mocks for backtests or signal validation
- **Style:** Short functions, explicit variable names, no premature abstraction
- **Files:** Edit existing before creating new; never create docs/README unless asked
- **Instruments:** Max 6–10 for Phase 1

---

## Hard Rules

- No new signal without Wilson CI lower bound > 33.3% in BOTH train AND test
- Research mode overlap = 72-81% — only trading mode results trusted
- Phase 1 = deterministic only. No LLM in the signal pipeline.
- Never propose scoring weights without backtest calibration
- No complexity before the simple version is validated
- No error handling for scenarios that cannot happen
- Max 6-10 instruments for Phase 1

---

## Position Sizing Rules (A3 research, 2026-06-05)

**At current capital (₹5-6k): use 1-2% risk per trade.**
Quarter-Kelly (6.9%) implies ₹11,900 position at ₹5k capital — not fundable. Apply quarter-Kelly only when capital > ₹30k.

| Capital | Recommended risk% | Risk/trade | BTC position | Fee impact |
|---------|-----------------|------------|-------------|------------|
| ₹5-6k | 1-2% | ₹50-120 | 0.02-0.05 BTC | ~7% of risk |
| ₹30k | 2-3% | ₹600-900 | 0.26-0.38 BTC | ~1% of risk |
| ₹1L+ | Quarter-Kelly (6.9%) | ₹6,900 | ~3 BTC | negligible |

**XAU/USD (MCX Gold Mini): requires ₹70k+ margin per lot. Paper only until capital grows.**

**Annual return at 2% risk, 18 trades, +0.3R expectancy = 10.8%/year.**
Trading returns alone won't reach ₹50k target. Salary injection post-conversion is the real multiplier.

## Return Projections (EUR/USD + USD/CAD when re-enabled, adj +0.093R avg, 7.8 trades/year)

| Risk% | ₹10k | ₹50k | ₹1L |
|---|---|---|---|
| 1% | +₹73/yr | +₹365/yr | +₹729/yr |
| 2% | +₹146/yr | +₹729/yr | +₹1,458/yr |
| 5% | +₹365/yr | +₹1,823/yr | +₹3,646/yr |

MDD estimate: 5-loss streak = risk% × 5 (e.g., 2% risk → -10% MDD)

---

## Related

- [[What Didn't Work]] — read before proposing anything new
- [[Streams]] — trading is Stream 2 of four
- [[North Star]] — the ₹7-8L/month goal this feeds
- [[Signal Matrix]] — confidence matrix for live decisions
- [[BTC_USD]] | [[XAU_USD]] | [[ETH_USD]] — instrument references
- [[trade-log]] — paper trade journal
