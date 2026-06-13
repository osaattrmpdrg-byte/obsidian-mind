"""Behavior tests for the api-usage audit script. Stdlib unittest only."""

import json
import os
import tempfile
import unittest

import audit


def write_ledger(lines):
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return path


class LoadLedgerTests(unittest.TestCase):
    def test_parses_valid_jsonl_into_entries(self):
        path = write_ledger([
            json.dumps({"ts": "2026-06-05T10:00", "provider": "perplexity",
                        "query": "btc breakout", "verdict": "pay", "tier": 1}),
            json.dumps({"ts": "2026-06-05T11:00", "provider": "gemini",
                        "query": "vault scan", "verdict": "vault-first", "tier": 2}),
        ])
        entries, warnings = audit.load_ledger(path)
        self.assertEqual(len(entries), 2)
        self.assertEqual(warnings, [])
        self.assertEqual(entries[0]["provider"], "perplexity")

    def test_skips_malformed_lines_and_warns(self):
        path = write_ledger([
            json.dumps({"ts": "2026-06-05T10:00", "provider": "perplexity",
                        "query": "q", "verdict": "pay", "tier": 1}),
            "{not valid json",
            "",
            json.dumps({"ts": "2026-06-05T12:00", "provider": "grok",
                        "query": "q2", "verdict": "pay", "tier": 1}),
        ])
        entries, warnings = audit.load_ledger(path)
        self.assertEqual(len(entries), 2)
        self.assertEqual(len(warnings), 1)
        self.assertIn("line 2", warnings[0])

    def test_missing_ledger_returns_empty_with_note(self):
        entries, warnings = audit.load_ledger("does-not-exist.jsonl")
        self.assertEqual(entries, [])
        self.assertEqual(warnings, ["no ledger yet"])


class SummaryTests(unittest.TestCase):
    def test_counts_and_costs_per_provider(self):
        entries = [
            {"provider": "perplexity", "verdict": "pay"},
            {"provider": "perplexity", "verdict": "pay"},
            {"provider": "perplexity", "verdict": "vault-first"},
            {"provider": "gemini", "verdict": "pay"},
        ]
        summary = audit.summarize_by_provider(entries)
        self.assertEqual(summary["perplexity"]["count"], 3)
        self.assertEqual(summary["perplexity"]["calls"], 2)
        self.assertAlmostEqual(summary["perplexity"]["est_cost_usd"], 0.01)
        self.assertEqual(summary["gemini"]["count"], 1)
        self.assertAlmostEqual(summary["gemini"]["est_cost_usd"], 0.0)


class DriftTests(unittest.TestCase):
    def test_flags_wasted_spend_and_untracked_calls(self):
        entries = [
            {"ts": "2026-06-05T10:00", "provider": "perplexity",
             "query": "btc ema breakout signal", "verdict": "pay"},
            {"ts": "2026-06-05T11:00", "provider": "perplexity",
             "query": "random nonsense topic xyz", "verdict": "pay"},
        ]
        artifacts = [
            {"name": "btc-ema.md", "date": "2026-06-05",
             "words": audit.tokenize("btc ema breakout historical performance")},
            {"name": "nzdusd.md", "date": "2026-06-07",
             "words": audit.tokenize("nzdusd trend characteristics breakout")},
        ]
        drift = audit.detect_drift(entries, artifacts)
        self.assertEqual([e["query"] for e in drift["wasted_spend"]],
                         ["random nonsense topic xyz"])
        self.assertEqual([a["name"] for a in drift["untracked"]],
                         ["nzdusd.md"])

    def test_ticker_query_matches_slug_artifact(self):
        # ledger "BTC/USD" -> {btc, usd}; slug "btcusd" -> {btcusd}.
        # Substring-aware matching must connect them so finance calls aren't
        # falsely flagged as wasted spend.
        entries = [{"ts": "2026-06-13T20:19", "provider": "perplexity-finance",
                    "query": "BTC/USD", "verdict": "pay"}]
        artifacts = [{"name": "2026-06-13 - btcusd.md", "date": "2026-06-13",
                      "words": audit.tokenize("btcusd")}]
        drift = audit.detect_drift(entries, artifacts)
        self.assertEqual(drift["wasted_spend"], [])
        self.assertEqual(drift["untracked"], [])

    def test_no_drift_when_everything_matches(self):
        entries = [{"ts": "2026-06-05T10:00", "provider": "perplexity",
                    "query": "btc ema breakout", "verdict": "pay"}]
        artifacts = [{"name": "a.md", "date": "2026-06-05",
                      "words": audit.tokenize("btc ema breakout performance")}]
        drift = audit.detect_drift(entries, artifacts)
        self.assertEqual(drift["wasted_spend"], [])
        self.assertEqual(drift["untracked"], [])


class FindArtifactsTests(unittest.TestCase):
    def test_discovers_dated_research_notes(self):
        vault = tempfile.mkdtemp()
        web = os.path.join(vault, "Research", "Web")
        os.makedirs(web)
        with open(os.path.join(web, "2026-06-05 - btc ema breakout.md"),
                  "w", encoding="utf-8") as f:
            f.write("# note")
        arts = audit.find_artifacts(vault)
        self.assertEqual(len(arts), 1)
        self.assertEqual(arts[0]["date"], "2026-06-05")
        self.assertIn("breakout", arts[0]["words"])

    def test_excludes_undated_notes(self):
        vault = tempfile.mkdtemp()
        rr = os.path.join(vault, "reference", "research")
        os.makedirs(rr)
        with open(os.path.join(rr, "api-decision-framework.md"),
                  "w", encoding="utf-8") as f:
            f.write("# framework, not an artifact")
        with open(os.path.join(rr, "2026-06-05 - real run.md"),
                  "w", encoding="utf-8") as f:
            f.write("# dated artifact")
        names = [a["name"] for a in audit.find_artifacts(vault)]
        self.assertEqual(names, ["2026-06-05 - real run.md"])


class RecordTests(unittest.TestCase):
    def test_append_creates_and_grows_ledger(self):
        path = os.path.join(tempfile.mkdtemp(), "api-ledger.jsonl")
        audit.record_entry(path, provider="perplexity", query="btc breakout",
                            verdict="pay", tier=1, ts="2026-06-13T10:00")
        audit.record_entry(path, provider="grok", query="x pulse",
                            verdict="vault-first", tier=2, ts="2026-06-13T11:00")
        entries, warnings = audit.load_ledger(path)
        self.assertEqual(warnings, [])
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["provider"], "perplexity")
        self.assertEqual(entries[0]["verdict"], "pay")
        self.assertEqual(entries[1]["tier"], 2)


class ReportTests(unittest.TestCase):
    def test_report_includes_costs_and_drift_flags(self):
        summary = {"perplexity": {"count": 2, "calls": 2, "est_cost_usd": 0.01}}
        drift = {"wasted_spend": [{"provider": "perplexity", "query": "q"}],
                 "untracked": [{"name": "orphan.md"}]}
        report = audit.build_report(summary, drift, ["no ledger yet"])
        self.assertIn("perplexity", report)
        self.assertIn("0.01", report)
        self.assertIn("WASTED", report.upper())
        self.assertIn("UNTRACKED", report.upper())
        self.assertIn("orphan.md", report)


if __name__ == "__main__":
    unittest.main()
