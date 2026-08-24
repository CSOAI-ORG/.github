#!/usr/bin/env node
/**
 * ops/banned-strings — CI gate for codenames that must never appear on public surfaces.
 * Usage: node ops/banned-strings.mjs [paths...]
 * Exit 0 = clean; exit 1 = hits found.
 */
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, extname } from "node:path";

const BANNED = [
  { label: "cibola", re: /\bcibola\b/i },
  { label: "dorado", re: /\bdorado\b/i },
  { label: "sovos", re: /\bsovos\b/i },
  { label: "MEOK-internal", re: /MEOK-internal/i },
];

const TEXT_EXT = new Set([
  ".md", ".txt", ".json", ".yaml", ".yml", ".html", ".ts", ".tsx",
  ".js", ".mjs", ".py", ".sh", ".csv", ".toml",
]);

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) {
      if (name === "node_modules" || name === ".git") continue;
      walk(p, out);
    } else if (TEXT_EXT.has(extname(name))) {
      out.push(p);
    }
  }
  return out;
}

const roots = process.argv.slice(2);
if (!roots.length) {
  console.error("Usage: node ops/banned-strings.mjs <path> [path...]");
  process.exit(2);
}

let hits = 0;
for (const root of roots) {
  const files = statSync(root).isDirectory() ? walk(root) : [root];
  for (const file of files) {
    const text = readFileSync(file, "utf8");
    for (const { label, re } of BANNED) {
      const m = text.match(re);
      if (m) {
        const line = text.slice(0, m.index).split("\n").length;
        console.error(`BANNED [${label}] ${file}:${line}: ${m[0]}`);
        hits++;
      }
    }
  }
}

if (hits) {
  console.error(`\nFAIL: ${hits} banned-string hit(s)`);
  process.exit(1);
}
console.log("PASS: zero banned-string hits");
process.exit(0);
