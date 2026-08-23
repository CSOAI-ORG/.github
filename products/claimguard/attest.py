"""Emit ClaimGuard verdicts as composable in-toto / DSSE attestations.

Self-contained (only `canonical` + `cryptography`) so ClaimGuard stays a
standalone PyPI package. A ClaimGuard report becomes an in-toto Statement v1 with
predicate type ``https://councilof.ai/attestations/claimguard/v1``; optionally
wrapped in a DSSE envelope signed with Ed25519. Tiers mirror the ecosystem:
unsigned Statement (tamper-evident by hash) → signed DSSE (identity-bound).
"""
from __future__ import annotations

import base64
import hashlib
import json
from typing import Any

from canonical import canonicalize
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

IN_TOTO_STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
DSSE_PAYLOAD_TYPE = "application/vnd.in-toto+json"
CLAIMGUARD_PREDICATE = "https://councilof.ai/attestations/claimguard/v1"


def _b64(b: bytes) -> str:
    return base64.standard_b64encode(b).decode("ascii")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def subject_digest(board: dict[str, Any], *, drop: str = "site_attestation") -> str:
    body = {k: v for k, v in board.items() if k != drop}
    return sha256_hex(canonicalize(body))


def to_intoto_statement(
    report: dict[str, Any], *, subject_name: str, subject_sha256: str
) -> dict[str, Any]:
    return {
        "_type": IN_TOTO_STATEMENT_TYPE,
        "subject": [{"name": subject_name, "digest": {"sha256": subject_sha256}}],
        "predicateType": CLAIMGUARD_PREDICATE,
        "predicate": report,
    }


def _pae(payload_type: bytes, payload: bytes) -> bytes:
    return b"DSSEv1 %d %s %d %s" % (len(payload_type), payload_type, len(payload), payload)


def to_dsse(statement: dict[str, Any], sign_key: Ed25519PrivateKey, *, keyid: str) -> dict[str, Any]:
    payload = json.dumps(statement, separators=(",", ":"), sort_keys=True).encode("utf-8")
    sig = sign_key.sign(_pae(DSSE_PAYLOAD_TYPE.encode("ascii"), payload))
    return {"payloadType": DSSE_PAYLOAD_TYPE, "payload": _b64(payload),
            "signatures": [{"keyid": keyid, "sig": _b64(sig)}]}


def verify_dsse(envelope: dict[str, Any], pubkey: bytes) -> bool:
    try:
        payload = base64.standard_b64decode(envelope["payload"])
        pae = _pae(envelope["payloadType"].encode("ascii"), payload)
        pk = Ed25519PublicKey.from_public_bytes(pubkey)
        for s in envelope.get("signatures", []):
            try:
                pk.verify(base64.standard_b64decode(s["sig"]), pae)
                return True
            except Exception:
                continue
    except Exception:
        return False
    return False


def load_signing_key(path: str) -> tuple[Ed25519PrivateKey, str]:
    """Load a raw 32-byte Ed25519 seed from a hex or base64url file."""
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read().strip()
    try:
        raw = bytes.fromhex(txt)
    except ValueError:
        pad = "=" * (-len(txt) % 4)
        raw = base64.urlsafe_b64decode(txt + pad)
    key = Ed25519PrivateKey.from_private_bytes(raw)
    pub = key.public_key().public_bytes_raw()
    keyid = base64.urlsafe_b64encode(pub).decode().rstrip("=")
    return key, keyid
