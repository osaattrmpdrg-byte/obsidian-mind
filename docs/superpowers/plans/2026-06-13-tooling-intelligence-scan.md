---
date: 2026-06-13
description: "Implementation plan for the daily AI-tooling intelligence scan — TDD tasks for the life-os GitHub Actions rail (fetch, dedup, A-filter classify, Telegram + vault delivery)."
tags:
  - work-note
  - automation
  - plan
status: proposed
quarter: Q2-2026
---

# Tooling Intelligence Scan — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A daily, deduped, near-free scan of how people use AI tooling (Claude Code, OpenClaw, Obsidian, MCP, agents) that surfaces project-attached "try/queue/ignore" verdicts to a dedicated Telegram channel and a compounding vault note.

**Architecture:** A self-contained Python script (`scripts/tooling_scan.py`) in the `life-os` repo, run daily by GitHub Actions on the proven `brief.py` rail (machine-off, Groq + free sources + optional Perplexity gap-fill). It fetches free HN/Reddit/arXiv items, dedups against a committed `tooling_seen.json` ledger, classifies new items with Groq against Dileep's active projects (the A-filter), and delivers: a Telegram one-liner to a dedicated channel (silent on no-new-signal days) + an AI-first digest note committed into the `obsidian-mind` vault via the GitHub contents API.

**Tech Stack:** Python 3.11 (stdlib `urllib`, `json`, `hashlib`), Groq SDK (already used by `brief.py`), GitHub Actions cron, Telegram Bot API, GitHub contents API. No new infrastructure class; no Claude Agent SDK credit consumed.

**Repos touched:**
- `C:\Users\drajg\life-os` (script, tests, workflow, seen-ledger) — GitHub `osaattrmpdrg-byte/life-os`
- `d:\projectsobsidian-mind` (digest notes land in `reference/research/tooling/`) — GitHub `osaattrmpdrg-byte/obsidian-mind`

**New GitHub secrets required (set in `life-os` repo settings → Secrets):**
- `TOOLING_CHAT` — chat_id of a NEW Telegram channel/group (same `@DileepLifeOSBot`, add the bot to it). Keeps tooling out of the trading approval chat (`TELEGRAM_CHAT`).
- `VAULT_PAT` — a GitHub PAT with `contents:write` on `osaattrmpdrg-byte/obsidian-mind`, for committing digest notes.
- `PERPLEXITY_API_KEY` — OPTIONAL. If absent, the scan runs free-sources-only; if present, it gap-fills. Build works day 1 without it.
- (already present: `GROQ_API_KEY`, `TELEGRAM_TOKEN`.)

---

### Task 1: Scaffold the scan module + stable item IDs

**Files:**
- Create: `C:\Users\drajg\life-os\scripts\tooling_scan.py`
- Create: `C:\Users\drajg\life-os\tests\test_tooling_scan.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_tooling_scan.py
from scripts.tooling_scan import item_id

def test_item_id_is_stable_and_url_based():
    a = {"title": "Claude Code tips", "url": "https://news.ycombinator.com/item?id=1"}
    b = {"title": "DIFFERENT TITLE", "url": "https://news.ycombinator.com/item?id=1"}
    c = {"title": "Claude Code tips", "url": "https://news.ycombinator.com/item?id=2"}
    assert item_id(a) == item_id(b)      # same URL → same id (title noise ignored)
    assert item_id(a) != item_id(c)      # different URL → different id
    assert len(item_id(a)) == 16         # short stable hex
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py::test_item_id_is_stable_and_url_based -v`
Expected: FAIL with `ModuleNotFoundError` / `ImportError: cannot import name 'item_id'`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/tooling_scan.py
"""
Daily AI-tooling intelligence scan for GitHub Actions.
Fetches free HN/Reddit/arXiv chatter about AI tooling, dedups against a seen-ledger,
classifies new items against Dileep's active projects (the A-filter) with Groq,
and delivers a Telegram one-liner + an AI-first vault note.

Usage:
  python scripts/tooling_scan.py            # real run
  python scripts/tooling_scan.py --dry-run  # fetch + classify, print, no deliver/commit
"""
import hashlib


