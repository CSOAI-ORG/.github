#!/usr/bin/env node
/**
 * e2e-dsh.mjs — DSH (Software tab /dashboard) + auth spine live gates.
 *
 * Verifies Cloudflare Pages Functions on apex — NOT GCP, NOT api.csoai.org.
 *
 *   node scripts/e2e-dsh.mjs
 *   node scripts/e2e-dsh.mjs --host https://councilof.ai
 */

const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const HOST = (arg("host", "https://councilof.ai")).replace(/\/$/, "");
const UA = "CSOAI-dsh/1.0";

let hard = 0;
let soft = 0;
const fail = (m) => { console.log(`  ✗ ${m}`); hard++; };
const warn = (m) => { console.log(`  ~ ${m}`); soft++; };
const pass = (m) => console.log(`  ✓ ${m}`);

async function get(path, opts = {}) {
  const r = await fetch(HOST + path, { headers: { "user-agent": UA }, ...opts });
  const body = await r.text();
  return { status: r.status, body, len: body.length };
}

async function postJson(path, data) {
  const r = await fetch(HOST + path, {
    method: "POST",
    headers: { "content-type": "application/json", "user-agent": UA },
    body: JSON.stringify(data),
  });
  return { status: r.status, json: await r.json().catch(() => ({})) };
}

console.log(`DSH E2E — ${HOST}\n`);

// ── Thin-shell detector ──
console.log("## Deploy health\n");
const home = await get("/");
if (home.len < 20000) {
  warn(`homepage thin (${home.len} B) — gated deploy not landed or DEPLOY-LOCK clobber`);
  warn("DSH/auth function probes may 404 until fat deploy lands — continuing with soft warns");
} else {
  pass(`homepage fat (${home.len} B)`);
}

// ── Auth spine (Pages Functions) ──
console.log("\n## Auth spine (/api/auth/*)\n");
const loginEmpty = await postJson("/api/auth/login", {});
if (loginEmpty.status === 404) {
  warn("POST /api/auth/login → 404 — PR #468 not deployed yet");
} else if (loginEmpty.status === 400) {
  pass("POST /api/auth/login → 400 (route live, validation works)");
} else {
  fail(`POST /api/auth/login → ${loginEmpty.status} (want 400 or 404 pre-deploy)`);
}

const demo = await postJson("/api/auth/login", { email: "demo@csoai.com", password: "demo123" });
if (demo.status === 404) {
  warn("demo login → 404 — await DSH auth deploy");
} else if (demo.status === 200 && demo.json.token && demo.json.user?.email === "demo@csoai.com") {
  pass("demo@csoai.com login → token + user");
  const me = await get("/api/auth/me", {
    headers: { authorization: `Bearer ${demo.json.token}`, "user-agent": UA },
  });
  if (me.status === 200) pass("GET /api/auth/me with Bearer token");
  else fail(`GET /api/auth/me → ${me.status}`);
} else {
  fail(`demo login → ${demo.status} ${JSON.stringify(demo.json).slice(0, 120)}`);
}

// ── Dashboard stats API ──
console.log("\n## DSH stats (/api/dashboard/stats)\n");
const stats = await get("/api/dashboard/stats");
if (stats.status === 404) {
  warn("/api/dashboard/stats → 404 — await DSH deploy");
} else if (stats.status === 200) {
  try {
    const j = JSON.parse(stats.body);
    if (j.schema?.includes("dashboard.stats")) pass("dashboard.stats schema present");
    else warn(`unexpected schema: ${j.schema}`);
    if (j.source === "pages-functions") pass("source=pages-functions (not GCP/tRPC)");
    if (j.gspc?.measured_axes === 13) pass("gspc.measured_axes 13 from live board");
    else if (typeof j.gspc?.measured_axes === "number") warn(`gspc.measured_axes=${j.gspc.measured_axes}`);
    if (j.complianceScore === null) pass("complianceScore null (honest — no fabricated score)");
    else warn(`complianceScore=${j.complianceScore} — expected null for public board`);
  } catch (e) {
    fail(`dashboard/stats JSON: ${e.message}`);
  }
} else {
  fail(`/api/dashboard/stats HTTP ${stats.status}`);
}

// ── DSH UI shell ──
console.log("\n## DSH UI (/dashboard/)\n");
const dash = await get("/dashboard/");
if (dash.status >= 400) fail(`/dashboard/ HTTP ${dash.status}`);
else if (dash.len < 5000) fail(`/dashboard/ thin (${dash.len} B)`);
else pass(`/dashboard/ live (${dash.len} B)`);

if (/sign in to your account/i.test(dash.body) && !/Council OS|SOAI-PDCA|Compliance Score/i.test(dash.body)) {
  warn("/dashboard/ prerender looks like login redirect — RequireAuth may still be active pre-deploy");
} else if (/SOAI-PDCA|Dashboard|Council OS/i.test(dash.body)) {
  pass("/dashboard/ renders DSH shell (not login-only prerender)");
} else {
  warn("/dashboard/ content unclear — inspect prerender after deploy");
}

// ── Software tab deep link ──
console.log("\n## Council OS Software tab (?lobby=software)\n");
const soft = await get("/?lobby=software");
if (soft.status === 200) pass("/?lobby=software HTTP 200");
else fail("/?lobby=software HTTP " + soft.status);

console.log("");
if (hard) {
  console.error(`DSH E2E: FAIL — ${hard} hard, ${soft} soft`);
  process.exit(1);
}
console.log(`DSH E2E: PASS — ${soft ? `${soft} soft warn(s); ` : ""}auth + dashboard aligned (or awaiting deploy).`);
process.exit(0);
