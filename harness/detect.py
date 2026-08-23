"""Move 1 (code) — Article 50 detection engine.

Verifies a supplied C2PA-style signed manifest (reusing ClaimGuard's verifier) and
returns a deterministic verdict plus a *signed* CSOAI detection receipt
(in-toto Statement -> DSSE). The watermark layer we cannot see is declared, never
claimed (honesty gate).
"""
from __future__ import annotations

import os
import sys
from typing import Any

_CG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "products", "claimguard"))
if os.path.isdir(_CG) and _CG not in sys.path:
    sys.path.insert(0, _CG)

from c2pa import verify_c2pa_manifest  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402

from receipts import DETECTION_PREDICATE, sign_payload_as_receipt  # noqa: E402


def detect(
    manifest: dict[str, Any],
    *,
    sign_key: Ed25519PrivateKey,
    signer_keyid: str,
    claims: list[str] | None = None,
    asset_hash: str | None = None,
) -> dict[str, Any]:
    res = verify_c2pa_manifest(manifest)

    if not res.ok:
        verdict = "UNVERIFIABLE"
    elif res.is_ai_marked:
        verdict = "AI_MARKED"
    else:
        verdict = "NOT_AI_MARKED"

    findings = [{"status": f.status, "code": f.code, "message": f.message} for f in res.findings]

    # Optional hard-binding to asset bytes.
    if asset_hash is not None:
        claim_hash = (manifest.get("claim") or {}).get("asset", {}).get("hash")
        if claim_hash != asset_hash:
            verdict = "UNVERIFIABLE"
            findings.append(
                {"status": "FAIL", "code": "detect.asset_mismatch",
                 "message": f"asset_hash {asset_hash} != manifest {claim_hash}"}
            )

    # Adjudicate any natural-language marking claims deterministically.
    claim_findings = []
    for c in claims or []:
        supported = verdict == "AI_MARKED"
        claim_findings.append(
            {"claim": c, "status": "PASS" if supported else "FAIL",
             "code": "claim.article50_supported" if supported else "claim.article50_unsupported"}
        )

    payload = {
        "verdict": verdict,
        "source_type": res.source_type,
        "manifest_signer": res.signer,
        "detected": {
            "metadata_layer": "verified" if any(
                f["code"] == "c2pa.signature_valid" for f in findings) else "unverified",
            "watermark_layer": "not_checked",
        },
        "findings": findings,
        "claims": claim_findings,
    }
    receipt = sign_payload_as_receipt(
        payload,
        sign_key,
        subject_name="ai-content-detection",
        keyid=signer_keyid,
        predicate_type=DETECTION_PREDICATE,
    )
    return {"ok": verdict != "UNVERIFIABLE", **payload, "receipt": receipt}
