# Council of AI — GitHub defaults

This repository holds the [CSOAI-ORG](https://github.com/CSOAI-ORG) profile
and the default community-health files used when a repository does not ship
its own.

**CSOAI Ltd** (UK Companies House 16939677) is an independent AI-measurement
body. We measure AI systems against the rules that govern them, sign the
result (Ed25519), and publish what we cannot yet measure. Measurement, not
certification. We do not remediate.

| Surface | URL |
|---|---|
| Public site | [councilof.ai](https://councilof.ai) |
| Living board | [councilof.ai/api/gspc](https://councilof.ai/api/gspc) |
| Axis name lock (agents) | [`docs/GSPC_AXIS_CANON.md`](docs/GSPC_AXIS_CANON.md) — 14 board + 2 in-lane; live API wins on counts |
| Master plan | [`docs/MASTER_PLAN.md`](docs/MASTER_PLAN.md) — Moody’s × LM Arena × AG-UI one ask→does-it system |
| Estate inventory | [`docs/ESTATE_INVENTORY.md`](docs/ESTATE_INVENTORY.md) — mined surfaces, gaps, track-loss |
| 100-step execute list | [`docs/STEPS_100.md`](docs/STEPS_100.md) — status of the weekend plan |
| Frontend audit checklist | [`docs/FRONTEND_AUDIT_CHECKLIST.md`](docs/FRONTEND_AUDIT_CHECKLIST.md) — all end-user types, live test matrix |
| Monorepo + RunPod ops | [`docs/MONOREPO_RUNPOD_OPS.md`](docs/MONOREPO_RUNPOD_OPS.md) — consolidation map, GPU signing lane |
| Live audit runner | `node scripts/run-frontend-audit.mjs` — one-command persona + route check |
| Chat vs AG-UI vs OpenRouter | [`docs/CHAT_AGUI_OPENROUTER.md`](docs/CHAT_AGUI_OPENROUTER.md) — three layers, one contract |
| Verify a grade (free) | [councilof.ai/gspc-verify/](https://councilof.ai/gspc-verify/) |
| Honesty gate | [councilof.ai/honesty/](https://councilof.ai/honesty/) |
| Firewall Charter | [councilof.ai/firewall-charter/](https://councilof.ai/firewall-charter/) |

Open measurement tooling: [carder](https://github.com/CSOAI-ORG/carder) ·
[inspect-receipts](https://github.com/CSOAI-ORG/inspect-receipts) ·
[a2a-signed-receipts](https://github.com/CSOAI-ORG/a2a-signed-receipts) ·
[codabench-gspc](https://github.com/CSOAI-ORG/codabench-gspc)

This repository is **not** a package, MCP server, or installable product.
See [`ESTATE.md`](ESTATE.md) for where the site, DID apex, and measurement packages live.

## Default files

| File | Purpose |
|---|---|
| [`profile/README.md`](profile/README.md) | Account profile shown at [github.com/CSOAI-ORG](https://github.com/CSOAI-ORG) |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | How we work in public |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | What we accept, and what we do not |
| [`SECURITY.md`](SECURITY.md) | How to report a vulnerability |
| [`SUPPORT.md`](SUPPORT.md) | Where to get help |
| [`.github/FUNDING.yml`](.github/FUNDING.yml) | GitHub Sponsors only — funds the instrument, never a result |
| [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE) | Default issue forms |
| [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) | Default pull-request checklist |

## Licence

MIT © CSOAI Ltd (UK 16939677)

Contact: [nicholas@csoai.org](mailto:nicholas@csoai.org)
