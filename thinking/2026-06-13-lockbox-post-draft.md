---
date: 2026-06-13
description: "DRAFT build-in-public content artifact (A5) — the anti-curve-fitting lockbox, framed as engineering not trading advice. For user review + publish; not posted by Claude."
tags:
  - thinking
  - content
  - draft
---

# DRAFT — "I gave my trading bot a way to lie to itself"

> [!warning] Draft for review — not published
> First artifact for the [[Content Niche]] test (Framing C: engineering, never signals). Review voice, confirm the [[Streams|"not trading-advice"]] constraint, then *you* publish. Success metric: any traction above baseline within ~2 weeks.

## Why this one
The [[Daily Watch Weekly Hunt|lockbox + trial-count registry]] is the strongest proof of the niche edge: it's the discipline AI-trading-hype content skips, it's already built and tested (18 tests green), and it's pure engineering — zero advisory/SEBI exposure. It demonstrates "I built the system AND the safeguards," which is the whole differentiator.

---

## Version 1 — X thread

**1/**
Everyone building an "AI trading bot" right now has the same hidden bug: the bot can fool itself into thinking it found an edge that isn't there.

I built the thing that stops mine. Here's the engineering. 🧵

**2/**
The trap: you generate 100 strategies, backtest each, keep the ones that pass.

Several will pass *by pure luck* — test enough random ideas and noise looks like signal. That "winner" then dies the moment it touches live money.

It's the multiple-comparisons problem, and it's everywhere.

**3/**
Testing *more* strategies doesn't find more edges. It finds more lucky noise.

So the goal isn't a bigger search. It's a search that can't lie to you. Four safeguards:

**4/ Safeguard 1 — the Lockbox**
A slice of price history the strategy generator *never* sees. A candidate gets exactly ONE shot at it, only after it's already passed everything else. Capped at a few shots per year.

You can't overfit to data you're not allowed to look at.

**5/ Safeguard 2 — trial-count penalty**
The system counts every candidate ever tested (N). As N grows, the bar to "pass" rises (Bonferroni / deflated-Sharpe intuition).

Test 200 ideas and the winner has to clear a much higher bar than your first one did. The counter is what stops a lucky fluke sneaking through.

**6/ Safeguard 3 — cross-instrument confirmation**
The same edge has to show up on 3+ independent markets (e.g. BTC, gold, EUR/USD).

Luck doesn't repeat across three unrelated markets. A real mechanism does.

**7/ Safeguard 4 — rationale first**
Before any backtest, I have to write the one-sentence economic reason the edge should exist. No rationale → rejected, no backtest run.

It forces "why would this work" *before* "did this work" — the order that matters.

**8/**
Here's the real lesson: the AI part is easy now. Claude will write the backtest in minutes.

The hard part — the part that actually protects capital — is the discipline that stops you believing your own noise. That's the engineering nobody posts about.

**9/**
Building this in public as I point a personal AI system at a real, small, disciplined trading account.

What's your anti-overfitting safeguard? Or are you (be honest) still keeping the strategies that "just worked"?

---

## Version 2 — long-form opener (blog / X article)

**The most dangerous line of code in an AI trading system is the one that decides a strategy "works."**

Large language models made strategy generation trivial. Ask, and you'll have a backtested momentum system in minutes. That's exactly the problem. When generating and testing 100 ideas costs nothing, you run straight into the oldest trap in quantitative finance: test enough random strategies and several will pass by luck alone. You keep the "winner." It dies live. You blame the market.

I didn't want a bigger strategy search. I wanted one that couldn't fool me. So before I let my system propose a single new strategy, I built four safeguards into the discovery pipeline itself — [continue with the four, engineering-framed, then the meta-point: the model is the easy part; the discipline is the moat].

---

## Voice notes (for the humanize pass)
- Direct, first-principles, slightly contrarian. No hype words ("game-changer", "insane", "🚀").
- Engineering register, not finance-guru. Never implies tradeable signals or returns.
- Short sentences. One idea per line. Concrete over abstract.
- Run through [[om-humanize]] before publishing if it still reads AI-ish.
