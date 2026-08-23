"""Move J38 — minimal append-only, hash-chained transparency log.

Each entry commits to the previous head, so any post-hoc edit breaks the chain.
Reuses the estate's RFC 8785 canonicalizer for deterministic leaf hashing. This is
the Phase-1 CSOAI log; Phase-2 mirrors DSSE entries to public Rekor (see
docs/RECEIPT_INTEROP.md).
"""
from __future__ import annotations

import hashlib
import os
import sys
from typing import Any

_CG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "products", "claimguard"))
if os.path.isdir(_CG) and _CG not in sys.path:
    sys.path.insert(0, _CG)

from canonical import canonicalize  # noqa: E402

GENESIS = "0" * 64


def _leaf(prev: str, entry: dict[str, Any]) -> str:
    return hashlib.sha256(canonicalize({"prev": prev, "entry": entry})).hexdigest()


class TransparencyLog:
    def __init__(self) -> None:
        self.entries: list[dict[str, Any]] = []

    def head(self) -> str:
        return self.entries[-1]["leaf"] if self.entries else GENESIS

    def append(self, entry: dict[str, Any]) -> dict[str, Any]:
        prev = self.head()
        rec = {"index": len(self.entries), "prev": prev, "entry": entry, "leaf": _leaf(prev, entry)}
        self.entries.append(rec)
        return rec

    def as_dict(self) -> dict[str, Any]:
        return {"size": len(self.entries), "head": self.head(), "log": self.entries}


def verify_chain(entries: list[dict[str, Any]]) -> bool:
    prev = GENESIS
    for i, rec in enumerate(entries):
        if rec.get("index") != i or rec.get("prev") != prev:
            return False
        if rec.get("leaf") != _leaf(prev, rec.get("entry", {})):
            return False
        prev = rec["leaf"]
    return True
