import base64
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_H = os.path.abspath(os.path.join(_HERE, ".."))
_CG = os.path.abspath(os.path.join(_HERE, "..", "..", "products", "claimguard"))
for p in (_H, _CG):
    if p not in sys.path:
        sys.path.insert(0, p)

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from canonical import canonicalize
from detect import detect
from register import build_register
from receipts import verify_dsse

KID = "did:web:test#k1"


def _ai_manifest():
    k = Ed25519PrivateKey.generate()
    claim = {
        "claim_generator": "t/1",
        "assertions": [{"label": "c2pa.actions", "data": {"digitalSourceType": "trainedAlgorithmicMedia"}}],
        "timestamp": "2026-08-23T00:00:00Z",
    }
    return {"claim": claim, "signature": {
        "alg": "Ed25519", "sig": k.sign(canonicalize(claim)).hex(),
        "public_key_x": base64.urlsafe_b64encode(k.public_key().public_bytes_raw()).decode().rstrip("=")}}


def test_detect_ai_marked_and_receipt_verifies():
    sk = Ed25519PrivateKey.generate()
    out = detect(_ai_manifest(), sign_key=sk, signer_keyid=KID, claims=["marked per Article 50"])
    assert out["verdict"] == "AI_MARKED" and out["ok"]
    assert verify_dsse(out["receipt"], sk.public_key().public_bytes_raw())
    assert out["claims"][0]["status"] == "PASS"


def test_detect_tampered_unverifiable():
    sk = Ed25519PrivateKey.generate()
    m = _ai_manifest()
    m["claim"]["assertions"][0]["data"]["digitalSourceType"] = "digitalCapture"  # after signing
    out = detect(m, sign_key=sk, signer_keyid=KID)
    assert out["verdict"] == "UNVERIFIABLE" and not out["ok"]


def test_detect_asset_hash_mismatch():
    sk = Ed25519PrivateKey.generate()
    out = detect(_ai_manifest(), sign_key=sk, signer_keyid=KID, asset_hash="sha256:nope")
    assert out["verdict"] == "UNVERIFIABLE"


def test_register_fails_dsh_overclaims_and_verifies_real_caps():
    sk = Ed25519PrivateKey.generate()
    reg = build_register(sk, signer_keyid=KID)
    assert reg["summary"]["verified"] >= 4
    assert reg["summary"]["failed"] == 0
    codes = {r["code"] for r in reg["dsh_claim_adjudication"] if r["status"] == "FAIL"}
    assert "claim.sixteen_axes" in codes
    assert "claim.certification" in codes
    assert verify_dsse(reg["receipt"], sk.public_key().public_bytes_raw())
