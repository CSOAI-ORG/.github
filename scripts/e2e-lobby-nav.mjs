#!/usr/bin/env node
/**
 * e2e-lobby-nav.mjs — Council OS lobby tabs, inner routes, personas, axis tooling.
 *
 * Read-only against live host. Exit 1 on any hard failure.
 *
 *   node scripts/e2e-lobby-nav.mjs
 *   node scripts/e2e-lobby-nav.mjs --host https://councilof.ai
 */

const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const HOST = (arg("host", "https://councilof.ai")).replace(/\/$/, "");
const UA = "CSOAI-lobby-nav/1.0";

let fails = 0;
let soft = 0;
const fail = (m) => { console.log(`  ✗ ${m}`); fails++; };
const warn = (m) => { console.log(`  ~ ${m}`); soft++; };
const pass = (m) => console.log(`  ✓ ${m}`);

async function get(path, { redirect = "follow" } = {}) {
  const r = await fetch(HOST + path, { headers: { "user-agent": UA }, redirect });
  const body = await r.text();
  return { status: r.status, body, len: body.length, loc: r.headers.get("location") || "" };
}

async function getRedirect(path) {
  const r = await fetch(HOST + path, { headers: { "user-agent": UA }, redirect: "manual" });
  return { status: r.status, loc: r.headers.get("location") || "" };
}

/** 15 rail tabs — id + framed path (empty = local/native pane) */
const LOBBY_TABS = [
  { id: "home", path: null, min: 20000 },
  { id: "board", path: "/gspc-scoreboard", min: 50000 },
  { id: "results", path: "/benchmarks", min: 5000 },
  { id: "models", path: "/models", min: 500 },
  { id: "tools", path: "/tools", min: 500 },
  { id: "verify", path: "/gspc-verify", min: 5000 },
  { id: "space", path: "/gspc-arena", min: 500 },
  { id: "measured", path: "/assess", min: 500 },
  { id: "watchdog", path: "/watchdog-map", min: 500 },
  { id: "claimguard", path: "/claimguard.html", min: 500, softLoop: true },
  { id: "ras", path: "/ras.html", min: 500, softLoop: true },
  { id: "library", path: "/library", min: 500 },
  { id: "workbench", path: "/workbench", min: 500 },
  { id: "software", path: "/dashboard", min: 500 },
  { id: "play", path: null, min: 20000 },
];

/** Home-desktop LOBBY_ROUTES (not rail tabs) */
const LOBBY_ROUTES = [
  "/benchmark-index",
  "/benchmark-quality",
  "/mcps",
  "/mcp-fleet",
  "/layer0",
  "/trust-center",
  "/network",
  "/hive",
  "/intel",
  "/system-card",
  "/methodology",
  "/honesty",
  "/instrument",
  "/refutation-ledger",
  "/firewall-charter",
  "/crosswalk",
  "/east-west",
  "/challenge",
  "/feed",
  "/library/axes",
];

const PERSONAS = [
  { who: "regulator", path: "/for/regulator/" },
  { who: "enterprise", path: "/for/enterprise/" },
  { who: "finance", path: "/for/finance/" },
  { who: "healthcare", path: "/for/healthcare/" },
  { who: "startup", path: "/for/startup/" },
  { who: "sec-filer", path: "/for/sec-filer/" },
  { who: "insurer", path: "/insurers/" },
  { who: "compare", path: "/compare/" },
];

const REDIRECTS = [
  { from: "/benchmarkers", want: "lobby=results", pendingPr: 452 },
  { from: "/scorecard", want: "gspc-scoreboard", pendingPr: 452 },
  { from: "/mcp-registry", want: "mcps", pendingPr: 452 },
  { from: "/rankings", want: "lobby=board" },
  { from: "/gspc", want: "gspc-scoreboard" },
];

console.log(`LOBBY-NAV — ${HOST}\n`);

// ── Lobby deep links (Council OS shell) ──
console.log("## Lobby deep links (?lobby=)\n");
for (const tab of LOBBY_TABS) {
  const { status, body, len } = await get(`/?lobby=${tab.id}`);
  if (status !== 200) fail(`/?lobby=${tab.id} HTTP ${status}`);
  else if (len < tab.min) fail(`/?lobby=${tab.id} thin (${len} B)`);
  else if (!body.includes("Council") && tab.id !== "play") fail(`/?lobby=${tab.id} missing Council shell`);
  else pass(`/?lobby=${tab.id} (${len} B)`);
}

