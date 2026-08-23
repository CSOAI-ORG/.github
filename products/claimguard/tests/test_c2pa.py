import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from canonical import canonicalize
from claimguard import audit
from c2pa import verify_c2pa_manifest


def _signed_manifest(source_type="trainedAlgorithmicMedia", **claim_overrides):
    key = Ed25519PrivateKey.generate()
    claim = {
        "claim_generator": "demo/1.0",
        "assertions": [{"label": "c2pa.actions", "data": {"digitalSourceType": source_type}}],
        "timestamp": "2026-08-23T00:00:00Z",
    }
    claim.update(claim_overrides)
    sig = key.sign(canonicalize(claim)).hex()
    pub = key.public_key().public_bytes_raw()
    return {
        "claim": claim,
        "signature": {
            "alg": "Ed25519",
            "sig": sig,
            "public_key_x": base64.urlsafe_b64encode(pub).decode().rstrip("="),
            "signer": "did:web:example#k1",
        },
    }


def _signed_board():
    key = Ed25519PrivateKey.generate()
    board = {
        "schema": "csoai.gspc-axes/0.5",
        "totals": {"axes": 14, "measured_axes": 13, "quotable_axes": 14,
                   "public_count": "13 measured of 14 quotable"},
        "axes": [{"axis": "governance", "status": "MEASURED", "accuracy": 0.7, "n": 10}],
    }
    sig = key.sign(canonicalize(board)).hex()
    board["site_attestation"] = {
        "signer": "did:web:csoai.org#board-attestation-1", "alg": "Ed25519", "sig": sig,
        "public_key_x": base64.urlsafe_b64encode(key.public_key().public_bytes_raw()).decode().rstrip("="),
    }
    return board


def test_c2pa_valid_ai_manifest():
    r = verify_c2pa_manifest(_signed_manifest())
    assert r.ok and r.is_ai_marked
    assert any(f.code == "c2pa.signature_valid" for f in r.findings)
    assert any(f.code == "c2pa.ai_source_marked" for f in r.findings)


def test_c2pa_tamper_breaks_signature():
    m = _signed_manifest()
    m["claim"]["assertions"][0]["data"]["digitalSourceType"] = "digitalCapture"
    r = verify_c2pa_manifest(m)
    assert not r.ok
    assert any(f.code == "c2pa.signature_invalid" for f in r.findings)


def test_c2pa_non_ai_source_is_warn_not_ai():
    # Re-sign a manifest that legitimately declares human capture.
    m = _signed_manifest(source_type="digitalCapture")
    r = verify_c2pa_manifest(m)
    assert r.ok  # signature fine
    assert not r.is_ai_marked
    assert any(f.code == "c2pa.non_ai_source" for f in r.findings)


def test_c2pa_missing_signature_fails():
    m = _signed_manifest()
    del m["signature"]
    r = verify_c2pa_manifest(m)
    assert not r.ok
    assert any(f.code == "c2pa.no_signature" for f in r.findings)


def test_article50_claim_supported_by_valid_manifest():
    r = audit(_signed_board(), ["this asset is marked per Article 50"], c2pa=_signed_manifest())
    assert r.ok
    assert any(f.code == "claim.article50_supported" for f in r.findings)


def test_article50_claim_unsupported_without_manifest():
    r = audit(_signed_board(), ["C2PA content credential attached"])
    assert not r.ok
    assert any(f.code == "claim.article50_unsupported" for f in r.findings)


def test_article50_claim_fails_on_tampered_manifest():
    m = _signed_manifest()
    m["claim"]["timestamp"] = "1999-01-01T00:00:00Z"  # mutate after signing
    r = audit(_signed_board(), ["machine-readable mark present"], c2pa=m)
    assert not r.ok
    assert any(f.code == "claim.article50_bad_manifest" for f in r.findings)


def test_article50_claim_fails_when_manifest_not_ai():
    r = audit(_signed_board(), ["marked as AI generated"], c2pa=_signed_manifest(source_type="digitalCapture"))
    assert not r.ok
    assert any(f.code == "claim.article50_not_ai_marked" for f in r.findings)
