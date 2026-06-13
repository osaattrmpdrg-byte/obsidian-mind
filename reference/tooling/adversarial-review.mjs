#!/usr/bin/env node
// Second-model adversarial review gate for /plan.
// Usage: node adversarial-review.mjs <plan-file> [model]
//   model defaults to gemini-2.5-flash (free, tested sufficient).
//   override with arg or ADV_REVIEW_MODEL env var; gemini-2.5-pro is the
//   quality pick once a paid Gemini tier exists (free-tier pro is quota-starved).
// Sends the plan to Gemini for ONE adversarial pass. Single pass by design —
// no greenlight loop. The chosen model is NEVER silently swapped: if it fails,
// the script exits with the error so the gate visibly did not run.

import { readFileSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const planPath = process.argv[2];
if (!planPath || !existsSync(planPath)) {
  console.error('Usage: node adversarial-review.mjs <plan-file> [model]');
  process.exit(2);
}

const model = process.argv[3] || process.env.ADV_REVIEW_MODEL || 'gemini-2.5-flash';

function loadKey() {
  if (process.env.GEMINI_API_KEY) return process.env.GEMINI_API_KEY;
  const envFiles = [
    'd:/projects/obsidian-second-brain/.env',
    join(homedir(), '.config', 'obsidian-second-brain', '.env'),
  ];
  for (const f of envFiles) {
    if (!existsSync(f)) continue;
    const m = readFileSync(f, 'utf8').match(/^GEMINI_API_KEY=(.+)$/m);
    if (m) return m[1].trim().replace(/^["']|["']$/g, '');
  }
  return null;
}

const key = loadKey();
if (!key) {
  console.error('GEMINI_API_KEY not found in env or obsidian-second-brain .env files');
  process.exit(2);
}

const plan = readFileSync(planPath, 'utf8');

const prompt = `You are an adversarial plan reviewer with no stake in this plan being approved. The plan below was written by a different AI model; assume it has blind spots about its own work. The plan involves code that handles real money (trading execution, position sizing, or live capital).

Attack the plan. Hunt specifically for:
1. Production failure modes: partial fills, API timeouts mid-order, duplicate submission on retry, rate-limit lockouts, stale data, network partitions at the worst moment
2. Money-loss paths: sizing math errors, missing balance checks, no kill switch, fee/precision/rounding mistakes, unit or currency confusion
3. Backtest integrity: lookahead bias, survivorship bias, data the live system will not actually have at decision time
4. Unstated assumptions that, if false, break the plan
5. Verification gaps: which step could ship broken without the plan's listed checks catching it

Do NOT comment on style, naming, or nice-to-haves. Only report findings that would change what gets built.

Output format:
VERDICT: BLOCK | PROCEED-WITH-FIXES | CLEAR
FINDINGS: numbered list, each with severity (CRITICAL/MAJOR/MINOR), the specific plan step affected, and the concrete failure scenario.
If you find nothing real, output "VERDICT: CLEAR" and stop. Do not invent findings to appear useful.

=== PLAN UNDER REVIEW ===
${plan}`;

async function call(m) {
  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent?key=${key}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
    },
  );
  if (!res.ok) throw new Error(`${m}: HTTP ${res.status} ${(await res.text()).slice(0, 300)}`);
  const data = await res.json();
  const text = data.candidates?.[0]?.content?.parts?.map((p) => p.text).join('') ?? '';
  if (!text) throw new Error(`${m}: empty response`);
  return text;
}

let review;
try {
  review = await call(model);
} catch (e) {
  // No silent fallback. Report which model failed and signal failure so the
  // gate visibly did not run — a missing review must never look like a clean
  // one. Set exitCode (not process.exit) so pending handles drain cleanly.
  console.error(`Adversarial review did NOT run — ${e.message}`);
  console.error(`To use a different model: node adversarial-review.mjs <plan-file> <model>`);
  process.exitCode = 1;
}
if (review) {
  console.log(`REVIEWED BY: ${model}\n`);
  console.log(review);
}
