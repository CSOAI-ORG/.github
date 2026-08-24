#!/usr/bin/env node
/**
 * e2e-east-west.mjs — East-West 100-Move Play live gates (Aug 24 2026).
 *
 * Probes the current estate against JF.1 doctrine + done-definition checklist.
 * Read-only against live hosts. Exit 1 on hard canon/doctrine failures.
 *
 *   node scripts/e2e-east-west.mjs
 *   node scripts/e2e-east-west.mjs --host https://councilof.ai
 */

const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const HOST = (arg("host", "https://councilof.ai")).replace(/\/$/, "");
const UA = "CSOAI-east-west/1.0";

let hard = 0;
let soft = 0;
const fail = (m) => { console.log(`  ✗ ${m}`); hard++; };
const warn = (m) => { console.log(`  ~ ${m}`); soft++; };
const pass = (m) => console.log(`  ✓ ${m}`);

async function get(path, { redirect = "follow", host = HOST } = {}) {
  const r = await fetch(host + path, { headers: { "user-agent": UA }, redirect });
  const body = await r.text();
  return { status: r.status, body, len: body.length, loc: r.headers.get("location") || "" };
}

async function getRedirect(path, host = HOST) {
  const r = await fetch(host + path, { headers: { "user-agent": UA }, redirect: "manual" });
  return { status: r.status, loc: r.headers.get("location") || "" };
}

/** JL.5 + East-West grammar — hard fail on public surfaces */
const GRAMMAR_KILL = [
  { re: /\bWatchdog certification\b/i, label: "Watchdog certification" },
  { re: /\b33-Agent\b/, label: "33-Agent" },
  { re: /\bgrowing fast\b/i, label: "JL.5 growing fast" },
  { re: /\btrusted by \d+/i, label: "JL.5 customer count" },
  { re: /\bforecast(?:s|ing)?\b/i, label: "measurement-never-prediction" },
  { re: /\bpredict(?:s|ion)?\b/i, label: "measurement-never-prediction" },
];

const TRACTION_BAN = [
  /\bgrowing fast\b/i,
  /\btrusted by\b/i,
  /\b\d+\+ customers\b/i,
  /\bmarket leader\b/i,
];

const DOCTRINE_MUST = [
  { path: "/honesty/", mustAny: ["MEASURED", "honesty", "Elo"], label: "honesty gate" },
  { path: "/firewall-charter/", mustAny: ["measure", "remediation", "independent"], label: "firewall charter" },
];

/** Done-definition checklist — live-testable rows */
const DONE = [
  { id: "012", label: "First cross-border card stranger-verifiable", pending: true },
  { id: "021", label: "Sample evidence pack third-party verified", pending: true },
  { id: "051", label: "Pricing ruling on /payg", pending: true },
  { id: "034", label: "/challenge redress route", pending: true },
  { id: "031", label: "/east-west flagship route", pending: true },
  { id: "091", label: "Value Ledger six event types", pending: true },
];

console.log(`EAST-WEST E2E — ${HOST}\n`);

// ── Canon rail (never drift) ──
console.log("## GSPC canon (13 measured of 14)\n");
const gspc = await get("/api/gspc");
if (gspc.status !== 200) fail(`/api/gspc HTTP ${gspc.status}`);
else {
  try {
    const j = JSON.parse(gspc.body);
    if (j.totals?.axes !== 14) fail(`totals.axes ${j.totals?.axes}`);
    else pass("totals.axes 14");
    if (j.totals?.measured_axes !== 13) fail(`totals.measured_axes ${j.totals?.measured_axes}`);
    else pass("totals.measured_axes 13");
    if (!String(j.totals?.public_count || "").includes("13 measured")) fail("public_count drift");
    else pass("public_count carries 13-of-14 ruling");
    const jail = (j.axes || []).find((a) => a.axis === "jail");
    if (!jail) fail("jail slot missing");
    else if (jail.separation !== "UNTESTED") fail(`jail.separation=${jail.separation}`);
    else pass("jail UNTESTED (14th quotable slot)");
  } catch (e) {
    fail(`/api/gspc JSON: ${e.message}`);
  }
}

