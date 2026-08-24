# Technical System Description — CSOAI GSPC Measurement Estate

**Entity:** CSOAI Ltd (UK Companies House 16939677)  
**Surface:** Council of AI — https://councilof.ai  
**As of:** 2026-08-24  
**Status:** Measurement, not certification

## 1. What the system does

CSOAI operates an independent AI-governance **measurement** instrument called GSPC (Governance · Safety · Provenance · Continuity). The instrument comprises 14 quotable slots on a public board; **13 measured of 14** as of the 2026-08-18 sitting. Each measured axis carries a frozen item bank, deterministic grading predicates (never LLM-as-judge), fleet run results, Wilson confidence intervals where n≥30, and McNemar separation tests where applicable.

The system publishes:

- A live Ed25519-signed board (`GET /api/gspc`)
- Per-axis Hugging Face datasets (frozen splits, CC-BY-4.0)
- Stranger-verifiable cards (`/gspc-verify` — 60-second in-browser verification)
- An insurability evidence pack (`GET /api/evidence-pack`)
- East-West crosswalk surfaces mapping measurements to EU, UK, US, Illinois, and China GB/T alignment frames

## 2. Model and data

| Component | Detail |
|-----------|--------|
| Board fleet | 19-model fleet (8 tuned council specialists + 6 base models + frontier cross-lab models) for 13 canonical axes |
| Jail axis (slot 14) | Separate 7-model fleet; separation UNTESTED; bank pending full publication |
| Grading | Deterministic predicates on 15,580 per-item rows (0 transport errors) |
| Reproducibility | Harness public in `csoai-static-deploy2` (commit bb15589c lineage) |
| Signing | Ed25519 (`did:web:csoai.org#estate-chain-1` / `#board-attestation-1`) |
| License | Board data CC-BY-4.0; attribute Council of AI, CSOAI Ltd 16939677 |

## 3. Outputs

All outputs are **signed measurement state**, never ranked scores for money:

- JSON board with per-axis accuracy, leader, separation status, harm metrics
- Evidence packs mapping receipts into underwriter-requested categories
- Benchmark-quality register (third-party benchmark process integrity — unsolicited, impartiality firewall in code)
- Regulator-facing surfaces are **free forever** where access tiers are described

## 4. What the system is not

- Not certification, accreditation, or conformity assessment
- Not legal determination or enforcement
- Not a parametric insurance trigger (evidence input only)
- No token, treasury, or settlement surfaces

## 5. Verification

Any third party can:

1. Fetch `/.well-known/did.json` for public keys
2. Canonicalise board JSON (RFC 8785 sorted keys)
3. Verify Ed25519 signature in-browser at `/gspc-verify`

**DOI (methodology spine):** 10.5281/zenodo.21991104
