# Frontend audit checklist — all end-user types

**Audit date:** 2026-08-23  
**Host under test:** `https://councilof.ai`  
**Truth rail:** [`/api/gspc`](https://councilof.ai/api/gspc) — 14 axes, 13 measured of 14  
**Canon:** [`GSPC_AXIS_CANON.md`](GSPC_AXIS_CANON.md) · **Plan:** [`MASTER_PLAN.md`](MASTER_PLAN.md)

Run locally: `node scripts/run-frontend-audit.mjs` (from this repo).

---

## Executive summary

| Gate | Result | Notes |
|---|---|---|
| Homepage fat (≥20 KB + CouncilLobby) | **PASS** | 213 KB, CouncilLobby chunk present |
| Living board `/gspc-scoreboard` | **PASS** | ~79 KB React board |
| API truth rail `/api/gspc` | **PASS** | Schema `csoai.gspc-axes/0.5`, 13/14 |
| ClaimGuard live attestation | **PASS** | Self-test + pytest (5/5) |
| Persona gauntlet (8 end-user types) | **FAIL** | 3/8 pass — buyer, auditor, researcher, regulator, enterprise 404 |
| Drift-guard (canon vs live) | **FAIL** | `/library`, `/honesty` 404 |
| assert-prerender-live | **FAIL** | `/gspc`, `/verify`, `/console` 404 |
| Playwright production-surfaces | **FAIL** | 49 failed — mostly legacy routes not in Council OS redesign |
| AG-UI deploy | **BLOCKED** | `/agui` 404; wire exists in `csoai-agui-wire` only |
| HF publishing | **BLOCKED** | Patches ready in `docs/hf-patches/`; needs HF write token |

**Root cause (route 404s):** Gated CI deploy runs `place-end-user-aliases.mjs` but production alias is still missing stranger URLs. Either the last gated deploy did not land on the production alias, or a concurrent thin rebuild overwrote alias files. See `councilof-ai/DEPLOY-LOCK.md`.

---

## End-user persona matrix

| Persona | Route | HTTP | Required markers | Status |
|---|---|---|---|---|
| **Visitor** | `/` | 200 | Council of AI, We measure | **PASS** |
| **Buyer** | `/pricing` | 404 | free | **FAIL** |
| **Auditor** | `/honesty` | 404 | council-oowm | **FAIL** |
| **Researcher** | `/library` | 404 | reference pages across | **FAIL** |
| **API agent** | `/api/gspc` | 200 | axes:14, measured_axes:13 | **PASS** |
| **A2A agent** | `/.well-known/agent-card.json` | 200 | doi, CSOAI Ltd | **PASS** |
| **Regulator** | `/regulators` | 404 | — | **FAIL** |
| **Enterprise** | `/start` | 404 | — | **FAIL** |

Lobby works via query param: `/?lobby=home` (200, CouncilLobby chunk). Direct `/lobby` is 404.

---

## Route inventory (apex)

### Working (200)

| Route | Size / notes |
|---|---|
| `/` | 213 KB fat shell + CouncilLobby |
| `/?lobby=home` | Same as home with lobby param |
| `/os/` | Council OS surface |
| `/gspc-scoreboard` | ~79 KB living React board |
| `/gspc-verify/` | Verify surface (trailing slash required) |
| `/arena`, `/govbench` | Arena / govbench |
| `/for/regulator` | Demographic landing |
| `/vs/vanta` | Vendor compare |
| `/about` | About page |
| `/api/gspc` | Truth rail JSON |
| `/api/health` | Health check |
| `/api/cross` | Cross-lab data |
| `/.well-known/mcp.json` | MCP catalog (measure, verify, jail-probe, enter-arena) |
| `/.well-known/agent-card.json` | A2A agent card |

### Broken (404) — coded, not deployed

| Route | Expected source | Fix |
|---|---|---|
| `/lobby` | `place-end-user-aliases` → home | Re-run gated deploy + disable Pages Git auto-deploy |
| `/scorecard` | alias → living board | same |
| `/honesty` | honesty page | same |
| `/library` | library hub | same |
| `/gspc` | alias → board | same |
| `/verify` | alias → gspc-verify | same |
| `/console` | alias → home | same |
| `/pricing`, `/start`, `/regulators` | STRANGER_DIRS | same |
| `/methodology` | methodology page | same |
| `/agui` | AG-UI wire deploy | Phase 2 — deploy `csoai-agui-wire` |
| `/live-ledger`, `/coliseum` | future surfaces | Phase 2+ |
| `/gspc-verify` (no slash) | pretty URL | alias script writes both forms |
| `/api/chat` | chat function | function bundle dropped or not deployed |
| `/api/cards` | PR #324 | **200** (deployed 2026-08-23 audit) |
| `/api/axis-register` | PR #324 | **200** (deployed 2026-08-23 audit) |

### Static host `csoai-site.pages.dev`

All tested routes return **403 Forbidden** from this audit environment. Do not rely on it as fallback until access is restored.

---

## Automated test results (2026-08-23)

### ClaimGuard (`CSOAI-ORG/claimguard`)

```
pytest: 5 passed
self-test: PASS — signature holds; mutation + overclaims FAIL as required
```

Rejects: "16 measured axes", "jail separation resolved". Accepts: "14 quotable axes".

### councilof-ai scripts (live)

| Script | Result |
|---|---|
| `assert-prerender-live.mjs` | FAIL — 3 checks (`/gspc`, `/verify`, `/console`) |
| `drift-guard.mjs` | FAIL — 2 drifts (`/library`, `/honesty`) |
| `persona-gauntlet.mjs` | FAIL — 5 personas |

### Playwright `production-surfaces.spec.ts`

49 failed, 8 skipped (BASE_URL=`https://councilof.ai`). Most failures are **legacy routes** from pre–Council OS redesign (`/compliance/*`, `/globe`, `/login`, `/crosswalk`, etc.) that are not in the current prerender manifest. These tests need updating to match Council OS routes, not blocking for apex alias fix.

---

## Work completed (this agent run)

| Item | Repo | Status |
|---|---|---|
| Axis canon (14+2, not 16) | `.github` PR #3 | Draft, mergeable |
| Master plan (Moody's × Arena × AG-UI) | `.github` | Done |
| Estate inventory | `.github` | Done |
| 100-step execute checklist | `.github` | Done |
| ClaimGuard product | `claimguard` main | **Landed** |
| HF patches (XR, affect, jail + Spaces) | `.github/docs/hf-patches` | Ready, needs upload |
| Apex clobber runbook | `councilof-ai` PR #312 | Closed (docs only) |
| Homepage fat restore | `councilof.ai` live | **Improved** (was 7 KB, now 213 KB) |

## Other agents' work reviewed

| Source | Work | Assessment |
|---|---|---|
| Hygiene agent | PR #2 merged — community health files | Good |
| PR #324 `councilof-ai` | `/api/cards`, `/api/axis-register`, `functions-guard.mjs`, Dorado bench, evidence-pack | **Recommend merge** — closes API 404 gap |
| Lobby AG-UI agent | No code PR | Retest only |
| Multiple internal agents | UX/voice/Council OS pushes to `.github` | Not merged to product repos |

---

## Owner actions (priority order)

1. **Cloudflare:** Disable Pages Git auto-deploy on `councilof-ai` project ([DEPLOY-LOCK.md](https://github.com/CSOAI-ORG/councilof-ai/blob/main/DEPLOY-LOCK.md))
2. **Re-run** `Build + deploy site` workflow (workflow_dispatch) on `councilof-ai`
3. **Merge** `.github` PR #3 (canon docs) and `councilof-ai` PR #324 (API functions guard)
4. **HF write token** → upload `docs/hf-patches/**`
5. **Verify** persona-gauntlet + drift-guard green after deploy

---

## Publishing & mining still needed

| Area | Action |
|---|---|
| HF XR card | Upload fixed README (currently DET clone) |
| HF Spaces | Create `gspc-affect`, `gspc-jail` from scaffolds |
| HF all 14 cards | Add Zenodo DOI `10.5281/zenodo.21991104` |
| `gspc-normalized` | Rebuild with care/affect/jail |
| Kaggle | Sync after HF fixes |
| AG-UI | Deploy to `/agui` on apex |
| ClaimGuard | MCP `claimguard.check` + `/api/chat` wire |
| Playwright suite | Update legacy route list to Council OS routes |
| Monorepo | See [`MONOREPO_RUNPOD_OPS.md`](MONOREPO_RUNPOD_OPS.md) |

---

## Gate definition of done

Frontend is **publish-ready** when all of:

- [ ] persona-gauntlet: 8/8 PASS
- [ ] drift-guard: PASS
- [ ] assert-prerender-live: PASS (apex + pages.dev alias)
- [ ] functions-guard: PASS (after PR #324)
- [ ] ClaimGuard CI on every deploy
- [ ] HF 14/14 cards + 14/14 Spaces
- [ ] AG-UI live at `/agui` with MCP tools wired
- [ ] No sitemap URL returns REAL-404 on apex
