import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from canonical import canonicalize
from claimguard import audit, main
from attest import (
    CLAIMGUARD_PREDICATE,
    subject_digest,
    to_dsse,
    to_intoto_statement,
    verify_dsse,
)


def _signed_board():
    key = Ed25519PrivateKey.generate()
    board = {
        "schema": "csoai.gspc-axes/0.5",
        "totals": {"axes": 14, "measured_axes": 13, "quotable_axes": 14,
                   "public_count": "13 measured of 14 quotable"},
        "axes": [{"axis": "governance", "status": "MEASURED", "accuracy": 0.7, "n": 10}],
    }
    board["site_attestation"] = {
        "signer": "did:web:csoai.org#board-attestation-1", "alg": "Ed25519",
        "sig": key.sign(canonicalize(board)).hex(),
        "public_key_x": base64.urlsafe_b64encode(key.public_key().public_bytes_raw()).decode().rstrip("="),
    }
    return board


def test_intoto_statement_shape():
    board = _signed_board()
    rep = audit(board, ["14 quotable axes"])
    stmt = to_intoto_statement(rep.to_dict(), subject_name="gspc-board",
                               subject_sha256=subject_digest(board))
    assert stmt["_type"].endswith("Statement/v1")
    assert stmt["predicateType"] == CLAIMGUARD_PREDICATE
    assert stmt["subject"][0]["digest"]["sha256"] == subject_digest(board)
    assert stmt["predicate"]["ok"] is True


def test_dsse_sign_and_verify():
    board = _signed_board()
    rep = audit(board)
    stmt = to_intoto_statement(rep.to_dict(), subject_name="b", subject_sha256=subject_digest(board))
    k = Ed25519PrivateKey.generate()
    env = to_dsse(stmt, k, keyid="did:web:test#k1")
    assert verify_dsse(env, k.public_key().public_bytes_raw())
    assert not verify_dsse(env, Ed25519PrivateKey.generate().public_key().public_bytes_raw())


def test_cli_intoto_output(capsys, tmp_path):
    # write a signed board to a file and run the CLI with --intoto
    import json as _json
    board = _signed_board()
    bf = tmp_path / "board.json"
    bf.write_text(_json.dumps(board))
    rc = main(["check", "--board", str(bf), "--claim", "14 quotable axes", "--intoto"])
    assert rc == 0
    out = _json.loads(capsys.readouterr().out)
    assert out["predicateType"] == CLAIMGUARD_PREDICATE
