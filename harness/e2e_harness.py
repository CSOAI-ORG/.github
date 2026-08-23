"""End-to-end battery — boots the backend, drives every surface, verifies signatures.

Run: python harness/e2e_harness.py   (exit 0 = all green)
Backend → engines → API → (frontend served) → signed receipts, all checked here.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import threading
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
_CG = os.path.abspath(os.path.join(_HERE, "..", "products", "claimguard"))
for p in (_HERE, _CG):
    if p not in sys.path:
        sys.path.insert(0, p)

import claimguard  # noqa: E402
import server as srv  # noqa: E402
from receipts import verify_dsse, dsse_statement, verify_intoto_subject  # noqa: E402

PORT = 8799
BASE = f"http://127.0.0.1:{PORT}"
fails = 0


def ok(m):
    print(f"  \u2713 {m}")


def bad(m):
    global fails
    fails += 1
    print(f"  \u2717 {m}")


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=10) as r:
        return json.loads(r.read().decode())


def post(path, obj):
    req = urllib.request.Request(BASE + path, data=json.dumps(obj).encode(),
                                 headers={"content-type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


def main():
    httpd = srv.run(PORT)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        pub = base64.urlsafe_b64decode(get("/.well-known/harness-key.json")["public_key_x"] + "==")

        print("## backend + truth rail")
        if get("/api/health").get("ok"):
            ok("/api/health")
        else:
            bad("/api/health")
        board = get("/api/gspc")
        rep = claimguard.audit(board)
        if rep.ok and any(f.code == "attestation.valid" for f in rep.findings):
            ok("/api/gspc signed board verifies via ClaimGuard")
        else:
            bad("/api/gspc board signature")

        print("## Move 1 — Article 50 detection")
        sample = get("/api/sample-manifest")
        d = post("/api/detect", {"manifest": sample, "claims": ["marked per Article 50"]})
        if d["verdict"] == "AI_MARKED":
            ok("detect valid manifest -> AI_MARKED")
        else:
            bad(f"detect valid -> {d['verdict']}")
        if verify_dsse(d["receipt"], pub):
            ok("detection receipt DSSE verifies")
        else:
            bad("detection receipt DSSE")
        if any(c["status"] == "PASS" for c in d.get("claims", [])):
            ok("Article 50 marking claim supported by manifest")
        else:
            bad("Article 50 claim adjudication")
        tampered = json.loads(json.dumps(sample))
        tampered["claim"]["assertions"][0]["data"]["digitalSourceType"] = "digitalCapture"
        dt = post("/api/detect", {"manifest": tampered})
        if dt["verdict"] == "UNVERIFIABLE":
            ok("tampered manifest -> UNVERIFIABLE")
        else:
            bad(f"tampered -> {dt['verdict']}")

        print("## Move 2 — receipt interop (in-toto/DSSE)")
        rec = get("/api/attestations/board.intoto.json")
        stmt = dsse_statement(rec)
        if verify_dsse(rec, pub) and verify_intoto_subject(stmt, board):
            ok("board round-trips as in-toto Statement + DSSE, subject digest matches")
        else:
            bad("board in-toto/DSSE round-trip")

        print("## Move 4 — agent distribution")
        card = get("/.well-known/agent-card.json")
        skills = {s["id"] for s in card.get("skills", [])}
        if {"detect", "verify", "claimguard.check"} <= skills:
            ok("agent-card advertises detect/verify/claimguard.check")
        else:
            bad(f"agent-card skills {skills}")

        print("## Move 5 — detector interop")
        m = get("/api/detector-interop")
        results = {(c["mark"], c["result"]) for c in m["cells"]}
        if ("c2pa", "READS") in results and any(r == "CANNOT_READ" for _, r in results):
            ok("interop matrix: c2pa READS + honest CANNOT_READ cells")
        else:
            bad("interop matrix cells")
        if verify_dsse(m["receipt"], pub):
            ok("interop matrix signed receipt verifies")
        else:
            bad("interop receipt")

        print("## reflexive — capability register + DSH claim adjudication")
        reg = post("/api/claimguard", {"claims": ["17 measured axes", "CSOAI certified this model"]})
        codes = {f["code"] for f in reg["findings"] if f["status"] == "FAIL"}
        axis_codes = {"claim.axis_overcount", "claim.sixteen_axes", "claim.fifteen_axes"}
        if "claim.certification" in codes and (codes & axis_codes):
            ok("ClaimGuard FAILs DSH overclaims (17 axes / certified)")
        else:
            bad(f"claim adjudication codes {codes}")
        r = get("/api/register")
        s = r["summary"]
        if s["failed"] == 0 and s["verified"] >= 4:
            ok(f"register: {s['verified']} verified, {s['unverified']} unverified (owner-gated), 0 failed")
        else:
            bad(f"register summary {s}")
        if any(row["status"] == "FAIL" for row in r["dsh_claim_adjudication"]):
            ok("register records DSH overclaims as FAIL rows (honesty gate)")
        else:
            bad("register claim rows")

        print("## frontend")
        with urllib.request.urlopen(BASE + "/", timeout=10) as resp:
            html = resp.read().decode()
        if "Council OS" in html and "Article 50 detect" in html:
            ok("frontend served (Council OS shell)")
        else:
            bad("frontend html")
    finally:
        httpd.shutdown()

    print()
    if fails:
        print(f"E2E: FAIL — {fails} check(s)")
        return 1
    print("E2E: PASS — backend, engines, receipts, frontend, register all green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
