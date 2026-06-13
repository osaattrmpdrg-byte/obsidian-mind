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
- [x] Fix scientific-notation serialization for small quantities *(✅ 2026-06-13 — `_plain_decimal` + `_signed_post(number_fields=)`, plain JSON numbers; regression test, 17 tests green)*
- [x] Mirror client into version control *(✅ 2026-06-13 — committed to `life-os/crypto_trading/` (`ca34986`) + `.gitignore` for `.env`; push pending user's terminal — interactive credential prompt)*
- [ ] Wire into scanner flow: signal fire → [[Signal Matrix]] check → user taps → `place_spot_order()` *(Phase 2 — Telegram bot in `D:\trading_system\bot\execution.py`)*
- [x] Test end-to-end in simulation before any live capital *(offline: mocked HTTP, all paths covered)*

### Verification
- [x] Place a test order below minimum size → clean rejection *(unit-tested + asserted no network call)*
- [ ] Place a valid test order → appears in CoinDCX Open Orders UI *(❌ BLOCKED — 400, CoinDCX-side; see below)*
- [ ] Cancel via API → disappears from Open Orders *(blocked — depends on the above)*

---

## ⚠️ Order placement returns 400 — root cause is CoinDCX-side, not our code (2026-06-12 / 13)

**Symptom:** every `place_spot_order` returns `HTTP 400 {"code":400,"message":"Invalid request"}`, identical across all variations (sell limit at +1.5%, +10%, +89% from market; qty 0.0001 and 0.00005; floats and strings; with and without `ecode`).

> [!warning] The earlier "read-only key" diagnosis was WRONG — corrected
> The first guess (key lacks Trading scope) was disproven by the dashboard screenshot: the key has **Place Limit Orders + Place Market Orders + Funds Balance + Account Details** all enabled, and IP `152.57.33.190` is whitelisted. Lesson: "uniform failure ⇒ permission issue" was a bad inference — uniformity *also* fits a constant-wrong-field or an account-side block, which is what it turned out to be.

**Systematically ruled out** (all via safe, rejected live attempts — no order ever created):
- Auth/HMAC ✓ (balances works) · trade permission ✓ (screenshot) · IP whitelist ✓
- Market identifier ✓ — `"BTCUSDT"` is correct: pair form `"B-BTC_USDT"` gives a *different* error (`422 Currency pair is not valid`), proving `BTCUSDT` is accepted and the 400 is **not** about the market
- Clock skew ✓ (0.6 s) · strings ✗ · floats ✗ · `ecode:"B"` ✗ · quantity size ✗ · **price-band ✗** (even +1.5% fails)
- **Our code matches the working reference lib (`svamja/coindcx-python`) verbatim** — identical body dict, `json.dumps(separators=(',',':'))`, HMAC signing, headers, market-as-is, numeric quantities. No mechanical difference remains.

**Conclusion:** not resolvable from our side. Leading explanations, both CoinDCX-side: (a) the **`B`-ecode (Binance-mirrored) USDT market may not be REST-orderable** for this account via `/exchange/v1/orders/create` despite `status:active`; or (b) an **account-level API-trading activation** beyond the key permission. **Next step = CoinDCX API support**, quoting the exact payload + 400, asking whether BTCUSDT (ecode B) spot is REST-orderable for this account. No more blind attempts. Not on the critical path (BTC paper phase).

## ✅ Scientific-notation serialization bug — FIXED (2026-06-13, TDD)

Confirmed and fixed: `json.dumps(0.00005)` → `"5e-05"`, which CoinDCX rejects. Bites any quantity below 0.0001 — *including the real 1e-05 minimum and any min-notional order* (~8.6e-05 BTC at $64k). The original 13 tests missed it (used 0.0012-size quantities). Fix in `coindcx_client.py`: `_plain_decimal()` + `_signed_post(number_fields=...)` emit `total_quantity`/`price_per_unit` as plain non-scientific **JSON numbers** (matching the reference lib's numeric contract) via placeholder injection. Regression test `test_small_quantity_not_scientific_notation`; **17 tests green**, smoke still passes. Independent of the 400 above — would have bitten once the 400 is resolved.

**Client status:** read path verified live; order construction matches the working reference and is now scientific-notation-safe. Order/cancel remain **unverified live**, blocked by the CoinDCX-side 400 — not by our code.

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
