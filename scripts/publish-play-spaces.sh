#!/usr/bin/env bash
# Publish Games / City / Coliseum Gradio+MCP Spaces to org csoai.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLAY="$ROOT/docs/hf-patches/spaces/play"
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
  cp "$PLAY/mcp_client.py" "$PLAY/requirements.txt" "$stage/"
  echo "→ space/$repo from $src"
  "$HF" repos create "$repo" --type space --space-sdk gradio --exist-ok --public || true
  "$HF" upload "$repo" "$stage" . --repo-type space \
    --commit-message "feat(play): Gradio MCP door — Games/City/Coliseum"
  rm -rf "$stage"
}

publish_one "csoai/games-catalog" "$PLAY/games"
publish_one "csoai/council-city" "$PLAY/city"
publish_one "csoai/council-coliseum" "$PLAY/coliseum"

echo "Published. Add MCP badge clients at https://huggingface.co/settings/mcp"
echo "Directory: connect/mcp/hf-play-spaces.json"
