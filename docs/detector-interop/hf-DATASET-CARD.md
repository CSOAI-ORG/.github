---
license: mit
pretty_name: CSOAI Detector Interoperability Suite
language:
  - en
tags:
  - eu-ai-act
  - article-50
  - c2pa
  - provenance
  - content-authenticity
  - detector-interoperability
task_categories:
  - other
---

# CSOAI Detector Interoperability Suite

An open, signed conformance suite for **detector interoperability** under EU AI
Act Article 50 (Code of Practice interop deadline **2027-02-02**): does detector D
read mark M? Each case is **self-verifying** — its manifest embeds the
`public_key_x`, so any verifier checks it offline.

- **Truth rail:** counts/leaders defer to <https://councilof.ai/api/gspc>.
- **Method DOI:** 10.5281/zenodo.21991104
- **Honesty gate:** we publish our own `CANNOT_READ` cells first; a `CANNOT_READ`
  is a valid, respected result — never faked.

## Structure
- `index.json` — machine-readable enumeration of all cases (marks, expected verdicts).
- `matrix.json` — the conformance matrix (live signed version at `/api/detector-interop`).
- `cases/<name>/manifest.json` + `label.json` — self-verifying case bundles.

## Use
```python
import json, urllib.request
from claimguard.c2pa import verify_c2pa_manifest  # pip install claimguard
idx = json.load(open("index.json"))
for c in idx["cases"]:
    m = json.load(open(c["manifest"]))
    res = verify_c2pa_manifest(m)
    print(c["case"], "->", "AI_MARKED" if (res.ok and res.is_ai_marked) else "REJECTED")
```

## Contribute
Add a detector column or a mark/case via PR (see `README.md`). Declare honestly
what you cannot read. Stats are Wilson + SEPARATED/TIE/UNTESTED — never Elo.

_Measurement, not certification. CSOAI Ltd (UK 16939677)._