def item_id(item: dict) -> str:
    """Stable 16-char id derived from the item URL only (title noise ignored)."""
    return hashlib.sha256(item["url"].strip().encode()).hexdigest()[:16]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py::test_item_id_is_stable_and_url_based -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py tests/test_tooling_scan.py
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): scaffold module + stable item IDs"
```

---

### Task 2: Seen-ledger dedup with bounded pruning

**Files:**
- Modify: `C:\Users\drajg\life-os\scripts\tooling_scan.py`
- Modify: `C:\Users\drajg\life-os\tests\test_tooling_scan.py`

- [ ] **Step 1: Write the failing test**

```python
from scripts.tooling_scan import dedup_new, prune_seen

def test_dedup_returns_only_unseen_items():
    seen = {"abcabcabcabcabc0": "2026-06-10"}  # one already-seen id
    items = [
        {"title": "Old", "url": "https://x/old"},
        {"title": "New", "url": "https://x/new"},
    ]
    # force the first item's id into seen
    from scripts.tooling_scan import item_id
    seen = {item_id(items[0]): "2026-06-10"}
    fresh = dedup_new(items, seen)
    assert [i["title"] for i in fresh] == ["New"]

def test_prune_seen_drops_entries_older_than_cutoff():
    seen = {"id_old": "2026-04-01", "id_new": "2026-06-12"}
    pruned = prune_seen(seen, today="2026-06-13", keep_days=30)
    assert "id_new" in pruned and "id_old" not in pruned
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py -v`
Expected: FAIL with `ImportError: cannot import name 'dedup_new'`

- [ ] **Step 3: Write minimal implementation**

```python
from datetime import date

def dedup_new(items: list[dict], seen: dict[str, str]) -> list[dict]:
    """Return items whose id is not already in the seen ledger."""
    out = []
    for it in items:
        if item_id(it) not in seen:
            out.append(it)
    return out

def prune_seen(seen: dict[str, str], today: str, keep_days: int = 30) -> dict[str, str]:
    """Drop ledger entries first-seen more than keep_days before today (ISO dates)."""
    t = date.fromisoformat(today)
    kept = {}
    for k, first_seen in seen.items():
        try:
            age = (t - date.fromisoformat(first_seen)).days
        except ValueError:
            age = 0  # malformed date → keep, will age out next valid run
        if age <= keep_days:
            kept[k] = first_seen
    return kept
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py tests/test_tooling_scan.py
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): seen-ledger dedup + bounded pruning"
```

---

### Task 3: Parse free-source responses (HN Algolia fixture)

**Files:**
- Modify: `C:\Users\drajg\life-os\scripts\tooling_scan.py`
- Modify: `C:\Users\drajg\life-os\tests\test_tooling_scan.py`

- [ ] **Step 1: Write the failing test**

```python
import json
from scripts.tooling_scan import parse_hn

def test_parse_hn_extracts_title_url_points():
    raw = json.dumps({"hits": [
        {"title": "Show HN: my Claude Code setup", "objectID": "111",
         "url": "https://blog.example/claude", "points": 42},
        {"title": "Ask HN: best Obsidian AI workflow?", "objectID": "222",
         "url": None, "points": 8},  # no url → fall back to HN item permalink
    ]})
    items = parse_hn(raw)
    assert items[0]["url"] == "https://blog.example/claude"
    assert items[0]["points"] == 42
    assert items[0]["source"] == "HN"
    assert items[1]["url"] == "https://news.ycombinator.com/item?id=222"  # permalink fallback
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py::test_parse_hn_extracts_title_url_points -v`
Expected: FAIL with `ImportError: cannot import name 'parse_hn'`

- [ ] **Step 3: Write minimal implementation**

```python
import json

def parse_hn(raw: str) -> list[dict]:
    """Parse HN Algolia search JSON into normalized items."""
    data = json.loads(raw)
    out = []
    for h in data.get("hits", []):
        title = (h.get("title") or "").strip()
        if not title:
            continue
        url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
        out.append({
            "title": title,
            "url": url,
            "points": int(h.get("points") or 0),
            "source": "HN",
        })
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py::test_parse_hn_extracts_title_url_points -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py tests/test_tooling_scan.py
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): HN Algolia response parser"
```

---

### Task 4: Live free-source fetchers (HN + Reddit) — integration glue

**Files:**
- Modify: `C:\Users\drajg\life-os\scripts\tooling_scan.py`

No unit test (network I/O). Verified by the dry-run in Task 9.

- [ ] **Step 1: Add the fetchers and topic list**

```python
import urllib.request

