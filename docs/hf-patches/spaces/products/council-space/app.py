"""Council Space — Hugging Face Space + MCP door.

Games and contest chrome load on councilof.ai/gspc-arena.
This Space MCP-exports the door + enter-arena. Not the engine.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _candidate in (_HERE, _HERE.parent, _HERE.parent.parent / "play"):
    if (_candidate / "mcp_client.py").exists():
        sys.path.insert(0, str(_candidate))
        break
    if (_candidate / "door_kit.py").exists():
        sys.path.insert(0, str(_candidate))

import gradio as gr

from door_kit import THEME, enter_arena, footer, living_totals
from mcp_client import SITES, fetch_board, pretty


def space_door() -> str:
    """Open the Council Space door (games load here on-site).

    Returns:
        JSON door card. Contest chrome is on councilof.ai/gspc-arena.
    """
    return pretty(
        {
            "kind": "council-space-door",
            "site": SITES["council_space"],
            "os": SITES["os"],
            "city": SITES["city"],
            "coliseum": SITES["coliseum"],
            "arena": SITES["arena"],
            "mcp": SITES["mcp"],
            "board": fetch_board(),
            "honesty": "Door only. Games load on-site. This Space is not the engine.",
        }
    )


with gr.Blocks(title="Council Space — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# Council Space
**Council of AI · CSOAI Ltd (UK 16939677)**

Live surface: [councilof.ai/gspc-arena](https://councilof.ai/gspc-arena) (`/games` is 404 — games load here).

This Space is a door + MCP server. MCP it from any site to reach Council Space / OS.
Measurement, not certification. Not a public Elo league.
"""
    )
    with gr.Tab("Space door"):
        door_out = gr.Code(label="council-space", language="json")
        gr.Button("Open space door").click(space_door, outputs=door_out)
        demo.load(space_door, outputs=door_out)
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
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    gr.Markdown(footer())

if __name__ == "__main__":
    demo.launch(mcp_server=True)
