"""Move 2 (code) — receipt interop: in-toto Statement v1 + DSSE envelope.

Turns the estate's Ed25519/RFC-8785 receipt into the envelope the ecosystem reads
(in-toto / DSSE), without changing how anything is measured or signed. A board
payload's DSSE `subject.digest.sha256` is computed over the *same* RFC 8785
canonical bytes we already sign, so our signature and the in-toto subject are the
same object.

Pure stdlib + cryptography + the estate's `canonical`. No network.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
from typing import Any

# Reuse the estate's canonicalizer whether claimguard is pip-installed or not.
_CG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "products", "claimguard"))
if os.path.isdir(_CG) and _CG not in sys.path:
    sys.path.insert(0, _CG)

from canonical import canonicalize  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.ed25519 import (  # noqa: E402
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

IN_TOTO_STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
DSSE_PAYLOAD_TYPE = "application/vnd.in-toto+json"
MEASUREMENT_PREDICATE = "https://councilof.ai/attestations/measurement/v1"
DETECTION_PREDICATE = "https://councilof.ai/attestations/detection/v1"


def _b64(b: bytes) -> str:
    return base64.standard_b64encode(b).decode("ascii")


def _b64d(s: str) -> bytes:
    return base64.standard_b64decode(s.encode("ascii"))


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_subject_digest(payload: dict[str, Any], *, drop: str = "site_attestation") -> str:
    """SHA-256 over RFC 8785 canonical bytes of payload minus the signature block —
    the exact bytes the board attestation signs."""
    body = {k: v for k, v in payload.items() if k != drop}
    return sha256_hex(canonicalize(body))


def to_intoto_statement(
    payload: dict[str, Any],
    *,
    subject_name: str,
    predicate_type: str = MEASUREMENT_PREDICATE,
    predicate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "_type": IN_TOTO_STATEMENT_TYPE,
        "subject": [
            {"name": subject_name, "digest": {"sha256": canonical_subject_digest(payload)}}
        ],
        "predicateType": predicate_type,
        "predicate": predicate if predicate is not None else payload,
    }


def _pae(payload_type: bytes, payload: bytes) -> bytes:
    """DSSE Pre-Authentication Encoding (spec: secure-systems-lab/dsse)."""
    return b"DSSEv1 %d %s %d %s" % (len(payload_type), payload_type, len(payload), payload)


def to_dsse(
    statement: dict[str, Any],
    sign_key: Ed25519PrivateKey,
    *,
    keyid: str,
) -> dict[str, Any]:
    payload = json.dumps(statement, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ptype = DSSE_PAYLOAD_TYPE.encode("ascii")
    sig = sign_key.sign(_pae(ptype, payload))
    return {
        "payloadType": DSSE_PAYLOAD_TYPE,
        "payload": _b64(payload),
        "signatures": [{"keyid": keyid, "sig": _b64(sig)}],
    }


def verify_dsse(envelope: dict[str, Any], pubkey: bytes) -> bool:
    """True iff at least one signature verifies over the PAE of the payload."""
    try:
        ptype = envelope["payloadType"].encode("ascii")
        payload = _b64d(envelope["payload"])
        pae = _pae(ptype, payload)
        pk = Ed25519PublicKey.from_public_bytes(pubkey)
        for s in envelope.get("signatures", []):
            try:
                pk.verify(_b64d(s["sig"]), pae)
                return True
            except Exception:
                continue
    except Exception:
        return False
    return False


def dsse_statement(envelope: dict[str, Any]) -> dict[str, Any]:
    """Decode the in-toto Statement carried by a DSSE envelope."""
    return json.loads(_b64d(envelope["payload"]).decode("utf-8"))


def verify_intoto_subject(statement: dict[str, Any], payload: dict[str, Any]) -> bool:
    """Recompute the subject digest from payload and compare to the statement."""
    want = canonical_subject_digest(payload)
    for subj in statement.get("subject", []):
        if subj.get("digest", {}).get("sha256") == want:
            return True
    return False


def sign_payload_as_receipt(
    payload: dict[str, Any],
    sign_key: Ed25519PrivateKey,
    *,
    subject_name: str,
    keyid: str,
    predicate_type: str = MEASUREMENT_PREDICATE,
    predicate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """One-call: payload -> in-toto Statement -> DSSE envelope (signed)."""
    stmt = to_intoto_statement(
        payload, subject_name=subject_name, predicate_type=predicate_type, predicate=predicate
    )
    return to_dsse(stmt, sign_key, keyid=keyid)
