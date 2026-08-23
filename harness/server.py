"""Council-OS reference backend (stdlib http.server) — aligns all moves.

Routes:
  GET  /                              -> frontend (web/index.html)
  GET  /api/health                    -> liveness + supported layers
  GET  /api/gspc                      -> signed board fixture (Move: truth rail)
  GET  /.well-known/agent-card.json   -> agent-card (Move 4)
  GET  /.well-known/ai-content-detection.json -> detection descriptor (Move 1)
  GET  /.well-known/harness-key.json  -> demo signer pubkey (b64url raw)
  GET  /api/detector-interop          -> signed interop matrix (Move 5)
  GET  /api/attestations/board.intoto.json -> board as in-toto/DSSE (Move 2)
  GET  /api/register                  -> self-verifying capability register
  POST /api/detect                    -> Article 50 detection + signed receipt (Move 1)
  POST /api/claimguard                -> run ClaimGuard over posted board/claims/c2pa

Demo signer key is generated at boot (did:web:localhost#harness-demo). The real
board key is the estate-chain lane — see docs/KEY_GOVERNANCE.md.
"""
from __future__ import annotations

import base64
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

_HERE = os.path.dirname(os.path.abspath(__file__))
_CG = os.path.abspath(os.path.join(_HERE, "..", "products", "claimguard"))
for p in (_HERE, _CG):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402

import claimguard  # noqa: E402
from board import make_board  # noqa: E402
from detect import detect  # noqa: E402
from register import build_register  # noqa: E402
from receipts import MEASUREMENT_PREDICATE, sign_payload_as_receipt  # noqa: E402

SIGNER_KEYID = "did:web:localhost#harness-demo"
_KEY = Ed25519PrivateKey.generate()
_PUB = _KEY.public_key().public_bytes_raw()
_BOARD = make_board(_KEY, signer=SIGNER_KEYID)


def _agent_card() -> dict[str, Any]:
    return {
        "name": "Council of AI — measurement agent (harness)",
        "provider": {"organization": "CSOAI Ltd", "url": "https://councilof.ai"},
        "did": "did:web:csoai.org",
        "doi": "10.5281/zenodo.21991104",
        "capabilities": {"signed_receipts": True, "streaming": False},
        "skills": [
            {"id": "measure", "description": "Deterministic GSPC axis grade (signed)"},
            {"id": "verify", "description": "Verify a signed board/receipt"},
            {"id": "detect", "description": "Article 50 / C2PA provenance verify (free)"},
            {"id": "claimguard.check", "description": "Fail overclaims + unbacked Article 50 marking"},
        ],
        "endpoints": {"detect": "/api/detect", "gspc": "/api/gspc", "register": "/api/register"},
    }


def _sample_manifest() -> dict[str, Any]:
    """A freshly-signed VALID AI manifest so the UI 'Detect' shows AI_MARKED."""
    from canonical import canonicalize
    k = Ed25519PrivateKey.generate()
    claim = {
        "claim_generator": "acme-diffusion/2.0",
        "assertions": [{"label": "c2pa.actions", "data": {"digitalSourceType": "trainedAlgorithmicMedia"}}],
        "asset": {"hash": "sha256:1a2b3c", "format": "image/png"},
        "timestamp": "2026-08-23T12:00:00Z",
    }
    return {
        "claim": claim,
        "signature": {
            "alg": "Ed25519", "sig": k.sign(canonicalize(claim)).hex(),
            "public_key_x": base64.urlsafe_b64encode(k.public_key().public_bytes_raw()).decode().rstrip("="),
            "signer": "did:web:acme.example#c2pa-1",
        },
    }


def _detection_descriptor() -> dict[str, Any]:
    return {
        "service": "Council of AI — free AI-content detection",
        "article": "EU AI Act Article 50(2)",
        "verifies": {"metadata_layer": "C2PA-style Ed25519/RFC8785", "watermark_layer": "declared, not checked"},
        "access": "free for all; unrestricted for authorities, media, fact-checkers, researchers, civil society",
        "endpoint": "/api/detect",
        "receipt": "signed in-toto/DSSE detection receipt",
    }


