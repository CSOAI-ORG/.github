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
  "board_axes": null,
      "measured_axes": null,
      "public_count": "(from GET /api/gspc — never freeze here)",
      "findings": [
    {
      "status": "FAIL",
      "code": "claim.sixteen_axes",
      "message": "16 jail-probe families are not 16 measured axes. Quote totals.public_count."
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

- Quote `totals.public_count` from GET `/api/gspc` — never freeze 13/14 or 15/22 in this spec
- Stale “13 of 14” FAILs when live `totals` are not 13 measured of 14 axes
- No Elo on GSPC public board
- Jail separation **UNTESTED** until McNemar gate
- `N measured` must match live `totals.measured_axes`

## CI gate

```bash
python3 products/claimguard/claimguard.py --self-test
python3 products/claimguard/claimguard.py check --live --claim "16 measured axes"
# expect FAIL
```

Wired into `scripts/batch-run-gates.mjs`.
