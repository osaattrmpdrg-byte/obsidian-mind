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

## CoinDCX REST API

- **A *generic* `400 Invalid request` on `/orders/create` is NOT necessarily a payload bug — and NOT necessarily a key-permission bug (2026-06-13)**: hit this hard. Reads (balances, market data) all work; every order write returns the same generic 400 regardless of payload. The *uniformity* tempted a "read-only key" diagnosis — **wrong** (the dashboard showed Trading permission enabled + IP whitelisted). Systematically ruled out: auth, trade permission, IP, market identifier (`"BTCUSDT"` is correct — pair form `"B-BTC_USDT"` gives a *different* `422`, proving the name is accepted), clock skew, string-vs-float numbers, `ecode` field, price-band. Our client was confirmed **byte-identical to the working `svamja/coindcx-python` reference lib**. Leading cause: the **`B`-ecode (Binance-mirrored) USDT markets may not be REST-orderable** for the account despite `status:active`, or an **account-level API-trading activation** is needed. **Lesson: "uniform failure ⇒ X" is a weak inference** — uniformity fits payload bugs, permission bugs, AND account-side blocks equally. When our code matches a known-working reference, stop guessing and go to exchange support. See [[CoinDCX Execution Layer]].
- **Small quantities serialize to scientific notation and break orders — FIXED (2026-06-13)**: `json.dumps(0.00005)` → `"5e-05"`, which CoinDCX rejects. Any quantity **< 0.0001** (including the `1e-05` market minimum and any min-notional-sized BTC order) hits it; offline tests with `0.0012`-size quantities won't catch it. Fix in `coindcx_client.py`: `_plain_decimal()` + `_signed_post(number_fields=...)` emit the fields as plain non-scientific **JSON numbers** (raw, unquoted — matches the reference lib) via placeholder injection. 17 tests green. See [[CoinDCX Execution Layer]].

## Backtest reproducibility & live-exit divergence

- **The live exit (`monitor_trades.py`) does NOT match the exit the proven edge was validated under (2026-06-13)** — `[VERIFIED]`, money-touching. Surfaced while testing a multi-indicator idea (see [[Research Queue#Parked — Phase 2]]). Hunt findings:
  - **EUR/USD +0.131R IS real and reproducible** — it's saved in `D:\trading_system\results\breakout_trail5_portfolio.csv` (EUR: n=92, 54.3% WR, raw +0.251R → adj +0.131R, 2004–2026, matches the vault exactly). The exit that produced it: **pure 5-bar trailing stop, NO fixed take-profit** — 73 `trail` exits, 19 losses, and **winners ran to +5.36R**. The right-tail winners ARE the edge.
  - **The live monitor truncates that edge.** `monitor_trades.py` exits with priority **SL > TP(+2.0R) > 5-bar trail**. The validated run had no TP cap; the live TP would chop every +2-to-+5R winner down to +2.0R — removing exactly the fat right tail that makes a 54%-WR strategy net-positive. A faithful reconstruction *with* the TP cap collapses EUR to −0.278R / 25% WR. **So live ≠ backtest, and the gap deletes the edge.**
  - **The generating script is GONE and there's no way to recover it: `D:\trading_system` is not a git repo** (`fatal: not a git repository`). Only `monitor_trades.py` references trailing logic, and it's the live monitor, not the backtester. The validation script that wrote `breakout_trail5_portfolio.csv` no longer exists in any form.
  - **XAU/USD +0.278R has ZERO saved artifact** — no XAU results CSV anywhere on the drive, no script. The live *primary* instrument's proven number is currently **unverifiable** (worse than EUR, which at least has the CSV). Treat XAU's [[Trading System#Proven Signals]] row as `[BROWSE NEEDED]` until re-derived.
  - **Correction to my first pass:** I initially claimed "the proven stats don't reproduce." Wrong — EUR reproduces from the saved CSV; *my* reconstruction was buggy (added a TP cap + too-tight trail). The real problems are the three above: lost script, live-exit divergence, missing XAU artifact.
  - **Before live capital (Path to Live Phase 4):** (1) remove the fixed TP from `monitor_trades.py` so live exit = validated pure-trailing; (2) re-derive XAU on a trailing exit and re-bless or correct +0.278R; (3) put `trading_system` under git so the next validated edge can't vanish. Experiment: `validate_confirming_filters.py`; gauntlet: `_gauntlet_adx_xau.py`. See [[Trading System]].

## Research scripts (Windows)

- **`UnicodeEncodeError` on ₹ / unicode (2026-06-05)**: `/research` (Perplexity) output containing `₹` crashes on Windows cp1252. Fix: set `$env:PYTHONUTF8 = "1"` before running. Same fix applies to running any trading script that prints `₹`/`—` — pass `PYTHONIOENCODING=utf-8`.
- **Now fixed at source in the obsidian-second-brain toolkit (2026-06-14)**: the per-run `PYTHONUTF8` workaround is no longer needed for the research scripts. `lib/config.py` reconfigures `stdout`/`stderr` to UTF-8 on import (covers every paid script that imports it), and `lib/vault.py` `write_note`/`append_to_log`/`append_to_daily` now write files with `encoding="utf-8"`. **Two distinct cp1252 traps, both bit this session**: (1) `print()` of unicode to the console (the old known one), and (2) `Path.write_text(s)` *defaulting* to cp1252 when saving notes — the second silently lost a finished Perplexity dossier because the crash fired *before* the save. **Lesson: on Windows, always pass `encoding="utf-8"` to every file write and reconfigure stdio; never rely on the platform default.** A subprocess that emits UTF-8 also needs the *caller* to read with `encoding="utf-8"` (or route emoji/progress to stderr so machine-mode stdout stays ASCII) — see the `vault_health.py --json` fix. Building the `/finance` tool ([[api-decision-framework]]) surfaced all of these.
