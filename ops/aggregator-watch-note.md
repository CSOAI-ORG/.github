# Aggregator Propagation Watch-Note (N5-12)

**Created:** 2026-08-24T17:30:00Z  
**Recheck:** 2026-08-25T18:00:00Z (tomorrow evening)

## Status: NOT A DONE-CLAIM

| Aggregator | Mechanism | Expected lag | Action tonight |
|------------|-----------|--------------|----------------|
| PulseMCP | `updated_since` ETL | ~24h | Passive watch |
| Glama | Auto-index GitHub + official registry | Minutes–unknown | `glama.json` committed with maintainers |
| Smithery | Separate submission (`smithery mcp publish`) | Manual | **Deferred to Nick** |
| GitHub MCP Registry | Manual curation via discussion thread | Manual | Request post **drafted, not posted** |

## glama.json

Committed at repo root with maintainers block (mandatory for org repos).

## Smithery draft (do not post without Nick)

```
smithery mcp publish --name io.github.CSOAI-ORG/gspc
```

## GitHub MCP Registry draft post (do not post without Nick)

**Title:** Request listing: io.github.CSOAI-ORG/gspc (CSOAI GSPC measurement MCP)

**Body:** Official MCP registry entry for CSOAI GSPC measurement server v1.0.2. Repository: https://github.com/CSOAI-ORG/csoai-static-deploy2 (workers/csoai-gspc-mcp). Remote: https://councilof.ai/api/assess

## Recheck checklist (2026-08-25 evening)

- [ ] PulseMCP shows gspc v1.0.2
- [ ] Glama indexes full metadata (repository, title, packages)
- [ ] Registry still v1.0.2 (preview registry may reset)