# AI-tooling search surface. Edit to retune scope.
QUERIES = [
    "Claude Code",
    "OpenClaw",
    "Obsidian AI workflow",
    "MCP server",
    "AI agent workflow",
]
REDDIT_SUBS = ["ClaudeAI", "ObsidianMD", "LocalLLaMA"]
_UA = {"User-Agent": "Mozilla/5.0 (tooling-scan)"}

def _get(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def fetch_hn(query: str, days: int = 2, hits: int = 10) -> list[dict]:
    """HN Algolia: stories matching query from the last `days` days."""
    import time
    since = int(time.time()) - days * 86400
    url = ("https://hn.algolia.com/api/v1/search_by_date"
           f"?query={urllib.parse.quote(query)}&tags=story"
           f"&numericFilters=created_at_i>{since}&hitsPerPage={hits}")
    try:
        return parse_hn(_get(url))
    except Exception:
        return []

def fetch_reddit(sub: str, limit: int = 10) -> list[dict]:
    """Top posts of the day from a subreddit via the public JSON API."""
    url = f"https://www.reddit.com/r/{sub}/top.json?t=day&limit={limit}"
    try:
        data = json.loads(_get(url))
    except Exception:
        return []
    out = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        title = (d.get("title") or "").strip()
        if not title:
            continue
        out.append({
            "title": title,
            "url": "https://www.reddit.com" + d.get("permalink", ""),
            "points": int(d.get("score") or 0),
            "source": f"r/{sub}",
        })
    return out

def gather_free() -> list[dict]:
    items = []
    for q in QUERIES:
        items += fetch_hn(q)
    for s in REDDIT_SUBS:
        items += fetch_reddit(s)
    # dedup within this run by id, keep highest-points copy
    best = {}
    for it in items:
        k = item_id(it)
        if k not in best or it["points"] > best[k]["points"]:
            best[k] = it
    return list(best.values())
```

Note: `import urllib.parse` is needed — add it to the top-of-file imports alongside `urllib.request`.

- [ ] **Step 2: Smoke-check the fetchers locally**

Run: `cd /c/Users/drajg/life-os && python -c "from scripts.tooling_scan import gather_free; xs=gather_free(); print(len(xs), 'items'); print(xs[0] if xs else 'none')"`
Expected: prints a non-zero count and one sample item dict (network permitting)

- [ ] **Step 3: Commit**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): live HN + Reddit free-source fetchers"
```

---

### Task 5: A-filter classification prompt (project attachment + verdict)

**Files:**
- Modify: `C:\Users\drajg\life-os\scripts\tooling_scan.py`
- Modify: `C:\Users\drajg\life-os\tests\test_tooling_scan.py`

- [ ] **Step 1: Write the failing test**

```python
from scripts.tooling_scan import build_classify_prompt, parse_classify_response, ACTIVE_PROJECTS

def test_classify_prompt_lists_items_and_projects():
    items = [{"title": "New MCP server for git", "url": "https://x/1", "source": "HN", "points": 5}]
    p = build_classify_prompt(items)
    assert "New MCP server for git" in p
    assert ACTIVE_PROJECTS[0] in p           # projects offered as attachment targets
    assert "try" in p.lower() and "ignore" in p.lower()  # verdict vocabulary present

def test_parse_classify_response_tolerates_fenced_json():
    raw = '```json\n[{"idx":0,"verdict":"try","project":"vault automation","why":"speeds notes"}]\n```'
    out = parse_classify_response(raw, n_items=1)
    assert out[0]["verdict"] == "try"
    assert out[0]["project"] == "vault automation"

def test_parse_classify_response_defaults_missing_to_ignore():
    out = parse_classify_response("not json at all", n_items=2)
    assert all(o["verdict"] == "ignore" for o in out)   # safe fallback, never crash
    assert len(out) == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py -k classify -v`
Expected: FAIL with `ImportError: cannot import name 'build_classify_prompt'`

- [ ] **Step 3: Write minimal implementation**

```python
import re

ACTIVE_PROJECTS = [
    "CoinDCX execution layer",
    "Hunt harness (strategy discovery)",
    "vault automation",
    "research pipeline",
]

def build_classify_prompt(items: list[dict]) -> str:
    lines = []
    for i, it in enumerate(items):
        lines.append(f"[{i}] ({it['source']}, {it['points']} pts) {it['title']}\n    {it['url']}")
    catalogue = "\n".join(lines)
    projects = "\n".join(f"- {p}" for p in ACTIVE_PROJECTS)
    return f"""You are an AI-tooling intelligence filter for a solo builder.

His ACTIVE PROJECTS (the only things a finding may attach to):
{projects}

For EACH item below, decide:
- verdict: "try" ONLY if it would concretely speed up one named project this week;
           "queue" if relevant but not now; "ignore" if generic/no attachment point.
- project: the exact active-project name it speeds up, or "" if none.
- why: one short clause (<=12 words).

Return ONLY a JSON array, one object per item, in order:
[{{"idx":0,"verdict":"try|queue|ignore","project":"<name or empty>","why":"..."}}]

ITEMS:
{catalogue}
"""

def parse_classify_response(raw: str, n_items: int) -> list[dict]:
    """Parse Groq output defensively. Any failure → all-ignore fallback (never crash)."""
    default = [{"idx": i, "verdict": "ignore", "project": "", "why": ""} for i in range(n_items)]
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if not m:
        return default
    try:
        arr = json.loads(m.group(0))
    except Exception:
        return default
    by_idx = {}
    for o in arr:
        if isinstance(o, dict) and "idx" in o:
            by_idx[int(o["idx"])] = {
                "idx": int(o["idx"]),
                "verdict": str(o.get("verdict", "ignore")).lower().strip(),
                "project": str(o.get("project", "")).strip(),
                "why": str(o.get("why", "")).strip(),
            }
    return [by_idx.get(i, default[i]) for i in range(n_items)]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py -k classify -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py tests/test_tooling_scan.py
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): A-filter classification prompt + defensive parser"
```

---

### Task 6: Digest assembly + the "has new signal" gate

**Files:**
- Modify: `C:\Users\drajg\life-os\scripts\tooling_scan.py`
- Modify: `C:\Users\drajg\life-os\tests\test_tooling_scan.py`

- [ ] **Step 1: Write the failing test**

```python
from scripts.tooling_scan import merge_verdicts, has_signal, telegram_line, build_vault_note

def _classified():
    items = [
        {"title": "MCP for Obsidian", "url": "https://x/1", "source": "HN", "points": 30},
        {"title": "Random blog", "url": "https://x/2", "source": "HN", "points": 1},
    ]
    verdicts = [
        {"idx": 0, "verdict": "try", "project": "vault automation", "why": "auto-links notes"},
        {"idx": 1, "verdict": "ignore", "project": "", "why": ""},
    ]
    return merge_verdicts(items, verdicts)

def test_merge_attaches_verdict_to_item():
    m = _classified()
    assert m[0]["verdict"] == "try" and m[0]["project"] == "vault automation"

def test_has_signal_true_when_try_or_queue_present():
    assert has_signal(_classified()) is True
    ignore_only = [{"verdict": "ignore"}]
    assert has_signal(ignore_only) is False

def test_telegram_line_leads_with_try_item():
    line = telegram_line(_classified())
    assert "MCP for Obsidian" in line and "vault automation" in line

def test_vault_note_has_frontmatter_and_wikilink():
    note = build_vault_note(_classified(), date_str="2026-06-13")
    assert note.startswith("---")
    assert "ai-first: true" in note
    assert "[[Tech Watch]]" in note
    assert "https://x/1" in note            # source URL preserved verbatim
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py -k "merge or signal or telegram or vault_note" -v`
Expected: FAIL with `ImportError: cannot import name 'merge_verdicts'`

- [ ] **Step 3: Write minimal implementation**

```python
def merge_verdicts(items: list[dict], verdicts: list[dict]) -> list[dict]:
    by_idx = {v["idx"]: v for v in verdicts}
    out = []
    for i, it in enumerate(items):
        v = by_idx.get(i, {"verdict": "ignore", "project": "", "why": ""})
        out.append({**it, "verdict": v["verdict"], "project": v["project"], "why": v["why"]})
    return out

def has_signal(classified: list[dict]) -> bool:
    return any(c.get("verdict") in ("try", "queue") for c in classified)

def _ranked(classified: list[dict]) -> dict:
    order = {"try": 0, "queue": 1, "ignore": 2}
    return sorted(classified, key=lambda c: (order.get(c["verdict"], 3), -c.get("points", 0)))

def telegram_line(classified: list[dict]) -> str:
    top = _ranked(classified)[0]
    proj = f" (speeds up {top['project']})" if top["project"] else ""
    return f"🛠 Tooling scan: {top['title']} — {top['verdict']}{proj}. Details in vault."

def build_vault_note(classified: list[dict], date_str: str) -> str:
    tries  = [c for c in classified if c["verdict"] == "try"]
    queued = [c for c in classified if c["verdict"] == "queue"]
    ignored = [c for c in classified if c["verdict"] == "ignore"]
    top = (tries or queued or classified)[0]
    desc = f"Daily AI-tooling scan {date_str} — top: {top['title'][:80]}"
    fm = (f"---\n"
          f"date: {date_str}\n"
          f"description: \"{desc}\"\n"
          f"type: research\n"
          f"tags: [research, tooling, automation]\n"
          f"ai-first: true\n"
          f"sources: [{', '.join(c['url'] for c in classified)}]\n"
          f"---\n\n")
    body = ["## For future Claude",
            f"Autonomous AI-tooling scan on {date_str}. New (deduped) items only. "
            f"Verdicts are A-filter: 'try' = speeds up a named active project this week. "
            f"Links: [[Tech Watch]], [[api-decision-framework]].\n"]
    def section(title, rows):
        body.append(f"## {title}")
        if not rows:
            body.append("_none_\n")
            return
        for c in rows:
            proj = f" → **{c['project']}**" if c["project"] else ""
            why = f" — {c['why']}" if c["why"] else ""
            body.append(f"- [{c['title']}]({c['url']}) ({c['source']}, {c['points']} pts){proj}{why}")
        body.append("")
    section("TRY (act this week)", tries)
    section("QUEUE (relevant, not now)", queued)
    section("Rejected tooling (ignored)", ignored)
    return fm + "\n".join(body)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py -k "merge or signal or telegram or vault_note" -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py tests/test_tooling_scan.py
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): digest assembly + has-signal gate + vault note builder"
```

---

### Task 7: Delivery glue — Groq classify call, Telegram, vault commit, ledger persistence

**Files:**
- Modify: `C:\Users\drajg\life-os\scripts\tooling_scan.py`

Integration glue (mirrors `brief.py` patterns). No unit tests; verified by Task 9 dry-run + Task 10 live trigger.

- [ ] **Step 1: Add the Groq classify call**

```python
import os
from groq import Groq

def classify(items: list[dict]) -> list[dict]:
    if not items:
        return []
    prompt = build_classify_prompt(items)
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
    )
    verdicts = parse_classify_response(resp.choices[0].message.content, len(items))
    return merge_verdicts(items, verdicts)
```

- [ ] **Step 2: Add Telegram delivery to the dedicated channel**

```python
def send_telegram(text: str) -> None:
    token = os.environ["TELEGRAM_TOKEN"]
    chat  = os.environ["TOOLING_CHAT"]          # dedicated channel, NOT TELEGRAM_CHAT
    data = json.dumps({"chat_id": chat, "text": text,
                       "disable_web_page_preview": True}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=15)
```

- [ ] **Step 3: Add vault-note commit via the GitHub contents API**

```python
import base64

VAULT_REPO = "osaattrmpdrg-byte/obsidian-mind"

def commit_vault_note(path: str, content: str, message: str) -> None:
    """PUT the note into obsidian-mind via the contents API (no clone needed)."""
    pat = os.environ["VAULT_PAT"]
    api = f"https://api.github.com/repos/{VAULT_REPO}/contents/{urllib.parse.quote(path)}"
    # look up existing sha (so re-runs on the same date update, not 422)
    sha = None
    try:
        head = urllib.request.Request(api, headers={
            "Authorization": f"Bearer {pat}", "Accept": "application/vnd.github+json",
            "User-Agent": "tooling-scan"})
        with urllib.request.urlopen(head, timeout=15) as r:
            sha = json.loads(r.read()).get("sha")
    except Exception:
        sha = None
    body = {"message": message,
            "content": base64.b64encode(content.encode()).decode()}
    if sha:
        body["sha"] = sha
    put = urllib.request.Request(api, data=json.dumps(body).encode(), method="PUT",
        headers={"Authorization": f"Bearer {pat}", "Accept": "application/vnd.github+json",
                 "User-Agent": "tooling-scan", "Content-Type": "application/json"})
    urllib.request.urlopen(put, timeout=20)
```

- [ ] **Step 4: Add seen-ledger load/save**

```python
from pathlib import Path

SEEN_PATH = Path(__file__).parent / "tooling_seen.json"

def load_seen() -> dict:
    if SEEN_PATH.exists():
        try:
            return json.loads(SEEN_PATH.read_text())
        except Exception:
            return {}
    return {}

def save_seen(seen: dict) -> None:
    SEEN_PATH.write_text(json.dumps(seen, indent=0, sort_keys=True))
```

- [ ] **Step 5: Commit**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): Groq classify + Telegram + vault commit + ledger I/O"
```

---

### Task 8: The `main()` orchestrator + `--dry-run`

**Files:**
- Modify: `C:\Users\drajg\life-os\scripts\tooling_scan.py`

- [ ] **Step 1: Add the orchestrator**

```python
import sys
from datetime import datetime

