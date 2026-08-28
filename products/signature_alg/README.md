# signature_alg (P5 — Continuity white-space grader)

Portable draft of the Continuity instrument-spine predicate.

## What it is

Deterministic check: **every signed record names its algorithm** so a verifier need not assume Ed25519. Mirrors deploy2 `pqcbench.py` `alg_agility`.

## What it is not

- Not a new board axis (board Continuity is already MEASURED on the live 14/14 board).
- Does not remint DOIs or require RunPod for the grader itself.
- Full wiring into `sov_instrument.py` lives on `csoai-static-deploy2` (grader currently still `rubric_deterministic`).

## Run

```bash
python3 -m products.signature_alg.grader
# or
python3 products/signature_alg/grader.py
```

## Wire-up (deploy2, free)

1. Point continuity lens `grader` → `signature_alg`.
2. Dispatch to this predicate (or import from `pqcbench.alg_agility`).
3. Extend `sov_instrument.py --selftest` with unsigned / no-alg / named-alg cases.
