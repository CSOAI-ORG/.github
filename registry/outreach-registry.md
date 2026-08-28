# Outreach registry — working protocol

**Machine DB:** [`outreach-registry.json`](./outreach-registry.json)  
**SQLite companion (agents):** [`../ops/knowledge/outreach.sqlite`](../ops/knowledge/outreach.sqlite)  
**Fire-book:** [`activation-pack.md`](./activation-pack.md)

## Anti-duplicate rule

Before any publish/submit:

1. Read `outreach-registry.json` + `ops/knowledge/outreach.sqlite`
2. If `status` is `LIVE` / `SENT` / `SUBMITTED` and `do_not` is set → **stop**
3. Never remint HF DOIs
4. Never mix **GSPC 14-slot board** counts with **EUNOMIA** (PR #645) counts

## Current-state audit (verified 2026-08-25T15:22Z)

| Surface | Status | Evidence |
|---------|--------|----------|
| GSPC API | LIVE | `14 measured of 14 quotable` |
| A2A card | LIVE | CDN description **14 measured of 14** |
| MCP registry | LIVE | `io.github.CSOAI-ORG/gspc` **1.0.3** isLatest |
| HF gspc-board | LIVE | DOI **10.57967/hf/10114** (do not remint) |
| HF gspc-bench-results | LIVE | DOI **10.57967/hf/10116** (do not remint) |
| HF Space | PARTIAL | sdk=gradio · runtime PAUSED · cpu-basic limit=0 |
| a2aagentlist | SENT | Gmail sent |
| awesome-a2a | SUBMITTED | PR #157 |
| Discussion #97 | GATED | CAPTCHA / 2FA |
| Kaggle board | STAGED | `export/kaggle-gspc-board/` — needs API token |

### Stale claims to ignore

- “Mint HF DOIs first” → **already done**
- “MCP ready-but-unpublished” → **1.0.3 is live**
- “10/13 axes” without naming EUNOMIA → **wrong board** (GSPC is 14/14)

## Connection map

```
councilof.ai/api/gspc  ──►  HF csoai/gspc-board (+ DOI)
        │                   HF csoai/gspc-bench-results (+ DOI)
        │                   HF Space (Gradio; runtime gated $)
        ├──► A2A /.well-known/agent-card.json
        ├──► MCP registry 1.0.3
        ├──► Layer0 / gspc-verify
        └──► directories (awesome-a2a, a2aagentlist, Discussion #97)
```

## Insurance outreach drafts (not sent)

Point to existing polished drafts (do not fork duplicate bodies):

- `trust/insurance-prep/aiuc-1-scoping-draft.md`
- `trust/insurance-prep/armilla-governance-draft.md`
- `trust/insurance-prep/munich-re-aisure-dd-draft.md`
- `trust/insurance-prep/testudo-one-pager.md`

Pointers also under `registry/outreach-drafts/`.
