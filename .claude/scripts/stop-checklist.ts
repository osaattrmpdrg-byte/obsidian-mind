#!/usr/bin/env node
/**
 * Stop hook — remind the user of session-wrap-up tasks and kick a
 * debounced QMD refresh so the next session opens against a current
 * index.
 *
 * Silently exits when the hook is being re-entered by a secondary
 * agent (stop_hook_active=true) to avoid recursive reminder output and
 * duplicated refresh spawns. Otherwise prints the vault-hygiene
 * checklist and routes through the same `triggerDebouncedRefresh`
 * entry the PostToolUse hook uses — one debounce contract, one spawn
 * shape, zero drift between the two paths.
 */

import { dirname, join, resolve as resolvePath } from "node:path";
import { fileURLToPath } from "node:url";
import { readStdinJson } from "./lib/hook-io.ts";
import { triggerDebouncedRefresh } from "./lib/qmd-refresh.ts";

const DEBOUNCE_MS = 30_000;
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
// See qmd-refresh.ts for the rationale behind the env override — it
// keeps parallel test workers from racing on the shared repo sentinel.
const SENTINEL_PATH =
	process.env["QMD_REFRESH_SENTINEL"] ??
	join(SCRIPT_DIR, ".qmd-refresh-sentinel");
const WORKER_PATH = resolvePath(SCRIPT_DIR, "qmd-refresh-run.ts");

type HookInput = {
	readonly stop_hook_active?: unknown;
};

const input = await readStdinJson<HookInput>();
if (input?.stop_hook_active === true) process.exit(0);

const today = new Date().toISOString().slice(0, 10);
const logPath = `thinking/session-logs/${today}-session.md`;

const mandate = [
	`MANDATORY — CAPTURE THIS SESSION BEFORE ENDING:`,
	`Run the /log-session routine (it defines the full structure): write or append`,
	`${logPath}, update brain/Memories.md Recent Context, and route any durable`,
	`knowledge to the right brain note. Do NOT auto-push git — that's the user's call.`,
	`For a full vault review instead, run /om-wrap-up.`,
].join("\n");

process.stdout.write(mandate + "\n");

triggerDebouncedRefresh({
	sentinelPath: SENTINEL_PATH,
	workerPath: WORKER_PATH,
	debounceMs: DEBOUNCE_MS,
	logPrefix: "stop-checklist",
});