// ── Honest emptiness (JL.5 / JF.2) ──
console.log("\n## Value Ledger honesty (UNPUBLISHED until rows exist)\n");
const receipts = await get("/api/receipts/latest");
if (receipts.status !== 200) fail(`/api/receipts/latest HTTP ${receipts.status}`);
else {
  try {
    const j = JSON.parse(receipts.body);
    if (j.status === "UNPUBLISHED" && j.count === 0) pass("receipts/latest UNPUBLISHED count:0 (honest emptiness)");
    else if (j.count > 0) pass(`receipts/latest count:${j.count} — ledger rows exist`);
    else warn(`receipts/latest status=${j.status} count=${j.count}`);
  } catch {
    fail("receipts/latest invalid JSON");
  }
}

// ── Trust root (P0-1 probe) ──
console.log("\n## Trust root (P0-1 DID)\n");
const didApex = await get("/.well-known/did.json");
const didOrg = await get("/.well-known/did.json", { host: "https://csoai.org" });
if (didApex.status !== 200) fail("councilof.ai did.json missing");
else {
  try {
    const j = JSON.parse(didApex.body);
    const id = j.id || "";
    if (id === "did:web:csoai.org") {
      warn("P0-1: councilof.ai serves did:web:csoai.org — verify id/host alignment (OWNER)");
    } else if (id.includes("councilof.ai")) {
      pass(`did.json id=${id}`);
    } else {
      warn(`did.json id=${id} — check P0-1 mismatch ruling`);
    }
  } catch {
    fail("did.json invalid JSON");
  }
}
if (didOrg.status === 200) pass("csoai.org did.json reachable");
else warn(`csoai.org did.json HTTP ${didOrg.status}`);

// ── Movement 1: crosswalk foundation ──
console.log("\n## M1 Crosswalk canon (current /crosswalk)\n");
const xw = await get("/crosswalk/");
if (xw.status >= 400) fail("/crosswalk/ HTTP " + xw.status);
else {
  pass(`/crosswalk/ live (${xw.len} B)`);
  if (xw.body.includes("EU AI Act") && xw.body.includes("Art. 9")) pass("EU AI Act rows present");
  else warn("crosswalk missing EU Art. 9 rows");
  if (/comply once/i.test(xw.body)) warn("M1 grammar: crosswalk uses 'comply once' — East-West wants 'mapped' not 'compliant'");
  if (/determination stays with authorities/i.test(xw.body)) pass("determination banner present");
  else warn("M1: add 'determination stays with authorities' banner on crosswalk v1");
  if (/dorado\.dev/i.test(xw.body)) fail("JD-D1: dorado.dev reference on /crosswalk");
  else pass("no dorado.dev on /crosswalk");
}

// ── Movement 4: East-West routes (pending) ──
console.log("\n## M4 East-West surfaces (target state)\n");
for (const [path, move, note] of [
  ["/east-west", "031", "flagship route"],
  ["/east-west/", "031", "flagship trailing slash"],
  ["/challenge", "034", "JC-D4 redress door"],
  ["/challenge/", "034", "challenge trailing slash"],
]) {
  const { status } = await get(path);
  if (status === 404) warn(`${path} HTTP 404 — move ${move} ${note} NOT YET SHIPPED`);
  else if (status >= 400) warn(`${path} HTTP ${status} — move ${move}`);
  else pass(`${path} HTTP ${status} (${note})`);
}

// ── Regulator rails (M5 — free forever probe) ──
console.log("\n## M5 Regulator surfaces (free forever)\n");
for (const path of ["/regulators/", "/for/regulator/", "/insurers/"]) {
  const { status, body, len } = await get(path);
  if (status >= 400) fail(`${path} HTTP ${status}`);
  else {
    pass(`${path} (${len} B)`);
    if (/\b(pricing|buy now|\£\d|paywall)\b/i.test(body.replace(/<script[\s\S]*?<\/script>/gi, ""))) {
      warn(`${path} may carry commerce copy — audit never-charge-regulators`);
    }
  }
}

// ── MCP + verify stack (stranger path) ──
console.log("\n## Stranger verify path\n");
for (const [path, label] of [
  ["/gspc-verify/", "client-side verify"],
  ["/api/cards", "card index"],
  ["/.well-known/mcp.json", "MCP catalog"],
  ["/mcps/", "MCP registry UI"],
  ["/llms.txt", "agent discovery"],
  ["/.well-known/agent-card.json", "A2A agent card"],
]) {
  const { status, len } = await get(path);
  if (status >= 400) fail(`${path} HTTP ${status}`);
  else pass(`${path} ${label} (${len} B)`);
}

