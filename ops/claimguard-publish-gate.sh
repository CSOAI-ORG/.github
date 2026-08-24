#!/usr/bin/env bash
# ops/claimguard-publish-gate — ClaimGuard + banned-strings before any public surface.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CG="$ROOT/products/claimguard/claimguard.py"
BS="$ROOT/ops/banned-strings.mjs"
BOARD="${BOARD:-$ROOT/export/gspc-board/board.json}"
LOG_DIR="$ROOT/ops/logs"
mkdir -p "$LOG_DIR"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$LOG_DIR/claimguard-$TS.log"

if [[ ! -f "$CG" ]]; then
  echo "FATAL: ClaimGuard not found at $CG" >&2
  exit 1
fi

TARGETS=("$@")
if [[ ${#TARGETS[@]} -eq 0 ]]; then
  TARGETS=("$ROOT/export" "$ROOT/trust/evidence-pack")
fi

{
  echo "=== ClaimGuard publish gate $TS ==="
  echo "board: $BOARD"
  echo "--- attestation + board integrity"
  python3 "$CG" check --board "$BOARD" --claim "13 measured of 14" || CG_FAIL=1
  echo "--- banned-strings"
  node "$BS" "${TARGETS[@]}" || BS_FAIL=1
} | tee "$LOG"

if [[ "${CG_FAIL:-0}" -eq 1 || "${BS_FAIL:-0}" -eq 1 ]]; then
  echo "GATE FAIL — see $LOG" >&2
  exit 1
fi
echo "GATE PASS — log: $LOG"
echo "$LOG"
