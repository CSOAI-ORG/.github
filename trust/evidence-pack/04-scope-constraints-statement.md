# Scope-Constraints Statement — CSOAI GSPC Measurement

**As of:** 2026-08-24

## 1. What the system cannot do

| Constraint | Detail |
|------------|--------|
| Certification | CSOAI does not certify, accredit, or issue conformity assessments |
| Legal determination | No regulatory rulings; crosswalks are measurement mappings only |
| Enforcement | No blocking, takedown, or compliance orders |
| Score commerce | Scores are never sold; no money in either direction with anything ranked |
| Token / treasury | No coin, ICO, or settlement surfaces |
| LLM-as-judge | All predicates are deterministic; unparsed responses are UNMEASURED, never scored as wrong |
| Parametric triggers | Evidence packs are underwriting input, not aiSure-style business-metric SLAs |

## 2. Human approval gates

| Action | Gate |
|--------|------|
| Public surface publish | ClaimGuard + banned-strings pass required |
| Board sitting rulings | Measurement director sign-off with documented provenance |
| DOI minting | Irreversible (locks rename/delete/visibility) — owner confirms final names |
| Marketplace seller registration | Owner accepts T&Cs (AMMP, ORGADMIN, Datarade commission) |
| Insurer outreach | Owner approves (AIUC-1, Armilla, Munich Re aiSure, Testudo) |
| G-Cloud application | Framework window closed; prep only until ~early 2028 reopen |

## 3. Measurement honesty rules

- **Grammar locked:** cite live `totals.public_count` from `/api/gspc` (currently "14 measured of 14 quotable"); never invent 22 axes
- **TIE means TIE:** Point-estimate lead without McNemar separation is not counted as a win
- **Fleet vs leader:** `mean_accuracy` averages leaders; `mean_fleet_mean` averages fleets — difference is selection, not skill
- **Reported vs measured:** Published aggregates in REPORTED state are never blended into MEASURED
- **First-of-niche claims:** "First dedicated governance leaderboard we could find on HF" — never "the first ever" unqualified

## 4. Data boundaries

- Third-party benchmark register: subjects did not participate; impartiality firewall excludes own instruments
- Human baseline figures: published aggregates only; no live human-capture pipeline yet
- Jail bank: pending full publication; 7-model fleet stated on axis, never conflated with board fleet
- slot15 and human-vs-ai: measured in-lane only, not on the public 14-slot board

## 5. Free-tier commitments

- Regulator-facing surfaces (HF datasets, agent card, evidence pack) are free
- Stranger verification at `/gspc-verify` — no account, no fee
- Signed where the trust root allows; unsigned-but-honest where signing not yet deployed (JL.5)

## 6. Known limitations (never overclaim)

- No SOC 2 Type II / ISO 42001 yet (roadmap: gap assessment first)
- Insurers accept evidence packages (AIUC-1-style), not raw signed cards alone
- Market rail dev-grade pending licensed feed
- MCP registry still "preview" — breaking changes possible
