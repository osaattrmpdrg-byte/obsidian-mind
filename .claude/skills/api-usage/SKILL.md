---
name: api-usage
description: Use BEFORE any paid API call (Perplexity / Grok / Gemini — via /research, /research-deep, /x-read, /x-pulse, /notebooklm, or direct provider calls) to gate the spend against the Tier 1/2/3 framework and log it, AND on demand ("audit api usage", "how much have I spent on APIs") to report spend per provider and ROI drift. The single operational layer over reference/research/api-decision-framework.md.
---

# api-usage

Full-lifecycle discipline for paid API spend (Perplexity, Grok, Gemini). A **gate**
on the way out, an **audit** on the way back, sharing one append-only ledger at
`brain/api-ledger.jsonl`.

Governing rule (from [[api-decision-framework]]): **API spend should translate to
money.** Never be cheap on Tier-1 tactical calls; scrutinize everything else. This
skill operationalizes that framework — it does not replace it. The framework note
stays the single source of truth for tier logic.

`scripts/audit.py` is stdlib-only (no pip installs). Run it with `python`.

---

## Gate mode (default — runs before a paid call)

Trigger: you are about to call Perplexity / Grok / Gemini (any of `/research`,
`/research-deep`, `/x-read`, `/x-pulse`, `/notebooklm`, or a direct provider API).

1. **Classify the query** against the three tiers in [[api-decision-framework]]:

   | Tier | What it is | Verdict |
   |---|---|---|
   | **Tier 1** | Tactical / pre-trade / real-time — feeds a decision with money on the line | **PAY** — no friction, call immediately |
   | **Tier 2** | Strategic — useful but not time-critical | **VAULT-FIRST** — QMD-check the vault; call only if missing or stale |
   | **Tier 3** | Foundational / definitional — Claude already knows this | **CLAUDE-ONLY** — do not call |

2. **For Tier 2 (VAULT-FIRST):** run a QMD query first. If the vault answers it,
   stop — use the vault, log the decision as `vault-first`. If the vault is missing
   or stale, escalate to a call and log it as `pay`.

3. **Emit the verdict + a one-line reason** to the user before proceeding.

4. **Log the decision.** On **PAY** or **VAULT-FIRST**, append one line to the ledger:

   ```bash
   python .claude/skills/api-usage/scripts/audit.py record \
     --provider perplexity --query "btc ema50/200 macro precursors" \
     --verdict pay --tier 1
   ```

   `--verdict` is `pay` | `vault-first` | `claude-only`; `--tier` is `1` | `2` | `3`.
   The record command creates the ledger on first use and stamps the timestamp and
   estimated cost automatically. Log the **final** verdict — a vault-first that
   escalates to an actual call is logged as `pay`, so cost accounting stays clean.
   Do not log CLAUDE-ONLY decisions (no call, nothing to track).

### Worked examples

- *"What's BTC funding doing right now before I size this trade?"* → **Tier 1 / PAY.**
  Real-time, pre-trade. Call Perplexity, log `--verdict pay --tier 1`.
- *"Broad scan of 20-bar breakout edge across FX majors."* → **Tier 2 / VAULT-FIRST.**
  QMD the vault first; the 2026-06-05 research notes may already cover it. Call only
  on a gap, log `vault-first` (or `pay` if escalated).
- *"What is the EMA50/200 golden cross?"* → **Tier 3 / CLAUDE-ONLY.** Definitional.
  Answer directly, no call, no log.

---

## Audit mode (on demand)

Trigger: "audit api usage", "how much have I spent on APIs", or a weekly cadence.

```bash
# print the report
python .claude/skills/api-usage/scripts/audit.py audit

# print AND save a dated note under brain/api-audits/
python .claude/skills/api-usage/scripts/audit.py audit --save
```

The report shows, per provider: calls logged, billable calls, and estimated cost
(period + lifetime total). It then cross-checks the ledger against research
artifacts in `Research/Web/` and `reference/research/` and flags **drift**:

- **WASTED SPEND** — a `pay` ledger entry with no matching artifact (paid, produced nothing).
- **UNTRACKED CALLS** — a dated research artifact with no matching ledger entry (a call that skipped the gate).

Matching is best-effort (date proximity + query/slug word overlap), so treat drift
as a prompt to investigate, not a hard accusation. `--save` writes
`brain/api-audits/API Audit YYYY-MM-DD.md` linking back to [[api-decision-framework]].

---

## Cost table

As of 2026-06-18, Perplexity calls (`research.py`, `research_deep.py`, `finance.py`)
compute **real token-based cost** per call via `lib/perplexity.py`'s `PRICING` table
and `estimate_cost()`, and log that real number to the ledger — not a flat guess.
This matters: the old flat `$0.005/call` estimate undercounted actual spend by ~10x,
because output tokens (not request count) drive Perplexity cost — `sonar-pro` output
is $15/M tokens vs plain `sonar` at $1/M. See [[api-decision-framework]] — Cost
Optimization Strategy — for the general rule this generalizes to any paid API.

`COST_TABLE` in `scripts/audit.py` is now a **fallback only**, used when a ledger
entry has no real `est_cost_usd` attached (manual `audit.py record` calls, or
legacy pre-fix rows).

| Provider | Real cost source | Fallback (if missing) |
|---|---|---|
| Perplexity Sonar / Sonar-Pro | token usage × `PRICING` table in `lib/perplexity.py` | $0.005 |
| Perplexity Finance Search | flat ~$0.005/invocation (not token-metered) | $0.005 |
| Perplexity Deep (research-deep) | sum of 3 calls' real token cost | $0.02 |
| Gemini | $0 | free tier |
| YouTube Data API | $0 | free quota |
| Grok | $0 (placeholder) | pending real pricing — [[grok-api-pending]] |

---

## Notes

- Ledger missing → audit reports "no ledger yet" but still counts artifacts (so a
  fresh vault shows historical research as UNTRACKED — expected; the ledger only
  logs from the day it starts).
- Malformed ledger lines are skipped with a warning, never crash the audit.
- Tests: `cd scripts && python -m unittest` (stdlib unittest, no pytest needed).
- Future: if the gate gets skipped in practice, add a PreToolUse hook for
  unbypassable enforcement (Approach C in the design spec).
