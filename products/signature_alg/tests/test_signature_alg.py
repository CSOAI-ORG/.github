"""Unit tests for P5 Continuity signature_alg grader."""
from products.signature_alg.grader import signature_alg, Unmeasured


def test_unsigned_unmeasured():
    r = signature_alg([{"payload": "x"}])
    assert r["status"] == "UNMEASURED"
    assert r["pass"] is False


def test_signed_no_alg_fails():
    r = signature_alg([{"sig": "ab" * 32}])
    assert r["status"] == "FAIL"
    assert r["pass"] is False


def test_named_alg_passes():
    r = signature_alg([{"sig": "ab" * 32, "alg": "Ed25519"}])
    assert r["pass"] is True
    assert r["status"] == "PASS"


def test_partial_label_fails():
    r = signature_alg([{"sig": "aa", "alg": "Ed25519"}, {"sig": "bb"}])
    assert r["pass"] is False


def test_expected_decl():
    ok = signature_alg([{"sig": "aa", "algorithm": "Ed25519"}], expected_decl="Ed25519")
    assert ok["pass"] and ok["expected_decl_match"] is True
    bad = signature_alg([{"sig": "aa", "algorithm": "Ed25519"}], expected_decl="ML-DSA-65")
    assert bad["pass"] is False and bad["expected_decl_match"] is False


def test_empty_raises():
    try:
        signature_alg([])
        assert False, "expected Unmeasured"
    except Unmeasured:
        pass
