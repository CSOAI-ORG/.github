"""Live MCP client checks — no invented 22/22."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp_client import (
    JAIL_FAMILIES,
    SITES,
    check_claim,
    fetch_board,
    load_fabric,
    mcp_call,
    pretty,
)


def test_sixteen_jail_families():
    assert JAIL_FAMILIES == [str(i) for i in range(1, 17)]


def test_sites_point_at_apex():
    for key in (
        "city",
        "coliseum",
        "arena",
        "council_space",
        "os",
        "faq",
        "east_west",
        "honesty",
        "mcp",
        "board",
    ):
        assert SITES[key].startswith("https://councilof.ai")


def test_fetch_board_is_live_or_unreachable():
    board = fetch_board()
    assert board["state"] in {"LIVE", "UNREACHABLE"}
    if board["state"] == "LIVE":
        assert board["axes"] == 22
        assert board["measured_axes"] == 15
        assert board["unmeasured_axes"] == 7
        assert "22.22" not in pretty(board)


def test_board_totals_tool():
    result = mcp_call("board_totals")
    assert result["state"] in {"LIVE", "UNREACHABLE", "MCP_ERROR"}
    if result["state"] == "LIVE":
        text = pretty(result)
        assert "22" in text
        assert "15" in text


def test_check_claim_rejects_overclaims():
    board = fetch_board()
    if board["state"] != "LIVE":
        return
    bad = check_claim("all 22 measured")
    assert bad["ok"] is False
    assert bad["findings"]
    sixteen = check_claim("we have 16 measured axes")
    assert sixteen["ok"] is False
    elo = check_claim("public Elo league")
    assert elo["ok"] is False
    live = check_claim(f"{board['measured_axes']} measured")
    assert live["ok"] is True


def test_load_fabric_lists_product_doors():
    fabric = load_fabric()
    assert fabric.get("schema") == "csoai.hf-product-spaces/1"
    ids = {row["id"] for row in fabric.get("spaces") or []}
    assert "csoai/council-os" in ids
    assert "csoai/mcp-fabric" in ids
    assert "csoai/gspc-verify" in ids
    assert len(ids) >= 12
