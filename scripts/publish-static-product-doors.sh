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
import json, os, sys, pathlib, urllib.error, urllib.request
from huggingface_hub import CommitOperationAdd, HfApi

catalog = json.loads(pathlib.Path(sys.argv[1]).read_text())
tpl = pathlib.Path(sys.argv[2]).read_text()
token = os.environ.get("HF_TOKEN")
api = HfApi(token=token)

def space_exists(repo: str) -> bool:
    try:
        req = urllib.request.Request(
            f"https://huggingface.co/api/spaces/{repo}",
            headers={"User-Agent": "CSOAI-publish/1.0"},
        )
        with urllib.request.urlopen(req, timeout=20):
            return True
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 401):
            return False
        raise

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
    print(f"→ static {repo}", flush=True)
    if not space_exists(repo):
        print(f"SKIP create {repo}: daily Space-create cap; create tomorrow if still missing", flush=True)
        continue
    # create_commit does not call /api/repos/create (hf upload does, and that is capped).
    api.create_commit(
        repo_id=repo,
        repo_type="space",
        operations=[
            CommitOperationAdd(path_in_repo="index.html", path_or_fileobj=html.encode()),
            CommitOperationAdd(path_in_repo="README.md", path_or_fileobj=readme.encode()),
        ],
        commit_message="feat(doors): live static door — org Gradio quota 0",
    )
print("static doors published")
PY
echo "MCP rail remains https://councilof.ai/mcp"
