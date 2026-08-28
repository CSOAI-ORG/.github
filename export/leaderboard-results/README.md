---
language:
- en
license: cc-by-4.0
tags:
- governance
- leaderboard
- measurement
pretty_name: GSPC Governance Leaderboard Results
size_categories:
- n<1K
task_categories:
- text-classification
dataset_info:
  features:
  - name: subject
    dtype: string
  - name: measured_axes
    dtype: int64
  - name: total_axes
    dtype: int64
  - name: as_of
    dtype: string
  splits:
  - name: leaderboard
    num_bytes: 0
    num_examples: 0
---

# GSPC Governance Leaderboard Results

Results dataset for the **csoai/gspc-governance-leaderboard** Space.

## Submission flow (PR-based)

This follows the retired Open-LLM-Leaderboard triad pattern (Space + harness + results dataset):

1. Fork this dataset repo
2. Add your row to `results.jsonl` (one JSON object per line)
3. Open a Pull Request with your measurement evidence
4. Maintainers review and merge — no automatic score acceptance

## Requirements

- Measurement only — not certification
- Signed evidence or reproducible harness link required
- Grammar: state measured-axis count honestly (e.g. "14 measured of 14")
- No ranked scores for money — this leaderboard renders signed measurement state

## Schema (results.jsonl)

```json
{"subject": "example-model", "measured_axes": 10, "total_axes": 14, "as_of": "2026-08-24", "evidence_url": "https://..."}
```

## First-of-niche note

HF Spaces search for "governance leaderboard" returned zero hits on 2026-08-24. This is the first dedicated governance leaderboard we could find on HF — adjacent safety leaderboards exist (AI-Secure, vectara, galileo-ai/agent-leaderboard).

## License

CC-BY-4.0
