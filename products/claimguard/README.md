# ClaimGuard

**The receipt for your claims.** Verifies a signed GSPC board’s Ed25519
`site_attestation`, payload completeness, and whether natural-language claims
are supported by the board.

Measurement, not certification. CSOAI Ltd (UK 16939677).

## Why it exists

Session failure mode: mutate a signed result after signing, or claim
“16 measured axes” / “jail separation resolved” when the living board says
otherwise. ClaimGuard fails those deterministically — including when we make them.

## Install

```bash
pip install cryptography
# or: pip install -e .
```

## Usage

```bash
python claimguard.py --self-test
python claimguard.py check --live
python claimguard.py check --live --claim "16 measured axes"
# N measured must match live totals.measured_axes (do not freeze 13 or 15 here)
python claimguard.py check --live --claim "all 22 measured"
```

Exit code `0` = PASS, `1` = FAIL.

## What it checks

1. **Attestation** — Ed25519 over RFC 8785 canonical JSON of payload minus `site_attestation` (same as `/api/gspc`).
2. **Payload** — `axes[]` non-empty, totals present, MEASURED rows not empty.
3. **Claims** — rejects 22/22 measured, “16 measured axes”, stale “13 of 14” when the living board is not 13/14, public Elo league, jail-separation-resolved while `UNTESTED`, certification language. `N measured` must match live `totals.measured_axes`.

Living board: https://councilof.ai/api/gspc  
Axis canon: https://github.com/CSOAI-ORG/.github/blob/main/docs/GSPC_AXIS_CANON.md

## Licence

MIT © CSOAI Ltd
