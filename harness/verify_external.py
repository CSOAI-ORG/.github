"""Move J44 — INDEPENDENT DSSE / in-toto verifier (interop proof).

Deliberately does NOT import receipts.py internals. It reconstructs the DSSE
Pre-Authentication Encoding straight from the spec and validates the in-toto
Statement structure, to demonstrate that any third party (auditor, GRC platform,
`cosign`-style tool) can verify a CSOAI receipt from the published envelope +
public key alone — i.e. our receipts are standard, not self-referential.
"""
from __future__ import annotations

import base64
import json
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

IN_TOTO_STATEMENT_TYPE = "https://in-toto.io/Statement/v1"


def _pae(payload_type: bytes, payload: bytes) -> bytes:
    # DSSE PAE, transcribed independently from the spec.
    return b"DSSEv1 " + str(len(payload_type)).encode() + b" " + payload_type + \
        b" " + str(len(payload)).encode() + b" " + payload


def verify_receipt_external(envelope: dict[str, Any], public_key_b64url: str) -> dict[str, Any]:
    out: dict[str, Any] = {"signature_ok": False, "intoto_structure_ok": False, "predicate_type": None}
    try:
        pad = "=" * (-len(public_key_b64url) % 4)
        pk = Ed25519PublicKey.from_public_bytes(base64.urlsafe_b64decode(public_key_b64url + pad))
        payload = base64.standard_b64decode(envelope["payload"])
        ptype = envelope["payloadType"].encode("ascii")
        pae = _pae(ptype, payload)
        for s in envelope.get("signatures", []):
            try:
                pk.verify(base64.standard_b64decode(s["sig"]), pae)
                out["signature_ok"] = True
                break
            except Exception:
                continue
        stmt = json.loads(payload)
        out["predicate_type"] = stmt.get("predicateType")
        subj = stmt.get("subject")
        out["intoto_structure_ok"] = (
            stmt.get("_type") == IN_TOTO_STATEMENT_TYPE
            and isinstance(subj, list) and len(subj) >= 1
            and isinstance(subj[0].get("digest", {}).get("sha256"), str)
            and isinstance(stmt.get("predicateType"), str)
        )
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out
