"""Verify each committed detector-interop case matches its declared label.

Ties docs/detector-interop/cases/* into CI: a case that stops verifying (or whose
label drifts) fails the batch. Uses ClaimGuard's C2PA verifier — the same code the
site Function and CLI use.
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CG = os.path.abspath(os.path.join(_HERE, "..", "..", "products", "claimguard"))
if _CG not in sys.path:
    sys.path.insert(0, _CG)

import pytest

from c2pa import verify_c2pa_manifest

CASES_DIR = os.path.abspath(os.path.join(_HERE, "..", "..", "docs", "detector-interop", "cases"))


def _case_dirs():
    if not os.path.isdir(CASES_DIR):
        return []
    return [os.path.join(CASES_DIR, d) for d in sorted(os.listdir(CASES_DIR))
            if os.path.isfile(os.path.join(CASES_DIR, d, "manifest.json"))]


def test_cases_present():
    assert _case_dirs(), "no detector-interop cases found"


@pytest.mark.parametrize("case", _case_dirs())
def test_case_matches_label(case):
    manifest = json.load(open(os.path.join(case, "manifest.json")))
    label = json.load(open(os.path.join(case, "label.json")))
    res = verify_c2pa_manifest(manifest)
    if label["expected_verdict"] == "AI_MARKED":
        assert res.ok and res.is_ai_marked, f"{case}: expected AI_MARKED, got ok={res.ok} ai={res.is_ai_marked}"
        if label.get("expected_source_type"):
            assert label["expected_source_type"] in (res.source_type or ""), \
                f"{case}: source_type {res.source_type} != {label['expected_source_type']}"
    elif label["expected_verdict"] == "UNVERIFIABLE":
        assert not res.ok, f"{case}: expected UNVERIFIABLE"
