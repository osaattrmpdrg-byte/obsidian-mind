---
date: 2026-06-05
description: "Architectural and workflow decisions worth recalling across sessions — each links to its source work note"
tags:
  - brain
---

# Key Decisions

Architectural or workflow decisions worth recalling. Link to the full [[Decision Record]] when one exists.

## Trading Bot Architecture

- **Angel One over KiteConnect (2026-06-05)**: KiteConnect costs ₹2,000/month. Angel One SmartAPI is free. Both support MCX. Angel One chosen because better docs = faster build on September 4 deadline. Finvasia (zero brokerage) is the next upgrade when trade volume justifies it.
- **Two-layer validation design (2026-06-05)**: Pre-trade check runs circuit breakers first (local, free — consecutive losses, daily P&L limit) and only calls Perplexity if Layer 1 passes. This saves credits AND enforces risk discipline. Never call paid API if a circuit breaker has fired.
- **Double validation as a feature (2026-06-05)**: GitHub Actions scanner + Cloud Run bot both scan independently. If both fire on the same signal, that's higher conviction to execute. Not redundancy — confirmation.
- **Cloud Run over always-on VM (2026-06-05)**: Bot runs with `--min-instances 1` on Cloud Run. ~$3-5/month vs $300 GCP credits (expire 2026-09-04). Scales to zero after credits, or upgrade to paid when trading generates income.
- **Scanner reliability = heartbeat, not just a better scheduler (2026-06-06)**: Driver was fear of *silent* scanner failures. Key insight: a scanner that alerts only on signal makes "no signal" and "scanner dead" look identical — silence either way. A new scheduler alone doesn't fix this. **Fix (priority order):** (1) **dead-man's switch via `healthchecks.io`** (free) — scanner pings on success, missed ping → loud alert; works on the *current* GitHub Actions setup today. (2) **Cloud Run Job + Cloud Scheduler** — exact cron, no 60-day auto-disable (GitHub silently disables scheduled workflows after 60 days of repo inactivity), same platform as the bot. (3) **keep GitHub Actions as a redundant 2nd scanner** — two independent clouds, both must fail to miss a signal (extends the "double validation as a feature" decision). MVP = #1 alone now. See [[Trading System]].

## How to Advise Dileep

- **Inform, don't gatekeep — price the grind (2026-06-06)**: Dileep is willing to grind and make compromises to hit the goal faster. Do NOT suppress aggressive paths to protect work-life balance. Propose the faster path *with* honest pros/cons: the real acceleration (quantified), the real cost to the life (named specifically), the failure modes, and reversibility — then let him decide. The [[Vision]] is the scoreboard for pricing a compromise, not a veto. His explicit instruction; supersedes the earlier "protect the balance" framing. See [[Vision#How Claude should use this]].
- **Proactively surface AND use productivity avenues (2026-06-06)**: Standing instruction — don't wait to be asked. When a task could be done faster/better with an available capability, flag it and *use* it. Confirmed high-value tools to actively fold into workflows: **`/youtube`** (transcript+comments mining → Weekly Hunt candidates, content niche signals) and **`/notebooklm`** (vault-grounded synthesis + audio overviews to absorb own research off-screen). Beyond these, **periodically run `/scout`** to discover new skills/MCPs/tools — Dileep wants to know "can I use something like this?" even for capabilities he isn't aware of yet. Tie every suggestion to the streams / [[North Star]] goal; guard against research becoming a time sink ([[Vision]]). Seed: `thinking/2026-06-06-research-intelligence-pipeline.md`.

## Session Workflow

