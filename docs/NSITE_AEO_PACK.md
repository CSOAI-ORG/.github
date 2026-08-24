# N-site AEO pack — extractable spray spec

**Goal:** One shared AEO / AG-UI contract for industry `*-site` shells — brand and skills per site, instrument and receipts shared.  
**Do not** fan out 27 divergent `index.html`s before Phase 3 HF lock + Phase 1 fat apex ([`MASTER_PLAN.md`](MASTER_PLAN.md) Phase 4).

---

## Shared contract (every N-site)

| Layer | Requirement |
|---|---|
| **AEO** | Machine-readable answers cite living board, not hardcoded leaders or axis counts |
| **AG-UI / lobby grammar** | Ask → tool → HITL (if write) → ledger; same session shape as Council OS |
| **Truth rail** | `GET https://councilof.ai/api/gspc` — schema `csoai.gspc-axes/0.5` |
| **Verify** | Link `https://councilof.ai/gspc-verify/` (trailing slash) |
| **Brand** | Cream / ink measurement body; site name is the hero; no purple SaaS defaults |
| **ClaimGuard** | Any grade / axis-count claim passes `products/claimguard/` rules before publish |

### Embedded canon (14+2, no Elo public)

Copy this block into pack README and CI assertions:

```
Quotable board slots:     14
Public measured ruling:   13 of 14
In-lane (not quotable):   +2  (slot15 / instrument-honesty, human-vs-ai)
Living “16” convention:   14+2 internal only — never sell “16 measured axes”
Public Elo on GSPC board: DOES NOT EXIST — Wilson + McNemar only
Tone:                     Measurement, not certification
```

Full names: [`GSPC_AXIS_CANON.md`](GSPC_AXIS_CANON.md).

---

## Outbound — instrument + flywheel

| Piece | Repo / surface | Duty |
|---|---|---|
| GSPC instrument | Living board + axis banks | Source of grades and empty cells |
| Flywheel CI | `CSOAI-ORG/flywheel-nsite` | Spray pack build, link check, claim lint |
| Pack artefact | extractable AEO/AGUI bundle | Brand tokens + skills + board widgets only |
| Method DOI | `10.5281/zenodo.21991104` | Cite on axis cards / site footnotes |

Outbound spray **pushes** site shells that deep-link measure / verify / arena — they do not host a second truth rail.

---

## Inbound — signed results → HF → API

```
N-site / harness run
  → signed result (Ed25519, RFC 8785 canonical JSON)
  → Hugging Face  csoai/csoai-benchmarks  (and per-axis csoai/gspc-*)
  → councilof.ai  GET /api/gspc
```

| Gate | Rule |
|---|---|
| Signature | Fail closed if attestation missing or mutated post-sign |
| Axis ids | Only the 14 board ids (plus labeled in-lane) |
| Publish | Empty cells stay empty; no fill-for-marketing |
| Claim text | ClaimGuard before README / AEO blob / lobby copy |

---

## Prove order (do not skip)

| # | Site family | Why first |
|---|---|---|
| 1 | **openmoe** | Richest shell; proves pack extraction |
| 2 | **landlaw** | Second vertical; proves brand swap without forking instrument |
| 3 | **diyhelp** | Consumer tone; proves AEO answers stay measurement-honest |
| 4 | **fintech** | Industry pack start |
| 5 | **healthtech** | Industry pack + care language — never imply clinical certification |

Only after 1–3 are green: govtech → regtech → care. Recreational long-tail waits.

---

## Pack contents (minimum extractable set)

```
nsite-aeo-pack/
  aeo/
    board-cite.json          # how answers must cite /api/gspc
    claim-rules.md           # mirror ClaimGuard overclaims
  agui/
    session-grammar.md       # ask / run / consent / ledger
    deep-links.ts            # lobby=home, gspc-verify/, arena
  brand/
    tokens.css               # cream/ink variables per site override
  ci/
    flywheel-nsite.yml       # link + claim + board schema checks
  README.md                  # this prove order + canon block
```

Sites may add **skills** and **sector copy**. Sites may not add a private Elo board or a second axis count.

---

## Fail closed

- Hardcoded “N axes” in marketing HTML  
- Elo / league as public GSPC grade  
- “Certified” / “approved” language  
- Jail “separation resolved” while UNTESTED  
- Spray before openmoe → landlaw → diyhelp prove  

Status of apex stranger routes: [`REVENUE_SURFACES.md`](REVENUE_SURFACES.md). Demo script: [`WEEKEND_DEMO.md`](WEEKEND_DEMO.md).