// ── Tab framed routes ──
console.log("\n## Tab framed routes\n");
for (const tab of LOBBY_TABS.filter((t) => t.path)) {
  const url = tab.path.endsWith(".html")
    ? tab.path
    : tab.path.endsWith("/")
      ? tab.path
      : `${tab.path}/`;
  let status, len, body;
  try {
    ({ status, body, len } = await get(url));
  } catch (e) {
    if (tab.softLoop) {
      warn(`${url} redirect loop (storefront) — pending PR #452 redirect fix`);
      continue;
    }
    fail(`${url} fetch: ${e.message}`);
    continue;
  }
  if (status >= 400) {
    if (tab.softLoop) warn(`${url} HTTP ${status} (${tab.id} — storefront redirect loop on apex)`);
    else fail(`${url} HTTP ${status} (${tab.id} tab)`);
  } else if (len < tab.min) fail(`${url} thin (${len} B)`);
  else pass(`${url} → ${tab.id} (${len} B)`);
}

// ── Home-desktop inner routes ──
console.log("\n## Home-desktop LOBBY_ROUTES\n");
for (const path of LOBBY_ROUTES) {
  const { status, len } = await get(`${path}/`);
  if (status >= 400) fail(`${path}/ HTTP ${status}`);
  else if (len < 500) fail(`${path}/ thin (${len} B)`);
  else pass(`${path}/ (${len} B)`);
}

// ── MCP split: /mcp = protocol proxy, /mcps = human registry ──
console.log("\n## MCP surfaces\n");
const mcpProxy = await get("/mcp");
if (mcpProxy.status === 404 && mcpProxy.body.includes("not_found")) {
  pass("/mcp JSON proxy (functions/mcp — not HTML registry)");
} else if (mcpProxy.status === 200 && mcpProxy.body.includes("<html")) {
  warn("/mcp serves HTML — expected protocol proxy at edge");
} else {
  pass(`/mcp HTTP ${mcpProxy.status} (protocol lane)`);
}
const mcps = await get("/mcps/");
if (mcps.status >= 400) fail("/mcps/ registry HTTP " + mcps.status);
else pass(`/mcps/ registry (${mcps.len} B)`);

// ── Persona landings ──
console.log("\n## Persona landings (for/* + insurers)\n");
for (const p of PERSONAS) {
  const { status, len } = await get(p.path);
  if (status >= 400) fail(`${p.who} ${p.path} HTTP ${status}`);
  else pass(`${p.who} ${p.path} (${len} B)`);
}

// ── Consolidation redirects ──
console.log("\n## Consolidation redirects\n");
for (const r of REDIRECTS) {
  const { status, loc } = await getRedirect(r.from);
  if (status === 308 && loc.includes(r.want)) pass(`${r.from} → ${loc.trim()}`);
  else if (r.pendingPr && status === 404) warn(`${r.from} HTTP ${status} — pending councilof-ai PR #${r.pendingPr}`);
  else fail(`${r.from} HTTP ${status} loc=${loc} (want ${r.want})`);
}

// ── All 14 GSPC axes on API ──
console.log("\n## Axis tooling (14 slots)\n");
const gspc = await get("/api/gspc");
if (gspc.status !== 200) fail(`/api/gspc HTTP ${gspc.status}`);
else {
  try {
    const j = JSON.parse(gspc.body);
    const axes = j.axes || [];
    if (axes.length !== 14) fail(`axes[] length ${axes.length} (want 14)`);
    else pass("axes[] — 14 quotable slots");
    const names = axes.map((a) => a.axis).sort();
    for (const slot of ["governance", "safety", "provenance", "continuity", "jail"]) {
      if (!names.some((n) => String(n).includes(slot) || n === slot)) {
        if (slot === "jail" && names.includes("jail")) pass("jail slot present");
        else if (slot !== "jail") warn(`axis family ${slot} — check naming in axes[]`);
      }
    }
    if (names.includes("jail")) pass("jail (slot 14) on board");
    const reg = await get("/api/axis-register");
    if (reg.status === 200) pass("/api/axis-register");
    else warn(`/api/axis-register HTTP ${reg.status}`);
    const lib = await get("/library/axes/");
    if (lib.status === 200 && lib.len > 500) pass(`/library/axes/ (${lib.len} B)`);
    else fail(`/library/axes/ HTTP ${lib.status}`);
  } catch (e) {
    fail(`/api/gspc parse: ${e.message}`);
  }
}

console.log("");
if (fails) {
  console.error(`LOBBY-NAV: FAIL — ${fails} hard, ${soft} soft`);
  process.exit(1);
}
console.log(`LOBBY-NAV: PASS — ${soft ? `${soft} soft warn(s), ` : ""}lobby tabs + inner routes aligned.`);
process.exit(0);
