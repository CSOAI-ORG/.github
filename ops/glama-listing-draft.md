# Glama listing draft — csoai/gspc (N5-12)

**Status:** DRAFT only — do not submit/spend without Nick. Live URL still **404** as of 2026-08-25T23:35Z (Apify + curl).

## Desired listing

| Field | Value |
|-------|-------|
| Name | CSOAI GSPC measurement |
| Slug | `csoai/gspc` or `@CSOAI-ORG/gspc` |
| Registry | `io.github.CSOAI-ORG/gspc` **1.0.3** (isLatest) |
| Description | Independent GSPC measurement over MCP: assess, board (**14 of 14**), verify cards. Measurement only — not certification. |
| Homepage | https://councilof.ai |
| Agent / board | https://councilof.ai/api/gspc |
| MCP remote | https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp |
| Repo | https://github.com/CSOAI-ORG/csoai-static-deploy2 (`workers/csoai-gspc-mcp`, `glama.json`, `registry/gspc.json`) |
| License | Measurement artefacts CC-BY-4.0; code see repo |

## Already on deploy2 main

- `glama.json` maintainers block (org requirement)
- Registry publish **1.0.3** with `board (14 of 14)`

## Blockers

1. No free public submit form found for Glama MCP servers (auto-index from GitHub/registry only).
2. Worker runtime still **1.0.0** until `CF_API_TOKEN` restored (registry is already 1.0.3).

## Recheck

- [ ] https://glama.ai/mcp/servers/csoai/gspc HTTP 200
- [ ] https://glama.ai/mcp/servers/@CSOAI-ORG/gspc HTTP 200
- [ ] Metadata shows 1.0.3 + 14 of 14
