#!/usr/bin/env node
/**
 * Verify product-space patches + live MCP worker.
 * Does not require HF_TOKEN. Fails if we overclaim 22/22 measured.
 */
import { readFileSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PROD = join(ROOT, "docs/hf-patches/spaces/products");
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

const expected = [
  "council-os",
  "council-space",
  "claimguard",
  "gspc-verify",
  "ras-assess",
  "faq",
  "east-west",
  "mcp-fabric",
  "playground",
];

for (const name of expected) {
  ok(existsSync(join(PROD, name, "app.py")), `exists ${name}/app.py`);
  ok(existsSync(join(PROD, name, "README.md")), `exists ${name}/README.md`);
}
ok(existsSync(join(PROD, "door_kit.py")), "exists door_kit.py");
ok(existsSync(join(PLAY, "mcp_client.py")), "exists shared mcp_client.py");

const dir = JSON.parse(readFileSync(join(ROOT, "connect/mcp/hf-product-spaces.json"), "utf8"));
ok(dir.spaces?.length >= 12, `directory has ${dir.spaces?.length} spaces (>=12)`);
ok(
  dir.spaces.every((s) => s.mcp_sse && s.site && s.id),
  "each space has id + mcp_sse + site"
);
ok(
  dir.spaces.every((s) => s.id.startsWith("csoai/")),
  "all spaces under org csoai"
);
ok(!/all 22 measured/i.test(JSON.stringify(dir)), "catalog does not claim all-22-measured");

const py = spawnSync(
  "python3",
  [
    "-c",
    `import ast
from pathlib import Path
root=Path(${JSON.stringify(PROD)})
for p in root.glob("*/app.py"):
    ast.parse(p.read_text())
    src=p.read_text()
    assert "mcp_server=True" in src, p
    assert "22/22" not in src, p
    assert "elo league" not in src.lower() or "not" in src.lower(), p
print("py_ok", len(list(root.glob("*/app.py"))))
`,
  ],
  { encoding: "utf8" }
);
ok(py.status === 0 && /py_ok/.test(py.stdout), `app.py parse + no 22/22 (${py.stderr || py.stdout})`);
if (py.stdout) console.log(py.stdout.trim());

const clientCheck = spawnSync(
  "python3",
  [
    "-c",
    `import sys
sys.path.insert(0, ${JSON.stringify(PLAY)})
from mcp_client import check_claim, fetch_board, load_fabric, mcp_call, mcp_tools_list, SITES
assert SITES["os"].startswith("https://councilof.ai")
assert SITES["faq"].endswith("/faq/")
assert SITES["east_west"].endswith("/east-west/")
b=fetch_board()
print("board", b.get("state"), b.get("public_count"))
assert b.get("state") in ("LIVE","UNREACHABLE")
if b.get("state")=="LIVE":
    bad=check_claim("all 22 measured")
    assert bad["ok"] is False and bad["findings"], bad
    bad16=check_claim("we have 16 measured axes")
    assert bad16["ok"] is False, bad16
    live=f"{b['measured_axes']} measured"
    good=check_claim(live)
    assert good["ok"] is True, good
    elo=check_claim("public Elo league")
    assert elo["ok"] is False, elo
fab=load_fabric()
print("fabric", fab.get("schema"), "spaces", len(fab.get("spaces") or []))
assert fab.get("schema")=="csoai.hf-product-spaces/1"
assert len(fab.get("spaces") or [])>=12
t=mcp_tools_list()
print("tools", t.get("state"), t.get("names"))
assert t.get("state") in ("LIVE","UNREACHABLE","MCP_ERROR")
if t.get("state")=="LIVE":
    assert "board_totals" in (t.get("names") or [])
    assert "verify_card" in (t.get("names") or [])
m=mcp_call("board_totals")
print("mcp", m.get("state"), m.get("ok"))
`,
  ],
  { encoding: "utf8" }
);
ok(clientCheck.status === 0, `live product mcp_client (${clientCheck.stderr || clientCheck.stdout})`);
if (clientCheck.stdout) console.log(clientCheck.stdout.trim());

if (failed) {
  console.error(`\n${failed} check(s) failed`);
  process.exit(1);
}
console.log("\nproduct-spaces verify PASS");
