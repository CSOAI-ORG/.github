# Council OS — engine kit (reference harness)

**This is NOT councilof.ai.** It is a self-contained reference rig living in the
`.github` canon/ops repo so the moves can be proven end-to-end offline. The real
site is the Vite/React SPA in [`CSOAI-ORG/councilof-ai`](https://github.com/CSOAI-ORG/councilof-ai)
(Cloudflare Pages). The engines here are framework-agnostic and are meant to be
**imported into Council OS**, not shipped as a separate site.

`server.py` (stdlib) and `web/index.html` are a **dev/QA console only** — throwaway
scaffolding to exercise the engines. Do not treat them as the product UI.

## What is real vs scaffolding

| File | Role | Destination inside Council OS |
|---|---|---|
| `../products/claimguard/` | ClaimGuard v0.3 (Article 50 / C2PA + `--intoto`) | PyPI + `CSOAI-ORG/claimguard`; MCP `claimguard.check`; CI gate in `councilof-ai` |
| `detect.py` | Article 50 detection engine → signed receipt | `councilof-ai` Cloudflare Function `POST /api/detect` (port to TS or run via RunPod wire) |
| `receipts.py` | in-toto Statement v1 + DSSE | `CSOAI-ORG/signed-receipts` (canonical import) |
| `tlog.py` | hash-chained transparency log | `councilof-ai` `GET /api/attestations/log` |
| `verify_external.py` | independent DSSE verifier (interop proof) | test/tooling; proves 3rd-party verifiability |
| `schemas/*.json` | published predicate schemas | served at `councilof.ai/schemas/*` + Zenodo DOI |
| `board.py` | **local fixture only** | replaced by live `GET /api/gspc` |
| `register.py` | reflexive capability register | `councilof-ai` Integrity tile / status page |
| `server.py`, `web/index.html` | **QA console only** | discard — the SPA is the real UI |

## Integration path (owner-gated, per STEPS_NEXT_100 Block H)
1. Port `detect` verify to a `councilof-ai` Cloudflare Function `/api/detect`
   (reuse `claimguard.c2pa` logic; TS mirror keeps finding codes stable).
2. Sign verdicts with the board key (not the demo key) — see `KEY_GOVERNANCE.md`.
3. Add the UI as **real SPA components** in `councilof-ai` matching its design
   system — do **not** hand-roll a separate site (this console's styling is not canon).
4. Respect DEPLOY-LOCK: gated deploy only; never enable Pages Git auto-deploy.

## Run the QA console
```bash
python3 harness/server.py 8787       # dev only
node scripts/run-all.mjs             # lint + tests + e2e battery
python3 harness/e2e_harness.py       # 19-check end-to-end
```
