# Execution phases — 2026-08-23

Buildable-here (`.github`) work is executed and proven; owner-gated work is flagged.

| Phase | What | Where | Status |
|---|---|---|---|
| **P1** | Real CI gate running the full batch (lint+tests+e2e) | `.github/workflows/harness-ci.yml` | ✅ done (YAML valid; runs `run-all.mjs`) |
| **P2** | Standard in-toto/DSSE receipts in the site patch (Node↔Python proven) | `docs/patches/councilof-ai-article50-detect/intoto.ts` | ✅ done (Node DSSE verifies via Python independent verifier) |
| **P3** | Detector-interop dataset scaffold (matrix + C2PA case) | `harness/` / `docs/` | ⏳ next |
| **P4** | Enhanced agent-card patch (signed_receipts + skills) | `docs/patches/councilof-ai-agent-card/` | ⏳ next |
| **P5** | Apply patches to `councilof-ai` + gated deploy | `councilof-ai` | 👤 owner-gated (token read-only; DEPLOY-LOCK) |

Guardrails: no hardcoded board counts; no certification; honesty over appearance;
never auto-deploy; every crypto claim cross-validated before handoff.
