#!/usr/bin/env node
/**
 * batch-run-gates.mjs — chain all live gates in one pass.
 *
 *   node scripts/batch-run-gates.mjs
 *   node scripts/batch-run-gates.mjs --host https://councilof.ai
 *   node scripts/batch-run-gates.mjs --retry 3 --wait 120
 *
 * Exit 1 if any gate fails after retries.
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
const RETRIES = Math.max(1, parseInt(arg("retry", "1"), 10) || 1);
const WAIT_SEC = Math.max(0, parseInt(arg("wait", "0"), 10) || 0);

const sleep = (s) => new Promise((r) => setTimeout(r, s * 1000));

function run(label, cmd, args, extraEnv = {}) {
  console.log(`\n${"=".repeat(60)}\n${label}\n${"=".repeat(60)}\n`);
  const r = spawnSync(cmd, args, {
    cwd: ROOT,
    stdio: "inherit",
    env: { ...process.env, ...extraEnv },
  });
  return r.status ?? 1;
}

async function runE2EWithRetry() {
  for (let i = 1; i <= RETRIES; i++) {
    const code = run(
      `E2E integration stack (attempt ${i}/${RETRIES})`,
      "node",
      ["scripts/e2e-integration-stack.mjs", "--host", HOST],
    );
    if (code === 0) return 0;
    if (i < RETRIES && WAIT_SEC > 0) {
      console.log(`\nWaiting ${WAIT_SEC}s for deploy/clobber window before retry...\n`);
      await sleep(WAIT_SEC);
    }
  }
  return 1;
}

async function main() {
  console.log(`BATCH-GATES — ${HOST} (retries=${RETRIES}, wait=${WAIT_SEC}s)\n`);

  let fails = 0;

  // Thin-shell early warning
  try {
    const home = await fetch(HOST.replace(/\/$/, "") + "/", {
      headers: { "user-agent": "CSOAI-batch-gates/1.0" },
    });
    const body = await home.text();
    const thin = body.length < 20000;
    console.log(`Homepage: ${body.length} bytes${thin ? " — THIN (deploy may be in flight or clobbered)" : " — fat OK"}`);
    if (thin) console.log("Tip: re-run with --retry 3 --wait 120 after gated deploy lands.\n");
  } catch (e) {
    console.log(`Homepage probe failed: ${e.message}\n`);
  }

  if (run("ClaimGuard self-test", "python3", ["products/claimguard/claimguard.py", "--self-test"])) {
    fails++;
  }

  if (await runE2EWithRetry()) fails++;

  if (run("Lobby nav E2E", "node", ["scripts/e2e-lobby-nav.mjs", "--host", HOST])) {
    fails++;
  }

  if (run("East-West E2E", "node", ["scripts/e2e-east-west.mjs", "--host", HOST])) {
    fails++;
  }

  if (run("DSH + auth E2E", "node", ["scripts/e2e-dsh.mjs", "--host", HOST])) {
    fails++;
  }

  if (run("Revenue rails E2E", "node", ["scripts/e2e-revenue.mjs", "--host", HOST])) {
    fails++;
  }

  if (run("Weekend demo smoke", "node", ["scripts/weekend-demo-smoke.mjs", "--host", HOST])) {
    fails++;
  }

  if (run("Mine live drifts", "node", ["scripts/mine-live-drifts.mjs", "--host", HOST])) {
    fails++;
  }

  if (run("Frontend audit", "node", ["scripts/run-frontend-audit.mjs", "--host", HOST])) {
    fails++;
  }

  console.log(`\n${"=".repeat(60)}`);
  if (fails) {
    console.error(`BATCH-GATES: FAIL — ${fails} gate(s) failed. See docs/STEPS_200.md`);
    process.exit(1);
  }
  console.log("BATCH-GATES: PASS — all gates green.");
  process.exit(0);
}

main();
