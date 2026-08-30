"""GSPC Verify — Hugging Face Space + MCP door.

Stranger verification lives on councilof.ai/gspc-verify/.
This Space MCP-exports verify_card and list_cards. Ed25519, not a blockchain toy.
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

from door_kit import THEME, footer, list_cards, living_totals, verify_card
from mcp_client import SITES, fetch_board, pretty


def verify_door() -> str:
    """Open the stranger-verify door.

    Returns:
        JSON door card. In-browser verify is on councilof.ai/gspc-verify/.
    """
    return pretty(
        {
            "kind": "gspc-verify-door",
            "site": SITES["verify"],
            "os": SITES["os"],
            "mcp": SITES["mcp"],
            "board": fetch_board(),
            "honesty": (
                "Ed25519 card verify via live MCP. "
                "Not an Ethereum certificate toy. No account, no fee."
            ),
        }
    )


with gr.Blocks(title="GSPC Verify — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# GSPC Verify
**Council of AI · CSOAI Ltd (UK 16939677)**

Live verify: [councilof.ai/gspc-verify/](https://councilof.ai/gspc-verify/) — no account, no fee.

This Space MCP-exports `verify_card` and `list_cards` so any site can verify
a signed card. **Not** a blockchain certificate playground.

Measurement, not certification.
"""
    )
    with gr.Tab("Verify door"):
        door_out = gr.Code(label="gspc-verify", language="json")
        gr.Button("Open verify door").click(verify_door, outputs=door_out)
        demo.load(verify_door, outputs=door_out)
    with gr.Tab("Verify card"):
        card = gr.Textbox(label="Card JSON or URL", lines=6)
        card_out = gr.Code(label="verify_card", language="json")
        gr.Button("Verify (live MCP)").click(verify_card, inputs=card, outputs=card_out)
    with gr.Tab("List cards"):
        axis = gr.Textbox(label="Axis filter (optional)", placeholder="governance")
        limit = gr.Slider(1, 50, value=10, step=1, label="limit")
        list_out = gr.Code(label="list_cards", language="json")
        gr.Button("List cards").click(list_cards, inputs=[axis, limit], outputs=list_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    gr.Markdown(footer())

if __name__ == "__main__":
    demo.launch(mcp_server=True)
