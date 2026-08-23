"""C2PA signed-metadata verifier (pragmatic subset) — Article 50 provenance layer.

EU AI Act Article 50(2) (enforceable 2026-08-02; legacy backstop 2026-12-02)
requires that generative-AI output be marked in a **machine-readable** way. The
Commission's Code of Practice pre-clears a dual layer: C2PA Content Credentials
(digitally signed metadata) **plus** a watermark. This module verifies the
*signed-metadata* half — the part ClaimGuard can check deterministically without
pixels — so a "marked per Article 50 / C2PA verified" claim can be proven or
failed the same way we prove or fail a board attestation.

Scope (honest):
- This is **not** a full C2PA (JUMBF / COSE / X.509) implementation. It verifies a
  JSON manifest whose ``claim`` is signed with Ed25519 over RFC 8785 canonical
  bytes — the same provenance primitive the estate already uses for the board.
- It checks the IPTC/schema.org ``digitalSourceType`` assertion that Article 50
  marking hangs on, the signature, and a timestamp.
- Full c2pa-rs manifests can be adapted upstream; the finding codes stay stable.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from canonical import canonicalize

# IPTC DigitalSourceType / schema.org tokens that denote AI-generated media.
# We match on substring so short tokens and full IRIs both resolve, e.g.:
#   "trainedAlgorithmicMedia"
#   "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
#   "https://schema.org/TrainedAlgorithmicMediaDigitalSource"
AI_SOURCE_TOKENS = (
    "trainedalgorithmicmedia",
    "compositewithtrainedalgorithmicmedia",
    "algorithmicmedia",
)
# Human/edited provenance — valid C2PA, but NOT an AI-generation mark.
NON_AI_SOURCE_TOKENS = (
    "digitalcapture",
    "humanedits",
    "minorhumanedits",
    "compositecapture",
)


@dataclass
class C2paFinding:
    status: str  # "PASS" | "FAIL" | "WARN"
    code: str
    message: str


@dataclass
class C2paResult:
    ok: bool = True
    is_ai_marked: bool = False
    source_type: str | None = None
    signer: str | None = None
    findings: list[C2paFinding] = field(default_factory=list)

    def _add(self, status: str, code: str, message: str) -> None:
        self.findings.append(C2paFinding(status, code, message))
        if status == "FAIL":
            self.ok = False


def _b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def _collect_source_types(claim: dict[str, Any]) -> list[str]:
    """Pull every digitalSourceType value out of the manifest's assertions."""
    out: list[str] = []
    for assertion in claim.get("assertions") or []:
        if not isinstance(assertion, dict):
            continue
        data = assertion.get("data")
        if not isinstance(data, dict):
            continue
        for key in ("digitalSourceType", "digital_source_type", "sourceType"):
            val = data.get(key)
            if isinstance(val, str):
                out.append(val)
    # Some manifests put it top-level on the claim.
    for key in ("digitalSourceType", "digital_source_type"):
        val = claim.get(key)
        if isinstance(val, str):
            out.append(val)
    return out


def _classify_source(source_types: list[str]) -> tuple[bool, str | None]:
    """(is_ai_marked, first_matched_token)."""
    for st in source_types:
        low = st.lower()
        if any(tok in low for tok in AI_SOURCE_TOKENS):
            return True, st
    for st in source_types:
        low = st.lower()
        if any(tok in low for tok in NON_AI_SOURCE_TOKENS):
            return False, st
    return False, (source_types[0] if source_types else None)


def verify_c2pa_manifest(
    manifest: dict[str, Any], *, pubkey: bytes | None = None
) -> C2paResult:
    """Verify a signed C2PA-style manifest. Never raises on bad input — reports."""
    res = C2paResult()
    if not isinstance(manifest, dict):
        res._add("FAIL", "c2pa.not_object", "manifest is not a JSON object")
        return res

    claim = manifest.get("claim")
    if not isinstance(claim, dict):
        res._add("FAIL", "c2pa.no_claim", "manifest.claim missing")
        return res

    sig = manifest.get("signature")
    if not isinstance(sig, dict) or not sig.get("sig"):
        res._add("FAIL", "c2pa.no_signature", "manifest.signature.sig missing")
    else:
        res.signer = sig.get("signer")
        x = pubkey
        if x is None:
            xb = sig.get("public_key_x")
            x = _b64url_decode(xb) if isinstance(xb, str) else None
        if x is None:
            res._add("FAIL", "c2pa.no_key", "no public_key_x and no offline key")
        else:
            try:
                pk = Ed25519PublicKey.from_public_bytes(x)
                pk.verify(bytes.fromhex(sig["sig"]), canonicalize(claim))
                res._add(
                    "PASS",
                    "c2pa.signature_valid",
                    f"claim signature verified ({res.signer or 'unnamed signer'})",
                )
            except Exception as e:  # noqa: BLE001 — report, don't crash
                res._add(
                    "FAIL",
                    "c2pa.signature_invalid",
                    f"Ed25519 verify failed over RFC8785 claim: {e}",
                )

    source_types = _collect_source_types(claim)
    if not source_types:
        res._add(
            "FAIL",
            "c2pa.no_source_type",
            "no digitalSourceType assertion (Article 50 marking absent)",
        )
    else:
        is_ai, matched = _classify_source(source_types)
        res.is_ai_marked = is_ai
        res.source_type = matched
        if is_ai:
            res._add("PASS", "c2pa.ai_source_marked", f"digitalSourceType={matched}")
        else:
            res._add(
                "WARN",
                "c2pa.non_ai_source",
                f"digitalSourceType={matched} is not an AI-generation mark",
            )

    if not claim.get("timestamp"):
        res._add("WARN", "c2pa.no_timestamp", "claim.timestamp missing (not tamper-timed)")

    return res
