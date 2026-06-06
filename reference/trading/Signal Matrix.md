---
date: 2026-06-05
description: "Trading signal confidence matrix — decision framework for PLACE / PAPER TEST / SKIP when a signal fires via Telegram."
tags:
  - reference
  - trading
---

# Signal — Trading Confidence Matrix

Triggered when EUR/USD, USD/CAD, XAU/USD, or BTC/USD signal is detected. Present this matrix and wait for explicit decision. Do not proceed to any action until user selects PLACE / PAPER TEST / SKIP.

---

## Confidence Matrix

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TRADING SIGNAL DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Pair:       [PAIR]          Direction:  [LONG / SHORT]
  Timeframe:  Daily           Detected:   [TIMESTAMP]

  SIGNAL CONDITIONS
  ─────────────────
  Regime:         EMA50 > EMA200          [✅ PASS / ❌ FAIL]
  Price filter:   close > EMA50           [✅ PASS / ❌ FAIL]
  20-bar breakout: close > prior 20-bar high [✅ PASS / ❌ FAIL]
  ATR filter:     ATR ≤ 2× 50-day avg ATR [✅ PASS / ❌ FAIL]

  CONDITIONS MET: [X/4]

  ENTRY PARAMETERS
  ─────────────────
  Entry price:    [PRICE]
  Stop loss:      [1.5×ATR below/above entry] = [PRICE]
  Exit method:    5-bar trailing low/high (forex) | 3.0×ATR TP (crypto)
  Max hold:       60 bars forex / 20 bars crypto

  CONFIDENCE SCORE
  ─────────────────
  Base (all 4 conditions):    60 pts
  Regime strength bonus:      [0–15 pts]  [EMA spread: X pips]
  ATR headroom bonus:         [0–15 pts]  [ATR at X% of limit]
  Historical context bonus:   [0–10 pts]  [last 5 similar: W/L/W/W/W]
  ─────────────────────────────────────────
  TOTAL CONFIDENCE:           [XX] / 100

  RISK CHECK (at your chosen risk %)
  ─────────────────
  Risk 1%:   [₹ amount] per trade
  Risk 2%:   [₹ amount] per trade

  HISTORICAL BASELINE (EUR/USD)
  ─────────────────
  Win rate:   54.3% (20yr) | 67.7% (2018–2026 test)
  Adj R:      +0.131R per trade | Frequency: ~4 trades/year

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  YOUR DECISION:

  [1] PLACE LIVE ORDER   — signal is clean, confidence high
  [2] PAPER TEST         — track without capital at risk
  [3] SKIP               — pass on this setup

  Confidence threshold:
  ≥ 80 → PLACE | 60–79 → PAPER TEST | < 60 → SKIP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## After Decision

**If PLACE:** Confirm entry, SL, and position size. Log to [[trade-log]].
**If PAPER TEST:** Log setup. Track outcome. Add to backtest validation data.
**If SKIP:** Note reason. If regime failed → expected. If personal judgment → note it.

---

## Telegram Setup

Scanner sends alert before presenting this matrix.
Bot: `@DileepLifeOSBot` | Chat ID: `5044254368`
Notification: "🚨 SIGNAL: [PAIR] [DIRECTION] detected. Open Claude Code to review."

## Related

- [[Trading System]] — full signal context
- [[Chief Trader]] — trading rules and workflow
- [[trade-log]] — log the trade after decision