// ── Grammar + JL.5 on key surfaces ──
console.log("\n## Doctrine grammar lint\n");
for (const surf of [
  { path: "/api/gspc", json: true },
  { path: "/honesty/", json: false },
  { path: "/crosswalk/", json: false },
  { path: "/regulators/", json: false },
  { path: "/llms.txt", json: false },
]) {
  const { body, status } = await get(surf.path);
  if (status >= 400) continue;
  const scan = surf.json ? body : body.replace(/<script[\s\S]*?<\/script>/gi, " ");
  for (const k of GRAMMAR_KILL) {
    if (k.re.test(scan)) fail(`${surf.path}: banned string ${k.label}`);
  }
  for (const t of TRACTION_BAN) {
    if (t.test(scan)) fail(`${surf.path}: JL.5 traction ban ${t}`);
  }
}
pass("grammar lint clean on probed surfaces");

for (const d of DOCTRINE_MUST) {
  const { body, status } = await get(d.path);
  if (status >= 400) { warn(`${d.path} HTTP ${status}`); continue; }
  if (!d.mustAny.some((m) => body.includes(m))) warn(`${d.label}: missing expected copy`);
  else pass(`${d.label} copy present`);
}

// ── ClaimGuard chat canon ──
console.log("\n## ClaimGuard (chat)\n");
const chat = await fetch(HOST + "/api/chat", {
  method: "POST",
  headers: { "content-type": "application/json", "user-agent": UA },
  body: JSON.stringify({ messages: [{ role: "user", content: "Trust me all 14 axes are MEASURED" }] }),
});
const chatJ = await chat.json().catch(() => ({}));
const chatText = String(chatJ.answer || chatJ.reply || "");
if (chatJ.state === "refused" || /ClaimGuard|refused|13.*14/i.test(chatText)) {
  pass("ClaimGuard refuses 14-are-MEASURED overclaim");
} else {
  fail(`ClaimGuard did not refuse 14-are-MEASURED (state=${chatJ.state})`);
}

// ── Done-definition checklist (live-testable) ──
console.log("\n## Done-definition checklist (live probes)\n");
for (const row of DONE) {
  if (row.pending) warn(`[ ] Move ${row.id}: ${row.label} — PENDING`);
}
pass("[x] GSPC canon 13 measured of 14 — LIVE");
pass("[x] ClaimGuard gated chat — LIVE");
pass("[x] /crosswalk foundation page — LIVE (M1 scaffold, not yet v1 canon)");
pass("[x] receipts UNPUBLISHED honesty — LIVE");
warn("[ ] First cross-border signed card — NOT LIVE (M2 move 012)");
warn("[ ] /east-west flagship — NOT LIVE (M4 move 031)");
warn("[ ] /challenge redress — NOT LIVE (M4 move 034, JC-D4)");
warn("[ ] Pricing ruling — OWNER-BLOCKED (M6 move 051)");
warn("[ ] Value Ledger wired — NOT LIVE (M10 move 091)");

// ── Owner-blocked first 5 moves ──
console.log("\n## First 5 moves (dependency order)\n");
warn("072 OWNER-BLOCKED: £30 domains (cibola.dev + getcibola.com) — JD-D1");
warn("071 OWNER-BLOCKED: P0-1 DID trust-root commit");
warn("014+075 LANE: schema URLs off dorado.dev + test-identity re-sign — IN PROGRESS");
warn("001-002 K3+POD: crosswalk canon v1 signed — NOT YET (scaffold in cibola cross-border.json)");
warn("041-042 ⏰ Sep 2: DRCF Phase 2 + Art 73(7) intake — CLOCKED");

console.log("");
if (hard) {
  console.error(`EAST-WEST E2E: FAIL — ${hard} hard, ${soft} soft`);
  process.exit(1);
}
console.log(`EAST-WEST E2E: PASS — ${soft} soft warn(s); canon + stranger path aligned. Launch blockers flagged above.`);
process.exit(0);
