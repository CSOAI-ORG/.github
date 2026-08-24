# Armilla Prep — OWNER-GATED (draft only)

**Timeline:** ≥90-day prep before coverage start  
**Route:** Broker-distributed · hello@armilla.ai (NOT sent by lanes)

## Governance questionnaire (draft)

| Question | Draft answer |
|----------|--------------|
| Ownership structure | CSOAI Ltd, UK #16939677, single founder |
| Oversight | Measurement director + ClaimGuard + corrections ledger |
| Incident history | See `trust/evidence-pack/03-monitoring-incident-log.md` |
| Scope limits | Measurement only; no certification; scores never sold |
| Human approval gates | Public publish, marketplace seller reg, insurer outreach |

## Technical assessment input list

Armilla platform tests: accuracy, fairness, robustness, security, red-team.

| Input | Source |
|-------|--------|
| Model performance | `GET /api/gspc` — per-axis accuracy, separation, harm |
| Risk controls | ClaimGuard, signing chain, reg-watch drift detection |
| Benchmark methodology | Zenodo DOI 10.5281/zenodo.21991104 |
| Verification | `/gspc-verify` — stranger Ed25519 check |
| Limitations | Evidence pack §6 — no SOC2/ISO42001 yet |
