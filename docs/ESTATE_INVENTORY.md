# Estate inventory (mined 2026-08-22)

Counts and leaders always defer to [`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc).  
Axis names: [`GSPC_AXIS_CANON.md`](GSPC_AXIS_CANON.md). Plan: [`MASTER_PLAN.md`](MASTER_PLAN.md).

## Measurement spine (core)

| Asset | Repo / URL | Status |
|---|---|---|
| Living board API | `councilof.ai/api/gspc` | **Live** |
| Site + lobby + scoreboard | `CSOAI-ORG/councilof-ai` | Homepage **fat** (213 KB); **alias routes 404** on apex |
| Static boards / SOVOS / scorecard | `CSOAI-ORG/csoai-static-deploy2` | Fat host live; Moody’s `scorecard.html` |
| AG-UI wire | `CSOAI-ORG/csoai-agui-wire` | Code verified; **not on apex** |
| MCP worker | via `councilof.ai/.well-known/mcp.json` | Tools: measure, verify, jail-probe, enter-arena |
| N-site #3 flywheel | `CSOAI-ORG/flywheel-nsite` | CI live |
| Dashboard (spare) | `CSOAI-ORG/csoai-dashboard` | Undeployed |
| Codabench challenge | `CSOAI-ORG/codabench-gspc` | Spec present; README missing |
| Axis boards / packs / regional | `gspc-axis-boards`, `gspc-packs-hub`, `gspc-regional` | HTML shells |
| Org profile | `CSOAI-ORG/.github` (this repo) | Canon + plan |

## Receipt / integrity tooling

| Asset | Repo | Status |
|---|---|---|
| Shared signed-receipt primitive | `signed-receipts` | Canonical |
| Inspect receipts | `inspect-receipts` | Live pattern |
| A2A signed receipts | `a2a-signed-receipts` | Draft SPEC only |
| Fact-cards / valves | `carder` | Strong |
| Brand badges | `brand-assets` | Minimal |
| Claim linter (SOVOS) | `csoai-static-deploy2/.../claim_linter.py` | Exists |
| **ClaimGuard product** | [`claimguard`](https://github.com/CSOAI-ORG/claimguard) | **Landed 2026-08-22** — live attestation verify + claim rules |
| ConsciousnessNonClaimGuard | `meok-ai` | Different product |

## Hugging Face (`csoai`) — GSPC public

**14 axis datasets:** gov, agi(safety), prv, asi, mcp, oss, mach, care, xr, det, art5, swarm, affect, jail  
**Meta:** boards, papers, arena-results, normalized, airbench-eu-mandatory-run, signed-fleet-boards-v2, signed-measurement-records  
**Spaces (12):** missing **affect** + **jail**  
**P0 defect:** `gspc-xr` README is a DET clone  
**Private/adjacent:** OOWM / SOV-SIGNAL corpora + models (router, sov33/34, gates)

## Kaggle (`nicktempleman`)

Mirrors present for all 14 axes including affect + jail + normalized + arena-results. Sync HF fixes (esp. XR) across.

## Zenodo

- Method: `10.5281/zenodo.21991104` → record `21991105`
- Evidence: `10.5281/zenodo.21973002` → `21973003`  
Cite on axis cards (mostly missing today).

## N-sites (`*-site`, ~27)

**Industry:** fintech, healthtech, govtech, regtech, care-industries, care-compliance, accountabilityof, biasdetectionof, dataprivacyof, ethicalgovernanceof, transparencyof  

**Product / vertical:** openmoe, landlaw, diyhelp, optimobile, openpatent, planthire, pokerhud, koikeeper, iokfarm, loopfactory, cobolbridge, commercialvehicle, socialmediamanager, sovereign-town, suicidestop, wowmcp  

**Rule:** one shared AEO/AGUI pack; brand + skills per site. Do not fan-out until Phase 3 HF lock + Phase 1 apex.

## MCP catalog

~356 repos with `mcp` in the name. **Not** the weekend readiness signal. Prefer GSPC MCP worker tools over catalog sprawl.

## Live route reality (apex `councilof.ai`) — audited 2026-08-23

| 200 | REAL 404 (coded in place-end-user-aliases, not on production alias) |
|---|---|
| `/` (213 KB + CouncilLobby), `/?lobby=home` | `/lobby`, `/scorecard`, `/honesty`, `/library` |
| `/api/gspc`, `/api/health`, `/api/cross`, `/api/cards`, `/api/axis-register` | `/api/chat` |
| `/gspc-scoreboard`, `/gspc-verify/` (slash) | `/gspc`, `/verify`, `/console`, `/gspc-verify` (no slash) |
| `/os/`, `/arena`, `/govbench`, `/about` | `/pricing`, `/regulators`, `/start`, `/methodology` |
| `/.well-known/mcp.json`, `agent-card.json` | `/agui`, `/coliseum`, `/live-ledger` |

Full matrix: [`FRONTEND_AUDIT_CHECKLIST.md`](FRONTEND_AUDIT_CHECKLIST.md).  
`csoai-site.pages.dev` returned 403 in audit env — do not rely as fallback.  
Sitemap advertises hundreds of keyword URLs that 404 on apex — trust debt.

## Board counting (do not mix)

| Set | N |
|---|---|
| Quotable board slots | 14 |
| Public measured ruling | 13 of 14 |
| In-lane honesty | +2 (`slot15` / instrument-honesty, `human-vs-ai`) |
| Living convention “16” | 14+2, **not** quotable |
| Public Elo league | **Does not exist** on GSPC API |

## Track-loss register (land or kill)

1. ~~ClaimGuard session files~~ → landed in `CSOAI-ORG/claimguard` (session jail evidence sigs still local-only)  
2. Apex vs fat deploy split  
3. AG-UI not on brand origin  
4. XR HF card contamination  
5. Affect/jail Spaces missing  
6. Chat count drift vs API  
7. 27 site forks without shared pack  
8. Claiming Elo as board ranking
