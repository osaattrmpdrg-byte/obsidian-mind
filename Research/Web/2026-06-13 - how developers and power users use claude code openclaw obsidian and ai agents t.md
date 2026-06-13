---
date: 2026-06-13
description: "Perplexity dossier on how 2026 power users wire Claude Code, OpenClaw, Obsidian and AI agents into always-on workflows — cron digests, vault-as-memory, MCP servers. First manual run of the tooling scan."
time: "14:47"
type: research
topic: "how developers and power users use Claude Code, OpenClaw, Obsidian, and AI agents to boost their workflow in 2026: notable setups, MCP servers, automation patterns, productivity workflows people actually adopt"
tags:
  - research
  - perplexity
  - how-developers-and-power-users-use-claud
model: sonar-pro
sources:
  - "https://maxmitcham.substack.com/p/how-to-build-an-ai-agent-operating"
  - "https://www.youtube.com/watch?v=6MBq1paspVU"
  - "https://www.ronforbes.com/blog/the-week-the-proactive-ai-assistant-went-mainstream"
  - "https://www.instagram.com/reel/DX6hPQsOQal/"
  - "https://claude-world.com/articles/openclaw-introduction/"
  - "https://www.facebook.com/groups/techtitansgroup/posts/1537028760957770/"
  - "https://sajalsharma.com/posts/openclaw-experiments/"
  - "https://www.contextstudios.ai/blog/the-complete-openclaw-guide-how-we-run-an-ai-agent-in-production-2026"
ai-first: true
---

## For future Claude

For future Claude: This note is a Perplexity Sonar deep dossier on "how developers and power users use Claude Code, OpenClaw, Obsidian, and AI agents to boost their workflow in 2026: notable setups, MCP servers, automation patterns, productivity workflows people actually adopt" performed on 2026-06-13 14:47. It captures key facts with recency markers, timeline, key players, contrarian views, and open questions. Every claim was sourced at the time of research - verify recency markers before relying on individual facts.

## Topic

how developers and power users use Claude Code, OpenClaw, Obsidian, and AI agents to boost their workflow in 2026: notable setups, MCP servers, automation patterns, productivity workflows people actually adopt

## Dossier

## Summary
Developers and power users in 2026 are increasingly running **Claude Code and OpenClaw as always‑on agents** wired into Obsidian, messaging apps, and MCP servers to automate both coding and knowledge work (as of 2026-03, contextstudios.ai[8]). These setups typically treat an **Obsidian vault as long‑term memory**, Claude Code as the local “hands” on the machine, and OpenClaw or similar orchestrators (Hermes, Cowork/Dispatch) as the control plane for multi‑step and scheduled workflows (as of 2026-05, maxmitcham.substack.com[1]; as of 2026-03, ronforbes.com[3]). Power users are converging on a small set of **automation patterns**: scheduled digest/cleanup crons, inbox and calendar triage, project dashboards synthesized from notes, and continuous refactoring of code and documentation (as of 2026-05, maxmitcham.substack.com[1]; as of 2026-04, sajalsharma.com[7]). MCP servers such as Gmail, Google Calendar, Google Workspace CLI, browser automation tools, and Obsidian‑like file interfaces are commonly used to give agents structured access to real data and actions (as of 2026-03, ronforbes.com[3]; as of 2026-05, maxmitcham.substack.com[1]). While the tooling has matured, there is still wide variation in real‑world adoption patterns, and many workflows remain bespoke and under‑documented outside of blog posts and small community demos (as of 2026-05, maxmitcham.substack.com[1]; as of 2026-04, sajalsharma.com[7]).

---

## Key Facts
- **Hermes + Claude Code + OpenClaw + Obsidian** is promoted as a compact “AI agent operating system” where Hermes orchestrates, Claude Code executes tasks, OpenClaw handles heavy tool calling, and Obsidian provides a three‑layer memory architecture (raw/wiki/output) (as of 2026-05, maxmitcham.substack.com[1]).

- In this stack, **Hermes** is positioned as the primary control layer that manages other tools and provides a clean way to run agent workflows from the terminal (as of 2026-05, maxmitcham.substack.com[1]).

- **OpenClaw** is recommended only for workflows that genuinely need many tool calls or complex coordination, not for routine day‑to‑day orchestration (as of 2026-05, maxmitcham.substack.com[1]).

- **Claude Code** is used as a command‑line coding and execution agent that can control the computer via natural language and is especially powerful when given large, persistent context files or an entire Obsidian vault to read (as of 2026-04, youtube.com[2]).

