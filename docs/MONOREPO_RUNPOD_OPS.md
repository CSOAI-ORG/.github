# Monorepo consolidation + RunPod ops map

**Goal:** One ops surface for canon docs, integrity products, frontend deploy gates, GPU signing lane, and HF publishing — without losing per-repo deploy boundaries.

**Audit date:** 2026-08-23

---

## Current repo map (what lives where)

```
CSOAI-ORG/
├── .github              ← THIS REPO: canon, plans, HF patches, ClaimGuard mirror, audit scripts
├── councilof-ai         ← Main frontend (Vite + CF Pages + Functions)
├── csoai-static-deploy2 ← SOVOS boards, scorecard.html, RunPod scripts, jail evidence
├── csoai-agui-wire      ← AG-UI reference (SSE session grammar)
├── claimguard           ← Integrity product (LANDED on main)
├── flywheel-nsite       ← N-site #3 CI pattern
├── signed-receipts      ← Shared Ed25519 primitive
├── carder               ← Fact-cards / valves
└── *-site (×27)         ← Industry/product sites (deferred until apex green)
```

**This repo (`.github`) is the canon + ops hub, not the app monorepo.** Product code stays in deploy repos; this repo holds:

- Axis canon and master plan
- HF ready-to-upload patches
- ClaimGuard mirror + audit runner
- RunPod ops runbook (extracted below)

---

## Proposed consolidation (phased)

### Phase 1 — Ops hub (this repo) ✅ in progress

| Path | Contents |
|---|---|
| `docs/GSPC_AXIS_CANON.md` | 14+2 axis truth |
| `docs/MASTER_PLAN.md` | Moody's × Arena × AG-UI |
| `docs/ESTATE_INVENTORY.md` | Mined estate map |
| `docs/STEPS_100.md` | Execute checklist |
| `docs/FRONTEND_AUDIT_CHECKLIST.md` | Live test matrix |
| `docs/hf-patches/` | Ready HF uploads |
| `products/claimguard/` | Mirror of integrity product |
| `scripts/run-frontend-audit.mjs` | One-command live audit |

### Phase 2 — Deploy coupling (councilof-ai)

Keep `councilof-ai` as the deploy repo but:

1. Import `functions-guard.mjs` from PR #324
2. CI calls ClaimGuard self-test against live `/api/gspc` post-deploy
3. `place-end-user-aliases.mjs` must run on every gated deploy (already in `deploy.yml`)
4. Subtree or npm package for shared canon strings (public_count, axis names)

### Phase 3 — GPU lane (csoai-static-deploy2 → ops/)

Extract RunPod scripts into documented ops lane without moving the 97-repo static tree:

| Script | Pod / target | Purpose |
|---|---|---|
| `trigger_3090_sims.sh` | `fpowppss5ngtkw` (RTX 3090) | Auto-relaunch `sim_burst.sh` — city+jail sim data |
| `trigger_nightly_pod.sh` | configurable `POD_ID` | Nightly batch keeper |
| `trigger_fix_loop.sh` | same | Fix-loop relaunch |
| `work_remote.sh` | Oracle + RunPod | Remote benchmark/funnel execution |
| `swarm_resume.sh` | RunPod → Oracle fallback | Swarm continuity |
| `runpod_migrate.sh` | one-time | Migrate SOV33 work to RunPod |

**3090 sim keeper** (`trigger_3090_sims.sh`):
- Cron hourly on Mac
- Resolves SSH endpoint fresh (RunPod endpoints drift)
- Checks `sim_burst.sh` alive; relaunches 8h burst if stopped
- Pod: `fpowppss5ngtkw` (sov-repull, RTX 3090)

**Remote work** (`work_remote.sh`):
```bash
bash work_remote.sh oracle status
bash work_remote.sh runpod deploy-refusal
bash work_remote.sh runpod run-pyrit
```

**Signing lane flow:**
```
RunPod 3090 sim_burst → evidence/harness/freeze/ → Mac sign (estate-chain-1)
  → /signed/*.json bundled in councilof-ai deploy → /api/gspc + /api/cards
```

### Phase 4 — AG-UI + MCP (same origin)

```
csoai-agui-wire  →  deploy to councilof.ai/agui
MCP worker       →  /.well-known/mcp.json (already live)
ClaimGuard       →  MCP claimguard.check + /api/chat lint
```

---

## RunPod inventory (from static-deploy2)

| Resource | ID / type | Role |
|---|---|---|
| Sim pod | `fpowppss5ngtkw` | RTX 3090, sim_burst, Ollama |
| Workhorse | `sov33-workhorse` | RTX 3090 migration target |
| A40 | on-demand | Heavy inference, 7B+ |
| H100 | on-demand | 32B+ training only |

**Budget guidance** (from `GPU_BUDGET_PLAN.md`):
- 3090: $0.22/hr — training, benchmarking, sim_burst
- A40: $0.44/hr — inference
- H100: $2.99/hr — 32B+ only

**Key evidence paths:**
- `evidence/harness/freeze/latest/govbench-owem-leaderboard.jsonl` — 129 rows, RunPod substrate
- `signed/board_living.json` — bundled into councilof-ai deploy
- Jail bank — pending McNemar gate (slot 14 UNTESTED separation)

---

## CI gates to wire across repos

| Gate | Repo | When |
|---|---|---|
| `persona-gauntlet.mjs` | councilof-ai | Post-deploy |
| `drift-guard.mjs` | councilof-ai | Scheduled + post-deploy |
| `assert-prerender-live.mjs` | councilof-ai | Post-deploy |
| `functions-guard.mjs` | councilof-ai | Post-deploy (PR #324) |
| `claimguard --self-test` | claimguard + councilof-ai | Every deploy |
| `run-frontend-audit.mjs` | .github | Weekly + on canon change |

---

## What NOT to consolidate yet

- **csoai-static-deploy2** full tree (86000+ files) — keep separate; ops scripts documented here
- **27 N-sites** — blocked until apex + HF 100/100
- **356 MCP catalog repos** — not a readiness signal
- **Dashboard spare** (`csoai-dashboard`) — undeployed, do not dual-ship

---

## Next consolidation commits (this repo)

1. ✅ `docs/FRONTEND_AUDIT_CHECKLIST.md`
2. ✅ `docs/MONOREPO_RUNPOD_OPS.md`
3. ✅ `scripts/run-frontend-audit.mjs`
4. Update `docs/STEPS_100.md` with audit gate statuses
5. Update `docs/ESTATE_INVENTORY.md` live route table
