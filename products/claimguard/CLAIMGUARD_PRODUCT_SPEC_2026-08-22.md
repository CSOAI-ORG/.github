# ClaimGuard product spec — 2026-08-22

## Problem
Signed-evidence pipelines share a failure mode: post-hoc mutation of a signed
board, or marketing claims that the signed board does not support. We hit both
in one week (fake jail “separation resolved”; overstated guardrail deltas).

## Product
Deterministic auditor: signature → payload completeness → claim support.
One CLI / one MCP tool / one CI gate. Truthy only when all FAIL findings are empty.

## Demo that matters
Self-test signs a board, mutates `totals.axes` after sign, proves verify fails
and “16 measured axes” fails. The tool auditing its author.

## Surfaces
| Surface | Status |
|---|---|
| CLI `claimguard.py` | Landed this repo |
| CI gate | `.github/workflows/claimguard.yml` |
| Article 50 / C2PA provenance (`--c2pa`, `c2pa.py`) | Landed v0.2 |
| MCP `claimguard.check` | Next |
| PyPI `claimguard` | Next |
| Council Ledger Integrity tile | Next |

## v0.2 — Article 50 provenance (2026-08-23)
EU AI Act Article 50(2) machine-readable marking is enforceable (2026-08-02;
legacy backstop 2026-12-02; detector interop 2027-02-02). v0.2 adds a
signed-C2PA-manifest verifier (`c2pa.py`) reusing the estate's RFC 8785 + Ed25519
primitive, plus claim rules that FAIL any "marked / watermarked / C2PA verified /
Article 50 compliant" claim not backed by a verifiable AI-marked manifest. This
positions ClaimGuard as the CI gate for Article 50 transparency claims and the
deterministic core of the free detection endpoint (see
`docs/ARTICLE50_DETECTION.md`).

## Non-goals
Not certification. Not remediation. Not a substitute for McNemar / bank
publication. Not a full c2pa-rs (JUMBF/COSE/X.509) — verifies the signed-metadata
layer and the watermark layer is out of scope for a deterministic linter.