def _interop_matrix() -> dict[str, Any]:
    payload = {
        "schema": "csoai.detector-interop/0.1",
        "marks": ["c2pa", "synthid", "watermark-x"],
        "detectors": ["csoai-detect"],
        "cells": [
            {"detector": "csoai-detect", "mark": "c2pa", "result": "READS",
             "note": "signed-metadata layer verified deterministically"},
            {"detector": "csoai-detect", "mark": "synthid", "result": "CANNOT_READ",
             "note": "watermark layer not decoded (honesty gate)"},
            {"detector": "csoai-detect", "mark": "watermark-x", "result": "CANNOT_READ",
             "note": "no decoder; declared, not faked"},
        ],
    }
    payload["receipt"] = sign_payload_as_receipt(
        payload, _KEY, subject_name="detector-interop", keyid=SIGNER_KEYID,
        predicate_type=MEASUREMENT_PREDICATE)
    return payload


class Handler(BaseHTTPRequestHandler):
    server_version = "CouncilOSHarness/0.1"

    def _send(self, code: int, obj: Any, ctype: str = "application/json") -> None:
        body = obj.encode("utf-8") if isinstance(obj, str) else json.dumps(obj, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):  # quiet
        pass

    def do_OPTIONS(self):
        self._send(204, "")

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            try:
                with open(os.path.join(_HERE, "web", "index.html"), "r", encoding="utf-8") as f:
                    return self._send(200, f.read(), "text/html; charset=utf-8")
            except FileNotFoundError:
                return self._send(404, {"error": "frontend not built"})
        if path == "/api/health":
            return self._send(200, {"ok": True, "layers": {"metadata": "verified", "watermark": "declared"}})
        if path == "/api/sample-manifest":
            return self._send(200, _sample_manifest())
        if path == "/api/gspc":
            return self._send(200, _BOARD)
        if path == "/.well-known/agent-card.json":
            return self._send(200, _agent_card())
        if path == "/.well-known/ai-content-detection.json":
            return self._send(200, _detection_descriptor())
        if path == "/.well-known/harness-key.json":
            return self._send(200, {"alg": "Ed25519", "keyid": SIGNER_KEYID,
                                    "public_key_x": base64.urlsafe_b64encode(_PUB).decode().rstrip("=")})
        if path == "/api/detector-interop":
            return self._send(200, _interop_matrix())
        if path == "/api/attestations/board.intoto.json":
            rec = sign_payload_as_receipt(_BOARD, _KEY, subject_name="gspc-board",
                                          keyid=SIGNER_KEYID, predicate_type=MEASUREMENT_PREDICATE)
            return self._send(200, rec)
        if path == "/api/register":
            return self._send(200, build_register(_KEY, signer_keyid=SIGNER_KEYID))
        return self._send(404, {"error": "not found", "path": path})

    def _read_json(self) -> dict[str, Any]:
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return {}
        return json.loads(self.rfile.read(n).decode("utf-8"))

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            body = self._read_json()
        except Exception as e:  # noqa: BLE001
            return self._send(400, {"error": f"bad json: {e}"})
        if path == "/api/detect":
            manifest = body.get("manifest")
            if not isinstance(manifest, dict):
                return self._send(400, {"error": "manifest (object) required"})
            out = detect(manifest, sign_key=_KEY, signer_keyid=SIGNER_KEYID,
                         claims=body.get("claims"), asset_hash=body.get("asset_hash"))
            return self._send(200, out)
        if path == "/api/claimguard":
            board = body.get("board") or _BOARD
            report = claimguard.audit(board, body.get("claims") or [], c2pa=body.get("c2pa"))
            return self._send(200, report.to_dict())
        return self._send(404, {"error": "not found", "path": path})


def run(port: int = 8787) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    return httpd


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    srv = run(p)
    print(f"Council-OS harness on http://127.0.0.1:{p}  (signer {SIGNER_KEYID})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