- The **Obsidian CLI** introduced the ability for external tools like Claude Code to read both Obsidian markdown files and their inter‑note relationships (graph), enabling agents to surface cross‑note patterns and connections (as of 2026-04, youtube.com[2]).

- At least one power user (Vin) runs a life‑management system where an Obsidian vault is filled with plans, specs, and technical guides rather than reflections, and custom Claude Code commands like `/today`, `/trace`, `/connect`, `/ghost`, and `/challenge` operate on that vault (as of 2026-04, youtube.com[2]).

- The `/today` command shown in that system pulls calendar data, tasks, and recent daily notes into a prioritized daily plan orchestrated by Claude Code with Obsidian as the data source (as of 2026-04, youtube.com[2]).

- A proposed automation pattern in the same system is a command that scans recent daily notes, identifies promising ideas, and prompts the user to create standalone notes or integrate them into existing files, reducing idea loss (as of 2026-04, youtube.com[2]).

- **Hermes‑based stacks** typically integrate external services such as Firecrawl (for scraping and browser control), Browserbase (for browser automation), and CameoFox (for more resilient browsing) as tools the agent can call (as of 2026-05, maxmitcham.substack.com[1]).

- Hermes‑style systems commonly connect to **Discord or Slack** so users can interact with agent workflows as if chatting with a bot, including standard Discord bot setup (application, bot token, intents, OAuth install) (as of 2026-05, maxmitcham.substack.com[1]).

- In the Hermes + Obsidian system, the Obsidian vault is explicitly treated as a **three‑layer memory system**: `raw/` for immutable source material, `wiki/` for agent‑compiled structured knowledge, and `output/` for generated deliverables like reports and slides (as of 2026-05, maxmitcham.substack.com[1]).

- That same guide proposes **crons** (scheduled automations) for “brain‑improving” tasks (updating memory, categorizing conversations, maintaining indexes, checking for stale pages) and “task‑executing” tasks (monitoring trends, drafting content, reviewing performance, updating docs) (as of 2026-05, maxmitcham.substack.com[1]).

- A recommended starter workflow in that guide is: install Hermes, connect model providers, connect a messaging platform, create the Obsidian vault using the raw/wiki/output schema, then set up one daily “brain digest” cron and one work‑oriented cron (e.g., trend scouting) (as of 2026-05, maxmitcham.substack.com[1]).

- **OpenClaw** is described as an open‑source framework that turns language models into autonomous agents that can run 24/7 across more than 20 messaging platforms, acting as an always‑on assistant (as of 2026-03, contextstudios.ai[8]).

- OpenClaw provides a **Gateway**‑like message routing layer that receives inputs from many platforms and forwards them to agents, analogous to how Anthropic’s later Channels feature routes messages from Telegram, Discord, and iMessage into Claude Code sessions (as of 2026-03, ronforbes.com[3]).

- Tutorials for OpenClaw describe using **Claude Code’s development workflow** to build and test “Skills” (tool‑augmented capabilities) for OpenClaw agents, showing Claude Code as the default dev environment rather than just a consumer‑facing tool (as of 2026-03, claude-world.com[5]).

- A production deployment described by Context Studios uses OpenClaw as a **backend orchestrator** for client‑facing assistants, with persistent state, tool calls, and monitoring, suggesting that agent frameworks are leaving “toy” status and entering production (as of 2026-03, contextstudios.ai[8]).

- At least one user reports running **OpenClaw instances connected to Obsidian and Claude Code** as part of a “command center”–style personal system visible in social media demos (as of 2026-04, instagram.com[4]).

- Another user (Sajal Sharma) reports spending a week with OpenClaw as a personal assistant, having already used Claude Code for a couple of months, suggesting staggered adoption where Claude Code is the entry point and OpenClaw adds persistence and always‑on capabilities later (as of 2026-04, sajalsharma.com[7]).

- Sajal describes an **Obsidian‑resident Claude Code instance** that acts as a persistent assistant tied to the vault, hinting at a pattern where Obsidian becomes the data and context layer while Claude Code performs active reasoning and editing (as of 2026-04, sajalsharma.com[7]).

- Ron Forbes characterizes Claude Code as his go‑to for **“heavy iteration and rapid development workflows”** because of its speed, while using a separate agent (Cowork/Dispatch) for more conversational tasks, indicating role specialization even within Anthropic’s tooling (as of 2026-03, ronforbes.com[3]).

