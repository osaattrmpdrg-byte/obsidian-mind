---
date: 2026-06-06
description: "Things that have bitten before and will bite again — pitfalls, edge cases, and testing traps"
tags:
  - brain
---

# Gotchas

Things that have bitten before and will bite again.

## Angel One SmartAPI

- **`smartapi-python` has incomplete dependency declarations (2026-06-06)**: `pip install smartapi-python` does NOT pull in `logzero` and `websocket-client`, but the package imports both at load time → `ModuleNotFoundError` on first import. Fix: `pip install smartapi-python pyotp python-dotenv logzero websocket-client`. **Add all five to `requirements.txt`** or the Cloud Run deploy will fail the same way. See [[Trading System]].
- **Segment codes are non-obvious (2026-06-06)**: `getProfile()` returns segments as `mcx_fo` (MCX commodity), `cde_fo` (currency derivatives / EUR/USD), `nse_fo`, `nse_cm`, etc. — NOT `"MCX"` / `"CDS"`. Match the `_fo`/`_cm` codes when checking segment activation.
- **TOTP needs the base32 SECRET, not the 6-digit code (2026-06-06)**: store the secret string from TOTP setup in `.env` as `ANGEL_ONE_TOTP_SECRET`; generate the rolling code at runtime with `pyotp.TOTP(secret).now()`. SmartAPI `generateSession(client, pin, totp)` — 2nd arg is the **MPIN**, 3rd is the generated code.

## Telegram signal bot

- **Callback-data float precision collapses FX prices (2026-06-12)**: the scanner's inline keyboard encoded entry/SL/TP into `callback_data` at `:.2f`. Fine for gold (4678.10) but for EUR/USD (1.15356 → "1.15") the entry, SL, and TP all round to nearly the same 2-dp value — the downstream Validate/Execute handler then trades against a corrupted price. Fix: format by instrument — `decimals = 2 if cfg["unit"] >= 1.0 else 5`, threaded through `send_signal_keyboard` and `_record_paper_trade`. Telegram `callback_data` hard limit is **64 bytes** — the 5-dp FX payload measures 51 bytes, safe, but check this whenever adding fields. Any new low-priced instrument (most FX, many alts) inherits this trap. See [[Trading System]].

## Angel One execution stub

- **`bot/execution.py` stub comments name the wrong env vars (2026-06-12)**: the commented-out `SmartConnect` block references `ANGEL_ONE_PASSWORD` and `ANGEL_ONE_TOTP`, but the actual `.env` (and `test_angel_login.py`) use `ANGEL_ONE_PIN` and `ANGEL_ONE_TOTP_SECRET` (base32 secret → `pyotp.TOTP(secret).now()` at runtime). Wire the real names when un-stubbing or login silently fails with a confusing error.
- **`placeOrder` ignores `stoploss`/`squareoff` on `variety="NORMAL"` (2026-06-12)**: the stub's order params include `stoploss` and `squareoff`, but those only take effect on bracket/robo varieties — on a NORMAL market order they're silently dropped, leaving the position with **no protective stop**. When wiring live orders, place the SL as a separate order (or use the correct variety). This is a money-losing trap, not a cosmetic one.

## Research scripts (Windows)

- **`UnicodeEncodeError` on ₹ / unicode (2026-06-05)**: `/research` (Perplexity) output containing `₹` crashes on Windows cp1252. Fix: set `$env:PYTHONUTF8 = "1"` before running. Same fix applies to running any trading script that prints `₹`/`—` — pass `PYTHONIOENCODING=utf-8`.
