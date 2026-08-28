---
license: cc-by-4.0
pretty_name: GSPC Board (Council of AI)
tags:
  - gspc
  - governance
  - evaluation
  - doi:10.57967/hf/10114
---

# GSPC Board — Council of AI

Independent AI-governance measurement board. **Source of truth:** [councilof.ai/api/gspc](https://councilof.ai/api/gspc).

- **Board slots:** 14 quotable axes  
- **Public ruling (live):** 14 measured of 14 quotable  
- **Jail (slot 14):** MEASURED; living-board separation **TIE** (a TIE is not a separated leader)  
- **DOI:** [10.57967/hf/10114](https://doi.org/10.57967/hf/10114) (dataset `csoai/gspc-board`)  
- **License:** CC-BY-4.0 — attribute Council of AI / CSOAI Ltd  
- **Attestation:** Ed25519 site attestation included in `board.json` (`site_attestation`)

## Files

| File | Role |
|------|------|
| `board.json` | Full signed board payload + DOI |
| `board.parquet.json` | Flat per-axis rows |
| `axis-register.json` | Axis id register / counting rule |

## Claim rules

Do **not** invent “22 axes.” Quotable board = **14**. In-lane honesty probes (`slot15`, `human-vs-ai`) are not board-quotable.

Measurement only — not certification.

## Attestation note

`board.json` is Ed25519-attested. Do **not** edit axis `note` fields in-place (breaks ClaimGuard). Live narrative for jail TIE / 14 of 14 is on HF README + https://councilof.ai/api/gspc (`totals.public_count`, per-axis status).
