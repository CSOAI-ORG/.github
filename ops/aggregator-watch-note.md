# Aggregator Propagation Watch-Note (N5-12)

**Created:** 2026-08-24T17:30:00Z  
**Last recheck:** 2026-08-25T17:12:00Z (RALPH)

## Status: WATCH (not a sales claim)

| Aggregator | Mechanism | Expected lag | Status 2026-08-25T17:12Z |
|------------|-----------|--------------|--------------------------|
| Official MCP registry | OIDC publish | Immediate | **LIVE** `io.github.CSOAI-ORG/gspc` **1.0.3** isLatest · `board (14 of 14)` |
| PulseMCP | `updated_since` ETL | ~24h | Probe 403/API-key — recheck later |
| Glama | Auto-index GitHub + official registry | Minutes–unknown | `glama.ai/mcp/servers/@CSOAI-ORG/gspc` still **404** · `glama.json` on deploy2 |
| Smithery | listing page | — | **LIVE** https://smithery.ai/servers/csoai/gspc |
| GitHub MCP Registry curation | Discussion thread | Manual | Draft only (below) |

## glama.json

Committed at repo root + on `csoai-static-deploy2` with maintainers block (mandatory for org repos).

## Smithery

**LIVE:** https://smithery.ai/servers/csoai/gspc (`npx -y smithery mcp add csoai/gspc`).

## GitHub MCP Registry draft post (do not post without Nick)

**Title:** Request listing: io.github.CSOAI-ORG/gspc (CSOAI GSPC measurement MCP)

**Body:** Official MCP registry entry for CSOAI GSPC measurement server **v1.0.3** (board 14 of 14). Repository: https://github.com/CSOAI-ORG/csoai-static-deploy2 (`workers/csoai-gspc-mcp` + `registry/gspc.json`). Remotes: https://councilof.ai/api/assess · https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp

## Recheck checklist

- [x] Official registry **1.0.3** isLatest with 14-of-14 description
- [ ] PulseMCP shows gspc ≥1.0.3
- [ ] Glama indexes full metadata (repository, title)
- [ ] Worker runtime `initialize.serverInfo.version` = 1.0.3 (needs `CF_API_TOKEN` restore)
  - Recheck 2026-08-25T17:37Z: both `csoai-gspc-mcp.nicholastempleman.workers.dev/mcp` and `councilof.ai/mcp` still report **1.0.0**

## Site llms.txt

CDN updated 2026-08-25T16:50Z via councilof-ai `0a61d80` — cites live 14 measured of 14 quotable.

## Site openapi.json

**LIVE** https://councilof.ai/openapi.json (HTTP 200, 2026-08-25T17:49Z) — shipped councilof-ai `8bb42b0`.

## Badge

**LIVE** `/badge/axes.json` → message **14 of 14** on councilof.ai + csoai.org (2026-08-25T17:59Z).
