"""Games catalog — Hugging Face Space + MCP door.

Games load into Council Space on councilof.ai. This Space is not a contest
engine. MCP tools list the catalog and proxy enter-arena / board_totals to
the live worker so any N-site or agent can call the same door.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _candidate in (_HERE, _HERE.parent):
    if (_candidate / "mcp_client.py").exists():
        sys.path.insert(0, str(_candidate))
        break

import gradio as gr

from mcp_client import SITES, fetch_board, mcp_call, pretty

GAMES = [
    {
        "id": "council-space",
        "name": "Council Space",
        "loads_into": SITES["council_space"],
        "note": "Chrome door. Games load here. Arenas stay on the measurement fleet.",
    },
    {
        "id": "coliseum",
        "name": "Coliseum of AI",
        "loads_into": SITES["coliseum"],
        "note": "Law-graded contest chrome. Not preference Elo as a public GSPC grade.",
    },
    {
        "id": "arena-rooms",
        "name": "Contest rooms",
        "loads_into": SITES["arena"],
        "note": "Leftover measurement rooms. Only rooms with a published n are quotable.",
    },
    {
        "id": "city",
        "name": "Council City",
        "loads_into": SITES["city"],
        "note": "Governed multi-agent city. Same living board. No second scoreboard.",
    },
]


def list_games() -> str:
    """List Council of AI games and where each one loads.

    Returns:
        JSON catalog. Games load on councilof.ai — this Space is not the engine.
    """
    board = fetch_board()
    return pretty(
        {
            "kind": "games-catalog",
            "honesty": "Catalog door. No contest engine on this Space.",
            "board": board,
            "games": GAMES,
            "mcp": SITES["mcp"],
            "verify": SITES["verify"],
        }
    )


def living_totals() -> str:
    """Return live GSPC board totals via the published MCP board_totals tool.

    Returns:
        Live slot count and measured count, labelled separately. Never summed.
    """
    via_mcp = mcp_call("board_totals")
    if via_mcp.get("ok"):
        return pretty(via_mcp)
    return pretty(fetch_board())


def enter_arena(agent_card_url: str, consent: bool) -> str:
    """Self-enrol an agent into Council Space via live MCP enter-arena.

    Args:
        agent_card_url: https URL of the visiting A2A agent card.
        consent: Must be true. Machine-readable consent to be measured.

    Returns:
        Unsigned intake receipt from the live worker, or UNREACHABLE.
    """
    if not consent:
        return pretty(
            {
                "ok": False,
                "state": "CONSENT_REQUIRED",
                "honesty": "enter-arena will not run without consent:true.",
            }
        )
    return pretty(
        mcp_call(
            "enter-arena",
            {"agent_card_url": agent_card_url.strip(), "consent": True},
        )
    )


THEME = gr.themes.Soft(
    primary_hue="stone",
    secondary_hue="amber",
    neutral_hue="stone",
)

with gr.Blocks(title="Games catalog — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# Games catalog
**Council of AI · CSOAI Ltd (UK 16939677)**

Games load into [Council Space](https://councilof.ai/gspc-arena).
This Space is a door + MCP server. It is **not** the contest engine.

Living counts: `GET https://councilof.ai/api/gspc` · MCP: `https://councilof.ai/mcp`  
Measurement, not certification. Empty slots stay empty.
"""
    )
    with gr.Tab("Catalog"):
        catalog_out = gr.Code(label="games", language="json")
        gr.Button("List games").click(list_games, outputs=catalog_out)
        demo.load(list_games, outputs=catalog_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    with gr.Tab("Enter arena"):
        url = gr.Textbox(
            label="Agent card URL",
            placeholder="https://example.org/.well-known/agent-card.json",
        )
        consent = gr.Checkbox(label="I consent to be measured", value=False)
        arena_out = gr.Code(label="enter-arena receipt", language="json")
        gr.Button("Enter arena (live MCP)").click(
            enter_arena, inputs=[url, consent], outputs=arena_out
        )
    gr.Markdown(
        f"[City]({SITES['city']}) · [Coliseum]({SITES['coliseum']}) · "
        f"[Arena]({SITES['arena']}) · [Verify]({SITES['verify']}) · "
        f"[MCP]({SITES['mcp']})"
    )

if __name__ == "__main__":
    demo.launch(mcp_server=True)
