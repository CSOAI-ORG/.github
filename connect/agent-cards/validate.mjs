#!/usr/bin/env node
/**
 * connect/agent-cards/validate.mjs — local A2A v1.0 card validator (N5-14).
 * Checks 8 required fields per a2a.proto v1.0.0.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const cardPath = process.argv[2] || join(__dir, "out/agent-card.json");
const card = JSON.parse(readFileSync(cardPath, "utf8"));

const REQUIRED = [
  "name", "description", "version", "capabilities",
  "supportedInterfaces", "defaultInputModes", "defaultOutputModes", "skills",
];
const BINDINGS = new Set(["JSONRPC", "GRPC", "HTTP+JSON"]);

const results = [];
function pass(msg) { results.push({ status: "PASS", msg }); }
function fail(msg) { results.push({ status: "FAIL", msg }); }

for (const f of REQUIRED) {
  if (card[f] === undefined) fail(`missing required field: ${f}`);
  else pass(`field present: ${f}`);
}

if (!Array.isArray(card.supportedInterfaces) || !card.supportedInterfaces.length) {
  fail("supportedInterfaces must be non-empty array");
} else {
  for (const [i, iface] of card.supportedInterfaces.entries()) {
    for (const k of ["url", "protocolBinding", "protocolVersion"]) {
      if (!iface[k]) fail(`supportedInterfaces[${i}] missing ${k}`);
    }
    if (iface.protocolBinding && !BINDINGS.has(iface.protocolBinding)) {
      fail(`supportedInterfaces[${i}] unknown protocolBinding: ${iface.protocolBinding}`);
    }
  }
  pass(`supportedInterfaces: ${card.supportedInterfaces.length} entry/entries`);
}

if (!Array.isArray(card.skills)) fail("skills must be array");
else {
  for (const [i, s] of card.skills.entries()) {
    if (!s.id || !s.name) fail(`skills[${i}] missing id or name`);
  }
  pass(`skills: ${card.skills.length} entry/entries`);
}

const outPath = join(__dir, "../../ops/logs/a2a-validator-local.json");
const report = {
  ts: new Date().toISOString(),
  card: cardPath,
  pass: results.filter((r) => r.status === "PASS").length,
  fail: results.filter((r) => r.status === "FAIL").length,
  results,
};
writeFileSync(outPath, JSON.stringify(report, null, 2) + "\n");

console.log(`A2A validator: ${report.pass} PASS, ${report.fail} FAIL`);
for (const r of results) console.log(`  [${r.status}] ${r.msg}`);
process.exit(report.fail ? 1 : 0);
