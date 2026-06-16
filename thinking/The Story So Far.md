---
date: 2026-06-06
description: "Plain-language record of the whole journey so far — for Dileep to read in one shot and track progress. Not a Claude working note."
tags:
  - thinking
  - journal
---

# The Story So Far

*A plain-English record of everything built across these sessions — for you to read top to bottom and know exactly where things stand. Last updated 2026-06-14.*

---

## The point of all this

**Goal: ₹7-8 lakh/month of passive income by age 27.** You're 22 now — a five-year window. Today's starting point: a ₹27k/month intern salary at Stackbox, of which ₹5-6k is investable.

The plan is four income streams that feed each other:

1. **Job (Stackbox)** — the engine. Funds everything else. Converting from intern to full-time around end of June 2026.
2. **Trading (systematic swing)** — the stream you've actually been building. A rule-based system that trades a proven edge.
3. **Content (faceless)** — idea stage. No face, no voice. Niche not yet chosen.
4. **AgriTech** — idea stage. Family land. Waiting for the other streams to mature.

The honest truth that shapes everything: at ₹5-6k, **trading returns alone (~11%/year) won't get you there.** The real multiplier is the salary growing and feeding capital in. So the early game is about *proving the system works* cheaply and safely — not about making money yet.

---

## How we got here, session by session

### May 19 — Laying the foundation
Built the skeleton of the trading system. Set up the Telegram bot (`@DileepLifeOSBot`) so the system can message you. Created a private GitHub repo to hold everything. Built the **core scanner** — the piece that watches the market and detects the trade signal (a "20-bar breakout"). Set up morning and evening briefing routines.

### May 21 — Making it actually run in the cloud
The scheduled routines couldn't reach Telegram (a platform block), so everything moved to **GitHub Actions** — free, always-on, runs on a schedule. The daily briefs got a free AI brain (Groq). Added the **gold (MCX) execution path** for India. Looked at prediction markets (Polymarket/Kalshi) and **rejected them** — geo-blocked in India and not passive. Kept the useful bits: position-sizing math (Kelly) and a way to track how accurate the system's predictions are (Brier score).

### May 22 — Safety and the paper-trade monitor
Found a security hole (a GitHub token sitting in plain text) and **fixed it** — secrets now live only in protected files. Submitted the Zerodha gold-segment activation. Built the **paper-trade monitor**: when a signal fires, it records a pretend trade and tracks it day by day until it hits its target or stop — logging the result. This is how you test the system without risking money.