- In early 2026, Anthropic launched **Agent Teams** enabling multiple Claude sessions to coordinate, divide work, and message each other, effectively providing a built‑in multi‑agent system rather than requiring external orchestrators for that pattern (as of 2026-03, ronforbes.com[3]).

- Anthropic also released **Scheduled Tasks** and a `/loop` command that let Claude run periodic tasks (like checking email, processing meeting notes, or flagging calendar conflicts) without user prompts, mirroring cron‑style patterns from Hermes/OpenClaw setups (as of 2026-03, ronforbes.com[3]).

- Anthropic’s **Dispatch** feature offers a persistent conversation accessible from mobile devices that can control files and apps on the user’s desktop, which Ron Forbes likens to OpenClaw’s always‑available messaging layer (as of 2026-03, ronforbes.com[3]).

- The **Channels** feature allows Claude Code sessions to receive messages from Telegram, Discord, and iMessage, effectively turning Claude Code into an action endpoint for multiple communication platforms (as of 2026-03, ronforbes.com[3]).

- **Computer Use** (Anthropic) allows Claude to see the user’s screen, click, type, and operate desktop applications in both Cowork and Claude Code, and is shipping to Pro and Max users rather than just being a demo, which dramatically increases the scope of automatable workflows (as of 2026-03, ronforbes.com[3]).

- Ron Forbes recommends new users start with a **Claude Pro subscription**, install the **Google Workspace CLI plugin**, and connect at least one MCP server (such as Gmail or Google Calendar) to give Claude access to real work artifacts (as of 2026-03, ronforbes.com[3]).

- A Facebook group discussion on “setting up Claude Code and Obsidian for agent workspace” describes using **Claude Code as a “general agent co‑founder”** and seeking guidance on structuring both codebases and Obsidian to support that role (as of 2026-04, facebook.com[6]).

---

## Timeline
- **2026-02** – Anthropic rolls out **Agent Teams**, enabling multiple Claude sessions to coordinate and message each other, a key primitive for multi‑agent workflows that previously required frameworks like OpenClaw or Hermes (as of 2026-03, ronforbes.com[3]).

- **2026-02** – **Scheduled Tasks** launch, allowing users to schedule recurring Claude actions, followed by `/loop` in early March to run ongoing agent “heartbeats” without manual prompting (as of 2026-03, ronforbes.com[3]).

- **2026-03-17** – **Dispatch** is introduced as a persistent Claude conversation accessible from phones and tablets that can operate on desktop files and applications, approximating OpenClaw’s messaging layer for always‑on assistants (as of 2026-03, ronforbes.com[3]).

- **2026-03-20 to 2026-03-26** – **Channels** expand Claude Code’s input routing to Telegram, Discord, and by March 26, iMessage, making Claude Code reachable from mainstream chat platforms (as of 2026-03, ronforbes.com[3]).

- **2026-03-24** – Anthropic ships **Computer Use** as a production feature for Pro/Max that lets Claude see screens and control desktop apps, enabling automated GUI workflows that previously required custom RPA tooling (as of 2026-03, ronforbes.com[3]).

- **2026-03** – Context Studios publishes a **complete OpenClaw guide** on operating AI agents in production, showing concrete patterns for 24/7 assistants and extended tool usage (as of 2026-03, contextstudios.ai[8]).

- **2026-03** – A tutorial on **OpenClaw Skills** demonstrates using Claude Code’s development workflow to rapidly prototype and test new agent capabilities within OpenClaw (as of 2026-03, claude-world.com[5]).

- **2026-04** – Vin releases a video walkthrough of his **Obsidian + Claude Code** system for life and work management, popularizing the pattern of treating Obsidian as structured context for Claude and using custom slash commands (as of 2026-04, youtube.com[2]).

- **2026-04** – Sajal Sharma publishes “A Week with OpenClaw as My Personal Assistant,” documenting the shift from ad‑hoc Claude Code usage to a persistent OpenClaw‑mediated assistant tied to an Obsidian vault (as of 2026-04, sajalsharma.com[7]).

- **2026-04** – Social media demos show OpenClaw running across multiple machines and messaging apps with an **Obsidian Command Center powered by Claude Code**, highlighting real‑world multi‑tool setups (as of 2026-04, instagram.com[4]).

- **2026-05** – Max Mitcham publishes “How to Build an AI Agent Operating System That Compounds Over Time,” specifying a concrete stack of Hermes + Claude Code + OpenClaw + Obsidian + crons, and offering a detailed Obsidian schema and starter workflows (as of 2026-05, maxmitcham.substack.com[1]).

