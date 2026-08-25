---
language:
- en
license: cc-by-4.0
tags:
- governance
- benchmark
- measurement
- gspc
pretty_name: GSPC Bench Results
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
  - name: separation
    dtype: string
  - name: leader
    dtype: string
  splits:
  - name: results
    num_bytes: 0
    num_examples: 14
---

# GSPC Bench Results

Per-axis bench-room result rows from the Council of AI GSPC measurement instrument.

## Summary

- **14 measured of 14** axes on the public board
- 4 separated leads, 9 ties, 1 untested separation (jail)
- Measurement only — not certification

## Files

| File | Description |
|------|-------------|
| `results.json` | Bench result rows with axis, bench, status, n, separation, leader |

## Live source

https://councilof.ai/api/gspc

## License

CC-BY-4.0 — attribute Council of AI, CSOAI Ltd 16939677
