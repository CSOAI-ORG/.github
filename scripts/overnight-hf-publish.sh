#!/usr/bin/env bash
# scripts/overnight-hf-publish.sh — HF overnight publish (N5-01..N5-06)
# Requires: HF_TOKEN with write/admin on org csoai
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "FATAL: HF_TOKEN not set (N5-01 blocked)" >&2
  exit 1
fi

HF="${HF_CLI:-hf}"
command -v "$HF" >/dev/null 2>&1 || HF=huggingface-cli

echo "=== N5-01: HF auth ==="
"$HF" auth whoami

echo "=== N5-07: ClaimGuard gate (before public) ==="
bash "$ROOT/ops/claimguard-publish-gate.sh" "$ROOT/export"

create_and_upload() {
  local type="$1" repo="$2" src="$3"
  echo "→ $type/$repo"
  "$HF" repo create --type "$type" "$repo" 2>/dev/null || true
  "$HF" upload --repo-type "$type" "$repo" "$src" . \
    --commit-message "feat(overnight): N5 pack export from council-os"
}

echo "=== N5-02: csoai/gspc-board ==="
create_and_upload dataset csoai/gspc-board "$ROOT/export/gspc-board"

echo "=== N5-03: csoai/gspc-bench-results ==="
create_and_upload dataset csoai/gspc-bench-results "$ROOT/export/bench-results"

echo "=== N5-04: cards already in README.md ==="

echo "=== N5-06: governance leaderboard Space + results dataset ==="
create_and_upload dataset csoai/gspc-leaderboard-results "$ROOT/export/leaderboard-results"
"$HF" repo create --type space --space-sdk gradio csoai/gspc-governance-leaderboard 2>/dev/null || true
create_and_upload space csoai/gspc-governance-leaderboard "$ROOT/export/gspc-governance-leaderboard"
# Live Space was sdk=static; export README sets sdk=gradio — restart to pick up SDK change
"$HF" spaces restart csoai/gspc-governance-leaderboard 2>/dev/null || true

echo "=== N5-05: DOIs — mint manually in repo Settings after names confirmed ==="
echo "WARNING: DOI locks rename/delete/visibility permanently"

echo "=== Verify from outside ==="
for url in \
  "https://huggingface.co/datasets/csoai/gspc-board" \
  "https://huggingface.co/datasets/csoai/gspc-bench-results" \
  "https://huggingface.co/spaces/csoai/gspc-governance-leaderboard" \
  "https://huggingface.co/datasets/csoai/gspc-leaderboard-results"
do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$url → HTTP $code"
done

echo "HF overnight publish complete."
