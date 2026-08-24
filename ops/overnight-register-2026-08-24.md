# Overnight Register — Five-Venue Pack (N5-01..N5-30)

**Pack:** 2026-08-24 evening → 2026-08-25 morning  
**Branch:** cursor/overnight-five-venues-ff6e  
**Disposer:** Nick (OWNER)

Append-only. Format: `move-ID · URL · commit SHA · timestamp · verification evidence`

---

## LANE-MEASURE (Hugging Face)

| Move | Status | Register line |
|------|--------|---------------|
| N5-01 | **GATED** | N5-01 · — · (pending) · 2026-08-24T17:14Z · `hf auth whoami` → Not logged in (no HF_TOKEN) |
| N5-02 | **STAGED** | N5-02 · https://huggingface.co/datasets/csoai/gspc-board · (pending push) · 2026-08-24T17:14Z · export committed; HF 401 without token |
| N5-03 | **STAGED** | N5-03 · https://huggingface.co/datasets/csoai/gspc-bench-results · (pending push) · 2026-08-24T17:14Z · export committed |
| N5-04 | **STAGED** | N5-04 · (cards in README.md) · (pending push) · 2026-08-24T17:14Z · full YAML frontmatter in export/*/README.md |
| N5-05 | **GATED** | N5-05 · DOI TBD · — · — · Mint after HF push + name confirmation (Settings → Generate DOI) |
| N5-06 | **STAGED** | N5-06 · https://huggingface.co/spaces/csoai/gspc-governance-leaderboard · (pending push) · 2026-08-24T17:14Z · Gradio 5.x scaffold + results dataset |

## LANE-OPS

| Move | Status | Register line |
|------|--------|---------------|
| N5-07 | **PASS** | N5-07 · ops/logs/claimguard-20260824T171430Z.log · (this commit) · 2026-08-24T17:14:30Z · ClaimGuard attestation PASS + banned-strings zero hits |
| N5-21 | **PASS** | N5-21 · trust/evidence-pack/ · (this commit) · 2026-08-24T17:14:30Z · same gate log |
| N5-22 | **PREP** | N5-22 · ops/adx/stage.sh · (this commit) · 2026-08-24T17:14Z · script committed; AMMP NOT executed |
| N5-23 | **PREP** | N5-23 · ops/adx/product-metadata.md · (this commit) · 2026-08-24T17:14Z · metadata + data-dictionary.csv |
| N5-24 | **PREP** | N5-24 · ops/snowflake/listing-draft.md · (this commit) · 2026-08-24T17:14Z · awaiting ORGADMIN terms |
| N5-25 | **PREP** | N5-25 · ops/datarade/listing-drafts.md · (this commit) · 2026-08-24T17:14Z · application draft; not submitted |

## LANE-CONNECT (MCP)

| Move | Status | Register line |
|------|--------|---------------|
| N5-08 | **STAGED** | N5-08 · connect/mcp/gspc/server.json · (this commit) · 2026-08-24T17:14Z · schema 2025-12-11; repository/title/packages restored |
| N5-09 | **STAGED** | N5-09 · version 1.0.2 · (this commit) · 2026-08-24T17:14Z · no prerelease trick |
| N5-10 | **GATED** | N5-10 · — · — · — · mcp-publisher login github requires owner OAuth device flow |
| N5-11 | **BASELINE** | N5-11 · https://registry.modelcontextprotocol.io/v0.1/servers?search=gspc · ops/mcp-registry-gspc-baseline.json · 2026-08-24T17:14Z · latest=1.0.1 missing fields; target 1.0.2 |
| N5-12 | **DONE** | N5-12 · ops/aggregator-watch-note.md · (this commit) · 2026-08-24T17:14Z · glama.json committed; recheck 2026-08-25T18:00Z |

## LANE-CONNECT (A2A)

| Move | Status | Register line |
|------|--------|---------------|
| N5-13 | **STAGED** | N5-13 · https://councilof.ai/.well-known/agent-card.json · (councilof-ai commit pending) · 2026-08-24T17:14Z · A2A v1.0 card generated; deploy pending |
| N5-14 | **STAGED** | N5-14 · connect/agent-cards/out/agent-card.json · (this commit) · 2026-08-24T17:14Z · 8 required fields present; validator run pending deploy |
| N5-15 | **PREP** | N5-15 · connect/a2a/directory-submissions.md · (this commit) · 2026-08-24T17:14Z · form draft; not submitted |
| N5-16 | **PREP** | N5-16 · connect/a2a/directory-submissions.md · (this commit) · 2026-08-24T17:14Z · registration draft |
| N5-17 | **PREP** | N5-17 · awesome-a2a PR draft in directory-submissions.md · (this commit) · 2026-08-24T17:14Z · PR not opened |
| N5-18 | **PREP** | N5-18 · Discussion #97 comment draft · (this commit) · 2026-08-24T17:14Z · not posted |
| N5-19 | **DEFERRED** | N5-19 · — · — · 2026-08-24T17:14Z · no GCP account — deferred to Nick morning sheet |

## LANE-TRUST + K3

| Move | Status | Register line |
|------|--------|---------------|
| N5-20 | **DONE** | N5-20 · trust/evidence-pack/ · (this commit) · 2026-08-24T17:14Z · 4 docs committed (KP.1) |
| N5-26 | **PREP** | N5-26 · trust/insurance-prep/aiuc-1-scoping-draft.md · (this commit) · 2026-08-24T17:14Z · owner-gated |
| N5-27 | **PREP** | N5-27 · trust/insurance-prep/armilla-governance-draft.md · (this commit) · 2026-08-24T17:14Z · owner-gated |
| N5-28 | **PREP** | N5-28 · trust/insurance-prep/munich-re-aisure-dd-draft.md · (this commit) · 2026-08-24T17:14Z · owner-gated |
| N5-29 | **PREP** | N5-29 · trust/insurance-prep/testudo-one-pager.md · (this commit) · 2026-08-24T17:14Z · owner-gated |
| N5-30 | **PREP** | N5-30 · ops/gcloud15/checklist.md · (this commit) · 2026-08-24T17:14Z · window closed; FTS alert steps documented |

---

## Done-definition scorecard (D1–D6)

| Done | Status | Notes |
|------|--------|-------|
| D1 HF Space live | **GATED** | HF_TOKEN required |
| D2 Datasets + DOIs | **GATED** | Exports staged; DOIs after push |
| D3 MCP 1.0.2 | **GATED** | server.json staged; OAuth for publish |
| D4 agent-card + directories | **PARTIAL** | Card staged for deploy; directories PREP |
| D5 Evidence pack | **DONE** | 4 docs + ClaimGuard pass |
| D6 Marketplace drafts | **DONE** | ADX/Snowflake/Datarade prep committed |

---

## Owner morning sheet (summary)

**Live after credentials:** HF datasets/Space/DOIs · MCP 1.0.2 publish · A2A card deploy · directory submissions

**Nick's seven decisions:** AWS AMMP · Snowflake ORGADMIN · Datarade commission · AIUC-1 scoping · Armilla outreach · Broker engagement · G-Cloud prep spend

**Needs nothing:** Gallagher Re (#68) · aggregator passive watch · Smithery/GitHub MCP Registry drafts queued
