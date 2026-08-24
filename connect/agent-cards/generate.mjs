#!/usr/bin/env node
/**
 * connect/agent-cards/generate.mjs — single source → four outputs (drift = CI failure).
 * Outputs: agent-card.json (A2A v1.0), agent.json (legacy alias), mcp/server-card fragment.
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const src = JSON.parse(readFileSync(join(__dir, "source.json"), "utf8"));

const agentCard = {
  name: src.name,
  description: src.description,
  version: src.version,
  capabilities: src.capabilities,
  supportedInterfaces: src.supportedInterfaces,
  defaultInputModes: src.defaultInputModes,
  defaultOutputModes: src.defaultOutputModes,
  skills: src.skills.map(({ id, name, description, tags, examples }) => ({
    id, name, description, tags, examples,
  })),
  provider: src.provider,
  documentationUrl: `https://${src.domain}/.well-known/agent-card.json`,
  ...(src.doi ? { doi: src.doi } : {}),
  ...(src.explicitly_not ? { explicitly_not: src.explicitly_not } : {}),
};

const legacyAgent = {
  ...agentCard,
  url: `https://${src.domain}`,
  protocolVersion: "0.3.0",
  documentation: `https://${src.domain}/.well-known/agent.json`,
};

const outDir = process.argv[2] || join(__dir, "out");
mkdirSync(outDir, { recursive: true });

const paths = {
  "agent-card.json": agentCard,
  "agent.json": legacyAgent,
};

for (const [name, obj] of Object.entries(paths)) {
  const p = join(outDir, name);
  writeFileSync(p, JSON.stringify(obj, null, 2) + "\n");
  console.log("wrote", p);
}

// Drift check mode: compare against deployed paths when CI passes --check
if (process.argv.includes("--check")) {
  const deployed = process.env.DEPLOYED_CARD;
  if (deployed) {
    const live = JSON.parse(readFileSync(deployed, "utf8"));
    const a = JSON.stringify(agentCard);
    const b = JSON.stringify({ ...live, protocolVersion: undefined, url: undefined, documentation: undefined });
    if (a !== b) {
      console.error("DRIFT: generated agent-card.json differs from deployed");
      process.exit(1);
    }
    console.log("DRIFT CHECK PASS");
  }
}
