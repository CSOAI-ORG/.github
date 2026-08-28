# Monitoring & Incident Log — CSOAI Measurement Estate

**As of:** 2026-08-24  
**Retention:** Append-only; corrections never deleted

## 1. Performance metrics (board-level)

| Metric | Value | Source |
|--------|-------|--------|
| Measured axes | 14 of 14 (live) | `GET /api/gspc` |
| Total items (board) | 887 | Signed board totals |
| Separated leads | 4 | McNemar p<0.05 |
| Ties | 9 | Lead not statistically separated |
| Untested separations | 1 | Jail axis |
| Mean macro-F1 (measured) | 0.7528 | Board totals |
| Mean accuracy (leaders) | 0.7318 | Board totals |
| Mean fleet mean | 0.5443 | Board totals |
| Mean harm | 0.4877 | Severity-weighted failure mass |
| Mean unparsed rate | 0.0813 | Reported UNMEASURED, never scored wrong |

**Living board stamp:** 2026-08-18T03:22:16Z, signed (`board_living.json` lineage).

## 2. Active monitoring controls

| Control | Frequency | Owner |
|---------|-----------|-------|
| Reg-watch provision re-hash | Daily | Automated pipeline |
| Signing chain integrity | Continuous | External watchdog (10-min) |
| Site attestation verify | On every board fetch | Client-side `/gspc-verify` |
| E2E revenue/gate suite | CI + overnight Ralph loop | LANE-OPS |
| ClaimGuard publish gate | Pre-public | LANE-OPS |

## 3. Incident documentation

### Corrections ledger (selected)

All incidents are published at `GET /api/corrections`. Representative entries:

| # | Date | Summary | Resolution |
|---|------|---------|------------|
| — | 2026-08 | Stale Zenodo DOI reference | Corrected to 10.5281/zenodo.21991104 |
| — | 2026-08 | Missing licence field on bench-card | Fixed same day (CC-BY-4.0) |
| 68 | 2026-08 | Gallagher Re index-usage claim | UNVERIFIED — no submission channel |
| 69 | 2026-08 | G-Cloud 15 window | Closed 30 Jan 2026; reopen ~early 2028 |

*Full ledger: signed, appended-never-edited at `/api/corrections`.*

### Operational incidents (2026-08)

| Date | Event | Impact | Status |
|------|-------|--------|--------|
| 2026-08-24 | `/api/auth/me` Ed25519 verify regression | DSH auth 401 | Fixed (#475), live 200 |
| 2026-08-19 | MCP registry 1.0.1 missing repository/title/packages | Incomplete registry entry | Republish 1.0.2 staged (EXE 161/162) |

## 4. Drift detection

- Measurement records carry `measured_on` timestamps and provision version pins
- When underlying regulatory text changes, affected axes are marked stale pending re-attestation
- Market rail (AI-theme index) is dev-grade (yfinance) — licensed feed swap on roadmap; limitation documented in evidence pack API

## 5. Uptime and availability

Primary surface: Cloudflare Pages (`councilof.ai`). Revenue E2E gates verify live endpoints including `/api/gspc`, `/api/evidence-pack`, `/api/counters`, `/api/eunomia-data`.
