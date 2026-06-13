"""api-usage audit: read the spend ledger, cross-check vault artifacts, report.

Stdlib-only. See docs/superpowers/specs/2026-06-07-api-usage-skill-design.md.
"""

import datetime
import glob
import json
import os
import re

# Seed unit costs (USD per call). Edit as pricing changes.
# grok cost is pending — see [[grok-api-pending]]; treated as $0 until known.
COST_TABLE = {
    "perplexity": 0.005,
    "perplexity-finance": 0.005,  # Finance Search: ~$5 / 1000 invocations
    "gemini": 0.0,
    "youtube": 0.0,
    "grok": 0.0,
}

# A logged call counts as a real (billable) call when its verdict is "pay".
# The gate logs the FINAL verdict: a vault-first that escalates to a call is
# logged as "pay", so cost accounting stays clean.
BILLABLE_VERDICTS = {"pay"}


def load_ledger(path):
    """Parse a JSONL ledger. Returns (entries, warnings); skips malformed lines."""
    entries = []
    warnings = []
    try:
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    warnings.append(f"skipped malformed ledger line {i}")
    except FileNotFoundError:
        return [], ["no ledger yet"]
    return entries, warnings


def summarize_by_provider(entries):
    """Per-provider {count, calls, est_cost_usd}. Cost counts billable calls only."""
    summary = {}
    for e in entries:
        provider = e.get("provider", "unknown")
        billable = e.get("verdict") in BILLABLE_VERDICTS
        row = summary.setdefault(
            provider, {"count": 0, "calls": 0, "est_cost_usd": 0.0})
        row["count"] += 1
        if billable:
            row["calls"] += 1
            row["est_cost_usd"] += COST_TABLE.get(provider, 0.0)
    return summary


_STOPWORDS = {"the", "and", "for", "with", "what", "how", "are", "was", "does",
              "from", "that", "this", "into", "over", "under", "plus"}


def tokenize(text):
    """Lowercased significant words (len>=3, minus stopwords) as a set."""
    words = re.split(r"[^a-z0-9]+", (text or "").lower())
    return {w for w in words if len(w) >= 3 and w not in _STOPWORDS}


def _ordinal(date_str):
    try:
        return datetime.date.fromisoformat(date_str[:10]).toordinal()
    except (ValueError, TypeError):
        return None


def _token_overlap(a_tokens, b_tokens):
    """Count a-tokens that equal or are contained in some b-token (or vice
    versa). Substring containment handles tickers: "btc"/"usd" vs slug "btcusd"."""
    count = 0
    for a in a_tokens:
        for b in b_tokens:
            if a == b or (len(a) >= 3 and a in b) or (len(b) >= 3 and b in a):
                count += 1
                break
    return count


def _matches(entry, artifact, day_window=1, min_overlap=2):
    """An entry matches an artifact on date proximity AND word overlap."""
    ed, ad = _ordinal(entry.get("ts", "")), _ordinal(artifact.get("date", ""))
    if ed is None or ad is None or abs(ed - ad) > day_window:
        return False
    overlap = _token_overlap(tokenize(entry.get("query", "")), artifact.get("words", set()))
    return overlap >= min_overlap


def detect_drift(entries, artifacts):
    """wasted_spend = billable entries with no artifact; untracked = artifacts
    with no entry. Best-effort match by date proximity + query/slug overlap."""
    wasted = []
    for e in entries:
        if e.get("verdict") not in BILLABLE_VERDICTS:
            continue
        if not any(_matches(e, a) for a in artifacts):
            wasted.append(e)
    untracked = [a for a in artifacts
                 if not any(_matches(e, a) for e in entries)]
    return {"wasted_spend": wasted, "untracked": untracked}


# Vault dirs scanned for research artifacts produced by paid calls.
ARTIFACT_GLOBS = ("Research/**/*.md", "reference/research/**/*.md")
_DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})\b")


def find_artifacts(vault_dir):
    """Discover dated research notes. Returns list of {name, path, date, words}."""
    artifacts = []
    seen = set()
    for pattern in ARTIFACT_GLOBS:
        for path in glob.glob(os.path.join(vault_dir, pattern), recursive=True):
            if path in seen:
                continue
            seen.add(path)
            name = os.path.basename(path)
            m = _DATE_PREFIX.match(name)
            if not m:
                # Undated files (e.g. the framework note itself) are not
                # paid-call artifacts — skip them.
                continue
            slug = name[m.end():]
            artifacts.append({"name": name, "path": path, "date": m.group(1),
                              "words": tokenize(slug)})
    return artifacts


