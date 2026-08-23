#!/usr/bin/env bash
# upload-hf-patches.sh — idempotent HF upload for docs/hf-patches/**
#
# Requires: HF_TOKEN with write access to org csoai
#   export HF_TOKEN=hf_...
#   bash scripts/upload-hf-patches.sh
#
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PATCHES="$ROOT/docs/hf-patches"

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "FATAL: HF_TOKEN not set. Export a write token for org csoai." >&2
  exit 1
fi

HF="${HF_CLI:-hf}"
command -v "$HF" >/dev/null 2>&1 || HF=huggingface-cli

upload_readme() {
  local dataset="$1"
  local file="$2"
  echo "→ datasets/csoai/$dataset README"
  "$HF" upload "csoai/$dataset" "$file" README.md --repo-type dataset --commit-message "fix(card): axis README from .github hf-patches"
}

upload_readme gspc-xr "$PATCHES/gspc-xr/README.md"
upload_readme gspc-affect "$PATCHES/gspc-affect/README.md"
upload_readme gspc-jail "$PATCHES/gspc-jail/README.md"

for space in gspc-affect gspc-jail; do
  SRC="$PATCHES/spaces/$space"
  if [[ -d "$SRC" ]]; then
    echo "→ spaces/csoai/$space"
    "$HF" upload "csoai/$space" "$SRC" . --repo-type space --commit-message "feat(space): scaffold from .github hf-patches" || \
      echo "WARN: space $space upload failed (may need create via huggingface.co/new-space)"
  fi
done

echo "HF upload batch complete."
