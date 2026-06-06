---
date: 2026-06-05
description: "XAU/USD instrument reference — backtest results, MCX Gold India execution path, signal logic."
tags:
  - reference
  - trading
  - instrument
---

# XAU/USD — Instrument Reference

## Backtest Results (20-bar breakout, LONG ONLY)

| Period | n | WR | Adj R | Verdict |
|---|---|---|---|---|
| Full 20yr | 206 | 46.6% | +0.278R | SIG |
| Train 2003-2017 | — | — | +0.237R | SIG |
| Test 2018-2026 | — | — | +0.170R | SIG |

**Frequency:** 8.96 completed trades/year
**Kelly (quarter):** 4.0% of equity

## Signal Logic

- Same as BTC: 20-bar breakout + EMA50/200 regime + ATR filter
- **LONG only** (short tested and rejected: adj = -0.061R)

## Execution — India Legal Path

- **MCX Gold Mini** via Angel One (SmartAPI execution)
- Scanner converts COMEX price to MCX INR equivalent at live USD/INR
- Account: **Angel One** (created 2026-06-05). Zerodha dropped — Kite Connect costs ₹2k/mo, SmartAPI is free.
- Scanner: GitHub Actions, 22:30 UTC weekdays (scans COMEX close) → Telegram alert → MCX trade during market hours

### Capital Requirements (A2 research, 2026-06-05)
- Lot notional: ~₹8.7L per Gold Mini lot
- Margin required: ~8-12% = **~₹70k-₹1.04L per lot minimum**
- **Implication: XAU/USD live trading requires ₹70k+ capital. Paper trading only until salary converts and capital grows.**

### Execution API — Angel One SmartAPI (primary, FREE)

> [!tip] Why Angel One over Zerodha
> Zerodha Kite Connect costs ₹2,000/month. SmartAPI is free. At ₹5-6k investable capital, this is the right call.

```python
from SmartApi import SmartConnect
obj = SmartConnect(api_key="YOUR_KEY")
obj.generateSession(clientCode, pwd, totp)  # TOTP required

obj.placeOrder({
    "exchange": "MCX",
    "tradingsymbol": "GOLDM<YYMM>",  # verify exact format in Angel One terminal
    "quantity": 1,
    "transactiontype": "BUY",
    "ordertype": "LIMIT",           # prefer LIMIT over SL-M (safer on MCX)
    "producttype": "CARRYFORWARD"   # equiv to Zerodha NRML
})
```

- MCX commodity segment must be activated in Angel One account
- MCX trading hours: ~9:00 AM – 11:30 PM IST
- Auth: API key + client ID + PIN + TOTP → session token
- Historical data: **Free** via SmartAPI (includes MCX)

> [!warning] April 2026 NSE algo guideline changes
> Angel One updated SmartAPI compliance from April 2026 per new NSE algo rules. Mainly affects NSE segment — confirm MCX is unaffected when account activates.

### Pre-live Checklist
- [x] Angel One account creation complete (2026-06-05)
- [x] MCX commodity segment activated (`mcx_fo` confirmed via API 2026-06-06)
- [x] Generate SmartAPI key from Angel One developer portal (2026-06-06)
- [x] Enable TOTP on Angel One account (2026-06-06)
- [x] Login verified via `test_angel_login.py` — `LOGIN OK`, account DILEEP RAJ G
- [ ] Verify Gold Mini symbol format via `obj.searchScrip(exchange="MCX", searchscrip="GOLD")`
- [ ] Verify current margin % on Angel One margin calculator
- [ ] Confirm NSE April 2026 changes don't restrict MCX API access

**Sample alert format:**
```
MCX GOLD  (USD/INR: 96.19)
Entry: ₹1,00,246   SL: ₹98,576   TP: ₹1,03,586
Risk/lot (Gold Mini 10g): ₹1,670
1% risk → ₹1,66,999 capital   |   2% risk → ₹83,500 capital
```

## Trade Journal

- [[trade-log]]

## Related

- [[2026-06-05 - gold xau trading signals]] — source signal research
- [[Trading System]] — full system context
- [[BTC_USD]] — crypto instrument (different execution path)
- [[What Didn't Work]] — XAU/USD short direction rejected (adj = -0.061R)
