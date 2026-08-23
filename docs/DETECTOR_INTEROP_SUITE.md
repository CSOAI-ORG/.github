# Move 5 — Detector-interoperability conformance suite (own 2027-02-02)

**Status:** design · **Owner:** Lane D (HF/benches) · **Forcing date:**
Art. 50 Code of Practice sets **2027-02-02** for an **interoperability solution
between detection mechanisms.** No neutral, open interop test exists yet.

> Uses the detector-interop axis (DetBench). Counts/leaders defer to
> [`/api/gspc`](https://councilof.ai/api/gspc).

---

## The gap nobody is filling

Article 50 lets providers mark content with *any* compliant technique (C2PA,
SynthID, other watermarks, fingerprints). By 2027-02-02 these detectors must
**interoperate** — detector X must be able to recognise mark Y. Today that is a
matrix of untested pairs. Whoever publishes the **neutral conformance test**
becomes the de-facto convener. We already have the axis for it (`detector-interop`
/ DetBench).

## Chess frame

- **Our move:** publish DetBench as an **open, signed interop conformance suite**
  — a public matrix of "does detector D read mark M?" with reproducible cases —
  and invite C2PA/CAI, model providers, UK AISI (Inspect), Epoch, and
  fact-checking networks to run against it.
- **Opponent replies:** (1) a vendor ships a proprietary interop test → ours is
  open + signed + free; (2) a standards body starts its own → we contribute ours
  as input and co-author (convener, not competitor); (3) "you're not neutral, you
  measure models" → we publish our own detector's failures (honesty gate) in the
  same matrix.
- **Tempo:** first credible public matrix before Q1 2027 = the reference everyone
  cites into the deadline.

---

## Suite shape

### Conformance matrix (`/api/detector-interop` + HF dataset)
```jsonc
{
  "schema": "csoai.detector-interop/0.1",
  "marks":     ["c2pa", "synthid", "watermark-x", "fingerprint-y"],
  "detectors": ["csoai-detect", "vendor-a", "vendor-b"],
  "cells": [
    { "detector": "csoai-detect", "mark": "c2pa", "result": "READS", "n": 200, "wilson": [0.97,1.0] },
    { "detector": "csoai-detect", "mark": "synthid", "result": "CANNOT_READ", "note": "watermark layer not decoded (honesty)" }
  ],
  "site_attestation": { "alg": "Ed25519", "signer": "did:web:csoai.org#board-attestation-1", "sig": "…" }
}
```
Rules:
- Same statistics as the board (Wilson intervals; SEPARATED/TIE/UNTESTED), no Elo.
- Publish **our own** `CANNOT_READ` cells first — the honesty gate is the
  credibility engine.
- Each cell reproducible from a public case bundle (carder-valved).

### Case bundles (HF `csoai/detector-interop`)
Signed sample content per mark (C2PA-manifested image, watermarked sample, etc.)
+ expected-detection labels, so anyone can reproduce a cell.

### Verifier
Reuse ClaimGuard `c2pa.py` for the C2PA column; declare (not fake) the columns we
can't yet decode.

## Build steps
1. `docs` (this file) → scope + call for participants.
2. HF dataset `csoai/detector-interop` with the matrix schema + first cases (C2PA
   column from ClaimGuard v0.2, real today).
3. `/api/detector-interop` serving the signed matrix (Move 2 receipt).
4. Outreach: C2PA/CAI, UK AISI, Epoch, EFCSN (see NEXT_WEEK_PLAN §7).
5. Zenodo-DOI the suite spec (IP, Move / §8).

## Done-when
A public, signed interop matrix exists with at least the C2PA column populated
from real ClaimGuard verification, our own gaps shown, and a documented way for a
third party to add a detector column.

## Non-goals
Not certifying detectors. Not hiding our own `CANNOT_READ` cells. Not ranking by
vote/Elo.
