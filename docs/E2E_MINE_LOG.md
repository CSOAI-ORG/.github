# E2E mine log — 2026-08-24 continuous loop

## Battery results (this loop)

| Gate | Result |
|------|--------|
| `e2e-integration-stack.mjs` | ✅ PASS (expanded: jail, ClaimGuard, sales, one-door `/chat` `/sov-os`) |
| `weekend-demo-smoke.mjs` | ✅ SALES-DEMO PASS |
| `run-frontend-audit.mjs` | ✅ PASS (honesty markers + scorecard stand-in fixed) |
| `mine-live-drifts.mjs` | 🔧 found **twelve-axes chat not refused** → fix in flight |
| ClaimGuard self-test + pytest | ✅ 5/5 + new `fourteen_measured` / `twelve_axes` rules |

## Drifts mined

1. **HARD (chat):** `"there are twelve GSPC axes"` returned `grounded` — should refuse. Patching councilof-ai ClaimGuard refuse list.
2. **SOFT:** apex `/scorecard` 404 — Moody’s HTML on `csoai-site.pages.dev/scorecard`; apex stand-in is `/gspc-scoreboard` (audit updated).
3. **SOFT (copy):** honesty page no longer contains `council-oowm` — audit markers → Elo/honesty/MEASURED.

## Improvements shipped this loop

- ClaimGuard: `claim.fourteen_measured` + `claim.twelve_axes` rules + self-test
- E2E: jail MEASURED/TIE (live), attestation, ClaimGuard refuse, sales surfaces, `/chat` `/sov-os` one-door
- Frontend audit: persona `mustAny`, scorecard stand-in, pricing/start routes
- New miner: `scripts/mine-live-drifts.mjs`
- Batch gates now chain: ClaimGuard → e2e → weekend-demo → mine → frontend-audit

## Run

```bash
node scripts/batch-run-gates.mjs
node scripts/mine-live-drifts.mjs
```
