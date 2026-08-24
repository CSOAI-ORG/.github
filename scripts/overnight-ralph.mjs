#!/usr/bin/env node
/**
 * overnight-ralph.mjs — Ralph-mode overnight batch runner.
 *
 * Loops batch-run-gates + revenue E2E on a schedule until green or max cycles.
 * Logs each cycle to stdout (pipe to file for overnight runs).
 *
 *   node scripts/overnight-ralph.mjs
 *   node scripts/overnight-ralph.mjs --host https://councilof.ai --cycles 12 --interval 900
 *   node scripts/overnight-ralph.mjs --cycles 48 --interval 1800  # every 30m for 24h
 */

import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};

const HOST = arg("host", "https://councilof.ai");
const CYCLES = Math.max(1, parseInt(arg("cycles", "6"), 10) || 6);
const INTERVAL = Math.max(60, parseInt(arg("interval", "600"), 10) || 600);
const RETRY_WAIT = Math.max(0, parseInt(arg("wait", "120"), 10) || 120);

const sleep = (s) => new Promise((r) => setTimeout(r, s * 1000));
const ts = () => new Date().toISOString();

function run(label, script, extraArgs = []) {
  console.log(`\n[${ts()}] ${label}`);
  const r = spawnSync("node", [join(ROOT, "scripts", script), "--host", HOST, ...extraArgs], {
    cwd: ROOT,
    stdio: "inherit",
  });
  return r.status ?? 1;
}

async function cycle(n) {
  console.log(`\n${"=".repeat(72)}\nRALPH CYCLE ${n}/${CYCLES} — ${HOST}\n${"=".repeat(72)}`);

  let fails = 0;
  if (run("batch-run-gates", "batch-run-gates.mjs", ["--retry", "2", "--wait", String(RETRY_WAIT)])) {
    fails++;
  }
  if (run("revenue E2E", "e2e-revenue.mjs")) {
    fails++;
  }

  if (!fails) {
    console.log(`\n[${ts()}] RALPH CYCLE ${n}: ALL GREEN — stopping early.`);
    return true;
  }
  console.log(`\n[${ts()}] RALPH CYCLE ${n}: ${fails} gate bundle(s) failed.`);
  return false;
}

async function main() {
  console.log(`OVERNIGHT-RALPH — host=${HOST} cycles=${CYCLES} interval=${INTERVAL}s wait=${RETRY_WAIT}s\n`);

  for (let i = 1; i <= CYCLES; i++) {
    const ok = await cycle(i);
    if (ok) process.exit(0);
    if (i < CYCLES) {
      console.log(`\n[${ts()}] Sleeping ${INTERVAL}s before next cycle…`);
      await sleep(INTERVAL);
    }
  }

  console.error(`\n[${ts()}] RALPH: exhausted ${CYCLES} cycles without all-green.`);
  process.exit(1);
}

main();