def main() -> None:
    dry = "--dry-run" in sys.argv
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today}] tooling scan starting (dry={dry})")

    seen = load_seen()
    raw = gather_free()
    print(f"  fetched {len(raw)} items")
    fresh = dedup_new(raw, seen)
    print(f"  {len(fresh)} new after dedup")

    if not fresh:
        print("  no new items — silent, no ping.")
        return

    classified = classify(fresh)

    if dry:
        for c in _ranked(classified):
            print(f"  [{c['verdict']}] {c['title']}  ({c['project']})")
        return

    if has_signal(classified):
        note = build_vault_note(classified, today)
        path = f"reference/research/tooling/{today} tooling scan.md"
        commit_vault_note(path, note, f"tooling scan {today}")
        send_telegram(telegram_line(classified))
        print("  delivered: vault note + Telegram")
    else:
        print("  new items but no try/queue signal — vault note skipped, silent.")

    # record everything seen this run, then prune
    for c in classified:
        seen[item_id(c)] = today
    seen = prune_seen(seen, today, keep_days=30)
    save_seen(seen)
    print(f"  ledger now {len(seen)} ids")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the full unit suite (nothing regressed)**

Run: `cd /c/Users/drajg/life-os && python -m pytest tests/test_tooling_scan.py -v`
Expected: PASS (all tests from Tasks 1–6)

