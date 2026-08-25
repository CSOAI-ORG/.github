#!/usr/bin/env node
/**
 * e2e-revenue.mjs — revenue + data-earning rails live gates.
 *
 * Probes commercial surfaces without inventing traction. Honest UNPUBLISHED is PASS.
 *
 *   node scripts/e2e-revenue.mjs
 *   node scripts/e2e-revenue.mjs --host https://councilof.ai
 */

const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const HOST = (arg("host", "https://councilof.ai")).replace(/\/$/, "");
const UA = "CSOAI-revenue/1.0";

let hard = 0;
let soft = 0;
const fail = (m) => { console.log(`  ✗ ${m}`); hard++; };
const warn = (m) => { console.log(`  ~ ${m}`); soft++; };
const pass = (m) => console.log(`  ✓ ${m}`);

async function get(path) {
  const r = await fetch(HOST + path, { headers: { "user-agent": UA } });
  const body = await r.text();
  let json = {};
  try { json = JSON.parse(body); } catch { /* html */ }
  return { status: r.status, body, len: body.length, json };
}

console.log(`REVENUE E2E — ${HOST}\n`);

console.log("## Sales surfaces\n");
for (const [path, min] of [
  ["/pricing", 10000],
  ["/start", 10000],
  ["/enterprise", 10000],
  ["/payg/", 5000],
  ["/eunomia-data/", 5000],
  ["/insurers/", 10000],
]) {
  const r = await get(path);
  if (r.status >= 400) fail(`${path} HTTP ${r.status}`);
  else if (r.len < min) warn(`${path} thin (${r.len} B)`);
  else pass(`${path} (${r.len} B)`);
}

console.log("\n## Data rails (API)\n");
const gspc = await get("/api/gspc");
if (gspc.status === 200 && gspc.json?.totals?.measured_axes === 14) {
  pass("GET /api/gspc — 14 measured (truth rail for data products)");
} else {
  fail(`GET /api/gspc — canon drift (${gspc.status})`);
}

const evidence = await get("/api/evidence-pack");
if (evidence.status === 200 && evidence.json?.schema?.includes("insurability-evidence-pack")) {
  pass("GET /api/evidence-pack — insurability pack schema live (M3·021)");
} else {
  fail(`GET /api/evidence-pack → ${evidence.status}`);
}

const eunomia = await get("/api/eunomia-data");
if (eunomia.status === 200 && eunomia.json?.gate?.kind === "x402") {
  pass(`GET /api/eunomia-data — x402 DATA rail ($${eunomia.json.gate.price_usd}/query)`);
  if (!eunomia.json.gate.pay_url) {
    warn("x402 pay_url empty — settlement MCP not bound (OWNER·052)");
  } else {
    pass(`x402 pay_url: ${eunomia.json.gate.pay_url}`);
  }
  const gateProbe = await fetch(`${HOST}/api/eunomia-data?x402=1`, { headers: { "user-agent": UA } });
  if (gateProbe.status === 402) pass("GET /api/eunomia-data?x402=1 → 402 Payment Required");
  else warn(`x402 gate probe → HTTP ${gateProbe.status} (expected 402)`);
} else {
  fail(`GET /api/eunomia-data → ${eunomia.status}`);
}

const counters = await get("/api/counters");
if (counters.status === 200 && counters.json?.schema?.includes("wave1-counters")) {
  pass("GET /api/counters — Wave-1 counters schema");
  const live = (counters.json.counters || []).filter((c) => c.status === "LIVE").length;
  if (live > 0) pass(`${live} counter(s) bound to live aggregates`);
  else warn("All counters UNPUBLISHED — honest zero state until live bind deploys");
} else {
  fail(`GET /api/counters → ${counters.status}`);
}

const waveDash = await get("/api/wave-dashboard");
if (waveDash.status === 200 && waveDash.json?.schema?.includes("wave-dashboard")) {
  pass("GET /api/wave-dashboard — runtime wave aggregates");
  const measured = (waveDash.json.waves || []).filter((w) => w.register === "MEASURED").length;
  pass(`${measured} wave(s) MEASURED from live APIs`);
} else if (waveDash.status === 404) {
  warn("/api/wave-dashboard → 404 — await challenge/wave PR deploy");
} else {
  warn(`/api/wave-dashboard → ${waveDash.status}`);
}

const challengeGet = await get("/api/challenge");
if (challengeGet.status === 200) pass("GET /api/challenge — redress door schema");
else if (challengeGet.status === 404) warn("GET /api/challenge → 404 — await deploy");
else fail(`GET /api/challenge → ${challengeGet.status}`);

const receipts = await get("/api/receipts/latest");
if (receipts.status === 200 && receipts.json?.status === "UNPUBLISHED" && receipts.json?.count === 0) {
  pass("GET /api/receipts/latest — honest empty ledger (no fabricated revenue)");
} else if (receipts.status === 200 && receipts.json?.count > 0) {
  pass(`GET /api/receipts/latest — ${receipts.json.count} settlement receipt(s) published`);
} else {
  fail(`GET /api/receipts/latest unexpected shape`);
}

console.log("\n## Conversion path\n");
const verify = await get("/gspc-verify/");
if (verify.status === 200) pass("/gspc-verify/ — free verify entry (top of funnel)");
else fail("/gspc-verify/ not live");

const mcp = await get("/.well-known/mcp.json");
if (mcp.status === 200 && /measure/.test(mcp.body)) pass("MCP measure tool listed (agent rail)");
else warn("MCP catalog probe inconclusive");

console.log("\n## Owner gates (informational)\n");
warn("051 OWNER-BLOCKED: PAYG pricing ruling — /payg shows 'pending ruling'");
warn("052 OWNER-BLOCKED: x402 settlement bind — pay_url until receipt MCP wired");
warn("058 OWNER-BLOCKED: first sale ledger row — receipts count stays 0 until sale");

console.log("");
if (hard) {
  console.error(`REVENUE E2E: FAIL — ${hard} hard, ${soft} soft`);
  process.exit(1);
}
console.log(`REVENUE E2E: PASS — ${soft} soft warn(s); sales surfaces + data rails aligned.`);
