#!/usr/bin/env node
/**
 * run-all.mjs — monorepo harness batch runner (parallel).
 *
 * Aligns every workstream from top and runs them concurrently, then prints one
 * aggregated report. Exit 1 if any lane fails.
 *
 *   node scripts/run-all.mjs
 */
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const LANES = [
  { name: "lint:python", cmd: "python3", args: ["-m", "py_compile",
      "products/claimguard/claimguard.py", "products/claimguard/canonical.py", "products/claimguard/c2pa.py",
      "harness/receipts.py", "harness/board.py", "harness/detect.py", "harness/register.py", "harness/server.py",
      "harness/tlog.py", "harness/verify_external.py", "harness/e2e_harness.py"] },
  { name: "lint:node", cmd: "node", args: ["--check", "scripts/run-frontend-audit.mjs"] },
  { name: "lint:node2", cmd: "node", args: ["--check", "scripts/e2e-integration-stack.mjs"] },
  { name: "test:claimguard", cmd: "python3", args: ["-m", "pytest", "-q", "products/claimguard"] },
  { name: "test:harness", cmd: "python3", args: ["-m", "pytest", "-q", "harness/tests"] },
  { name: "e2e:full-stack", cmd: "python3", args: ["harness/e2e_harness.py"] },
];

function runLane(lane) {
  return new Promise((res) => {
    const started = Date.now();
    const p = spawn(lane.cmd, lane.args, { cwd: ROOT });
    let out = "";
    p.stdout.on("data", (d) => (out += d));
    p.stderr.on("data", (d) => (out += d));
    p.on("close", (code) => res({ name: lane.name, code, ms: Date.now() - started, out }));
    p.on("error", (e) => res({ name: lane.name, code: 1, ms: Date.now() - started, out: String(e) }));
  });
}

console.log(`RUN-ALL — ${LANES.length} lanes in parallel\n`);
const results = await Promise.all(LANES.map(runLane));

let failed = 0;
const w = Math.max(...results.map((r) => r.name.length));
for (const r of results) {
  const ok = r.code === 0;
  if (!ok) failed++;
  console.log(`  ${ok ? "\u2713 PASS" : "\u2717 FAIL"}  ${r.name.padEnd(w)}  ${(r.ms / 1000).toFixed(2)}s`);
}
if (failed) {
  console.log(`\nfailing lane output:\n`);
  for (const r of results.filter((x) => x.code !== 0)) {
    console.log(`----- ${r.name} -----\n${r.out.trim()}\n`);
  }
  console.error(`RUN-ALL: FAIL — ${failed}/${results.length} lane(s)`);
  process.exit(1);
}
console.log(`\nRUN-ALL: PASS — all ${results.length} lanes green`);
