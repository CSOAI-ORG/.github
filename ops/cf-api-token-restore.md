# Restore CF_API_TOKEN for MCP worker + static deploy (owner action)

**Why (two surfaces):**

1. Official MCP registry is **1.0.3** (`board (14 of 14)`), but live Workers still answer `initialize.serverInfo.version = **1.0.0**`:
   - `https://councilof.ai/mcp`
   - `https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp`
2. `csoai.org` chrome lags `csoai-static-deploy2` **main** (honesty/arenas already cite **14 measured of 14** + jail **TIE** on tip: `5ce429a` / `7b0aa77`). Historical **Deploy static site** runs failed at “Deploy to Cloudflare Pages” (last seen 2026-08-16) — empty/missing CF secrets are the likely cause.

Source on `csoai-static-deploy2` already says MCP **1.0.3** (`workers/csoai-gspc-mcp/src/index.js` + `package.json`). Deploy workflow:

`.github/workflows/deploy-csoai-gspc-mcp.yml` → `cloudflare/wrangler-action@v3` needs:

| Secret | Used as |
|--------|---------|
| `CF_API_TOKEN` | `apiToken` (Workers + Pages) |
| `CF_ACCOUNT_ID` | `accountId` |

## Owner steps (Nick)

1. Cloudflare dashboard → My Profile → API Tokens → create token with **Edit Cloudflare Workers** and **Cloudflare Pages** edit (account scoped to CSOAI).
2. GitHub → `CSOAI-ORG/csoai-static-deploy2` → Settings → Secrets → Actions → set `CF_API_TOKEN` + `CF_ACCOUNT_ID`.
3. Actions → **Deploy csoai-gspc-mcp Worker** → Run workflow (`workflow_dispatch`), or push a no-op under `workers/csoai-gspc-mcp/`.
4. Re-run / restore the static Pages deploy path so `csoai.org/honesty` and `/arenas` pick up main tip.
5. Verify:

```bash
curl -sS -X POST https://councilof.ai/mcp \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"check","version":"0"}}}'
# expect serverInfo.version == "1.0.3"

curl -sS https://csoai.org/honesty | grep -o '14 measured of 14'
curl -sS https://csoai.org/arenas | grep -o '14 measured of 14'
```

**Lane cannot spend or create CF tokens.** No DOI remint. No board change.