- [ ] **Step 3: Commit**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): main orchestrator with --dry-run"
```

---

### Task 9: Local dry-run verification (real fetch + real Groq, no deliver)

**Files:** none (verification only)

- [ ] **Step 1: Set Groq key and dry-run**

Run:
```bash
cd /c/Users/drajg/life-os && GROQ_API_KEY=<your_groq_key> python scripts/tooling_scan.py --dry-run
```
Expected: prints fetched count, new-after-dedup count, and a ranked verdict list. No Telegram, no commit. If zero items, re-run (HN/Reddit transient) or widen `QUERIES`.

- [ ] **Step 2: Sanity-check the A-filter output**

Confirm at least the verdicts look sane (generic items → ignore; a Claude/Obsidian/MCP item plausibly → try/queue with a project name). If everything is "ignore", tighten the prompt wording in `build_classify_prompt` and re-run. No commit unless you change code.

---

### Task 10: GitHub Actions workflow (daily cron) + secrets

**Files:**
- Create: `C:\Users\drajg\life-os\.github\workflows\tooling-scan.yml`

- [ ] **Step 1: Create the dedicated Telegram channel + secrets (manual, one-time)**

Do these in order, outside code:
1. In Telegram, create a new channel or group (e.g. "Tooling Scan"); add `@DileepLifeOSBot` as admin/member.
2. Get its chat_id (send a message, then `https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates` → read `chat.id`).
3. In `github.com/osaattrmpdrg-byte/life-os` → Settings → Secrets and variables → Actions, add:
   - `TOOLING_CHAT` = that chat_id
   - `VAULT_PAT` = a fine-grained PAT with `Contents: Read and write` on `obsidian-mind`
   - (optional) `PERPLEXITY_API_KEY` if/when gap-fill is wired (Task 11)

- [ ] **Step 2: Write the workflow**

```yaml
# .github/workflows/tooling-scan.yml
name: Tooling Scan
on:
  schedule:
    - cron: "17 2 * * *"      # 02:17 UTC daily — off the :00/:30 herd
  workflow_dispatch:
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install groq --quiet
      - name: Run tooling scan
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TOOLING_CHAT: ${{ secrets.TOOLING_CHAT }}
          VAULT_PAT: ${{ secrets.VAULT_PAT }}
        run: python scripts/tooling_scan.py
      - name: Persist seen-ledger
        run: |
          git config user.name "tooling-scan"
          git config user.email "bot@users.noreply.github.com"
          git add scripts/tooling_seen.json
          git diff --cached --quiet || git commit -m "chore(tooling-scan): update seen-ledger [skip ci]"
          git push
