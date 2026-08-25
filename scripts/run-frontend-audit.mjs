#!/usr/bin/env node
/**
 * run-frontend-audit.mjs — one-command live frontend audit for all end-user types.
 *
 * Runs from CSOAI-ORG/.github without needing a full councilof-ai clone.
 * Fetches public URLs on councilof.ai and checks persona + canon gates.
 *
 * Usage:
 *   node scripts/run-frontend-audit.mjs
 *   node scripts/run-frontend-audit.mjs --host https://councilof.ai
 *
 * Exit 1 if any gate fails.
 */

const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const HOST = (arg("host", "https://councilof.ai")).replace(/\/$/, "");
const UA = "CSOAI-frontend-audit/1.0";

const KILL = [/\bsovereign\b/i, /\bceasai\b/i, /\bbyzantine\b/i, /\bBFT\b/, /Watchdog certification/i, /33-Agent/i];

const PERSONAS = [
  { who: "visitor", path: "/", must: ["Council of AI", "We measure"] },
  { who: "buyer", path: "/pricing", must: ["free"] },
  // Honesty page discloses Elo as non-GSPC; literal "council-oowm" retired from copy.
  { who: "auditor", path: "/honesty", mustAny: ["Elo", "honesty", "MEASURED"] },
  { who: "researcher", path: "/library", mustAny: ["reference", "Library", "library"] },
  { who: "api-agent", path: "/api/gspc", must: ['"axes": 14', '"measured_axes": 14', "14 measured of 14"], json: true },
  { who: "a2a-agent", path: "/.well-known/agent-card.json", must: ['"doi"', "CSOAI Ltd"], json: true },
  { who: "regulator", path: "/regulators", must: [] },
  { who: "enterprise", path: "/start", must: [] },
];

const ROUTES = [
  { path: "/", minBytes: 20000, label: "homepage fat" },
  { path: "/gspc-scoreboard", minBytes: 50000, label: "living board" },
  { path: "/os/", status: 200 },
  { path: "/gspc-verify/", status: 200 },
  { path: "/lobby", status: 200 },
  // Moody's HTML scorecard lives on csoai-site; apex uses living board as scorecard.
  { path: "/gspc-scoreboard", status: 200, label: "scorecard stand-in (living board)" },
  { path: "/honesty", status: 200 },
  { path: "/library", status: 200 },
  { path: "/gspc", status: 200 },
  { path: "/verify", status: 200 },
  { path: "/pricing", status: 200 },
  { path: "/start", status: 200 },
  { path: "/api/health", status: 200 },
  { path: "/api/cards", status: 200 },
  { path: "/api/axis-register", status: 200 },
  { path: "/.well-known/mcp.json", status: 200 },
  { path: "/benchmarks/", status: 200, label: "Benchmarkers tab route" },
  { path: "/benchmark-index/", status: 200, label: "meta-benchmark index" },
  { path: "/mcps/", status: 200, label: "MCP registry UI" },
  { path: "/watchdog-map/", status: 200 },
  { path: "/library/axes/", status: 200, label: "14-axis library" },
  { path: "/for/regulator/", status: 200, label: "regulator persona" },
  { path: "/for/enterprise/", status: 200, label: "enterprise persona" },
];

let fails = 0;
const fail = (m) => { console.log(`  ✗ ${m}`); fails++; };
const pass = (m) => console.log(`  ✓ ${m}`);

async function fetchText(path) {
  const r = await fetch(`${HOST}${path}`, { headers: { "user-agent": UA }, redirect: "follow" });
  const body = await r.text();
  return { status: r.status, body, len: body.length };
}

console.log(`FRONTEND-AUDIT — ${HOST}\n`);

// ── Persona gauntlet ──
console.log("## Persona gauntlet (8 end-user types)\n");
for (const p of PERSONAS) {
  try {
    const { status, body } = await fetchText(p.path);
    if (status !== 200) { fail(`${p.who} ${p.path}: HTTP ${status}`); continue; }
    if (p.json) { try { JSON.parse(body); } catch { fail(`${p.who} ${p.path}: invalid JSON`); continue; } }
    const must = p.must || [];
    const mustAny = p.mustAny || [];
    const missing = must.filter((m) => !body.includes(m));
    if (missing.length) { fail(`${p.who} ${p.path}: missing ${JSON.stringify(missing)}`); continue; }
    if (mustAny.length && !mustAny.some((m) => body.includes(m))) {
      fail(`${p.who} ${p.path}: need any of ${JSON.stringify(mustAny)}`);
      continue;
    }
    const scan = p.json ? body : body.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ").replace(/<[^>]+>/g, " ");
    const killers = KILL.filter((re) => re.test(scan));
    if (killers.length) { fail(`${p.who} ${p.path}: kill-string ${killers.map(String).join(", ")}`); continue; }
    pass(`${p.who} ${p.path}`);
  } catch (e) {
    fail(`${p.who} ${p.path}: ${e.message}`);
  }
}

// ── Route inventory ──
console.log("\n## Route inventory\n");
for (const r of ROUTES) {
  try {
    const { status, body, len } = await fetchText(r.path);
    if (r.status && status !== r.status) { fail(`${r.path} HTTP ${status} (want ${r.status})`); continue; }
    if (r.minBytes && len < r.minBytes) { fail(`${r.path} ${len} bytes < ${r.minBytes} (${r.label})`); continue; }
    if (r.path === "/" && !body.includes("CouncilLobby")) { fail(`${r.path} missing CouncilLobby chunk`); continue; }
    pass(`${r.path} ${r.label || status}${r.minBytes ? ` (${len} bytes)` : ""}`);
  } catch (e) {
    fail(`${r.path}: ${e.message}`);
  }
}

// ── Canon API check ──
console.log("\n## Canon API\n");
try {
  const { status, body } = await fetchText("/api/gspc");
  if (status !== 200) { fail(`/api/gspc HTTP ${status}`); }
  else {
    const j = JSON.parse(body);
    if (j?.schema !== "csoai.gspc-axes/0.5") fail(`schema ${j?.schema}`);
    else pass(`schema csoai.gspc-axes/0.5`);
    if (j?.totals?.axes !== 14) fail(`totals.axes ${j?.totals?.axes}`);
    else pass(`totals.axes 14`);
    if (j?.totals?.measured_axes !== 14) fail(`totals.measured_axes ${j?.totals?.measured_axes}`);
    else pass(`totals.measured_axes 14`);
    if (!String(j?.totals?.public_count || "").includes("14 measured of 14")) fail(`public_count drift`);
    else pass(`public_count carries ruling`);
  }
} catch (e) {
  fail(`/api/gspc: ${e.message}`);
}

console.log("");
if (fails) {
  console.error(`FRONTEND-AUDIT: FAIL — ${fails} check(s). See docs/FRONTEND_AUDIT_CHECKLIST.md`);
  process.exit(1);
}
console.log("FRONTEND-AUDIT: PASS — all gates green.");
process.exit(0);