---

## Key Players
- **Anthropic / Claude team** – Provider of **Claude Code, Agent Teams, Scheduled Tasks, Dispatch, Channels, and Computer Use**, which collectively enable local code execution, multi‑agent setups, cross‑platform messaging, and GUI automation used by developers and power users (as of 2026-03, ronforbes.com[3]).

- **OpenClaw maintainers / community** – Builders of the **open‑source OpenClaw framework** that turns LLMs into autonomous agents running 24/7 across 20+ messaging platforms, often wired into Claude Code for execution and Obsidian or other stores for memory (as of 2026-03, contextstudios.ai[8]; as of 2026-03, claude-world.com[5]).

- **Max Mitcham** – Author of a widely circulated Substack guide framing Hermes + OpenClaw + Claude Code + Obsidian as an **AI agent operating system**, including concrete folder structures, automation patterns, and deployment advice that many power users reference (as of 2026-05, maxmitcham.substack.com[1]).

- **Vin (creator of Obsidian + Claude Code workflow)** – Power user showcasing a deep integration of **Obsidian CLI with Claude Code**, plus custom slash commands like `/today`, `/trace`, and `/connect`, influencing how others design vault‑centric agent workflows (as of 2026-04, youtube.com[2]).

- **Ron Forbes** – Commentator and practitioner who documented the week **proactive AI assistants went mainstream**, drawing parallels between OpenClaw‑style agents and Anthropic’s new features, and recommending practical MCP setups (as of 2026-03, ronforbes.com[3]).

- **Context Studios** – Organization running **OpenClaw agents in production**, publishing a “complete OpenClaw guide” that details how to operate agents as robust backend services and how to integrate them into business workflows (as of 2026-03, contextstudios.ai[8]).

- **Sajal Sharma** – Developer documenting his experience with **OpenClaw and Claude Code as personal assistants** layered over an Obsidian vault, providing a ground‑level view of what individuals actually adopt and adjust over a week (as of 2026-04, sajalsharma.com[7]).

- **Hermes developer(s)** – Creators of **Hermes**, a control‑layer tool for orchestrating agents and tool usage; their guidance around using Hermes as the main controller with OpenClaw, Claude Code, and Obsidian forms a pattern many technically inclined users are trialing (as of 2026-05, maxmitcham.substack.com[1]).

---

## Contrarian Views
- **Skepticism about heavy tool stacks** – Max Mitcham explicitly warns against adding every integration to Hermes or OpenClaw “just because you can,” arguing that complexity and fragility outweigh benefits until a workflow demonstrably needs those tools (as articulated by Max; as of 2026-05, maxmitcham.substack.com[1]).

- **Caution on OpenClaw overuse** – The same guide argues users **do not need OpenClaw** for daily orchestration and should limit it to heavy tool‑calling scenarios, countering a trend of enthusiasts running everything through OpenClaw for novelty (as articulated by Max; as of 2026-05, maxmitcham.substack.com[1]).

- **Concern about agent autonomy vs reliability** – Production discussions (e.g., Context Studios) emphasize monitoring, guardrails, and constrained tool access, implicitly challenging the notion of truly autonomous agents and suggesting that human‑in‑the‑loop review remains critical (as articulated by Context Studios; as of 2026-03, contextstudios.ai[8]).

- **“All‑in‑Obsidian” vs specialized tools** – Vin’s system uses Obsidian as the central memory plane for nearly everything (plans, specs, technical guides), which may conflict with views that structured data belongs in purpose‑built tools (task managers, CRMs, issue trackers); while explicit critiques are not quoted, this tension is visible in community debates referenced in platform discussions (inferred from contrast between Obsidian‑centric systems and tool‑specific MCP integrations; as of 2026-04, youtube.com[2]; as of 2026-03, ronforbes.com[3]).

- **Questioning mainstream readiness** – Ron Forbes portrays 2026 as “the week the proactive AI assistant went mainstream” but also notes that features like Scheduled Tasks and Channels are new, implying that stability, UX, and organization‑wide adoption are still maturing, contrary to hype suggesting fully solved AI agents (as articulated by Ron; as of 2026-03, ronforbes.com[3]).

---

## Recommended Further Reading
- **“How to Build an AI Agent Operating System That Compounds Over Time” (Max Mitcham)** – Detailed walkthrough of a Hermes + OpenClaw + Claude Code + Obsidian stack, including file schemas, cron patterns, and practical hosting issues, useful as a blueprint for similar setups (as of 2026-05, maxmitcham.substack.com[1]).