```

- [ ] **Step 3: Commit and push**

```bash
git -C "C:/Users/drajg/life-os" add .github/workflows/tooling-scan.yml
git -C "C:/Users/drajg/life-os" commit -m "ci(tooling-scan): daily cron workflow"
git -C "C:/Users/drajg/life-os" push
```

- [ ] **Step 4: Manual trigger + verify (evidence before done)**

1. GitHub → `life-os` → Actions → "Tooling Scan" → Run workflow.
2. Wait ~60s. Expected: green run; logs show fetched/new counts.
3. If new try/queue signal existed: check the dedicated Telegram channel for the one-liner, and `obsidian-mind` for `reference/research/tooling/<today> tooling scan.md`.
4. Confirm `scripts/tooling_seen.json` got a commit in `life-os`.
5. Re-run immediately: the second run should report "0 new after dedup" (proves dedup works end-to-end).

---

### Task 11: (OPTIONAL) Perplexity gap-fill

**Files:**
- Modify: `C:\Users\drajg\life-os\scripts\tooling_scan.py`
- Modify: `C:\Users\drajg\life-os\.github\workflows\tooling-scan.yml`

Only do this if free sources prove thin in practice (Task 10 regularly returns few items). Otherwise skip — free-first is the default per [[api-decision-framework]].

- [ ] **Step 1: Add a conditional gap-fill in `gather_free` callsite**

```python
def gather(min_free: int = 6) -> list[dict]:
    """Free sources first; Perplexity gap-fill ONLY if thin AND key present."""
    items = gather_free()
    key = os.environ.get("PERPLEXITY_API_KEY")
    if len(items) < min_free and key:
        items += _perplexity_gapfill(key)
        # re-dedup within run
        best = {}
        for it in items:
            k = item_id(it)
            if k not in best or it.get("points", 0) > best[k].get("points", 0):
                best[k] = it
        items = list(best.values())
    return items
