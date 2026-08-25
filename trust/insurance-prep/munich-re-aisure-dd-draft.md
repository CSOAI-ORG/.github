# Munich Re aiSure Prep — OWNER-GATED (draft only)

**Route:** Via Mosaic (Lloyd's Syndicate 1609) · broker engagement required  
**No lane execution**

## Due-diligence pack skeleton (mapped to published asks)

### 1. Technical system description

See `trust/evidence-pack/01-technical-system-description.md`

- Architecture: Cloudflare Pages + Workers + HF datasets + Ed25519 signing
- Training-data sources: Frozen public item banks per axis (HF datasets)
- Test methodology: Deterministic predicates, McNemar separation, Wilson CI

### 2. Performance benchmark results

| Metric | Value | Source |
|--------|-------|--------|
| Measured axes | 14/14 (live `totals.public_count`) | https://councilof.ai/api/gspc |
| Mean accuracy (leaders) | 0.7318 | Board |
| Separated leads | 4 | Board |
| Hallucination-rate | N/A — not an LLM-output benchmark | — |
| Bias | Per-axis fleet distributions published | Board |

*Field-level data dictionary for aiSure: UNKNOWN — not publicly disclosed; not fabricated.*

### 3. Operational monitoring programme

See `trust/evidence-pack/03-monitoring-incident-log.md`

| What | Frequency | Owner |
|------|-----------|-------|
| Reg-watch re-hash | Daily | Automated |
| Signing chain | Continuous | Watchdog |
| E2E gates | CI + overnight | LANE-OPS |

### 4. Governance framework

See `trust/evidence-pack/02-governance-oversight-record.md`