def build_report(summary, drift, warnings, period_label="lifetime"):
    """Render a human-readable audit report string."""
    lines = [f"# API Usage Audit ({period_label})", ""]
    if warnings:
        lines += ["> " + "; ".join(warnings), ""]

    lines.append("## Spend by provider")
    total = 0.0
    if summary:
        for provider in sorted(summary):
            row = summary[provider]
            total += row["est_cost_usd"]
            lines.append(
                f"- **{provider}**: {row['count']} logged, {row['calls']} calls"
                f" ~ ${row['est_cost_usd']:.4f}")
    else:
        lines.append("- (no entries)")
    lines += [f"- **Total est. spend: ${total:.4f}**", ""]

    wasted = drift.get("wasted_spend", [])
    untracked = drift.get("untracked", [])
    lines.append(f"## WASTED SPEND ({len(wasted)})")
    lines += ([f"- {e.get('provider')}: \"{e.get('query')}\" - paid, no artifact found"
               for e in wasted] or ["- none"])
    lines.append("")
    lines.append(f"## UNTRACKED CALLS ({len(untracked)})")
    lines += ([f"- {a.get('name')} - artifact with no ledger entry"
               for a in untracked] or ["- none"])
    return "\n".join(lines)


def record_entry(ledger_path, provider, query, verdict, tier, ts=None,
                 est_cost_usd=None):
    """Append one gate decision to the JSONL ledger (creating it if needed)."""
    if ts is None:
        ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    if est_cost_usd is None:
        est_cost_usd = COST_TABLE.get(provider, 0.0) if verdict == "pay" else 0.0
    entry = {"ts": ts, "provider": provider, "query": query,
             "verdict": verdict, "tier": tier, "est_cost_usd": est_cost_usd}
    os.makedirs(os.path.dirname(os.path.abspath(ledger_path)), exist_ok=True)
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def _default_vault_root():
    # scripts/ -> api-usage/ -> skills/ -> .claude/ -> <vault>
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", "..", "..", ".."))


def run_audit(vault_dir):
    """Pure orchestration over the vault: returns the rendered report string."""
    ledger_path = os.path.join(vault_dir, "brain", "api-ledger.jsonl")
    entries, warnings = load_ledger(ledger_path)
    summary = summarize_by_provider(entries)
    artifacts = find_artifacts(vault_dir)
    drift = detect_drift(entries, artifacts)
    return build_report(summary, drift, warnings)


def _ledger_path(vault_dir):
    return os.path.join(vault_dir, "brain", "api-ledger.jsonl")


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description="Audit/record paid API usage.")
    parser.add_argument("--vault", default=_default_vault_root(),
                        help="vault root (defaults to this skill's vault)")
    sub = parser.add_subparsers(dest="cmd")

    pa = sub.add_parser("audit", help="report spend + ROI drift (default)")
    pa.add_argument("--save", action="store_true",
                    help="write a dated audit note under brain/api-audits/")
    pa.add_argument("--date", help="YYYY-MM-DD for the saved note filename")

    pr = sub.add_parser("record", help="append one gate decision to the ledger")
    pr.add_argument("--provider", required=True)
    pr.add_argument("--query", required=True)
    pr.add_argument("--verdict", required=True,
                    choices=["pay", "vault-first", "claude-only"])
    pr.add_argument("--tier", required=True, type=int, choices=[1, 2, 3])
    pr.add_argument("--ts")
    args = parser.parse_args(argv)

    if args.cmd == "record":
        entry = record_entry(_ledger_path(args.vault), provider=args.provider,
                             query=args.query, verdict=args.verdict,
                             tier=args.tier, ts=args.ts)
        print(f"Logged: {entry['provider']} / {entry['verdict']} "
              f"(tier {entry['tier']}) ~ ${entry['est_cost_usd']:.4f}")
        return 0

    save = getattr(args, "save", False)
    date = getattr(args, "date", None)
    report = run_audit(args.vault)
    print(report)

    if save:
        date = date or datetime.date.today().isoformat()
        out_dir = os.path.join(args.vault, "brain", "api-audits")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"API Audit {date}.md")
        front = (f"---\ndate: {date}\n"
                 "description: \"API usage audit — spend per provider, ROI drift "
                 "(wasted spend, untracked calls)\"\n"
                 "tags:\n  - brain\n  - api-audit\n---\n\n")
        body = report + "\n\nRelated: [[api-decision-framework]]\n"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(front + body)
        print(f"\nSaved: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
