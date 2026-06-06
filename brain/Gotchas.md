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

## Research scripts (Windows)

- **`UnicodeEncodeError` on ₹ / unicode (2026-06-05)**: `/research` (Perplexity) output containing `₹` crashes on Windows cp1252. Fix: set `$env:PYTHONUTF8 = "1"` before running.
