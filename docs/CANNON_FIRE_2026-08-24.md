# CANNON FIRE — 2026-08-24 results

**Status:** Sales-demo stack is LIVE. E2E green. Board canon restored.

## Fired and yielded today

| Lane | Result |
|------|--------|
| Apex fat | ✅ ~214KB homepage (was 7KB thin shell) |
| App.tsx conflict | ✅ Fixed (PR #420/#421) — deploy unblocked |
| Board canon | ✅ Restored 14 axes + jail after PR #425 honesty-lock regression (PR #444) |
| Chat canon | ✅ Then “13 measured of 14”; ClaimGuard refuses 16/twelve overclaims (PR #434). **Live now:** cite `totals.public_count` (14 measured of 14 quotable as of 2026-08-25). |
| MCP catalog | ✅ 4 tools live (`measure` `verify` `jail-probe` `enter-arena`) |
| One-door OS | ✅ `/ag-ui` `/agui` → `/?lobby=home` |
| **E2E integration** | ✅ **PASS** (15/15) |
| **Weekend demo smoke** | ✅ **SALES-DEMO READINESS: PASS** |
| ClaimGuard self-test | ✅ PASS |
| HF 14 axis cards | ✅ Ready under `docs/hf-patches/axes/` (upload needs `HF_TOKEN`) |
| Revenue / IP docs | ✅ WEEKEND_DEMO · REVENUE_SURFACES · IP_PORTFOLIO · NSITE_AEO_PACK |
| Batch runner | ✅ `scripts/batch-run-gates.mjs` |

## Sales path live now

```
Stranger → /gspc-verify/ (free)
         → /?lobby=home (ask)
         → /api/gspc (14 / 13 of 14)
         → /gspc-scoreboard
         → /start or /enterprise
         → MCP measure/verify
```

Script: [`docs/WEEKEND_DEMO.md`](WEEKEND_DEMO.md)  
Smoke: `node scripts/weekend-demo-smoke.mjs`

## Remaining blockers (owner only)

1. **DEPLOY-LOCK** — disable Cloudflare Pages Git auto-deploy on `councilof-ai`
2. **`AGUI_WIRE_URL`** — RunPod wire on Pages env
3. **`HF_TOKEN`** — then `bash scripts/upload-hf-patches.sh` ships all 14 cards + Spaces

## Frontend audit leftovers (non-blocking for sales demo)

- `/scorecard` still 404 on apex (Moody’s HTML lives on `csoai-site.pages.dev/scorecard`)
- `/honesty` copy missing literal `council-oowm` string (page 200)

## IP inventory for growth conversations

See [`docs/IP_PORTFOLIO.md`](IP_PORTFOLIO.md) — ClaimGuard, GSPC instrument + DOI, signed receipts, living board, arena, HF×14, MCP tools, one-door OS.

**Do not invent revenue multiples.** Pitch measurement integrity + free verify + enterprise start.
