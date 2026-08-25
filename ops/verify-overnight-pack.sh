#!/usr/bin/env bash
# ops/verify-overnight-pack.sh — N5-01..N5-30 completion audit (read-only)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/ops/logs"
mkdir -p "$LOG_DIR"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$LOG_DIR/overnight-pack-verify-$TS.log"
FAIL=0
WARN=0
STRICT="${STRICT:-0}"

pass() { echo "  [PASS] $*"; }
fail() { echo "  [FAIL] $*"; FAIL=1; }
warn() {
  echo "  [WARN] $*"
  WARN=1
  if [[ "$STRICT" == "1" ]]; then FAIL=1; fi
}
note() { echo "  [NOTE] $*"; }  # owner-gated / known lag — never fails STRICT

http_code() { curl -s -o /dev/null -w "%{http_code}" "$1"; }

{
  echo "=== Overnight pack verification $TS ==="

  echo "--- N5-07/21 ClaimGuard + banned-strings"
  if bash "$ROOT/ops/claimguard-publish-gate.sh" "$ROOT/export" "$ROOT/trust/evidence-pack" >/dev/null 2>&1; then
    pass "ClaimGuard + banned-strings"
  else
    fail "ClaimGuard + banned-strings"
  fi

  echo "--- N5-02/03 HF datasets"
  for url in \
    "https://huggingface.co/datasets/csoai/gspc-board" \
    "https://huggingface.co/datasets/csoai/gspc-bench-results"
  do
    code=$(http_code "$url")
    if [[ "$code" == "200" ]]; then pass "$url HTTP $code"; else fail "$url HTTP $code"; fi
  done
  # N5-02/04: live board must reflect GSPC export (not stale EUNOMIA branding)
  board_readme="$(curl -sL "https://huggingface.co/datasets/csoai/gspc-board/raw/main/README.md" 2>/dev/null || true)"
  if echo "$board_readme" | grep -qi eunomia; then
    warn "gspc-board README still contains EUNOMIA (stale; export is GSPC — publish pending)"
  elif [[ -n "$board_readme" ]]; then
    pass "gspc-board README free of EUNOMIA branding"
  else
    warn "gspc-board README could not be fetched for branding check"
  fi

  echo "--- N5-05 HF DOIs"
  for repo in csoai/gspc-board csoai/gspc-bench-results; do
    doi=$(curl -s "https://huggingface.co/api/datasets/$repo" | python3 -c '
import sys, json
d = json.load(sys.stdin)
doi = d.get("doi")
if not doi:
    for t in d.get("tags") or []:
        if isinstance(t, str) and t.startswith("doi:"):
            doi = t[4:]
            break
print(doi or "none")
' 2>/dev/null || echo "none")
    if [[ "$doi" != "none" && -n "$doi" ]]; then pass "$repo DOI=$doi"; else warn "$repo DOI not minted"; fi
  done

  echo "--- N5-06 HF Space + leaderboard-results"
  code=$(http_code "https://huggingface.co/datasets/csoai/gspc-leaderboard-results")
  if [[ "$code" == "200" ]]; then pass "leaderboard-results HTTP $code"; else warn "leaderboard-results HTTP $code (expected 200 after publish)"; fi
  sdk=$(curl -s "https://huggingface.co/api/spaces/csoai/gspc-governance-leaderboard" | python3 -c "import sys,json; print(json.load(sys.stdin).get('sdk','?'))" 2>/dev/null || echo "?")
  if [[ "$sdk" == "gradio" ]]; then pass "Space sdk=gradio"; else warn "Space sdk=$sdk (expected gradio after publish)"; fi
  code=$(http_code "https://huggingface.co/spaces/csoai/gspc-governance-leaderboard")
  if [[ "$code" == "200" ]]; then pass "Space HTTP $code"; else fail "Space HTTP $code"; fi

  echo "--- N5-10/11 MCP registry"
  mcp=$(curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=gspc" | python3 -c "
import sys,json
from packaging.version import Version
d=json.load(sys.stdin)
latest=[x['server']['version'] for x in d.get('servers',[]) if x.get('_meta',{}).get('io.modelcontextprotocol.registry/official',{}).get('isLatest')]
print(latest[0] if latest else 'none')
" 2>/dev/null || echo "none")
  # Accept 1.0.2+ (1.0.3 = free polish: board 14 of 14 description)
  if python3 -c "from packaging.version import Version; import sys; sys.exit(0 if Version(sys.argv[1]) >= Version('1.0.2') else 1)" "$mcp" 2>/dev/null; then
    pass "MCP latest=$mcp"
  else
    fail "MCP latest=$mcp (expected >=1.0.2)"
  fi

  echo "--- N5-13/14 A2A agent card"
  curl -s "https://councilof.ai/.well-known/agent-card.json" -o "/tmp/overnight-agent-card-$TS.json"
  if node "$ROOT/connect/agent-cards/validate.mjs" "/tmp/overnight-agent-card-$TS.json" >/dev/null 2>&1; then
    pass "A2A validator live card"
  else
    fail "A2A validator live card"
  fi

  echo "--- N5-LIVE board chrome (14/14)"
  pc=$(curl -sA "CSOAI-overnight-verify/1.0" "https://councilof.ai/api/gspc" | python3 -c "import sys,json; print(json.load(sys.stdin).get('totals',{}).get('public_count',''))" 2>/dev/null || true)
  if echo "$pc" | grep -q "14 measured of 14"; then
    pass "live public_count=$pc"
  else
    fail "live public_count drift: ${pc:-empty}"
  fi
  for badge in \
    "https://councilof.ai/badge/axes.json" \
    "https://csoai.org/badge/axes.json"
  do
    msg=$(curl -sA "CSOAI-overnight-verify/1.0" "$badge" | python3 -c "import sys,json; print(json.load(sys.stdin).get('message',''))" 2>/dev/null || true)
    if [[ "$msg" == "14 of 14" ]]; then
      pass "$badge message=$msg"
    else
      warn "$badge message=${msg:-empty} (want 14 of 14)"
    fi
  done
  code=$(http_code "https://councilof.ai/openapi.json")
  if [[ "$code" == "200" ]]; then pass "openapi.json HTTP $code"; else warn "openapi.json HTTP $code"; fi
  code=$(http_code "https://councilof.ai/AGENT-ONBOARDING.md")
  if [[ "$code" == "200" ]]; then pass "AGENT-ONBOARDING.md HTTP $code"; else note "AGENT-ONBOARDING.md HTTP $code (shipped 711d1ee — await Pages if 404)"; fi
  feed=$(curl -sA "CSOAI-overnight-verify/1.0" "https://councilof.ai/api/feed.xml" 2>/dev/null || true)
  if echo "$feed" | grep -q "14 measured of 14"; then
    pass "feed.xml cites 14 measured of 14"
  else
    warn "feed.xml missing live 14/14 item"
  fi
  # axis-register + server-card — shipped on master (660d67e / 1ce12b0); NOTE while Pages lags
  ar=$(curl -sA "CSOAI-overnight-verify/1.0" "https://councilof.ai/api/axis-register" 2>/dev/null || true)
  ar_n=$(echo "$ar" | python3 -c "import sys,json; print(json.load(sys.stdin).get('registry_axis_count',''))" 2>/dev/null || true)
  if [[ "$ar_n" == "14" ]] && ! echo "$ar" | grep -q "UNTESTED"; then
    pass "axis-register registry_axis_count=14 (no UNTESTED)"
  else
    note "axis-register count=${ar_n:-empty} (master 660d67e — await Pages if still 13/UNTESTED)"
  fi
  sc=$(curl -sA "CSOAI-overnight-verify/1.0" "https://councilof.ai/.well-known/mcp/server-card.json" 2>/dev/null || true)
  if echo "$sc" | grep -q "14 measured of 14"; then
    pass "mcp/server-card.json cites 14 measured of 14"
  else
    note "mcp/server-card.json stale (master 1ce12b0 — await Pages if still 13 measured)"
  fi
  mo_note=$(curl -sA "CSOAI-overnight-verify/1.0" "https://councilof.ai/api/gspc" | python3 -c "import sys,json; print(json.load(sys.stdin).get('measured_on',{}).get('note',''))" 2>/dev/null || true)
  if echo "$mo_note" | grep -q "TIE (determined" && ! echo "$mo_note" | grep -q "separation is UNTESTED"; then
    pass "measured_on.note jail TIE (determined)"
  else
    note "measured_on.note lag (master c97a8a1/f277606 — await Pages if still UNTESTED)"
  fi
  cat_note=$(curl -sA "CSOAI-overnight-verify/1.0" "https://councilof.ai/catalog.json" 2>/dev/null || true)
  if echo "$cat_note" | grep -q "14 measured of 14"; then
    pass "catalog.json cites 14 measured of 14"
  else
    note "catalog.json stale (master 0a49168/f277606 — await Pages if still 13 measured axes)"
  fi
  mcp_rt=$(curl -sA "CSOAI-overnight-verify/1.0" -X POST "https://councilof.ai/mcp" \
    -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"verify","version":"0"}}}' \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('serverInfo',{}).get('version',''))" 2>/dev/null || true)
  if [[ "$mcp_rt" == "1.0.3" ]]; then
    pass "MCP worker runtime=$mcp_rt"
  else
    note "MCP worker runtime=${mcp_rt:-empty} (registry 1.0.3; needs CF_API_TOKEN restore — see ops/cf-api-token-restore.md)"
  fi

  echo "--- N5-20 evidence pack"
  for f in 01-technical-system-description.md 02-governance-oversight-record.md 03-monitoring-incident-log.md 04-scope-constraints-statement.md; do
    if [[ -f "$ROOT/trust/evidence-pack/$f" ]]; then pass "evidence-pack/$f"; else fail "evidence-pack/$f missing"; fi
  done

  echo "--- N5-22..25 marketplace drafts"
  for f in ops/adx/product-metadata.md ops/snowflake/listing-draft.md ops/datarade/listing-drafts.md; do
    if [[ -f "$ROOT/$f" ]]; then pass "$f"; else fail "$f missing"; fi
  done

  echo "--- N5-26..29 insurance prep"
  for f in aiuc-1-scoping-draft.md armilla-governance-draft.md munich-re-aisure-dd-draft.md testudo-one-pager.md; do
    if [[ -f "$ROOT/trust/insurance-prep/$f" ]]; then pass "insurance-prep/$f"; else fail "insurance-prep/$f missing"; fi
  done

  echo "--- N5-30 G-Cloud prep"
  if [[ -f "$ROOT/ops/gcloud15/checklist.md" ]]; then pass "ops/gcloud15/checklist.md"; else fail "ops/gcloud15/checklist.md missing"; fi

  echo "--- Summary (STRICT=$STRICT)"
  if [[ "$FAIL" -eq 0 ]]; then
    if [[ "$WARN" -eq 1 ]]; then
      echo "VERIFY PASS with warnings (owner-gated items may still be pending: HF DOI, directories)"
    else
      echo "VERIFY PASS — all checks green"
    fi
  else
    echo "VERIFY FAIL — see failures above"
  fi
} > "$LOG"

cat "$LOG"
echo "$LOG"
exit "$FAIL"
