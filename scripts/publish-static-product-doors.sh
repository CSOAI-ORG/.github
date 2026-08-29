#!/usr/bin/env bash
# Publish product doors as STATIC Spaces (org csoai cpu-basic quota is 0,
# so Gradio Spaces pause and cannot start). Living board is fetched in-page.
# MCP rail remains https://councilof.ai/mcp.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CATALOG="$ROOT/connect/mcp/hf-product-spaces.json"
TPL="$ROOT/docs/hf-patches/spaces/static-doors/template.html"
HF="${HF_CLI:-hf}"
command -v "$HF" >/dev/null 2>&1 || HF=huggingface-cli

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "FATAL: HF_TOKEN unset" >&2
  exit 1
fi

python3 - "$CATALOG" "$TPL" <<'PY'
import json, os, sys, tempfile, subprocess, pathlib
catalog = json.loads(pathlib.Path(sys.argv[1]).read_text())
tpl = pathlib.Path(sys.argv[2]).read_text()
hf = os.environ.get("HF_CLI", "hf")
for row in catalog["spaces"]:
    repo = row["id"]
    title = repo.split("/", 1)[1]
    site = row["site"]
    tools = ", ".join(row.get("tools") or [])
    html = (tpl.replace("__TITLE__", title)
               .replace("__SITE__", site)
               .replace("__TOOLS__", tools or "board_totals"))
    desc = f"{title} door to Council OS. Living GET /api/gspc."[:60]
    readme = f"""---
title: {title}
emoji: 📗
colorFrom: yellow
colorTo: gray
sdk: static
pinned: false
license: cc-by-4.0
short_description: {desc}
---

# {title} — door

Live site: {site}

This Space is a **static door**. Org `csoai` has cpu-basic quota 0, so Gradio
Spaces cannot start. MCP from anywhere: [`https://councilof.ai/mcp`](https://councilof.ai/mcp).

Living counts: [GET /api/gspc](https://councilof.ai/api/gspc) — quote `totals.public_count`.
Measurement, not certification. CSOAI Ltd (UK 16939677).
"""
    stage = tempfile.mkdtemp()
    pathlib.Path(stage, "index.html").write_text(html, encoding="utf-8")
    pathlib.Path(stage, "README.md").write_text(readme, encoding="utf-8")
    print(f"→ static {repo}")
    # exist-ok create still counts against the daily Space-create cap — only create if missing.
    probe = subprocess.run(
        [hf, "spaces", "info", repo],
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        subprocess.run(
            [hf, "repos", "create", repo, "--type", "space", "--sdk", "static",
             "--public"],
            check=True,
        )
    subprocess.run(
        [hf, "upload", repo, stage, ".", "--repo-type", "space",
         "--commit-message", "feat(doors): live static door — org Gradio quota 0",
         "--delete", "app.py", "--delete", "mcp_client.py", "--delete", "door_kit.py",
         "--delete", "requirements.txt", "--delete", "catalog.json",
         "--delete", "style.css"],
        check=True,
    )
print("static doors published")
PY
echo "MCP rail remains https://councilof.ai/mcp"
