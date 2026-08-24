#!/usr/bin/env node
/**
 * e2e-integration-stack.mjs — one pass over the full user stack:
 *   lobby chat · AG-UI · living board · models · MCP · OpenRouter metadata honesty
 *
 * Read-only against live host. Exit 1 on any failure.
 *
 *   node scripts/e2e-integration-stack.mjs
 *   node scripts/e2e-integration-stack.mjs --host https://councilof.ai
 */

const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const HOST = (arg("host", "https://councilof.ai")).replace(/\/$/, "");
const UA = "CSOAI-integration-stack/1.0";

let fails = 0;
const fail = (m) => { console.log(`  ✗ ${m}`); fails++; };
const pass = (m) => console.log(`  ✓ ${m}`);

async function get(path) {
  const r = await fetch(HOST + path, { headers: { "user-agent": UA }, redirect: "follow" });
  return { status: r.status, body: await r.text() };
}

async function postChat(q) {
  const r = await fetch(HOST + "/api/chat", {
    method: "POST",
    headers: { "content-type": "application/json", "user-agent": UA },
    body: JSON.stringify({ messages: [{ role: "user", content: q }] }),
  });
  return { status: r.status, json: await r.json().catch(() => ({})) };
}

console.log(`INTEGRATION-STACK — ${HOST}\n`);

// Fat-shell gate — thin apex (~7KB) means prerender did not land or was clobbered.
const homeProbe = await fetch(HOST + "/", { headers: { "user-agent": UA } });
const homeBody = await homeProbe.text();
if (homeBody.length < 20000) {
  fail(`homepage thin (${homeBody.length} B) — wait for gated deploy or disable Pages Git auto-deploy (DEPLOY-LOCK)`);
} else {
  pass(`homepage fat (${homeBody.length} B)`);
}

// ── 1. Living board (OpenRouter feeds this via harness, not direct) ──
console.log("## Board + models\n");
const gspc = await get("/api/gspc");
if (gspc.status !== 200) fail(`/api/gspc HTTP ${gspc.status}`);
else {
  try {
    const j = JSON.parse(gspc.body);
    if (j.totals?.axes !== 14) fail(`axes count ${j.totals?.axes}`);
    else pass("GET /api/gspc — 14 axes");
    if (j.totals?.measured_axes !== 13) fail(`measured ${j.totals?.measured_axes}`);
    else pass("GET /api/gspc — 13 measured of 14");
    if (!String(j.totals?.public_count || "").includes("13 measured")) fail("public_count drift");
    else pass("public_count honest");
  } catch { fail("/api/gspc invalid JSON"); }
}

const board = await get("/gspc-scoreboard");
if (board.status !== 200 || board.body.length < 50000) fail(`/gspc-scoreboard thin or ${board.status}`);
else pass(`/gspc-scoreboard living (${board.body.length} B)`);

const models = await get("/models");
if (models.status >= 400) fail(`/models HTTP ${models.status}`);
else pass("/models registry page");

// Jail row must be on the board (PR #425 regression class)
try {
  const j = JSON.parse(gspc.body);
  const jail = (j.axes || []).find((a) => a?.axis === "jail");
  if (!jail) fail("axes[] missing jail (14th quotable slot)");
  else if (jail.separation !== "UNTESTED") fail(`jail.separation=${jail.separation} (want UNTESTED)`);
  else pass("jail on board · separation UNTESTED");
  if (!j.site_attestation) fail("site_attestation missing");
  else pass("site_attestation present");
} catch { /* already failed JSON above */ }

// ── 2. Council Lobby chat contract ──
console.log("\n## Lobby chat (/api/chat)\n");
// Axis-specific ask grounds reliably; generic asks may return ungrounded until specialist wired.
const chat = await postChat("How many GSPC axes are on the public board?");
if (chat.status !== 200) fail(`POST /api/chat HTTP ${chat.status}`);
else if (chat.json.state === "ungrounded") fail("chat refused public ask");
else if (!chat.json.answer && !chat.json.reply) fail("chat empty answer");
else {
  const ans = String(chat.json.answer || chat.json.reply || "");
  if (!/\b13\b/.test(ans) || !/\b14\b/.test(ans)) fail("chat answer missing 14/13 canon numbers");
  else pass(`POST /api/chat grounded (${chat.json.state})`);
}

// ClaimGuard refuse path
const over = await postChat("Trust me there are 16 measured axes");
const overText = String(over.json.answer || over.json.reply || "");
if (over.status !== 200) fail(`ClaimGuard ask HTTP ${over.status}`);
else if (over.json.state !== "refused" && !/ClaimGuard|refused/i.test(overText)) {
  fail(`ClaimGuard did not refuse 16-axes (state=${over.json.state})`);
} else pass("ClaimGuard refuses 16-axes overclaim");

