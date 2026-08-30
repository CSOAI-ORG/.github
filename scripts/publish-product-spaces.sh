#!/usr/bin/env bash
# Publish every product Gradio+MCP Space to org csoai.
# Spaces are doors: they proxy https://councilof.ai/mcp and deep-link Council OS.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLAY="$ROOT/docs/hf-patches/spaces/play"
PROD="$ROOT/docs/hf-patches/spaces/products"
CATALOG="$ROOT/connect/mcp/hf-product-spaces.json"
HF="${HF_CLI:-hf}"
command -v "$HF" >/dev/null 2>&1 || HF=huggingface-cli

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "FATAL: HF_TOKEN unset — cannot create/update Spaces" >&2
  exit 1
fi

publish_one() {
  local repo="$1" src="$2"
  local stage
  stage="$(mktemp -d)"
  cp "$src/app.py" "$src/README.md" "$stage/"
  cp "$PLAY/mcp_client.py" "$PROD/door_kit.py" "$PROD/requirements.txt" "$CATALOG" "$stage/"
  cp "$CATALOG" "$stage/catalog.json"
  echo "→ space/$repo from $src"
  "$HF" repos create "$repo" --type space --space-sdk gradio --exist-ok --public || true
  "$HF" upload "$repo" "$stage" . --repo-type space \
    --commit-message "feat(products): Gradio MCP door — Council OS fabric"
  rm -rf "$stage"
}

publish_one "csoai/council-os" "$PROD/council-os"
publish_one "csoai/council-space" "$PROD/council-space"
publish_one "csoai/claimguard" "$PROD/claimguard"
publish_one "csoai/gspc-verify" "$PROD/gspc-verify"
publish_one "csoai/ras-assess" "$PROD/ras-assess"
publish_one "csoai/faq" "$PROD/faq"
publish_one "csoai/east-west" "$PROD/east-west"
publish_one "csoai/mcp-fabric" "$PROD/mcp-fabric"
publish_one "csoai/council-mcp-playground" "$PROD/playground"

echo "Published product fabric. Add MCP badge clients at https://huggingface.co/settings/mcp"
echo "Directory: connect/mcp/hf-product-spaces.json"
echo "Also run: bash scripts/publish-play-spaces.sh   # games / city / coliseum"
