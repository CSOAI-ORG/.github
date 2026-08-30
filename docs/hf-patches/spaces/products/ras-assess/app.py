"""RAS assess — Hugging Face Space + MCP door.

RAS = Receipts + Arena + Scorecard over the AG-UI wire.
Not a separate RAS product string. Door to lobby / verify / arena.
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

from door_kit import THEME, enter_arena, footer, living_totals, verify_card
from mcp_client import SITES, fetch_board, pretty


def ras_door() -> str:
    """Open the RAS (Receipts + Arena + Scorecard) door.

    Returns:
        JSON door card. RAS is the AG-UI path, not a second product brand.
    """
    return pretty(
        {
            "kind": "ras-assess-door",
            "meaning": "Receipts + Arena + Scorecard over AG-UI",
            "lobby": SITES["lobby"],
            "os": SITES["os"],
            "verify": SITES["verify"],
            "arena": SITES["arena"],
            "mcp": SITES["mcp"],
            "board": fetch_board(),
            "honesty": "Not a separate RAS product. Same living board. No second scorecard.",
        }
    )


with gr.Blocks(title="RAS assess — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# RAS assess
**Council of AI · CSOAI Ltd (UK 16939677)**

**RAS = Receipts + Arena + Scorecard** on the AG-UI wire.
Lobby: [/?lobby=home](https://councilof.ai/?lobby=home).

This Space MCP-connects that path. It does not host a second scorecard.
Measurement, not certification.
"""
    )
    with gr.Tab("RAS door"):
        door_out = gr.Code(label="ras", language="json")
        gr.Button("Open RAS door").click(ras_door, outputs=door_out)
        demo.load(ras_door, outputs=door_out)
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
    with gr.Tab("Verify receipt"):
        card = gr.Textbox(label="Card JSON or URL", lines=6)
        card_out = gr.Code(label="verify_card", language="json")
        gr.Button("Verify (live MCP)").click(verify_card, inputs=card, outputs=card_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    gr.Markdown(footer())

if __name__ == "__main__":
    demo.launch(mcp_server=True)
