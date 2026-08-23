import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_H = os.path.abspath(os.path.join(_HERE, ".."))
_CG = os.path.abspath(os.path.join(_HERE, "..", "..", "products", "claimguard"))
for p in (_H, _CG):
    if p not in sys.path:
        sys.path.insert(0, p)

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from board import make_board
from receipts import (
    dsse_statement,
    sign_payload_as_receipt,
    to_dsse,
    to_intoto_statement,
    verify_dsse,
    verify_intoto_subject,
)

KID = "did:web:test#k1"


def _key():
    return Ed25519PrivateKey.generate()


def test_intoto_subject_digest_matches_board():
    k = _key()
    board = make_board(k, signer=KID)
    stmt = to_intoto_statement(board, subject_name="gspc-board")
    assert stmt["_type"].endswith("Statement/v1")
    assert verify_intoto_subject(stmt, board)


def test_dsse_roundtrip_verifies():
    k = _key()
    board = make_board(k, signer=KID)
    rec = sign_payload_as_receipt(board, k, subject_name="gspc-board", keyid=KID)
    pub = k.public_key().public_bytes_raw()
    assert verify_dsse(rec, pub)
    assert verify_intoto_subject(dsse_statement(rec), board)


def test_dsse_rejects_wrong_key():
    k = _key()
    board = make_board(k, signer=KID)
    rec = sign_payload_as_receipt(board, k, subject_name="gspc-board", keyid=KID)
    other = _key().public_key().public_bytes_raw()
    assert not verify_dsse(rec, other)


def test_dsse_rejects_tampered_payload():
    k = _key()
    stmt = to_intoto_statement({"a": 1}, subject_name="x")
    rec = to_dsse(stmt, k, keyid=KID)
    # flip a byte in the base64 payload
    import base64 as b64
    raw = bytearray(b64.standard_b64decode(rec["payload"]))
    raw[0] ^= 0x01
    rec["payload"] = b64.standard_b64encode(bytes(raw)).decode()
    assert not verify_dsse(rec, k.public_key().public_bytes_raw())
