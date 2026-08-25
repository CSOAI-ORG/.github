# Snowflake Marketplace — PREP / CONDITIONAL OVERNIGHT

**Entity:** CSOAI Ltd (UK #16939677)  
**Legal name for public listing:** CSOAI Ltd

## Private listing (overnight-executable IF ORGADMIN terms accepted)

Provider Studio steps:

1. Build draft listing → attach secure share `CSOAI.GSPC.BOARD_EXPORT`
2. Metadata: description, data dictionary, business-needs tags
3. Sample SQL (validated by Snowflake):

```sql
SELECT axis, bench, status, n, leader, separation
FROM CSOAI.GSPC.BOARD_EXPORT
WHERE status = 'MEASURED'
ORDER BY axis;
```

4. Publish to named consumer accounts (immediate — no Marketplace approval)

**Gate:** Private listing URL OR explicit "awaiting ORGADMIN" note if terms not yet accepted.

## Public free listing (draft only)

Provider Studio draft:

- Title: CSOAI GSPC Board Export
- Description: Signed governance measurement board — 14 measured of 14. Measurement only.
- Tags: governance, ai-safety, compliance, measurement
- Profile approval (~1 business day) required before public listing

## Owner decision

Nick must accept Provider & Consumer Terms as ORGADMIN before any publish.