```

Implement `_perplexity_gapfill(key)` to call the Sonar API for "recent AI tooling workflow posts", normalize results into the same `{title,url,points,source}` shape (`source="Perplexity"`, `points=0`), and return `[]` on any error. Point `main()` at `gather()` instead of `gather_free()`. Add `PERPLEXITY_API_KEY: ${{ secrets.PERPLEXITY_API_KEY }}` to the workflow env.

- [ ] **Step 2: Dry-run with the key set, confirm gap-fill only fires when free < min_free, commit.**

```bash
git -C "C:/Users/drajg/life-os" add scripts/tooling_scan.py .github/workflows/tooling-scan.yml
git -C "C:/Users/drajg/life-os" commit -m "feat(tooling-scan): optional Perplexity gap-fill (conditional)"
```

---

## Self-review

**Spec coverage:** daily cron (Task 10) ✓, free-first sources (Tasks 3–4) ✓, Perplexity gap-fill optional (Task 11) ✓, dedup seen-ledger (Tasks 2, 7, 8) ✓, A-filter project attachment (Task 5) ✓, dedicated Telegram channel (Task 7) ✓, vault note compounding (Tasks 6–7) ✓, silent-on-no-signal (Task 8) ✓, no Claude Agent SDK credit used (GitHub Actions + Groq/free, Task 10) ✓. Experiments-interactive and kill-criterion are operational (not code) — documented in the spec, no task needed.

**Placeholder scan:** the only deferred item is `_perplexity_gapfill` body in Task 11, which is explicitly OPTIONAL and gated on real need; every Phase-1 task has complete code.

**Type consistency:** item dict shape `{title, url, points, source}` is uniform across `parse_hn`, `fetch_reddit`, `gather_free`; `verdict` objects `{idx, verdict, project, why}` consistent across `build_classify_prompt`/`parse_classify_response`/`merge_verdicts`; `item_id` used identically in dedup, ledger write, and within-run dedup.

**Security:** no PAT in code — `VAULT_PAT`/`GROQ_API_KEY`/`TELEGRAM_TOKEN`/`TOOLING_CHAT` all via Actions secrets/env. (Separately: rotate the plaintext PATs currently embedded in both repos' git remote URLs.)