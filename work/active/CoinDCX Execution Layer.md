---
date: 2026-06-05
description: "Build the one-tap CoinDCX REST API execution layer for BTC/USDT live trades — the critical gap between paper trading and live capital."
tags:
  - work-note
  - trading
status: active
quarter: Q2-2026
---

# CoinDCX Execution Layer

## What & Why

The gap between paper trading and live capital. Without this, signals fire but no trade can be placed. Goal: one tap to execute when a signal fires via Telegram.

> [!info] API Cost
> CoinDCX REST API is **free**. You need: KYC-verified CoinDCX account + API key from Settings → API dashboard.

---

## Research Findings (2026-06-05)

Source: A1 research via Perplexity Sonar → saved to `Research\Web\`

| Item | Finding |
|------|---------|
| Authentication | HMAC-SHA256 over JSON payload + API key/secret |
| Spot order call | `create_spot_order(market, side, order_type, total_quantity)` |
| Symbol format | `BTCUSDT` (no slash) — confirm via `get_markets` first |
| Rate limits | **Not publicly documented** — need empirical test call |
| Min order size | **Not static** — call `get_markets_details` at runtime before every order |
| ccxt | CoinDCX not in ccxt exchange list — direct REST only |

**Architecture reference:** [CoinDCX-API-calls](https://github.com/tapanmeena/CoinDCX-API-calls) — full algo platform on CoinDCX REST. Study before building.

---

## Build Checklist

### Pre-build (account setup)
- [x] Confirm CoinDCX KYC is complete and API trading is enabled *(verified via live auth, 2026-06-12)*
- [x] Generate API key: CoinDCX dashboard → Settings → API → Create key *(2026-06-12)*
- [x] Store key + secret in `D:\crypto_trading\.env` *(2026-06-12 — user pasted into `.env.example`; moved to `.env`, example restored to placeholders, neither file git-tracked)*

### Implementation
- [x] Create `D:\crypto_trading\coindcx_client.py` *(built test-first, 2026-06-05)*
  - [x] HMAC-SHA256 auth helper (`sign`, signs exact payload bytes — guards the 401 bug)
  - [x] `get_market_details(symbol)` — fetch min order size dynamically
  - [x] `place_spot_order(symbol, side, quantity, order_type="market_order")` function
  - [x] 13-test offline suite `test_coindcx_client.py` — all green
- [x] Empirically test rate limits with a minimal read call (balances endpoint) *(✅ 2026-06-12 — `smoke_coindcx.py` all green: auth OK, BTCUSDT min_quantity=1e-05 precision=5, below-min guard works. Balances: ~0.00027 BTC, 0.031 ETH, 1.14 USDT)*
- [x] Limit-order support added to client *(2026-06-12 — `price_per_unit` param, TDD, 16 tests green; enables zero-fill-risk order/cancel verification)*
- [ ] Wire into scanner flow: signal fire → [[Signal Matrix]] check → user taps → `place_spot_order()` *(Phase 2 — Telegram bot in `D:\trading_system\bot\execution.py`)*
- [x] Test end-to-end in simulation before any live capital *(offline: mocked HTTP, all paths covered)*

### Verification
- [x] Place a test order below minimum size → clean rejection *(unit-tested + asserted no network call)*
- [ ] Place a valid test order → appears in CoinDCX Open Orders UI *(ready: unfillable limit buy, 1e-05 BTC @ $40k ≈ $0.40 — needs explicit user go-ahead, permission-gated 2026-06-12)*
- [ ] Cancel via API → disappears from Open Orders *(runs immediately after the above)*

---

## Hard Rules

- Never skip the [[Signal Matrix]] confidence check before executing
- Always call `get_market_details` before placing — min size is dynamic
- No live trade without paper mode test passing first
- Direct REST only — not ccxt

---

## Related

- [[Trading System]] — full system context and pending steps
- [[Trading Research Queue]] — A2 (Zerodha MCX) and A3 (position sizing) still to run
- [[BTC_USD]] — the instrument this executes on
- [[Signal Matrix]] — confidence gate before every execution
- [[What Didn't Work]] — ccxt rejected (CoinDCX not in exchange list)
