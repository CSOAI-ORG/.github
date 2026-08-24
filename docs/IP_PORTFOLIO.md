# IP portfolio — valuation / sales inventory

**Entity:** CSOAI Ltd (UK Companies House **16939677**) · trading as Council of AI  
**Posture:** Independent measurement body. Measurement, not certification.  
**This file inventories assets for diligence and sales conversation — not a revenue forecast.** No ARR, bookings, or customer counts are asserted here.

Truth rail: [`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc)

---

## Portfolio map

| Asset | What it is | Where it lives | Diligence hook |
|---|---|---|---|
| **ClaimGuard** | Deterministic claim auditor: Ed25519 attestation + RFC 8785 canonical JSON + natural-language overclaim rules | [`products/claimguard/`](../products/claimguard/) · `CSOAI-ORG/claimguard` | Self-test proves mutation after sign fails; rejects “16 measured axes”, public Elo, certification language |
| **GSPC 14-axis instrument** | Quotable board of 14 axes; public ruling 13 of 14 measured; +2 in-lane honesty (non-quotable) | Living board API + axis banks | Canon [`GSPC_AXIS_CANON.md`](GSPC_AXIS_CANON.md) |
| **Method DOI** | Frozen method citation | Zenodo `10.5281/zenodo.21991104` (record `21991105`) | Cite on cards; evidence DOI `10.5281/zenodo.21973002` |
| **Signed receipts** | Card / board signatures; inspectable | `signed-receipts`, `inspect-receipts`, board `site_attestation` | Recompute at `/gspc-verify/` |
| **did:web:csoai.org** | Publishing / key identity | `csoai.org/.well-known/did.json` (static apex) | Keys not behind the SPA login |
| **Living board API** | Machine-readable grades, intervals, SEPARATED/TIE/UNTESTED | `GET /api/gspc` | Schema `csoai.gspc-axes/0.5` |
| **Arena** | Law-graded contest UX | `councilof.ai/arena` · MCP `enter-arena` | Not preference Elo as public GSPC grade |
| **HF banks ×14** | One public dataset per board axis under `csoai/` | gov, agi, prv, asi, mcp, oss, mach, care, xr, det, art5, swarm, affect, jail | Meta banks + Spaces (affect/jail Spaces still open) |
| **MCP tools** | Agent surface | `/.well-known/mcp.json` → worker | `measure` · `verify` · `jail-probe` · `enter-arena` (+ `claimguard.check` wire) |
| **One-door Council OS** | Single public OS door | `https://councilof.ai/?lobby=home` | `/ag-ui`, `/agui`, `/chat` redirect — no second console |

---

## ClaimGuard (integrity product)

- **Crypto:** Ed25519 over RFC 8785 JCS of payload minus `site_attestation`  
- **Checks:** attestation → payload completeness → claim support  
- **Sales line:** “The receipt for your claims” — fails closed on our own overclaims  
- **Not:** certification, remediation, or a substitute for McNemar / bank publication  

Spec: [`products/claimguard/CLAIMGUARD_PRODUCT_SPEC_2026-08-22.md`](../products/claimguard/CLAIMGUARD_PRODUCT_SPEC_2026-08-22.md) · MCP wire: [`CLAIMGUARD_MCP.md`](CLAIMGUARD_MCP.md)

---

## GSPC instrument + DOI

| Set | Count | Public language |
|---|---|---|
| Board slots | 14 | “14-slot GSPC board” |
| Measured ruling | 13 of 14 | Live `totals.public_count` |
| In-lane | +2 | Honesty probes — not board-quotable |
| Elo league on `/api/gspc` | none | Do not value as if it existed |

Method DOI belongs on axis cards and diligence packs; counts always defer to the live API.

---

## Receipts + identity

```
canonical JSON  →  SHA-256  →  Ed25519 sign  →  publish
verify: drop content_id + signature, recompute, check key at did:web:csoai.org
```

Browser path: [`https://councilof.ai/gspc-verify/`](https://councilof.ai/gspc-verify/)

---

## Living board + Arena

| Surface | IP character |
|---|---|
| Living board API | Continuous published measurement stamp (Moody’s-style scorecard data) |
| Scoreboard UI | `/gspc-scoreboard` render of predicates only |
| Arena | LM-Arena-style contest UX bound to law-graded outcomes |
| Honesty / Elo | Optional separate disclosure surfaces — **not** GSPC public grade |

---

## HF banks ×14

| # | Axis | Dataset |
|---|---|---|
| 1–14 | governance … jail | `csoai/gspc-gov` … `csoai/gspc-jail` (see canon table) |

Inbound spray path: signed results → `csoai/csoai-benchmarks` → `/api/gspc` ([`NSITE_AEO_PACK.md`](NSITE_AEO_PACK.md)).

---

## MCP tool surface

| Tool | Job |
|---|---|
| `measure` | Run / fetch measurement against frozen rules |
| `verify` | Recompute / check signed artefact |
| `jail-probe` | Jail-axis probe (separation honesty) |
| `enter-arena` | Contest entry |
| `claimguard.check` | (wire) refuse overclaims against live board |

Catalogue: [`https://councilof.ai/.well-known/mcp.json`](https://councilof.ai/.well-known/mcp.json)

---

## One-door Council OS

Public product door is **Council Lobby / Council OS** only:

`https://councilof.ai/?lobby=home`

Ask → board → verify → arena is the sales path ([`WEEKEND_DEMO.md`](WEEKEND_DEMO.md)). Secondary AG-UI hosts are reference or redirect — not a second brand OS.

---

## What is not in the portfolio (do not invent)

- Public Elo league as a GSPC ranking product  
- Certification marks or regulator approvals  
- Guaranteed insurer reliance  
- Hardcoded revenue multiples or “pipeline” figures in this repo  

Commercial conversation stays on **signed evidence artefacts**, **assessment work**, and **enterprise onboarding** — never a fee for a ranking or placement. Surface status: [`REVENUE_SURFACES.md`](REVENUE_SURFACES.md).
