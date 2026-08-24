---
language:
- en
license: cc-by-4.0
tags:
- governance
- safety
- measurement
- gspc
- ai-governance
pretty_name: GSPC Board Export
size_categories:
- n<1K
task_categories:
- text-classification
dataset_info:
  features:
  - name: axis
    dtype: string
  - name: bench
    dtype: string
  - name: status
    dtype: string
  - name: n
    dtype: int64
  - name: accuracy
    dtype: float64
  - name: leader
    dtype: string
  - name: separation
    dtype: string
  splits:
  - name: board
    num_bytes: 0
    num_examples: 14
---

# GSPC Board Export

**Council of AI · CSOAI Ltd (UK #16939677)**

Signed export of the GSPC 14-slot governance measurement board: **13 measured of 14** (jail axis quotable, separation UNTESTED).

## What this is

- Measurement, not certification
- Deterministic grading on frozen item banks — never LLM-as-judge
- Ed25519-signed live board at https://councilof.ai/api/gspc
- Verify in-browser: https://councilof.ai/gspc-verify

## Files

| File | Description |
|------|-------------|
| `board.json` | Full signed board payload |
| `axis-register.json` | Axis register metadata |
| `board.parquet.json` | Flat 14-row export for viewer |

## Grammar

Public count: **13 measured of 14 quotable** (GSPC ruling 2026-08-18). Scores are never sold. Regulators read free.

## Citation

```
Council of AI / CSOAI Ltd. GSPC Board Export. https://huggingface.co/datasets/csoai/gspc-board
DOI: (mint after final name confirmation)
```

## License

CC-BY-4.0 — attribute Council of AI, CSOAI Ltd 16939677, councilof.ai
