"""Local signed board fixture for the harness.

NOT the live board. The live truth rail is https://councilof.ai/api/gspc and
counts/leaders defer to it. This fixture lets the backend + frontend + e2e run
fully offline (the live apex 404s parts of the surface), and is clearly marked as
a fixture so no one mistakes it for a published measurement.
"""
from __future__ import annotations

import base64
import os
import sys
from typing import Any

_CG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "products", "claimguard"))
if os.path.isdir(_CG) and _CG not in sys.path:
    sys.path.insert(0, _CG)

from canonical import canonicalize  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402

# 14 board axis ids per docs/GSPC_AXIS_CANON.md (+ jail measured, separation UNTESTED).
_AXIS_IDS = [
    "governance", "safety", "provenance", "continuity", "conformance", "openness",
    "machinery-conformity", "care", "cross-reality", "detector-interop",
    "art5-safeguard", "swarm", "affect", "jail",
]


def make_board(sign_key: Ed25519PrivateKey, *, signer: str) -> dict[str, Any]:
    axes = []
    for aid in _AXIS_IDS:
        row: dict[str, Any] = {"axis": aid, "status": "MEASURED", "accuracy": 0.7, "n": 40}
        if aid == "jail":
            row = {"axis": aid, "status": "MEASURED", "separation": "UNTESTED", "n": 71}
        axes.append(row)
    board: dict[str, Any] = {
        "schema": "csoai.gspc-axes/0.5",
        "_fixture": True,
        "_note": "local harness fixture — not the live board; live truth: https://councilof.ai/api/gspc",
        "totals": {
            "axes": 14,
            "measured_axes": 13,
            "quotable_axes": 14,
            "public_count": "13 measured of 14 quotable",
        },
        "axes": axes,
    }
    sig = sign_key.sign(canonicalize(board)).hex()
    pub = sign_key.public_key().public_bytes_raw()
    board["site_attestation"] = {
        "signer": signer,
        "alg": "Ed25519",
        "sig": sig,
        "public_key_x": base64.urlsafe_b64encode(pub).decode().rstrip("="),
    }
    return board