### May 23 — Crypto, cleanup, and discipline
Cleaned up the laptop (removed 11 startup programs, uninstalled AnyDesk for security, restructured drives). Built and ran the **crypto backtest** — and Bitcoin passed the bar with a strong edge. **Rejected Fibonacci trading** (can't be tested objectively). Critically: realised EUR/USD and USD/CAD were in the scanner but **couldn't be legally traded from India**, so disabled them. This was the right call at the time — but see June 5, because part of it turned out to be a misunderstanding.

### June 5 — The big clarity session
This was the turning point. Several things happened:

- **Merged two separate note-vaults into one brain** so everything Claude knows lives in one place.
- A **grill-me session** forced the real goal into the open — the ₹7-8L target and the four-stream strategy. Before this, the system existed but the *why* wasn't written down.
- Ran a full batch of **trading research** (seven deep questions). Outcomes: chose the broker, set the position-sizing rules, and **rejected a pile of currency pairs** (more on that below).
- **Reopened EUR/USD.** The "it's illegal in India" belief was half-wrong — trading EUR/USD through an *offshore app* is illegal, but trading it as a *futures contract on India's own NSE exchange* is perfectly legal. That distinction brought back your single best-tested signal.
- Designed **"Daily Watch, Weekly Hunt"** — a disciplined way to look for new strategies without falling into the trap of testing hundreds of random ideas and fooling yourself with luck.
- Set up **automatic session logging** so progress gets captured without you asking.

### June 6 — Going live (the broker) and the plan
- **Angel One is live.** Account created, API key generated, security (TOTP) enabled, and confirmed that both the gold and currency trading segments are active. The system can now technically place real orders.
- **Approved the plan of action** (below): paper-test first, then go live small.
- Built the **CoinDCX execution layer** (for Bitcoin) — the code that places crypto orders, written carefully with tests. Waiting on you to generate the API key.
- Set the **GCP cloud-credits strategy** — how to use $300 of free Google Cloud credits for one-time heavy computation without creating a future bill.
- Designed the **Edge Generalization Sweep** — a one-time big computation to answer "is this trading edge actually real and universal, or did we just get lucky with crypto?"
- Wrote the detailed build plan for making paper-trading actually work.

---

### June 12 — Both rails verified + the anti-self-deception machine
- **Angel One re-verified live** (existing key works — no new key needed). **CoinDCX smoke test passed** and the account is funded; added limit-order support so you can run a zero-risk order→cancel test. Still pending *you*: place the unfillable test order, confirm it in the app, cancel it.
- Built the **Lockbox + trial-count registry** — the part that stops the system fooling itself. It holds out a slice of history the strategy generator never sees, lets each candidate touch it once, and raises the pass bar as you test more ideas. This is the discipline most "AI trading" content skips entirely.
- **EUR/USD re-enabled in the live scanner** (and fixed a real bug that was mangling FX prices in the alerts).

### June 13-14 — Turning the lens on the tools (and a possible new stream)
This stretch wasn't about trading — it was about the *tooling and the streams themselves*.
- **Researched how people actually use Claude / OpenClaw / Obsidian / AI agents.** The standout finding: your vault already *out-tools* the creators teaching this — some of whom sell a "Content OS" setup for $197 that is *less* than what you already have.
- That became a **content-niche hypothesis** (finally un-blocking Stream 3): build-in-public as *"I built the AI second-brain these creators teach — then pointed it at a live trading account with the risk discipline the hype skips."* Engineering, not trading-advice. First post drafted (the Lockbox story). Pending your OK on the "not trading-advice" framing.
- Found a **billing reality**: from June 15, Claude splits into two pools — your interactive sessions (plenty, but unusable by overnight agents) and a separate ~$20/month autonomous budget on Pro. That killed the "overnight agent army" idea as unaffordable on Pro and pushed everything onto cheap/free rails.
- Settled the **multiple-agents question** you raised: yes, more agents help — especially for *catching your own blind spots in decisions* (an adversarial panel), run live (≈free), not as an always-on swarm. A "decision gate" is queued to build.
- Wrote a standing **"Working With Me"** note so any future session starts already knowing how you think — and wired the vault to read it every session.
- Cleared tooling friction: installed `defuddle`, fixed the research + YouTube scripts, started a permission allowlist.

### June 15 — The trajectory fork: considering the armed forces
The "something that could change your trajectory" — you shared it: **you're considering a life in the armed forces.** You'd already done a deep grilling session (14 Jun) and built a real [[Defence Career Strategy]] (now in the vault). The honest reconciliation against everything else here:
- It's a **[[Vision]]-level decision**, not a career tweak — the ₹7-8L goal was always the *means* to the life in Vision; defence maxes one half of that life (meaning, discipline, service, nature) and sacrifices the other (autonomy, building your own thing, rootedness). That trade is the real question, and it's yours.
- **Your financial work isn't wasted** — SSC has no pension, so the trading system + investing discipline become the *backbone* the path needs; and the *automated* trading system is the one income stream that survives a service life.
- **The deepest untested assumption:** "why defence = tactical impact on people's lives" — asserted, not grilled, when the day-to-day is ~90% admin. Next session we run a panel on exactly that, and you get the eye exam done (the first gate).

Status: **considering, not decided.** Nothing in the income plan was torn up — just flagged.

---

## The trading system, in plain words

**The edge (the one rule that makes money):** Buy when the price breaks above its highest point of the last 20 days, *but only* when the market is already in a clear uptrend (a fast average above a slow average). Set a stop-loss at 1.5× the recent volatility. Ride the trend; exit when it turns.

That's it. One rule, tested hard, that holds up. Everything else is plumbing.

**Where it's proven to work:**
- **Gold (XAU)** — solid edge, long-only.
- **Bitcoin** — strong edge (currently waiting for the market to flip into an uptrend before it can trade).
- **EUR/USD** — your best-tested signal, now legally tradeable via NSE.

**How trades get executed:**
- **Gold & EUR/USD** → Angel One (India-legal, free API).
- **Bitcoin** → CoinDCX.

**How much you risk:** 1-2% of capital per trade at current size. (The fancier "quarter-Kelly" sizing only makes sense once you have more than ~₹30k.)

**The cost reality:** EUR/USD costs only ~₹2,700 per lot — your cheapest and most accessible instrument. Gold needs ~₹70,000 per lot, so gold stays paper-only until your capital grows.

---

## What we tried and threw away (and why it matters)

This list is the real value — it's everything you *won't* waste time re-trying:

- **Offshore forex apps** (OANDA, etc.) — illegal in India. The lesson: it's not "is forex legal?" but "*where* are you trading it?" Indian exchange = fine, offshore app = violation.
- **Japanese yen pairs (EUR/JPY, GBP/JPY, USD/JPY)** — Japan's central bank intervenes violently and unpredictably, which destroys trend-following.
- **NZD/USD and AUD/USD** — no clean, repeatable edge.
- **GBP/USD** — Brexit and the 2022 crash broke its reliability.
- **Fibonacci levels** — can't be tested objectively, so they're out (the whole system is "only trade what you can prove").
- **RSI-recovery and fixed take-profits** — tested, didn't work.
- **Prediction markets** — geo-blocked and not passive.
- **A "daily strategy generator"** — sounds clever, but mass-testing random ideas guarantees you'll find lucky garbage that dies with real money. Replaced with the disciplined Weekly Hunt.
- **Zerodha as broker** — costs ₹2,000/month for the API. Switched to **Angel One**, which is free.

---

## Where you stand right now (2026-06-15)

- **⚡ Big open question:** whether to pursue an **armed-forces career** ([[Defence Career Strategy]]) — a Vision-level fork. Considering, not decided. Next: eye exam + a [[panel]] on the core motive.
- **Trading:** both rails verified live; one manual CoinDCX test order still pending you. System unchanged and disciplined (Lockbox now guards new-strategy discovery).
- **Content (Stream 3):** niche finally defined — pending your OK on the "not trading-advice" framing — with the first post drafted.
- **Tooling:** faster and safer (defuddle installed, scripts fixed, permission allowlist, a standing "how to work with me" contract the vault reads every session).
- **Open:** the possible trajectory change you're weighing (not yet shared), and the small CoinDCX test order.

### The approved plan of action

1. **Build** — make the paper-trade logging work (plan already written).
2. **Paper** — let the system run; collect **5-6 paper trades** on gold/EUR-USD. This proves the *plumbing* works (not the edge — the edge is already proven; 5-6 is enough because waiting for 20 would take a year at this trade frequency).
3. **Calibrate** — check that the live results match the backtest.
4. **Go live small** — real money, 1 lot, EUR/USD first (cheapest).

---

## Things only you can do (open reminders)

- **Aug 28** — GCP billing audit before the **Sept 4** free-credit cliff (make sure nothing flips to paid).
- Generate the **CoinDCX API key** when ready to wire up Bitcoin execution.
- Open/confirm the **IDFC First Bank** account for isolated trading capital.

---

## Bigger bets, designed but not built

- **Edge Generalization Sweep** — a one-time cloud computation (funded by free GCP credits) to test whether the breakout edge holds across *every* asset class, not just the ones you stumbled onto. Tells you definitively which instruments to trust. Designed, paused at the build step.
- **Content & AgriTech streams** — still idea-stage. The plan is to use the same cloud credits to help pick a content niche with data, when you're ready to turn to it.

---

*This is a personal tracking note. For the live, linked version Claude maintains, see [[Trading System]] and [[Streams]].*
