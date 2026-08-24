#!/usr/bin/env node
/**
 * weekend-demo-smoke.mjs — sales-demo readiness gate (ask → board → verify → arena stack).
 *
 * Hits the four demo critical paths on councilof.ai and prints PASS/FAIL.
 *
 *   node scripts/weekend-demo-smoke.mjs
 *   node scripts/weekend-demo-smoke.mjs --host https://councilof.ai
 *
 * Exit 0 only when all required checks pass.
 */

const arg = (k, d) => {
  const i = process.argv.indexOf("--" + k);
  return i > 0 ? process.argv[i + 1] : d;
};
const HOST = (arg("host", "https://councilof.ai")).replace(/\/$/, "");
const UA = "CSOAI-weekend-demo-smoke/1.0";

const MCP_TOOLS = ["measure", "verify", "jail-probe", "enter-arena"];

let fails = 0;
const rows = [];
const pass = (id, detail) => rows.push({ id, ok: true, detail });
const fail = (id, detail) => {
  rows.push({ id, ok: false, detail });
  fails++;
};

async function get(path) {
  const r = await fetch(HOST + path, { headers: { "user-agent": UA }, redirect: "follow" });
  return { status: r.status, body: await r.text(), headers: r.headers };
}

async function postChat(content) {
  const r = await fetch(HOST + "/api/chat", {
    method: "POST",
    headers: { "content-type": "application/json", "user-agent": UA },
    body: JSON.stringify({ messages: [{ role: "user", content }] }),
  });
  const json = await r.json().catch(() => ({}));
  return { status: r.status, json };
}

console.log(`WEEKEND-DEMO-SMOKE — ${HOST}\n`);

// ── 1. Living board API ──
{
  const { status, body } = await get("/api/gspc");
  if (status !== 200) fail("api.gspc", `HTTP ${status}`);
  else {
    try {
      const j = JSON.parse(body);
      const axes = j.totals?.axes;
      const measured = j.totals?.measured_axes;
      const publicCount = String(j.totals?.public_count || "");
      if (axes !== 14) fail("api.gspc.axes", `totals.axes=${axes} (want 14)`);
      else pass("api.gspc.axes", "14 quotable slots");
      if (measured !== 13) fail("api.gspc.measured", `measured_axes=${measured} (want 13)`);
      else pass("api.gspc.measured", "13 measured of 14");
      if (!publicCount.includes("13 measured")) {
        fail("api.gspc.public_count", `public_count=${JSON.stringify(publicCount)}`);
      } else pass("api.gspc.public_count", publicCount);
      if (!j.site_attestation) fail("api.gspc.attestation", "missing site_attestation");
      else pass("api.gspc.attestation", "site_attestation present");
      if (!Array.isArray(j.axes) || j.axes.length !== 14) {
        fail("api.gspc.rows", `axes[] length ${j.axes?.length}`);
      } else pass("api.gspc.rows", "axes[] length 14");
    } catch (e) {
      fail("api.gspc", `invalid JSON: ${e.message}`);
    }
  }
}

// ── 2. Verify surface (trailing slash) ──
{
  const { status, body } = await get("/gspc-verify/");
  if (status !== 200) fail("gspc-verify", `HTTP ${status}`);
  else if (body.length < 500) fail("gspc-verify", `thin body (${body.length} B)`);
  else pass("gspc-verify", `HTTP 200 · ${body.length} B`);
}

// ── 3. Lobby axis ask via POST /api/chat ──
{
  const ask = "How many GSPC axes are on the public board?";
  const { status, json } = await postChat(ask);
  const text = String(json.answer || json.reply || json.message?.content || "");
  if (status !== 200) fail("api.chat", `HTTP ${status}`);
  else if (!text) fail("api.chat", "empty answer");
  else if (json.state === "ungrounded" || json.state === "refused") {
    fail("api.chat.state", `state=${json.state}`);
  } else {
    pass("api.chat", `HTTP 200 · state=${json.state || "n/a"}`);
    // Negation-safe: "Never 14 are MEASURED" must not trip the overclaim gate.
    const plain = text.replace(/[*_`#]/g, " ").replace(/\s+/g, " ");
    const negated = (re) => {
      const m = plain.match(re);
      if (!m) return false;
      const idx = m.index ?? 0;
      const before = plain.slice(Math.max(0, idx - 24), idx).toLowerCase();
      return !/\b(never|not|no|don't|do not|instead of)\b[\s\S]*$/i.test(before);
    };
    const overclaims = [
      [/\b16\s+(measured\s+)?axes?\b/i, "16-axes overclaim"],
      [/\b15\s+(measured\s+)?axes?\b/i, "15-axes overclaim"],
      [/\b14\s+are\s+MEASURED\b/i, "claims 14 MEASURED (board ruling is 13 of 14)"],
      [/\ball\s+14\s+(axes?\s+)?(are\s+)?MEASURED\b/i, "claims all 14 measured"],
      [/\bElo\b/i, "Elo as board language"],
      [/\bcertif(y|ied|ication)\b/i, "certification language"],
    ];
    const hits = overclaims.filter(([re]) => negated(re)).map(([, label]) => label);
    if (hits.length) fail("api.chat.canon", hits.join("; "));
    else if (!/\b14\b/.test(plain)) fail("api.chat.canon", "answer missing 14-slot language");
    else if (!/\b13\b/.test(plain) && !/13 measured/i.test(plain)) {
      fail("api.chat.canon", "answer missing 13-measured ruling language");
    } else pass("api.chat.canon", "no overclaim vs 14/13 ruling");
  }
}

// ── 4. MCP catalogue ──
{
  const { status, body } = await get("/.well-known/mcp.json");
  if (status !== 200) fail("mcp.json", `HTTP ${status}`);
  else {
    try {
      const j = JSON.parse(body);
      const tools = j.measured?.tools || [];
      for (const t of MCP_TOOLS) {
        if (!tools.includes(t) && !body.includes(t)) fail(`mcp.${t}`, "missing");
        else pass(`mcp.${t}`, "listed");
      }
    } catch {
      for (const t of MCP_TOOLS) {
        if (!body.includes(t)) fail(`mcp.${t}`, "missing");
        else pass(`mcp.${t}`, "listed");
      }
    }
  }
}

// ── Report ──
console.log("## Checks\n");
for (const r of rows) {
  console.log(`  ${r.ok ? "PASS" : "FAIL"}  ${r.id} — ${r.detail}`);
}

const requiredFail = fails;
console.log("");
if (requiredFail === 0) {
  console.log("SALES-DEMO READINESS: PASS");
  console.log("Arc ready: ask → board (/api/gspc) → verify → MCP tools.");
  process.exit(0);
} else {
  console.log(`SALES-DEMO READINESS: FAIL (${requiredFail} check${requiredFail === 1 ? "" : "s"})`);
  console.log("See docs/WEEKEND_DEMO.md · docs/REVENUE_SURFACES.md · docs/patches/councilof-ai-claimguard-chat/");
  process.exit(1);
}
