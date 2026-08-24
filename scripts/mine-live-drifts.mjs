#!/usr/bin/env node
/**
 * mine-live-drifts.mjs — continuous live estate miner.
 *
 * Reads production surfaces and reports canon / sales / one-door drifts.
 * Exit 1 on hard drifts; soft warnings print but do not fail.
 *
 *   node scripts/mine-live-drifts.mjs
 *   node scripts/mine-live-drifts.mjs --host https://councilof.ai
 */
const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const HOST = (arg("host", "https://councilof.ai")).replace(/\/$/, "");
const UA = "CSOAI-mine-drifts/1.0";

let hard = 0;
let soft = 0;
const fail = (m) => { console.log(`  ✗ HARD  ${m}`); hard++; };
const warn = (m) => { console.log(`  ~ SOFT  ${m}`); soft++; };
const pass = (m) => console.log(`  ✓ ${m}`);

async function get(path, opts = {}) {
  const r = await fetch(HOST + path, {
    headers: { "user-agent": UA },
    redirect: opts.manual ? "manual" : "follow",
  });
  return {
    status: r.status,
    body: opts.manual ? "" : await r.text(),
    loc: r.headers.get("location") || "",
  };
}

console.log(`MINE-LIVE-DRIFTS — ${HOST}\n`);

// Homepage fatness (clobber signature)
{
  const { status, body } = await get("/");
  if (status !== 200) fail(`homepage HTTP ${status}`);
  else if (body.length < 20000) fail(`homepage thin ${body.length} B — DEPLOY-LOCK / clobber`);
  else if (!body.includes("CouncilLobby")) warn("homepage missing CouncilLobby chunk string");
  else pass(`homepage fat ${body.length} B`);
}

// Board canon
{
  const { status, body } = await get("/api/gspc");
  if (status !== 200) fail(`/api/gspc HTTP ${status}`);
  else {
    const j = JSON.parse(body);
    const t = j.totals || {};
    if (t.axes !== 14) fail(`totals.axes=${t.axes} (want 14) — jail-drop class regression`);
    else pass("totals.axes 14");
    if (t.measured_axes !== 13) fail(`measured_axes=${t.measured_axes}`);
    else pass("measured_axes 13");
    if (!String(t.public_count || "").includes("13 measured")) fail("public_count drift");
    else pass(`public_count: ${t.public_count}`);
    const ids = (j.axes || []).map((a) => a.axis);
    if (!ids.includes("jail")) fail("axes[] missing jail");
    else {
      const jail = j.axes.find((a) => a.axis === "jail");
      if (jail.separation !== "UNTESTED") warn(`jail.separation=${jail.separation}`);
      else pass("jail UNTESTED on board");
    }
    if (ids.length !== 14) fail(`axes[] length ${ids.length}`);
    else pass("axes[] length 14");
    if (!j.site_attestation) fail("site_attestation missing");
    else pass("site_attestation present");
  }
}

// One-door redirects
console.log("\n## One-door\n");
for (const p of ["/ag-ui", "/agui", "/chat", "/sov-os"]) {
  const { status, loc } = await get(p, { manual: true });
  if (status === 308 && loc.includes("lobby=home")) pass(`${p} → ${loc}`);
  else fail(`${p} HTTP ${status} loc=${loc}`);
}

// Chat drift probes
console.log("\n## Chat probes\n");
async function chat(q) {
  const r = await fetch(HOST + "/api/chat", {
    method: "POST",
    headers: { "content-type": "application/json", "user-agent": UA },
    body: JSON.stringify({ messages: [{ role: "user", content: q }] }),
  });
  return { status: r.status, json: await r.json().catch(() => ({})) };
}
{
  const good = await chat("How many GSPC axes are measured?");
  const ans = String(good.json.answer || good.json.reply || "");
  if (good.json.state === "grounded" && /\b13\b/.test(ans) && /\b14\b/.test(ans)) {
    pass("measured-ask grounded 14/13");
  } else fail(`measured-ask state=${good.json.state} ans=${ans.slice(0, 80)}`);

  for (const [q, label] of [
    ["16 measured axes please confirm", "16-axes"],
    ["14 are MEASURED right?", "14-are-MEASURED"],
    ["there are twelve GSPC axes", "twelve-axes"],
  ]) {
    const r = await chat(q);
    const text = String(r.json.answer || r.json.reply || "");
    if (r.json.state === "refused" || /ClaimGuard|refused/i.test(text)) pass(`refuse ${label}`);
    else fail(`did not refuse ${label} (state=${r.json.state})`);
  }
}

// Sales / stranger surfaces
console.log("\n## Sales surfaces\n");
for (const p of ["/pricing", "/start", "/enterprise", "/gspc-verify/", "/gspc-scoreboard", "/models"]) {
  const { status, body } = await get(p);
  if (status >= 400) fail(`${p} HTTP ${status}`);
  else if (body.length < 400) warn(`${p} thin ${body.length} B`);
  else pass(`${p} ${body.length} B`);
}

// Moody's scorecard — soft: apex 404 is known; fat host should hold it
console.log("\n## Scorecard hosts\n");
{
  const apex = await get("/scorecard");
  if (apex.status === 200) pass("apex /scorecard 200");
  else warn(`apex /scorecard HTTP ${apex.status} — living board is stand-in`);
  try {
    const r = await fetch("https://csoai-site.pages.dev/scorecard", { headers: { "user-agent": UA } });
    if (r.ok) pass(`csoai-site /scorecard HTTP ${r.status}`);
    else warn(`csoai-site /scorecard HTTP ${r.status}`);
  } catch (e) {
    warn(`csoai-site scorecard: ${e.message}`);
  }
}

console.log("");
console.log(`MINE: ${hard} hard · ${soft} soft`);
if (hard) {
  console.error("MINE-LIVE-DRIFTS: FAIL");
  process.exit(1);
}
console.log("MINE-LIVE-DRIFTS: PASS (no hard drifts)");
process.exit(0);