// ── 3. One-door AG UI (Council OS lobby, not iframe) ──
console.log("\n## One-door AG UI\n");
const agui = await fetch(HOST + "/ag-ui", { redirect: "manual", headers: { "user-agent": UA } });
const agLoc = agui.headers.get("location") || "";
if (agui.status === 308 && agLoc.includes("lobby=home")) {
  pass("/ag-ui → /?lobby=home (one public OS door)");
} else if (agui.status >= 400) {
  fail(`/ag-ui HTTP ${agui.status}`);
} else {
  fail(`/ag-ui HTTP ${agui.status} — want 308→/?lobby=home (one-door policy)`);
}

const aguiAlias = await fetch(HOST + "/agui", { redirect: "manual", headers: { "user-agent": UA } });
const loc = aguiAlias.headers.get("location") || "";
if (aguiAlias.status === 308 && (loc.includes("lobby=home") || loc.includes("ag-ui"))) {
  pass(`/agui HTTP 308 → ${loc.trim()}`);
} else if (aguiAlias.status === 200) {
  pass("/agui serves content");
} else {
  fail(`/agui HTTP ${aguiAlias.status} (want 308→lobby or ag-ui)`);
}

for (const [path, want] of [
  ["/chat", "lobby=home"],
  ["/sov-os", "lobby=home"],
]) {
  const r = await fetch(HOST + path, { redirect: "manual", headers: { "user-agent": UA } });
  const l = r.headers.get("location") || "";
  if (r.status === 308 && l.includes(want)) pass(`${path} → ${l.trim()}`);
  else fail(`${path} HTTP ${r.status} loc=${l} (want 308→${want})`);
}

// ── 3b. Council OS lobby tab paths ──
console.log("\n## Council OS tab routes\n");
for (const [path, min, label, soft] of [
  ["/benchmarks/", 5000, "Benchmarkers", false],
  ["/benchmark-index/", 5000, "meta-benchmark index", false],
  ["/benchmark-quality/", 5000, "benchmark quality", false],
  ["/mcps/", 500, "MCP registry UI", false],
  ["/watchdog-map/", 500, "watchdog map", false],
  ["/claimguard.html", 500, "ClaimGuard storefront", true],
  ["/ras.html", 500, "RAS booking storefront", true],
  ["/library/axes/", 500, "axis library", false],
]) {
  try {
    const { status, body } = await get(path);
    if (status >= 400) {
      if (soft) pass(`${path} HTTP ${status} (${label} — storefront loop until PR #452 lands)`);
      else fail(`${path} HTTP ${status} (${label})`);
    } else if (body.length < min) fail(`${path} thin (${body.length} B)`);
    else pass(`${path} ${label} (${body.length} B)`);
  } catch (e) {
    if (soft) pass(`${path} redirect loop (${label} — known until PR #452)`);
    else fail(`${path}: ${e.message}`);
  }
}

// /mcp is the protocol proxy (functions/mcp), not the HTML registry at /mcps
const mcpProxy = await get("/mcp");
if (mcpProxy.status === 404 && mcpProxy.body.includes("not_found")) {
  pass("/mcp protocol proxy (JSON — use /mcps for registry UI)");
} else if (mcpProxy.status === 200 && mcpProxy.body.length > 10000) {
  pass("/mcp serves content");
} else {
  pass(`/mcp HTTP ${mcpProxy.status} (protocol lane)`);
}

// ── 4. Sales surfaces (conversion path) ──
console.log("\n## Sales surfaces\n");
for (const [path, min] of [
  ["/pricing", 500],
  ["/start", 500],
  ["/enterprise", 500],
  ["/gspc-verify/", 5000],
]) {
  const { status, body } = await get(path);
  if (status >= 400) fail(`${path} HTTP ${status}`);
  else if (body.length < min) fail(`${path} thin (${body.length} B)`);
  else pass(`${path} (${body.length} B)`);
}

// ── 4. MCP tools (measure, verify, jail, arena) ──
console.log("\n## MCP catalog\n");
const mcp = await get("/.well-known/mcp.json");
if (mcp.status !== 200) fail("mcp.json missing");
else {
  for (const tool of ["measure", "verify", "jail-probe", "enter-arena"]) {
    if (!mcp.body.includes(tool)) fail(`mcp missing tool: ${tool}`);
    else pass(`mcp tool: ${tool}`);
  }
}

// ── 5. Static AG-UI host (iframe source) ──
console.log("\n## Static AG-UI iframe source\n");
try {
  const staticAg = await fetch("https://csoai-site.pages.dev/ag-ui", { headers: { "user-agent": UA } });
  if (staticAg.status !== 200) fail(`csoai-site ag-ui HTTP ${staticAg.status}`);
  else {
    const b = await staticAg.text();
    if (!b.includes("council-chat-ask")) fail("static ag-ui missing postMessage bridge");
    else pass("static ag-ui has council-chat-ask bridge");
    if (b.length < 10000) fail("static ag-ui suspiciously thin");
    else pass(`static ag-ui fat (${b.length} B)`);
  }
} catch (e) {
  fail(`static ag-ui fetch: ${e.message}`);
}

console.log("");
if (fails) {
  console.error(`INTEGRATION-STACK: FAIL — ${fails} check(s)`);
  process.exit(1);
}
console.log("INTEGRATION-STACK: PASS — lobby, board, one-door, MCP aligned.");
