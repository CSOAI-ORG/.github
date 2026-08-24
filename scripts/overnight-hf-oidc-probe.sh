#!/usr/bin/env bash
# scripts/overnight-hf-oidc-probe.sh — test HF Trusted Publishers OIDC per repo (N5-01)
# Run inside GitHub Actions after configuring publishers on each HF repo.
set -euo pipefail

HF="${HF_CLI:-hf}"
command -v "$HF" >/dev/null 2>&1 || HF=huggingface-cli

if [[ -z "${GITHUB_ACTIONS:-}" ]]; then
  echo "FATAL: OIDC probe only runs in GitHub Actions" >&2
  exit 1
fi

RESOURCES=(
  datasets/csoai/gspc-board
  datasets/csoai/gspc-bench-results
  datasets/csoai/gspc-leaderboard-results
  spaces/csoai/gspc-governance-leaderboard
)

FAIL=0
echo "=== HF Trusted Publishers OIDC probe $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

for resource in "${RESOURCES[@]}"; do
  echo "--- $resource ---"
  if token=$(HF_OIDC_RESOURCE="$resource" "$HF" auth token 2>/dev/null); then
    if HF_TOKEN="$token" "$HF" auth whoami >/dev/null 2>&1; then
      echo "  [PASS] OIDC exchange + whoami"
    else
      echo "  [FAIL] token exchanged but whoami failed"
      FAIL=1
    fi
  else
    echo "  [FAIL] OIDC exchange failed (publisher not configured or claims mismatch)"
    FAIL=1
  fi
done

if [[ "$FAIL" -eq 0 ]]; then
  echo "PROBE PASS — all ${#RESOURCES[@]} resources authenticated"
else
  echo "PROBE FAIL — fix Trusted Publishers on failing repos"
fi
exit "$FAIL"
