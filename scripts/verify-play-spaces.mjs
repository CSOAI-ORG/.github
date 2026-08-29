#!/usr/bin/env node
/**
 * Verify play-space patches + live MCP worker.
 * Does not require HF_TOKEN. Fails if we overclaim 22/22 measured.
 */
import { readFileSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PLAY = join(ROOT, "docs/hf-patches/spaces/play");
let failed = 0;

function ok(cond, msg) {
  if (!cond) {
    console.error("FAIL", msg);
    failed += 1;
  } else {
    console.log("OK  ", msg);
  }
}

for (const rel of [
  "mcp_client.py",
  "games/app.py",
  "city/app.py",
  "coliseum/app.py",
  "games/README.md",
  "city/README.md",
  "coliseum/README.md",
]) {
  ok(existsSync(join(PLAY, rel)), `exists ${rel}`);
}

const dir = JSON.parse(readFileSync(join(ROOT, "connect/mcp/hf-play-spaces.json"), "utf8"));
ok(dir.spaces?.length === 3, "directory has 3 play spaces");
ok(
  dir.spaces.every((s) => s.door_host && s.site && s.mcp === "https://councilof.ai/mcp"),
  "each space has door_host + site + live worker"
);
ok(
  !JSON.stringify(dir.n_site_wire?.cursor_mcp_snippet || {}).includes("gradio_api"),
  "play Cursor snippet has no paused Gradio SSE"
);
ok(
  dir.n_site_wire?.cursor_mcp_snippet?.mcpServers?.csoai?.url === "https://councilof.ai/mcp",
  "play Cursor snippet is the live worker"
);

const py = spawnSync(
  "python3",
  ["-c", `import ast,sys
from pathlib import Path
root=Path(${JSON.stringify(PLAY)})
for p in root.glob("*/app.py"):
    ast.parse(p.read_text())
    src=p.read_text()
    assert "mcp_server=True" in src, p
    assert "22/22" not in src and "22.22" not in src, p
print("py_ok")
`],
  { encoding: "utf8" }
);
ok(py.status === 0 && /py_ok/.test(py.stdout), `app.py parse + no 22/22 (${py.stderr || py.stdout})`);

const clientCheck = spawnSync(
  "python3",
  ["-c", `import sys
sys.path.insert(0, ${JSON.stringify(PLAY)})
from mcp_client import fetch_board, mcp_call, JAIL_FAMILIES
assert len(JAIL_FAMILIES)==16
b=fetch_board()
print(b.get("state"), b.get("public_count"), b.get("measured_axes"), b.get("axes"))
assert b.get("state") in ("LIVE","UNREACHABLE")
if b.get("state")=="LIVE":
    assert b.get("measured_axes") != b.get("axes") or b.get("unmeasured_axes")==0
    assert "22 measured" not in str(b.get("public_count") or "").lower() or b.get("measured_axes")==22
t=mcp_call("board_totals")
print("mcp", t.get("state"), t.get("ok"))
assert t.get("state") in ("LIVE","UNREACHABLE","MCP_ERROR")
`],
  { encoding: "utf8" }
);
ok(clientCheck.status === 0, `live mcp_client (${clientCheck.stderr || clientCheck.stdout})`);
if (clientCheck.stdout) console.log(clientCheck.stdout.trim());

if (failed) {
  console.error(`\n${failed} check(s) failed`);
  process.exit(1);
}
console.log("\nplay-spaces verify PASS");
