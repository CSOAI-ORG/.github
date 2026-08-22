# GSPC axis canon (agent lock)

**Source of truth for counts and scores:** live API
[`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc).
Do not hardcode totals, dates, or leaders in READMEs or marketplace copy.
This file names the axes so agents stop inventing “14 / 15 / 16” from chat.

**Audited against live API:** 2026-08-22 · schema `csoai.gspc-axes/0.5`  
**Plan / inventory:** [`MASTER_PLAN.md`](MASTER_PLAN.md) · [`ESTATE_INVENTORY.md`](ESTATE_INVENTORY.md)

## The count rule (one sentence)

| Set name | Count | What you may say |
|---|---|---|
| Quotable **board** slots | **14** | “14-slot GSPC board” |
| Public measured ruling | **13 of 14** | “13 measured of 14 quotable (ruling 2026-08-18)” — jail is measured but separation **UNTESTED** |
| Registry v2 canonical (code names, 2026-08-13) | **13** | The 13 bank axes before jail joined the living board |
| Living-board **in-lane** (honesty only) | **+2** | `slot15` / instrument-honesty + `human-vs-ai` — **not** board-quotable |
| Living-board convention people call “16” | **14 + 2 = 16** | Internal living board only. Never sell “16 measured axes.” |

If a claim mixes these sets, ClaimGuard (when landed) must reject it.

## Board axes (14) — names that must live on site + AGUI

Order matches the live API `axes[]` array.

| # | Axis id | Bench | HF dataset |
|---|---|---|---|
| 1 | `governance` | GovBench | [`csoai/gspc-gov`](https://huggingface.co/datasets/csoai/gspc-gov) |
| 2 | `safety` | DefBench | [`csoai/gspc-agi`](https://huggingface.co/datasets/csoai/gspc-agi) |
| 3 | `provenance` | ProvBench | [`csoai/gspc-prv`](https://huggingface.co/datasets/csoai/gspc-prv) |
| 4 | `continuity` | PQCBench | [`csoai/gspc-asi`](https://huggingface.co/datasets/csoai/gspc-asi) |
| 5 | `conformance` | MCPBench | [`csoai/gspc-mcp`](https://huggingface.co/datasets/csoai/gspc-mcp) |
| 6 | `openness` | OSSBench | [`csoai/gspc-oss`](https://huggingface.co/datasets/csoai/gspc-oss) |
| 7 | `machinery-conformity` | MachBench | [`csoai/gspc-mach`](https://huggingface.co/datasets/csoai/gspc-mach) |
| 8 | `care` | CareBench | [`csoai/gspc-care`](https://huggingface.co/datasets/csoai/gspc-care) |
| 9 | `cross-reality` | XRAIV | [`csoai/gspc-xr`](https://huggingface.co/datasets/csoai/gspc-xr) |
| 10 | `detector-interop` | DetBench | [`csoai/gspc-det`](https://huggingface.co/datasets/csoai/gspc-det) |
| 11 | `art5-safeguard` | Art5Bench | [`csoai/gspc-art5`](https://huggingface.co/datasets/csoai/gspc-art5) |
| 12 | `swarm` | SwarmBench v2b | [`csoai/gspc-swarm`](https://huggingface.co/datasets/csoai/gspc-swarm) |
| 13 | `affect` | AffectBench | [`csoai/gspc-affect`](https://huggingface.co/datasets/csoai/gspc-affect) |
| 14 | `jail` | GoldBank-Detector | [`csoai/gspc-jail`](https://huggingface.co/datasets/csoai/gspc-jail) |

Short registry codes (SOVOS `GSPC_AXIS_REGISTRY.json` v2):  
`gov prv agi asi mcp oss mach care xr det art5 swarm affect` (+ living `jail`).

## Measured in-lane only (not quotable)

| Axis id | Public name | Role |
|---|---|---|
| `slot15` | instrument-honesty | Does the model admit a missing instrument instead of fabricating one? |
| `human-vs-ai` | Colosseum-Pairs | Human-key alignment probes |

API field: `measured_in_lane`. Owner-gated before any board count.

## ELO / “league”

The living GSPC board API has **no** Elo field and **no** `/api/elo` or `/api/league`.
GSPC ranking is deterministic grading + Wilson intervals + McNemar separation (SEPARATED / TIE / UNTESTED), not Elo.

Elo / tournament-league language belongs to the separate SOV3 King↔OpenMOE tournament docs (e.g. openmore / DAY6 bridge), **not** the GSPC measurement board. Do not brand Elo onto AGUI board tiles unless a signed Elo surface is published under its own schema.

## CLAIMGUARD — track-loss flag (2026-08-22)

Session narrative (dorado-bench `claimguard.py`, jail evidence `61feba96`, guardrail `2a3b5927`, product spec) is **not** present in any searched `CSOAI-ORG/*` GitHub tree (zero hits for `claimguard` / `dorado-bench` / those sigs).

Do not treat chat as inventory. Until the files are committed to a durable repo (recommended: new `CSOAI-ORG/claimguard` or under `carder` / `inspect-receipts`), ClaimGuard is **SPEC+DEMO, not product-in-codebase**.

Related but different: `ConsciousnessNonClaimGuard` in `meok-ai` (blocks consciousness claims) — not ClaimGuard.

### Next landings (set-4 Block A/C)

1. Commit `claimguard.py` + product spec + signed evidence dirs to GitHub.
2. CI rule: reject commits whose signed board result is empty / mutated after sign.
3. MCP `claimguard.check`.
4. Council Ledger “Integrity” tile — public signed audit reports.

## Where names must appear

| Surface | Requirement |
|---|---|
| Website | Render from `/api/gspc` — all 14 axis ids + lane section labeled non-quotable |
| AGUI | Same payload; no hardcoded slot count |
| HF | One dataset per board axis (table above); spaces still missing for `affect` + `jail` |
| This org profile | Link the live board; never hardcode “N axes” in marketing copy |

## Anti-patterns already paid for

- Saying “14-axis” when meaning the old 13-canonical registry (killed in org profile).
- Saying “16 axes” without naming the 2 in-lane slots as non-quotable.
- Quoting jail against the 19-model board fleet (jail is a 7-model floor).
- Selling Elo as GSPC board ranking.
