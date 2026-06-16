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

> [!success] CLEARED 2026-06-16 — both blocking items done.
> 1. ✅ **Exit fix DEPLOYED.** `2dd7aac` confirmed on `origin/main` (live GitHub Actions monitor now runs the validated trailing exit, not the old buggy +2R-TP exit). ⚠️ Per the validation below, this only fixes the **paper monitor's bookkeeping** — it does NOT make the system live-tradeable. No real capital regardless.
> 2. ✅ **Leaked OAuth token revoked** (Dileep, 2026-06-16); git access re-authenticated afterward.
>
> **Still open (eventual, non-blocking):** collapse the two drifting copies (`D:\trading_system` ↔ `life-os/trading_system`) to one source of truth; give `D:\trading_system` a remote so the recovered engine has off-machine backup.

> [!failure] VALIDATION + PANEL COMPLETE (2026-06-16, autonomous) — the EUR +0.131R edge does NOT survive realistic fills. Verdict: **KILL the current implementation; edge unconfirmed.**
> Ran the fill-timing test (`D:\trading_system\validate_fill_timing.py`) + the three unfinished panel lenses. The live monitor is fully **synthetic** (no resting broker orders) and runs the morning *after* a breach (00:30 UTC), so the earliest real fill is `open[j+1]` — for the trail **and** the SL.
> - **Fill timing (decisive):** golden close-fill = +0.150R (sanity, matches +0.131); **trail→next-open = −0.040R (dead)**; **both→next-open = +0.002R (≈ zero)**. The breach-bar-close fill was capturing ~0.15R unreachable live. Risk lens's REVISE was generous — this is KILL for the current next-morning batch exit.
> - **Refute lens:** 4 FX pairs backtested, only EUR positive (AUD/JPY fail, **GBP has negative expectancy −0.040R yet "passes" the WR gate**) → 1-of-4 at the margin = consistent with noise. The gate itself is **mis-specified**: `Wilson-WR-lo > 33.3%` assumes a fixed 1:2 R:R, but this is a *variable-win trailing* strategy, so WR is the wrong test. No out-of-sample / walk-forward — entire 2004–2026 span is in-sample.
> - **Provenance lens:** the engine was **reverse-engineered to fit** the golden CSV (commit `816bb24`), so "engine reproduces golden" is **circular** — it proves a match, not that the original +0.131R was correct. Original generating script is gone; the reverse-engineered engine inherited the same optimistic fill model. No independent validation exists anywhere in the chain.
> - **Data-integrity lens:** ✓ golden EUR has **0 overlapping trades** (non-overlap intact); ⚠️ data is yfinance FX `=X` bars — **0 volume on 100% of bars** = indicative quotes, not traded prices, yet the whole exit logic keys on intrabar `low` breaches; XAU uses `GC=F` futures, not spot.
> - **The one lever:** the kill is *execution-driven*, not proven signal-driven. To revive, exits must fill **at/near the breach** — an at-close/intraday monitor, or a **resting broker stop/trailing-stop**. Even then, OOS validation on real broker data is required before confidence. **No real capital on EUR (or any pair) until fills happen at-breach AND an OOS test holds.**
> See [[Gotchas#Backtest reproducibility & live-exit divergence]].

> [!info] EXECUTION-PATH PROOF (2026-06-16, autonomous) — Gate 1 PASSED, Gate 2 still open. Script: `D:\trading_system\validate_execution_path.py`.
> Tested the two executable fill models. Result (EUR, span-aligned): close/golden **+0.150** · current next-morning monitor **+0.002 (dead)** · **resting broker stops −0.026 (DEAD)** · **at-close +0.150 (SURVIVES, ~21 pips slippage headroom)**.
> - **Counterintuitive core finding:** the edge *is* the post-breach **intraday recovery**. On breach days price dips through the 5-bar-low trail intraday and then **closes back above it** (close-fill raw +0.270R vs resting-fill raw +0.094R). A resting trailing stop fills you at the low and **forfeits the bounce** → it's *worse than doing nothing*. **Do NOT use a resting trailing stop.**
> - **The executable model = HYBRID:** resting **hard SL at −1R** (intraday gap protection, realistically ~−1.026R) **+ at-close trailing exit** (market-exit when the 5-bar low is breached, checked at the *bar close*, not next morning). This is exactly the golden model and it is reachable live. Implementation = reschedule the monitor cron from 00:30-next-morning to the **bar-close instant** + exit-at-detection; keep a resting −1R broker stop.
> - **⛔ Gate 1 ≠ Gate 2.** This proves *IF the edge is real, you can capture it.* It does NOT prove the edge is real. Two unaddressed gaps remain before any capital: (1) **in-sample only** — no OOS/walk-forward; multiple-testing (1-of-4 pairs) + circular provenance still stand; (2) **wrong-instrument data** — backtest is yfinance `EURUSD=X` spot (**0 volume, indicative quotes**); live is the **NSE EUR/USD future** (different hours/close/spread). Re-confirm the 21-pip headroom on real NSE-futures data + real spread.
> See [[Gotchas#Backtest reproducibility & live-exit divergence]].

> [!check] GATE 2a — OOS / ROBUSTNESS (2026-06-16, autonomous). Script: `D:\trading_system\validate_oos.py` (at-close model). **Partial PASS — edge looks MORE real than the panel feared, with one fragility flag.**
> - ✅ **Temporal — alive recently, not a relic.** Eras: 2004-09 **+0.334** · 2010-15 **−0.125** · 2016-20 **+0.315 sig** · **2021-26 +0.120 sig**. Second half **+0.153 sig** > first half +0.148. So the edge survives into the current decade — but expect **multi-year negative regimes** (2010-15 bled).
> - ⚠️ **Tail — FRAGILE (inherent to trend-following).** Dropping the **single** biggest winner cuts adjR +0.150 → +0.094 (−37% from one trade); top-3 → +0.025; top-5 → negative. Top-5 winners = 5.36/3.30/3.27/2.70/2.56 R. The edge **is** the fat right tail → high variance, long flat/down stretches, winners MUST run (confirms: no TP). Effective confidence is lower than n=92 implies.
> - ✅ **Breadth — NOT cherry-picked.** Same fixed rules on 8 FX pairs → **5/8 positive** (USD/JPY **+0.356**, USD/CAD +0.213, EUR/USD +0.150, GBP/JPY +0.141, EUR/JPY +0.066; neg: GBP/USD −0.014, AUD/USD −0.060, NZD/USD −0.145). A **broad breakout/trend effect**, not a EUR fluke — substantially rebuts the panel's "1-of-4 = noise." Also a preliminary YES for [[Edge Generalization Sweep]]'s core premise.
> - **Implication:** tail-fragility's natural hedge is **diversifying across the positive pairs** (spreads the "which decade has the big trend" risk) — IF India-legal instruments exist (USD/CAD already blocked; check NSE availability per [[FEMA Forex Legality]]).
> - **Still blocking capital:** Gate 2b unresolved — all of the above is yfinance **spot** data (0 volume), not the **NSE future** actually traded. Tail-dependence makes fill quality on the ~5 big winners decisive, which is exactly where spot-vs-futures + real spread bite. **No capital until Gate 2b confirms on real NSE-futures data.**
> See [[Gotchas#Backtest reproducibility & live-exit divergence]].

> [!failure] GATE 2b — REAL-INSTRUMENT CHECK via Angel One (2026-06-16, autonomous). **EUR/USD is UNTRADEABLE; no currently-working FX edge exists in a liquid+legal Indian vehicle.** Scripts: `fetch_nse_probe.py`, `validate_usdinr.py` (read creds from `.env`, print only data — keys never seen).
> Pulled real NSE data from Angel SmartAPI (currency segment `cde_fo` live; login OK).
> - **The NSE EUR/USD cross-currency future is dead-liquid.** Near-month at peak liquidity (`EURUSD26JUNFUT`, 9 days to expiry): **~92 lots/day, flat single-print OHLC on 5 of 10 days**, and it diverges **11–36 pips from spot** — *exceeding the entire 21-pip edge headroom before spread.* Control (proves the API works): **USD/INR monthly = 312,614 lots/day, 0/31 flat.** A ~3,400× gap. Expired-contract tokens aren't in the scrip master and the underlying (`UNDCUR`) returns 0 bars, so no long futures history is even retrievable.
> - **Every cross-currency pair with an edge is an NSE cross-currency future → all equally thin** (USD/JPY same pattern). So the entire Gate-2a basket (EUR/USD, USD/JPY, GBP/USD, JPY crosses) is non-vehicle. USD/CAD already blocked.
> - **USD/INR — the ONLY liquid + legal NSE FX future — tested:** full-period **+0.199 sig** (stronger than EUR, less tail-fragile), BUT **2021–2026 = −0.041 (dead in the current regime)** — RBI-managed bands whipsaw breakouts — and it's confounded by **3.7%/yr structural INR-depreciation drift** (long-only on a rising asset flatters the result).
> - **NET:** the pairs that *work now* (EUR/USD et al.) **aren't tradable** (illiquid); the instrument that's *tradable* (USD/INR) **isn't working now**. **There is no currently-tradable, currently-working FX breakout edge in India-legal instruments.** Found before risking ₹1 — exactly the point of the gates.
> - **Forward (best shot at a real vehicle):** re-run Gate 1/2a/2b on **crypto (BTC/ETH)** — liquid, legal, **24/7 so the at-close execution path is even cleaner** (no overnight gaps). Blocked on the CoinDCX order-create 400 ([[CoinDCX Execution Layer]]). MCX **Gold** is liquid+legal but already failed the *edge* gate. **EUR/USD scanner should be disabled** — the signal fires but there's no vehicle to trade it. Update [[FEMA Forex Legality]] (legal ≠ liquid) and [[Streams]].
> See [[Gotchas#Backtest reproducibility & live-exit divergence]].

> [!success] CRYPTO REVALIDATION — BTC is the real opportunity (2026-06-16, autonomous). Script: `D:\trading_system\validate_crypto.py`. **The trading thesis is alive — it's BTC, not FX.**
> Ran the full Gate 1/2a/2b battery on BTC/ETH (yfinance daily, **real volume** — 0% zero-vol bars, unlike FX `=X`).
> - **BTC/USD: adjR +1.686, sig.** POSITIVE in **every** era: 2015-17 +3.505 · 2018-20 +2.725 · 2021-23 **+0.421 (bear!)** · 2024-26 **+0.405 (recent)**. **Tail-robust** (drop top-3 → still +1.09, unlike FX). Survives **0.42R** of cost (crypto fees ~0.2R round-trip → huge margin).
> - **Drift control (the skeptic's question — is it just being long BTC?):** NO. Through the **2022 bear (buy-and-hold −73%) the regime filter took 1 trade, −1.0R** — it sidestepped the crash. Regime-long only **44% of days**; flat the rest. The edge is timing, not passive exposure. (Caveat: naive holding still made +20,000% on BTC specifically; the system's value is **risk-adjusted** drawdown control + it's a generalizable rule.)
> - **ETH/USD: +0.555 but NOT significant** (n=46) and tail-fragile (drop top-3 → negative). Secondary at best.
> - **All three gates pass for BTC:** capturable (at-close, even cleaner 24/7), real edge (all-era, tail-robust), tradable vehicle (deep liquidity, real bars, legal in India). **The binding constraint is now ONLY execution — the CoinDCX order-create 400.** That single bug is the gate between this body of work and real money.
> - **BTC regime is currently NONE** (EMA50 < EMA200) → no signal until it flips bullish. Use the wait to fix execution.
> See [[CoinDCX Execution Layer]], [[Gotchas#Backtest reproducibility & live-exit divergence]].

---

## Proven Signals

| Pair | Direction | WR | Adj R | n | Status |
|---|---|---|---|---|---|
| EUR/USD | Long | 54.3% | +0.131R (spot only) | 92 | ❌ **UNTRADEABLE (Gate 2b FAILED 2026-06-16).** Edge is real-ish & capturable in theory, but the NSE EUR/USD future trades **~92 lots/day, flat OHLC half the days, 11-36 pip spot-divergence > the 21-pip headroom.** No liquid+legal vehicle. **Disable the scanner.** See Gate 2b callout |
| USD/CAD | Short | — | +0.054R | — | SIG train+test — **PERMANENTLY BLOCKED** (not on NSE cross-currency) |
| XAU/USD | Long | 41.7% (test) | +0.277R (test) | 152 | ⚠️ **FAILS GATE under validated exit (2026-06-14)** — test Wilson-lo **30.1% < 33.3%** (train passes at 38.9%). Edge positive but under-powered in test (n=60). **DOWNGRADE: scanner may watch, NO real capital** until test significance is earned |
| BTC/USD | Long | 52.7% | **+1.686R** (at-close, n=74) | 74 | ✅ **STRONGEST EDGE IN THE SYSTEM (revalidated 2026-06-16).** Positive every era incl 2022 bear; tail-robust; real volume; survives 0.42R cost; regime filter sidesteps crashes (1 trade/−1R through −73%). Liquid+legal+24/7. **Only blocker = CoinDCX execution (400).** Regime currently NONE → waits for EMA50>EMA200 flip. See crypto callout |
| ETH/USD | Long | 47.4% | +0.321R | 57 | NOT SIG in test — **PHASE 2, deferred** |

**Minimum bar:** Wilson CI lower bound > 33.3% (break-even for 1:2 R:R) in BOTH train AND test. Not just positive expectancy.

> [!success] Reconciled 2026-06-14 — validated exit recovered, live monitor aligned
> The lost exit was recovered and rebuilt as a tested engine (`backtest/trail_engine.py`, reproduces the golden EUR file **to the trade**): long-only, hard SL −1R, **5-bar trailing stop** (`min(low[j-5:j])`, excludes current bar, not reset at entry), fill at the **breach bar's close**, **no TP, no max-hold**. Findings:
> - **EUR/USD +0.131R reproduced & re-blessed.**
> - **XAU/USD FAILS the gate** under the validated exit — test-period Wilson-lo 30.1% < 33.3% (the old "+0.278R" was the test-window point estimate, never gate-checked). Positive but under-powered. Artifact now saved: `results/breakout_trail5_XAU.csv`.
> - **Live monitor aligned** — `monitor_trades.py` had a +2R TP cap (deleted the right-tail winners; reconstruction with TP = −0.278R) **plus** a too-tight trail that reset at entry and exited at the trail level. Both fixed; live exit is now byte-identical to the engine. `trading_system` is now under git (branch `trailing-exit-reconciliation`).
> See [[Gotchas#Backtest reproducibility & live-exit divergence]].

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
| XAU/USD | NONE (as of 2026-06-11) | GitHub Actions 22:30 UTC | No signals fired yet. Execution via **Angel One SmartAPI** (account created 2026-06-05). |
| EUR/USD | SHORT regime (as of 2026-06-11) — long signal needs flip | **Re-enabled 2026-06-12** (deploy pending `git push` of life-os) | Legal via NSE EUR/USD futures. See [[FEMA Forex Legality]]. Alerts now carry NSE sizing block (lot margin, risk/lot ₹, IST hours). Paper trade → live. |
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

1. ~~Angel One API key~~ ✅ VERIFIED 2026-06-12 — key + client code + PIN + TOTP secret all in `.env`, `test_angel_login.py` passes: **MCX active, currency derivatives active**. Both execution segments unlocked.
2. ~~Perplexity key~~ ✅ Already set in `.env` — Layer 2 live-tested 2026-06-12 (correctly returned NO GO on a fake test signal).
3. ~~Run the bot locally first~~ ✅ END-TO-END VERIFIED 2026-06-12 — test signal → keyboard → Validate tap → circuit breakers → Perplexity → verdict → message edit. Full pipeline works.
4. **⚠️ WIRE LIVE ORDER PLACEMENT — `bot/execution.py` SmartConnect block (DO NOT FORGET)**
   - **Trigger: when the paper gate reaches 5-6 logged trades** (Path to Live Phase 4). One-session job.
   - What's stubbed: `place_order()` returns "not wired up" when key is set. Wire: `generateSession(CLIENT_CODE, PIN, pyotp.TOTP(TOTP_SECRET).now())` — note .env names are `ANGEL_ONE_PIN`/`ANGEL_ONE_TOTP_SECRET`, NOT the `PASSWORD`/`TOTP` names in the stub's comment.
   - Needs: `searchScrip` for front-month symboltoken (MCX gold AND NSE EUR/USD `cde_fo`), branch by instrument, SL order placement. Stub's `stoploss`/`squareoff` params are ignored on variety NORMAL — needs separate SL order or ROBO variety check.
   - Start 1 lot, 1-2% risk, **EUR/USD first** (cheapest lot).
5. **Deploy bot to Cloud Run** — see `D:\trading_system\docs\deploy.md`. Run: `gcloud run deploy trading-bot --source . --region asia-south1 --min-instances 1`. $300 GCP credits expire 2026-09-04.
5. **Bake breakout signal into scorer.py + engine.py** — currently validated separately in validate_breakout.py
3. **Position sizing calculator** — given capital + risk% → expected annual return output (research pending — see [[Trading Research Queue]] A3)
4. **short_agent.py** — EMA50 rejection logic (not RSI inversion — different entry)
5. ~~Instrument expansion — EUR/JPY, GBP/JPY, NZD/USD~~ ❌ All rejected (B1-B2, see [[What Didn't Work]]). Forex expansion closed except EUR/USD below.

### EUR/USD re-enablement (GO — legal cleared 2026-06-05, scanner re-enabled 2026-06-12)
1. Activate **currency derivatives segment** (not just MCX) — account created 2026-06-05 *(user action)*
2. ~~Re-point scanner to EUR/USD~~ ✅ 2026-06-12 — PAIRS re-enabled, NSE sizing block on alerts, FX callback precision fixed (5 decimals), brief memory updated. Committed in life-os; **push pending**.
3. Data-source note: scanner fires on yfinance spot daily close (22:00 UTC); NSE futures track spot, settle INR, trade 9:00–17:00 IST → place at next session open. Alert says this.
4. Re-point execution: NSE EUR/USD futures (1,000 EUR lot, ~₹2,700-3,300 margin) via Angel One currency segment — needs SmartAPI key
5. **Paper trade through live pipeline** before any real capital (own hard rule — backtest SIG ≠ live edge)
6. Then live. Capital note from live numbers: risk/lot ≈ ₹875 at current ATR → 1 lot ≈ 15% risk at ₹5-6k capital. 1%-risk sizing needs ~₹87k. Paper data will inform whether to take >2% risk per trade at current capital.

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
