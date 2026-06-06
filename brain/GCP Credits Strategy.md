---
date: 2026-06-06
description: "How to use the $300 GCP trial credits toward the income goal without building a cost cliff — two-assets model, self-sustaining rule, and the chosen direction."
tags:
  - brain
  - strategy
---

# GCP Credits Strategy

The $300 Google Cloud trial credits expire **2026-09-04**. The framing that matters:

## The two-assets model

You don't have one asset, you have two:

1. **Trial credits ($300, expire 2026-09-04)** — for **one-time heavy bursts**: backtest sweeps, model training, bulk data/asset generation. Run hard, produce an artifact, shut down. No tail.
2. **GCP "Always Free" tier (never expires)** — a small always-on VM, Cloud Run (2M req/mo), Cloud Functions (2M/mo), Cloud Scheduler, BigQuery (1TB/mo), 5GB storage, Firestore. All ₹0 forever *if you stay under the limits*. `[VERIFIED — confirm exact limits in console]`

## The self-sustaining rule

> [!important] Design rule for anything built on GCP
> **Persistent / always-on → Always Free tier. Expensive-but-occasional → trial credits. Nothing that survives the cliff is allowed to cost money.**

To keep Always-Free services alive after the trial ends you **upgrade to a paid account** (required, or services pause) but stay under the free limits → bill stays ₹0. Backstop with a **budget alert + cap** so an overrun can't surprise-bill you. This supersedes the earlier "[[Key Decisions|Cloud Run with --min-instances 1, ~$3-5/mo]]" plan — prefer **webhook / scale-to-zero** so the trading bot is ₹0 *and* survives the cliff.

## Chosen direction — unblock the stuck streams

Use the credits for one-time **edge-discovery bursts** that break current blockers across [[Streams]], not just trading:

1. **[[Edge Generalization Sweep]]** (Trading, designed) — does the breakout edge generalize, and which instruments to go live on. A genuine compute job that fits the credits.
2. **Content Niche Discovery Engine** (Content, not started) — break the "no niche defined" blocker with data-driven niche ranking. Flag: more API+analysis than heavy compute, so GCP's role here is hosting/storage, not crunching.

## Guardrails

- GCP **budget alert** ($50, email at 50/90/100%).
- Spot VMs + **shutdown-script auto-delete** — never leave a VM running overnight.
- Billing audit reminder logged for **2026-08-28** (see [[Streams#System Reminders]]).

## Related

- [[Streams]] — the four income streams these credits serve
- [[Edge Generalization Sweep]] — sub-project 1
- [[North Star]] — every credit spent should translate to the ₹7-8L goal
- [[Key Decisions]] — supersedes the older Cloud Run min-instances plan
