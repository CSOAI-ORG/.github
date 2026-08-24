# ClaimGuard MCP tool — wire spec

**Product:** `products/claimguard/` (mirror of `CSOAI-ORG/claimguard`)  
**Purpose:** Refuse overclaims against the signed GSPC board (`/api/gspc`).

## Tool descriptor

```json
{
  "name": "claimguard.check",
  "description": "Check a natural-language claim against the live signed GSPC board. Returns PASS/FAIL/WARN with Ed25519-verified findings. Measurement, not certification.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "claim": {
        "type": "string",
        "description": "Natural-language claim to verify (e.g. '16 measured axes', 'jail separation resolved')"
      },
      "board_url": {
        "type": "string",
        "description": "Optional board JSON URL (default: https://councilof.ai/api/gspc)"
      }
    },
    "required": ["claim"]
  }
}
```

## Response shape

```json
{
  "ok": false,
  "board_axes": 14,
  "measured_axes": 13,
  "public_count": "13 measured of 14 (SITTING 1, 2026-08-18)",
  "findings": [
    {
      "status": "FAIL",
      "code": "AXIS_COUNT_OVERCLAIM",
      "message": "Claim implies 16 measured board axes; live board has 14 quotable slots, 13 measured."
    }
  ]
}
```

## Wire paths

| Surface | Status | Path |
|---------|--------|------|
| CLI | ✅ | `python claimguard.py check --live --claim "..."` |
| MCP worker | ⏳ | Add to `csoai-gspc-mcp` worker `tools/list` |
| `/api/chat` | ⏳ | Grade-claiming asks → ClaimGuard before answer |
| AG-UI wire | ⏳ | `claimguard.check` alongside measure/verify |

## Canon rules enforced

- 14 quotable board slots; public ruling **13 of 14 measured**
- +2 in-lane (`slot15`, `human-vs-ai`) — not board-quotable
- No Elo on GSPC public board
- Jail separation **UNTESTED** until McNemar gate
- `public_count` string must match `/api/gspc` totals

## CI gate

```bash
python3 products/claimguard/claimguard.py --self-test
python3 products/claimguard/claimguard.py check --live --claim "16 measured axes"
# expect FAIL
```

Wired into `scripts/batch-run-gates.mjs`.
