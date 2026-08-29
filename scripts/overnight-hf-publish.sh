#!/usr/bin/env bash
# scripts/overnight-hf-publish.sh — HF overnight publish (N5-01..N5-06)
# Auth: HF_TOKEN secret OR GitHub Actions Trusted Publishers OIDC (HF_OIDC_RESOURCE per repo).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

HF="${HF_CLI:-hf}"
command -v "$HF" >/dev/null 2>&1 || HF=huggingface-cli

USE_OIDC=0
if [[ -z "${HF_TOKEN:-}" ]]; then
  if [[ -n "${GITHUB_ACTIONS:-}" ]]; then
    USE_OIDC=1
    echo "HF_TOKEN unset — using Trusted Publishers OIDC (per-repo HF_OIDC_RESOURCE)"
  else
    echo "FATAL: HF_TOKEN not set and not in GitHub Actions (N5-01 blocked)" >&2
    exit 1
  fi
fi

oidc_resource_for() {
  local type="$1" repo="$2"
  case "$type" in
    dataset) echo "datasets/$repo" ;;
    space) echo "spaces/$repo" ;;
    model) echo "$repo" ;;
    *) echo "$repo" ;;
  esac
}

refresh_hf_token() {
  local type="$1" repo="$2"
  if [[ "$USE_OIDC" == "1" ]]; then
    export HF_OIDC_RESOURCE
    HF_OIDC_RESOURCE="$(oidc_resource_for "$type" "$repo")"
    HF_TOKEN="$("$HF" auth token)"
    export HF_TOKEN
  fi
}

echo "=== N5-01: HF auth ==="
refresh_hf_token dataset csoai/gspc-board
"$HF" auth whoami

echo "=== N5-07: ClaimGuard gate (before public) ==="
bash "$ROOT/ops/claimguard-publish-gate.sh" "$ROOT/export"

create_and_upload() {
  local type="$1" repo="$2" src="$3"
  refresh_hf_token "$type" "$repo"
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
refresh_hf_token space csoai/gspc-governance-leaderboard
"$HF" repo create --type space --space-sdk gradio csoai/gspc-governance-leaderboard 2>/dev/null || true
create_and_upload space csoai/gspc-governance-leaderboard "$ROOT/export/gspc-governance-leaderboard"
# Live Space was sdk=static; export README sets sdk=gradio — restart to pick up SDK change
"$HF" spaces restart csoai/gspc-governance-leaderboard 2>/dev/null || true

echo "=== Product doors on Hub (static — org cpu-basic quota is 0) ==="
if [[ -n "${HF_TOKEN:-}" ]]; then
  bash "$ROOT/scripts/publish-static-product-doors.sh" || echo "WARN: static door publish failed (non-fatal for overnight board pack)"
else
  echo "HF_TOKEN unset — skip product-space publish"
fi

echo "=== N5-05: DOIs — mint manually in repo Settings after names confirmed ==="
echo "WARNING: DOI locks rename/delete/visibility permanently"

echo "=== Verify from outside ==="
VERIFY_LOG="$ROOT/ops/logs/hf-publish-verify-$(date -u +%Y%m%dT%H%M%SZ).log"
{
  for url in \
    "https://huggingface.co/datasets/csoai/gspc-board" \
    "https://huggingface.co/datasets/csoai/gspc-bench-results" \
    "https://huggingface.co/spaces/csoai/gspc-governance-leaderboard" \
    "https://huggingface.co/datasets/csoai/gspc-leaderboard-results"
  do
    code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    echo "$url → HTTP $code"
  done
  sdk=$(curl -s "https://huggingface.co/api/spaces/csoai/gspc-governance-leaderboard" | python3 -c "import sys,json; print(json.load(sys.stdin).get('sdk','?'))" 2>/dev/null || echo "?")
  echo "Space sdk=$sdk (expected gradio)"
  if curl -s "https://huggingface.co/datasets/csoai/gspc-board/README.md" | grep -qi eunomia; then
    echo "WARN: gspc-board README still contains EUNOMIA — re-check card refresh"
  else
    echo "OK: gspc-board README free of EUNOMIA branding"
  fi
} | tee "$VERIFY_LOG"

echo "HF overnight publish complete. Verify log: $VERIFY_LOG"
