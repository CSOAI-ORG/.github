# East-West 100-Move Play — Execution Tracker

Date: 2026-08-24 · Companion to PLAYBOOK-GTM-300-2026-08-24  
E2E gate: `node scripts/e2e-east-west.mjs` · Full stack: `node scripts/batch-run-gates.mjs`

## Live E2E snapshot (2026-08-24 ~09:52 UTC)

| Gate | Result |
|------|--------|
| batch-run-gates.mjs | **PASS** |
| e2e-lobby-nav.mjs | **PASS** (5 soft — PR #452 redirects pending deploy) |
| e2e-integration-stack.mjs | **PASS** |
| weekend-demo-smoke.mjs | **PASS** |
| mine-live-drifts.mjs | **PASS** (1 soft: apex /scorecard 404) |
| run-frontend-audit.mjs | **PASS** (8/8 personas) |

Run with me anytime:

```bash
node scripts/batch-run-gates.mjs
node scripts/e2e-east-west.mjs
node scripts/e2e-lobby-nav.mjs
```

## Done-definition checklist (verifiable today)

| Box | Status | Evidence |
|-----|--------|----------|
| First cross-border signed card | **NOT LIVE** | No cross-border card type on /api/cards yet (M2·012) |
| Sample pack stranger-verified | **NOT LIVE** | M3·021 |
| Pricing published | **OWNER-BLOCKED** | /payg redirects; ruling pending M6·051 |
| First inbound (ledger row) | **NOT LIVE** | /api/receipts/latest `UNPUBLISHED` count:0 ✓ honest |
| Doctrine intact | **PARTIAL** | 13/14 canon ✓ · ClaimGuard ✓ · /challenge 404 · crosswalk uses legacy GRC copy |

## Movement status (100 moves)

Legend: ✅ live/testable · 🔧 in progress · ⏰ clocked · 🔒 OWNER-BLOCKED · ⬜ not started

### M1 Crosswalk canon (001–010)

| Move | Tier | Status | Notes |
|------|------|--------|-------|
| 001 | 👑 | ⬜ | cibola `axes/domains/cross-border.json` scaffold exists; EU/UK/IL/CN v1 tables NOT frozen |
| 002 | 💎 | ⬜ | EU table with Art 9–15 rows |
| 003 | 🥇 | ⬜ | UK DRCF table |
| 004 | 🥇 | ⬜ | Illinois SB 315 ⏰ audits Jan 1 2028 |
| 005 | 🥇 | ⬜ | China GB/T honest line |
| 006 | 💎 | ⬜ | Methodology + determination banner |
| 007 | 🥇 | ⬜ | Supersession chain |
| 008 | 🥇 | ⬜ | US row (TRAIGA ⏰ Sep 1) |
| 009 | 🥇 | 🔧 | ClaimGuard in .github + chat; East-West row CI pending |
| 010 | 🥇 | 🔒 | M1 exit — OWNER checklist |

**Current:** `/crosswalk/` live (83KB) — GRC framework matrix, NOT yet East-West v1 canon.

### M2 Schema & cards (011–020)

| Move | Status | Notes |
|------|--------|-------|
| 011–012 | ⬜ | Cross-border card type + first card |
| 013 | ⬜ | Frozen vectors |
| 014 | 🔧 | Schema URLs → councilof.ai (interim); dorado.dev sweep pending |
| 015 | ⬜ | Conformance runner |
| 016–020 | ⬜ | Domain freeze, I-D-01, index, lint, exit |

### M3 Evidence packs (021–030)

All ⬜ — sample pack (021) gates launch.

### M4 Front-end takeover (031–040)

| Move | Status | Notes |
|------|--------|-------|
| 031 /east-west | ⬜ | **404** on apex today |
| 032 | ⬜ | Board cross-border row on /api/gspc |
| 033 | 🔧 | /gspc-verify live; crosswalk render in verify pending |
| 034 /challenge | ⬜ | **404** — JC-D4 open |
| 035 | ⬜ | llms.txt + agent-card East-West update |
| 036 | ⬜ | cibola Pages nav |
| 037 | ⬜ | meok.ai touchpoint |
| 038 | 🔧 | /regulators/ live (117KB) — desk wiring pending |
| 039 | ⬜ | Codename CI |
| 040 | 🔒 | M4 exit — OWNER |

**Shipped (Council OS):** PR [#452](https://github.com/CSOAI-ORG/councilof-ai/pull/452) — Benchmarkers tab, /mcps registry, redirects (await deploy).

### M5 Regulator rails (041–050)

| Move | Status | Notes |
|------|--------|-------|
| 041–042 | ⏰ | DRCF Sep 2 — Art 73(7) intake proposal |
| 043 | ⬜ | Four jurisdiction desk pages |
| 044–048 | ⬜ | White-label kits, TRAIGA watch, free-forever terms, onboarding, CI |
| 049 | 🔒 | Intro letters — OWNER sends |
| 050 | 🔒 | M5 exit |

### M6 Commercial (051–060)

All 🔒/⬜ — pricing ruling (051) OWNER-BLOCKED.

### M7 Measurement ops (061–070)

| Move | Status | Notes |
|------|--------|-------|
| 071 | ⬜ | Cross-border domain board |
| 072–079 | ⬜ | Banks, corpus, gates, jail honesty, nightly, disclosure, CI, lint |
| 080 | 🔒 | M7 exit |

### M8 Trust & hygiene (071–080)

| Move | Status | Notes |
|------|--------|-------|
| 071 P0-1 DID | 🔒 | did:web:csoai.org on councilof.ai — id/host mismatch probe |
| 072 domains | 🔒 | £30 cibola.dev + getcibola.com — JD-D1 |
| 073 | ⬜ | dorado.dev migration sweep |
| 074 UKIPO | 🔒 | £170 trademark |
| 075 | ⬜ | Test-identity re-sign (JD-D2) |
| 076–080 | ⬜ | Link lint, key custody, corrections, grammar audit, exit |

### M9 Press (081–090)

All ⬜/🔒 — K3 drafts, OWNER sends.

### M10 Value Ledger (091–100)

| Move | Status | Notes |
|------|--------|-------|
| 091 | ⬜ | Six event types wired |
| 092–099 | ⬜ | Pipelines + JL.5 CI |
| 100 | 🔒 | LAUNCH VERDICT — OWNER |

**Honest today:** `/api/receipts/latest` → `UNPUBLISHED`, `count: 0`.

## First 5 moves (execute in order)

1. **072** 🔒 OWNER — Buy cibola.dev + getcibola.com (£30)
2. **071** 🔒 OWNER — P0-1 DID commit (resolvable issuer)
3. **014 + 075** 🔧 LANE — Schema URLs → councilof.ai; re-sign vectors
4. **001–002** K3+POD — Crosswalk v1 signed + EU table
5. **041–042** ⏰ Sep 2 — DRCF filing with Art 73(7) intake

## PRs open

| Repo | PR | What |
|------|-----|------|
| councilof-ai | [#452](https://github.com/CSOAI-ORG/councilof-ai/pull/452) | Council OS nav wiring |
| .github | [#9](https://github.com/CSOAI-ORG/.github/pull/9) | Lobby + East-West E2E gates |

## Owner gates (cannot agent-execute)

- DEPLOY-LOCK (Pages Git auto-deploy off councilof-ai)
- AGUI_WIRE_URL (RunPod :8785)
- HF_TOKEN (axis patch upload)
- 051 pricing ruling · 052 x402 rail · 058 first sale
- 071 DID · 072 domains · 074 UKIPO
