#!/usr/bin/env python3
"""Generate index.json enumerating every detector-interop case + its label.

Machine-readable manifest for HF / agents. Deterministic (sorted); a drift between
index.json and the cases on disk fails CI (harness/tests/test_interop_index.py).

    python docs/detector-interop/build_index.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(HERE, "cases")


def build() -> dict:
    rows = []
    for name in sorted(os.listdir(CASES)):
        d = os.path.join(CASES, name)
        mf = os.path.join(d, "manifest.json")
        lf = os.path.join(d, "label.json")
        if not (os.path.isfile(mf) and os.path.isfile(lf)):
            continue
        label = json.load(open(lf))
        rows.append({
            "case": name,
            "mark": label.get("mark"),
            "expected_verdict": label.get("expected_verdict"),
            "expected_source_type": label.get("expected_source_type"),
            "manifest": f"cases/{name}/manifest.json",
        })
    return {
        "schema": "csoai.detector-interop-index/0.1",
        "count": len(rows),
        "cases": rows,
    }


if __name__ == "__main__":
    idx = build()
    out = os.path.join(HERE, "index.json")
    with open(out, "w") as f:
        json.dump(idx, f, indent=2)
        f.write("\n")
    print(f"wrote {out} ({idx['count']} cases)")
