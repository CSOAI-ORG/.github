# Detector-interoperability suite (open, signed) — own 2027-02-02

Article 50's Code of Practice sets **2027-02-02** for interoperability between
detection mechanisms. This is the open, neutral conformance test for "does
detector D read mark M?" — the thing the ecosystem must build. We publish our own
`CANNOT_READ` cells first (honesty gate). Implements the plan in
[`DETECTOR_INTEROP_SUITE.md`](../DETECTOR_INTEROP_SUITE.md).

> Counts/leaders defer to [`/api/gspc`](https://councilof.ai/api/gspc); stats are
> Wilson + SEPARATED/TIE/UNTESTED, never Elo.

## Contents
- `matrix.json` — the conformance matrix (static template; live signed version at
  `/api/detector-interop`).
- `cases/<name>/manifest.json` + `label.json` — **self-verifying** case bundles.
  Each manifest embeds its `public_key_x`, so any verifier checks it offline. The
  `c2pa_ai_image` case is verified in CI (`harness/tests/test_interop_cases.py`)
  against ClaimGuard's C2PA verifier → expected `AI_MARKED`.

## Add a detector column
1. Run your detector over each `cases/*/manifest.json` (and future watermarked
   media cases).
2. Report `READS` / `CANNOT_READ` per mark with n + Wilson interval.
3. Open a PR adding your `{detector, mark, result, n, wilson}` cells. Declare
   honestly what you cannot read — `CANNOT_READ` is a valid, respected cell.

## Add a mark/case
Add `cases/<mark>_<desc>/` with a signed `manifest.json` (or watermarked sample +
detection labels) and `label.json` stating the expected verdict.

## Roadmap
Real watermarked-media cases (SynthID etc.) via partner detectors; HF dataset
`csoai/detector-interop`; Zenodo DOI; invitations to C2PA/CAI, UK AISI (Inspect),
Epoch, and fact-checking networks (see `NEXT_WEEK_PLAN` §7).
