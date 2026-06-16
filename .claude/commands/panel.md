---
description: Run an adversarial multi-agent decision panel — spawn diverse-lens skeptics that independently pressure-test a decision/plan/claim, surface every loophole, and return a survive/revise/kill verdict. The decision-layer extension of the lockbox discipline.
category: decision
triggers_en: ["run a panel", "run a decision panel", "panel this", "grill this with a panel", "decision gate"]
---

Execute `/panel <decision, plan, or claim>`:

A decision gate: independent agents catch the loopholes a single pass misses. Runs **interactively** (parallel subagents — draws the abundant pool, ≈free per [[Claude Subscription Billing]]). For a large/complex decision, may use the Workflow tool instead (standing tool-authority per [[Working With Me#Efficiency mandate standing — Dileep 2026-06-15|the efficiency mandate]]).

1. **Restate the decision in one sentence.** If it's vague, sharpen it first — a panel on a fuzzy question returns fuzzy verdicts. State the implicit claim being tested.

2. **Pick the optimum number of lenses** (typically 3–5; scale to stakes). Each lens is a **separate subagent**, told to argue its angle *hard* and independently — not to hedge or converge. Default lenses:
   - **Correctness / feasibility** — is the reasoning sound? does it actually work? what's assumed-but-unverified?
   - **Risk / downside (asymmetric)** — map the *worst realistic* outcome and whether it's survivable ([[North Star|Asymmetric Thinking]]). What would make this fail catastrophically?
   - **Refute-it (steelman the case AGAINST)** — argue the strongest case to NOT do this. Default to "reject" unless the case is overwhelming.
   - **Edge** — can the edge be stated in one sentence? If not, it isn't found ([[North Star|Edge Before Action]]).
   - *(add as fits)* **Cost / reversibility**, **second-order effects**, **a domain lens** (e.g. for money decisions: a trading-risk lens).

3. **Independence is the make-or-break.** Lenses must be genuinely different and argued separately — N agents reasoning alike just echo and manufacture false confidence. Give each its own framing; do not let them see each other's conclusions before judging.

4. **Each agent returns:** verdict (`proceed` / `revise` / `kill`) · the single strongest loophole it found · confidence · the one change that would most improve the decision.

5. **Synthesize:**
   - **Proceed** only if it survives — majority `proceed` AND no unaddressed fatal risk from the risk/refute lenses.
   - Surface **every** loophole found, ranked by severity — not just the verdict.
   - On `revise`/`kill`: state exactly **what would have to change** to flip it to proceed.
   - Output a tight verdict block:
     ```
     PANEL · <one-line decision>
     Lenses: <n>  →  proceed <x> / revise <y> / kill <z>
     VERDICT: <proceed | revise | kill>
     Loopholes (severity order): ...
     To flip to proceed: ...
     ```

6. **Money-path decisions get extra rigor** — anything touching live capital, order execution, `D:\trading_system`, or `D:\crypto_trading`. The panel *complements*, never replaces, the [[Daily Watch Weekly Hunt|lockbox]] (catches fake edges) and the `/plan` adversarial gate (catches code errors). Three different nets for three different failure modes.

7. **Be honest about the panel's limits.** It catches reasoning loopholes and unconsidered risks; it does **not** catch overfit edges (that's the lockbox) or facts only live data can settle (flag those for `/research`).

**Note:** Built 2026-06-15 — the "decision gate" from the multi-agent reframe. It's `/grill-me` upgraded from one interrogator to a diverse independent panel. See [[Key Decisions#Session Workflow]], [[AI Tooling Workflow Patterns]].
