# Aggregator Propagation Watch-Note (N5-12)

**Created:** 2026-08-24T17:30:00Z  
**Last recheck:** 2026-08-25T16:33:00Z (RALPH)

## Status: WATCH (not a sales claim)

| Aggregator | Mechanism | Expected lag | Status 2026-08-25T16:33Z |
|------------|-----------|--------------|--------------------------|
| Official MCP registry | OIDC publish | Immediate | **LIVE** `io.github.CSOAI-ORG/gspc` **1.0.3** isLatest · `board (14 of 14)` |
| PulseMCP | `updated_since` ETL | ~24h | Probe 403/API-key — recheck later |
| Glama | Auto-index GitHub + official registry | Minutes–unknown | `glama.ai/mcp/servers/@CSOAI-ORG/gspc` still **404** · `glama.json` on deploy2 |
| Smithery | `smithery mcp publish` | Manual | **Deferred to Nick** |
| GitHub MCP Registry curation | Discussion thread | Manual | Draft only (below) |

## glama.json

Committed at repo root + on `csoai-static-deploy2` with maintainers block (mandatory for org repos).

## Smithery draft (do not post without Nick)

```
smithery mcp publish --name io.github.CSOAI-ORG/gspc
```

## GitHub MCP Registry draft post (do not post without Nick)

**Title:** Request listing: io.github.CSOAI-ORG/gspc (CSOAI GSPC measurement MCP)

**Body:** Official MCP registry entry for CSOAI GSPC measurement server **v1.0.3** (board 14 of 14). Repository: https://github.com/CSOAI-ORG/csoai-static-deploy2 (`workers/csoai-gspc-mcp` + `registry/gspc.json`). Remotes: https://councilof.ai/api/assess · https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp

## Recheck checklist

- [x] Official registry **1.0.3** isLatest with 14-of-14 description
- [ ] PulseMCP shows gspc ≥1.0.3
- [ ] Glama indexes full metadata (repository, title)
- [ ] Worker runtime `initialize.serverInfo.version` = 1.0.3 (needs `CF_API_TOKEN` restore)
