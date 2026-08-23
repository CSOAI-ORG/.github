import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_H = os.path.abspath(os.path.join(_HERE, ".."))
_CG = os.path.abspath(os.path.join(_HERE, "..", "..", "products", "claimguard"))
for p in (_H, _CG):
    if p not in sys.path:
        sys.path.insert(0, p)

import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from board import make_board
from receipts import MEASUREMENT_PREDICATE, sign_payload_as_receipt
from tlog import TransparencyLog, verify_chain
from verify_external import verify_receipt_external

KID = "did:web:test#k1"


def test_transparency_log_chain_verifies_and_detects_tamper():
    log = TransparencyLog()
    for i in range(5):
        log.append({"subject": "x", "n": i})
    assert verify_chain(log.entries)
    # tamper an entry payload
    log.entries[2]["entry"]["n"] = 999
    assert not verify_chain(log.entries)


def test_independent_verifier_agrees_on_valid_receipt():
    k = Ed25519PrivateKey.generate()
    board = make_board(k, signer=KID)
    rec = sign_payload_as_receipt(board, k, subject_name="gspc-board", keyid=KID,
                                  predicate_type=MEASUREMENT_PREDICATE)
    pub_b64url = base64.urlsafe_b64encode(k.public_key().public_bytes_raw()).decode().rstrip("=")
    out = verify_receipt_external(rec, pub_b64url)
    assert out["signature_ok"] and out["intoto_structure_ok"]
    assert out["predicate_type"] == MEASUREMENT_PREDICATE


def test_independent_verifier_rejects_wrong_key():
    k = Ed25519PrivateKey.generate()
    board = make_board(k, signer=KID)
    rec = sign_payload_as_receipt(board, k, subject_name="gspc-board", keyid=KID)
    other = base64.urlsafe_b64encode(
        Ed25519PrivateKey.generate().public_key().public_bytes_raw()).decode().rstrip("=")
    out = verify_receipt_external(rec, other)
    assert out["signature_ok"] is False
    # structure is still well-formed even if signature fails
    assert out["intoto_structure_ok"] is True