- **Session capture is obsidian-mind-native (2026-06-05)**: The `/log-session` skill (`~/.claude/commands/log-session.md`) was rewritten away from dead life-os paths. It now writes `thinking/session-logs/{date}-session.md`, updates `brain/Memories.md` Recent Context, and routes durable knowledge to the right brain note — **no GitHub auto-push** (git sync is the user's responsibility per CLAUDE.md). The Stop hook (`.claude/scripts/stop-checklist.ts`) references the skill rather than duplicating the structure, so there's a single source of truth. `/log-session` = lightweight capture; `/om-wrap-up` = full vault review.

## Trading Strategy & Instruments

- **EUR/USD reopened via NSE futures (2026-06-05)**: The "FEMA grey area" that disabled EUR/USD was a misunderstanding. EUR/USD is **legal** via NSE exchange-traded cross-currency futures (SEBI circular CIR/MRD/DP/20/2016, verified still in force). What's illegal is funding *offshore* forex brokers via LRS Schedule III — not the currency pair. Mental model: it's not "is forex legal?" but "WHERE are you trading it?" — Indian exchange = legal, offshore app = FEMA violation. EUR/USD (+0.131R, SIG train+test) marked **GO**, ~₹2,700/lot (cheapest instrument), same Angel One rails as gold. CA consultation **waived** as disproportionate at current scale (revisit when trading multiple lots). USD/CAD stays dead — not listed on NSE. See [[FEMA Forex Legality]].
- **Forex pair expansion closed (2026-06-05)**: EUR/JPY + GBP/JPY rejected (BoJ/MoF intervention risk), NZD/USD rejected (correlation twin of already-dead AUD/USD + no India-legal spot route). All JPY crosses permanently off. Tradeable universe = India-legal only: MCX gold, crypto (CoinDCX), NSE EUR/USD. See [[What Didn't Work]].
- **Position sizing at small capital (2026-06-05)**: At ₹5-6k use 1-2% risk/trade. Quarter-Kelly (6.9%) implies an unfundable position at this capital — only apply when capital > ₹30k. Trading returns alone (~10.8%/yr) won't hit the ₹50k target; salary injection post-conversion is the real multiplier. See [[Trading System#Position Sizing Rules]].
- **EMA50 rejection short deferred to Phase 2 (2026-06-05)**: No published edge, no India-legal short execution at small capital, same knife-catching family as already-rejected XAU short. Park until 20+ live long trades validate the core system.
- **"Daily Watch, Weekly Hunt" over a daily strategy generator (2026-06-05)**: A [[grill-me]] session killed the idea of a daily sweep that generates + backtests new strategies. Reason: mass-testing freely-generated candidates through a single-strategy gate manufactures false edges (multiple-comparisons / data-snooping) — the "winner" dies live. Replaced with two parts: **Daily Watch** (monitor the one proven edge — regime flip, signal fired, macro via CoinGecko MCP; invents nothing) + **Weekly Hunt** (one candidate at a time, gated by rationale-first → train backtest → cross-instrument confirmation on 3+ assets → a never-seen lockbox touched once → a trial-count penalty that raises the bar as N grows). New strategies are a "nice problem to have" *after* the proven edge earns. See [[Daily Watch Weekly Hunt]].

## Cloud / Infrastructure Strategy

- **GCP credits = two assets, not one (2026-06-06)**: $300 trial credits (expire 2026-09-04) are for **one-time heavy bursts**; the separate **"Always Free" tier** (never expires) is for **persistent always-on** services. Self-sustaining rule: *persistent → Always Free, expensive-but-occasional → trial credits, nothing that survives the cliff is allowed to cost money.* This **supersedes** the older "Cloud Run with `--min-instances 1` ~$3-5/mo" plan — prefer webhook / scale-to-zero so the bot is ₹0 *and* survives the cliff. Direction chosen: spend credits on **edge-discovery bursts that unblock stuck streams** (trading + content), not on hosting. See [[GCP Credits Strategy]].
- **Edge Generalization Sweep methodology — Hybrid, max breadth (2026-06-06)**: To answer "is the breakout edge real or just curve-fit to crypto," run **Phase 1 Lock-and-Apply** (fixed BTC-winning params applied *unchanged* across a maximum-breadth cross-asset universe, **correlation-aware aggregation** so correlated crypto can't fake the verdict) then **Phase 2 walk-forward + bootstrap** (CIs on expectancy *and worst-case drawdown*) on the tradeable survivors only. Long-only, daily bars, breakout edge only. Same anti-false-edge spirit as [[Daily Watch Weekly Hunt]]. See [[Edge Generalization Sweep]].

## Research & Intelligence Infrastructure

- **obsidian-second-brain integration (2026-06-05)**: 21 commands installed in `.claude/commands/`. Research scripts at `d:/projects/obsidian-second-brain/scripts/research/`. APIs: Perplexity (paid, ₹~₹0.02-0.80/query), Gemini (free tier), YouTube (free quota). Grok skipped for now.
- **API spend rule (2026-06-05)**: Tactical queries (pre-trade, real-time regime) — always spend, no compromise. Strategic queries (strategy research) — research once, cache in vault, reuse via `/trading-research`. See [[api-decision-framework]].

## Vault & Tooling Infrastructure

- **Obsidian MCP over REST CLI (2026-06-05)**: Local REST API plugin v4.1.3 has built-in MCP — no extra wrapper needed. Configured in `.mcp.json` as `type: http` at `https://127.0.0.1:27124/mcp/`. Bearer token in `.mcp.json` headers. Self-signed cert imported to Windows Trusted Root CA store. Gives Claude direct tool access to live vault (read, create, search, backlinks) without shelling out to CLI.
- **Community plugins installed (2026-06-05)**: Local REST API with MCP (v4.1.3, primary Claude↔Obsidian bridge), Templater (dynamic templates). Obsidian Git not found in plugin browser — manual git sync for now.
- **obsidian-cli npm fallback (2026-06-05)**: `obsidian-cli` installed globally. Requires `OBSIDIAN_API_KEY` env var. Use only if MCP is down — MCP is preferred.
- **CoinGecko MCP added, CoinDCX MCP rejected (2026-06-05)**: Added official CoinGecko MCP to `.mcp.json` (`type: http`, `https://mcp.api.coingecko.com/mcp`, free/keyless, read-only data) for live crypto market data during strategy sessions. Activates on Claude Code restart. Rejected the community CoinDCX MCP — it duplicates the self-built [[CoinDCX Execution Layer]] Python client and would hold trade credentials in stranger's code. Zerodha Kite / Angel One broker MCPs deferred until those accounts are KYC-live; broker MCP is *deploy* phase, not *validate* phase — backtesting runs on free historical data. Surfaced via a `/scout` full-refresh.

## Pending Integrations

- **Grok API — skipped for now (2026-06-05)**: Only needed for `/x-read` and `/x-pulse` (X/Twitter real-time discourse). Skipped because Perplexity + Gemini covers 90% of research needs and Grok costs add up with regular use. **Add when**: you want to monitor what X is saying about a topic in real-time, track discourse around a launch, or analyze a specific viral thread. Get key from console.x.ai — set `GROK_API_KEY` in `d:\projects\obsidian-second-brain\.env`.