- **“How I Use Obsidian + Claude Code to Run My Life” (Vin’s video)** – Concrete demonstration of custom commands, Obsidian CLI integration, and daily rituals that turn Claude Code into a persistent thinking partner tied to a real vault (as of 2026-04, youtube.com[2]).

- **“The Week the Proactive AI Assistant Went Mainstream” (Ron Forbes)** – Analysis of Anthropic’s Agent Teams, Scheduled Tasks, Dispatch, Channels, and Computer Use, and how they compare to OpenClaw‑style frameworks, helpful for understanding platform convergence (as of 2026-03, ronforbes.com[3]).

- **“The Complete OpenClaw Guide: How We Run an AI Agent in Production” (Context Studios)** – Deep dive into productionizing OpenClaw agents, including architecture, monitoring, and common pitfalls, valuable for anyone considering always‑on agents in a business context (as of 2026-03, contextstudios.ai[8]).

- **“A Week with OpenClaw as My Personal Assistant” (Sajal Sharma)** – Narrative of a real user iterating on OpenClaw and Claude Code workflows over a week, highlighting what sticks, what breaks, and how these tools feel in everyday use (as of 2026-04, sajalsharma.com[7]).

- **OpenClaw Skills tutorial on Claude‑world** – Step‑by‑step guide showing how to use Claude Code to develop Skills for OpenClaw, offering a practical bridge between code‑centric work and agent orchestration (as of 2026-03, claude-world.com[5]).

---

## Open Questions
- **Real adoption vs enthusiast setups** – Outside of blog posts and niche communities, it is unclear how many teams or individuals are running complex combinations of Claude Code, OpenClaw, and Obsidian in daily production; systematic adoption data or surveys are not yet available in public sources (as of 2026-05, maxmitcham.substack.com[1]; as of 2026-04, sajalsharma.com[7]).

- **Security and compliance practices** – Public guides rarely detail threat models, secret management, or compliance controls for always‑on agents with access to email, calendars, and files;

## Sources

- https://maxmitcham.substack.com/p/how-to-build-an-ai-agent-operating
- https://www.youtube.com/watch?v=6MBq1paspVU
- https://www.ronforbes.com/blog/the-week-the-proactive-ai-assistant-went-mainstream
- https://www.instagram.com/reel/DX6hPQsOQal/
- https://claude-world.com/articles/openclaw-introduction/
- https://www.facebook.com/groups/techtitansgroup/posts/1537028760957770/
- https://sajalsharma.com/posts/openclaw-experiments/
- https://www.contextstudios.ai/blog/the-complete-openclaw-guide-how-we-run-an-ai-agent-in-production-2026

## Relevance to my setup (read this first)

This is the first manual run of the system designed in [[Tooling Intelligence Scan — Design]] — proof the concept surfaces real, adoptable patterns. Directly relevant findings:

- **The cron-digest pattern is the mainstream play.** Power users converge on scheduled "brain digest" + "task" crons over an Obsidian vault — exactly the [[Tooling Intelligence Scan — Design|tooling scan]] and the existing `brief.py` rail. Validates the direction.
- **Three-layer vault memory** (`raw/` → `wiki/` → `output/`) is a documented pattern (Max Mitcham) worth comparing against this vault's `brain/` + `reference/` + `thinking/` split.
- **Vin's custom Claude Code commands** (`/today`, `/connect`, `/challenge`) over an Obsidian vault mirror this vault's `/om-*` and `/obsidian-*` skills — a source of command ideas. See [[Skills]].
- **Anthropic's own Scheduled Tasks / `/loop` / Channels / Computer Use** now cover much of what OpenClaw/Hermes stacks were bolted on for — relevant to [[Claude Subscription Billing|what's worth building vs waiting for native]].
- **Consistent contrarian note:** don't add OpenClaw/heavy tool stacks until a workflow demonstrably needs them — matches [[North Star|Edge Before Action]] and the decision to drop the autonomous experiment layer on Pro.

## Related

- [[Tech Watch]] — this dossier is the AI-tooling slice of the tech-intelligence framework
- [[Tooling Intelligence Scan — Design]] — the system this run prototypes
- [[Claude Subscription Billing]] — native Anthropic scheduling features vs build-it-yourself, under the Pro credit ceiling
- [[api-decision-framework]] — Tier-2 "research once, reuse forever" strategic awareness run
- [[Skills]] — vault command patterns to compare against Vin's `/today` / `/connect` setup
