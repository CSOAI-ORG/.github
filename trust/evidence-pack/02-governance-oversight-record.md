# Governance & Oversight Record — CSOAI Ltd

**Entity:** CSOAI Ltd (UK #16939677)  
**As of:** 2026-08-24

## 1. Ownership and legal structure

| Field | Value |
|-------|-------|
| Legal name | CSOAI Ltd |
| Jurisdiction | England & Wales |
| Companies House | 16939677 |
| Public brand | Council of AI (councilof.ai) |
| Measurement director | Nicholas Templeman, Founder |
| Contact | nicholas@csoai.org (14-day right-of-reply on corrections) |

## 2. Oversight structure

- **Measurement doctrine:** Scores are never sold. Regulators read free. No token surfaces.
- **Impartiality firewall:** Council instruments are structurally excluded from the benchmark-quality register (enforced in code).
- **ClaimGuard:** Every public claim is checked against signed board state before publish (`measure/claimguard` + `ops/banned-strings`).
- **Corrections ledger:** Published mistakes are appended, never silently edited (`GET /api/corrections` — 13+ self-caught corrections, signed).
- **Sitting rulings:** Board composition changes (e.g. 14-slot ruling 2026-08-18) are documented with provenance, not retroactive edits.

## 3. Escalation paths

| Event | Owner | Action |
|-------|-------|--------|
| Measurement challenge | Measurement director | `POST /api/challenge` — receipt issued; corrections appended if upheld |
| Provision amendment | Reg-watch pipeline | Daily re-hash; measurements go stale on text change — re-attest required |
| Signing key compromise | Estate chain | External watchdog (10-min dead-man's switch); boot-time fail-fast assertions |
| Public claim dispute | Named owner | 14-day right-of-reply; corrections ledger entry if wrong |

## 4. Professional indemnity

£5M PI cover advertised for managing-agent due diligence (policy CHPR5355800XB). Coverage details available on request to qualified counterparties.

## 5. Regulatory posture

CSOAI **measures** AI system behaviour against in-force regulatory provisions. It does **not** issue regulatory determinations. Crosswalk surfaces map measurements to EU AI Act, UK framework, NIST AI RMF, and other cited provisions — determination remains with competent authorities.

## 6. Lanes propose, owner disposes

Owner-gated actions (insurer outreach, marketplace seller registration, ORGADMIN terms, G-Cloud application) require explicit owner approval. Overnight lanes produce drafts and staged scripts only.
