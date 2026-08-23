"""'Make sure DSH actually does this' — a self-verifying capability register.

Applies CSOAI's own honesty-gate mechanic reflexively: instead of *asserting* the
roadmap works, it runs live checks and records an honest row per capability
(VERIFIED / PARTIAL / UNVERIFIED), and it runs ClaimGuard against DSH's own
marketing claims so overclaims (e.g. "17 measured axes", "certified",
"money-in wired") are FAILED, not published. The whole register is emitted as a
signed receipt.
"""
from __future__ import annotations

import os
import sys
from typing import Any, Callable

_CG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "products", "claimguard"))
if os.path.isdir(_CG) and _CG not in sys.path:
    sys.path.insert(0, _CG)

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402

import claimguard  # noqa: E402
from board import make_board  # noqa: E402
from detect import detect  # noqa: E402
from receipts import (  # noqa: E402
    MEASUREMENT_PREDICATE,
    dsse_statement,
    sign_payload_as_receipt,
    verify_dsse,
    verify_intoto_subject,
)

# Claims lifted from the DSH report + roadmap. Some are honest, some are overclaims
# that MUST fail — the register proves the difference instead of trusting the text.
DSH_CLAIMS = [
    "13 measured of 14 quotable",          # honest, matches canon
    "17 measured axes",                     # OVERCLAIM — must fail
    "16 measured axes",                     # OVERCLAIM — must fail
    "CSOAI certified this model",           # certification language — must fail
    "jail separation resolved",             # UNTESTED on board — must fail
    "public Elo league ranking",            # not on GSPC API — must fail
    "14 quotable axes",                     # honest
]


def _verified(evidence: str) -> dict[str, Any]:
    return {"status": "VERIFIED", "evidence": evidence}


def _partial(evidence: str) -> dict[str, Any]:
    return {"status": "PARTIAL", "evidence": evidence}


def _unverified(reason: str) -> dict[str, Any]:
    return {"status": "UNVERIFIED", "evidence": reason}


def _check(fn: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    try:
        return fn()
    except Exception as e:  # noqa: BLE001
        return {"status": "FAIL", "evidence": f"{type(e).__name__}: {e}"}


def build_register(sign_key: Ed25519PrivateKey, *, signer_keyid: str) -> dict[str, Any]:
    board = make_board(sign_key, signer=signer_keyid)

    def cap_move3() -> dict[str, Any]:
        # ClaimGuard v0.2 actually fails an overclaim.
        r = claimguard.audit(board, ["16 measured axes"])
        ok = any(f.code == "claim.sixteen_axes" and f.status.value == "FAIL" for f in r.findings)
        return _verified("claimguard.audit fails '16 measured axes'") if ok else {"status": "FAIL", "evidence": "did not fail overclaim"}

    def cap_detect() -> dict[str, Any]:
        # Build a valid AI manifest and confirm AI_MARKED + verifiable receipt.
        import base64
        from canonical import canonicalize
        k = Ed25519PrivateKey.generate()
        claim = {"claim_generator": "t/1", "assertions": [
            {"label": "c2pa.actions", "data": {"digitalSourceType": "trainedAlgorithmicMedia"}}],
            "timestamp": "2026-08-23T00:00:00Z"}
        m = {"claim": claim, "signature": {"alg": "Ed25519", "sig": k.sign(canonicalize(claim)).hex(),
             "public_key_x": base64.urlsafe_b64encode(k.public_key().public_bytes_raw()).decode().rstrip("=")}}
        d = detect(m, sign_key=sign_key, signer_keyid=signer_keyid, claims=["marked per Article 50"])
        rc_ok = verify_dsse(d["receipt"], sign_key.public_key().public_bytes_raw())
        return _verified(f"verdict={d['verdict']}, receipt_verifies={rc_ok}") if (d["verdict"] == "AI_MARKED" and rc_ok) else {"status": "FAIL", "evidence": str(d["verdict"])}

    def cap_receipts() -> dict[str, Any]:
        rec = sign_payload_as_receipt(board, sign_key, subject_name="gspc-board",
                                      keyid=signer_keyid, predicate_type=MEASUREMENT_PREDICATE)
        pub = sign_key.public_key().public_bytes_raw()
        stmt = dsse_statement(rec)
        ok = verify_dsse(rec, pub) and verify_intoto_subject(stmt, board)
        return _verified("board -> in-toto Statement -> DSSE round-trips + subject digest matches") if ok else {"status": "FAIL", "evidence": "round-trip failed"}

    def cap_board() -> dict[str, Any]:
        r = claimguard.audit(board)
        ok = any(f.code == "attestation.valid" for f in r.findings)
        return _verified("signed board fixture verifies via claimguard") if ok else {"status": "FAIL", "evidence": "board sig invalid"}

    rows = {
        "move1.detection_endpoint_engine": _check(cap_detect),
        "move2.receipt_interop_intoto_dsse": _check(cap_receipts),
        "move3.claimguard_article50": _check(cap_move3),
        "board.signed_fixture": _check(cap_board),
        # Honestly out of reach from this sandbox — declared, not faked:
        "move1.live_api_detect_deployed": _unverified("owner-gated: needs councilof-ai deploy (STEPS_100 Block B/G)"),
        "move4.a2a_registry_listed": _unverified("owner-gated: registry auth; owner joined A2A Registry 2026-08-22"),
        "move5.detector_interop_published": _partial("C2PA column real via ClaimGuard; other detector columns pending partners"),
        "move6.key_rotation_policy": _unverified("owner-gated: did.json + estate-chain custody"),
        "dsh.csoai_mail_read": _unverified("owner-gated: IMAP creds not present in this sandbox"),
        "dsh.money_in_usdc_x402": _unverified("owner-gated + unverifiable here: no chain access, no paying buyer confirmed"),
    }

    # Adjudicate DSH's own claims — overclaims must FAIL.
    claim_report = claimguard.audit(board, DSH_CLAIMS)
    claim_rows = [
        {"code": f.code, "status": f.status.value, "message": f.message}
        for f in claim_report.findings
        if f.code.startswith("claim.")
    ]

    summary = {
        "verified": sum(1 for r in rows.values() if r["status"] == "VERIFIED"),
        "partial": sum(1 for r in rows.values() if r["status"] == "PARTIAL"),
        "unverified": sum(1 for r in rows.values() if r["status"] == "UNVERIFIED"),
        "failed": sum(1 for r in rows.values() if r["status"] == "FAIL"),
    }

    payload = {
        "schema": "csoai.capability-register/0.1",
        "_note": "reflexive honesty gate — verified rows are live-checked; unverified are owner-gated, not hidden",
        "summary": summary,
        "capabilities": rows,
        "dsh_claim_adjudication": claim_rows,
        "claim_report_ok": claim_report.ok,
    }
    receipt = sign_payload_as_receipt(
        payload, sign_key, subject_name="capability-register",
        keyid=signer_keyid, predicate_type=MEASUREMENT_PREDICATE,
    )
    return {**payload, "receipt": receipt}
