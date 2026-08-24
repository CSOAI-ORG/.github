#!/usr/bin/env bash
# upload-hf-patches.sh — idempotent HF upload for docs/hf-patches/**
#
# Uploads all 14 board-axis dataset READMEs from docs/hf-patches/axes/
# plus affect/jail Spaces from docs/hf-patches/spaces/.
#
# Requires: HF_TOKEN with write access to org csoai
#   export HF_TOKEN=hf_...
#   bash scripts/upload-hf-patches.sh
#
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PATCHES="$ROOT/docs/hf-patches"
AXES="$PATCHES/axes"

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "FATAL: HF_TOKEN not set. Export a write token for org csoai." >&2
  exit 1
fi

HF="${HF_CLI:-hf}"
command -v "$HF" >/dev/null 2>&1 || HF=huggingface-cli

upload_readme() {
  local dataset="$1"
  local file="$2"
  if [[ ! -f "$file" ]]; then
    echo "FATAL: missing card $file" >&2
    exit 1
  fi
  echo "→ datasets/csoai/$dataset README"
  "$HF" upload "csoai/$dataset" "$file" README.md --repo-type dataset \
    --commit-message "fix(card): axis README from .github hf-patches/axes"
}

# Canon order — docs/GSPC_AXIS_CANON.md (14 quotable board axes)
DATASETS=(
  gspc-gov
  gspc-agi
  gspc-prv
  gspc-asi
  gspc-mcp
  gspc-oss
  gspc-mach
  gspc-care
  gspc-xr
  gspc-det
  gspc-art5
  gspc-swarm
  gspc-affect
  gspc-jail
)

for dataset in "${DATASETS[@]}"; do
  upload_readme "$dataset" "$AXES/$dataset/README.md"
done

for space in gspc-affect gspc-jail; do
  SRC="$PATCHES/spaces/$space"
  if [[ -d "$SRC" ]]; then
    echo "→ spaces/csoai/$space"
    "$HF" upload "csoai/$space" "$SRC" . --repo-type space \
      --commit-message "feat(space): scaffold from .github hf-patches" || \
      echo "WARN: space $space upload failed (may need create via huggingface.co/new-space)"
  else
    echo "WARN: missing space scaffold $SRC"
  fi
done

echo "HF upload batch complete (14 axes + affect/jail spaces)."
