"""FAQ — Hugging Face Space + MCP door.

Honest machine-readable answers. Counts always come from GET /api/gspc.
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

from door_kit import THEME, footer, living_totals
from mcp_client import SITES, fetch_board, pretty


def faq_door() -> str:
    """Return the living FAQ: what Council OS is, how to MCP, how to verify.

    Returns:
        JSON FAQ. Axis counts are quoted from the living board, never frozen.
    """
    board = fetch_board()
    return pretty(
        {
            "kind": "council-faq",
            "site": SITES["faq"],
            "os": SITES["os"],
            "board": board,
            "answers": [
                {
                    "q": "What is Council OS?",
                    "a": "The one public product door. Live at https://councilof.ai/os and /?lobby=home.",
                },
                {
                    "q": "How many axes are measured?",
                    "a": "Quote totals.public_count from GET /api/gspc. Do not freeze a full-board measured claim.",
                    "live": board.get("public_count"),
                },
                {
                    "q": "Is this certification?",
                    "a": "No. Measurement, not certification. Empty slots stay empty.",
                },
                {
                    "q": "How do I verify a grade?",
                    "a": "https://councilof.ai/gspc-verify/ — no account, no fee. Or MCP verify_card.",
                },
                {
                    "q": "How do I MCP to Council OS from anywhere?",
                    "a": "Add a product Space at huggingface.co/settings/mcp, or call https://councilof.ai/mcp directly.",
                },
                {
                    "q": "What are the 16 jails?",
                    "a": "jail-probe families 1–16 on the live worker. That is not 16 board axes.",
                },
                {
                    "q": "Is there a public Elo league?",
                    "a": "No. GSPC public ranking is Wilson + McNemar.",
                },
            ],
            "mcp": SITES["mcp"],
            "honesty": "FAQ door. Counts are live or UNREACHABLE — never a cached table.",
        }
    )


with gr.Blocks(title="FAQ — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# FAQ
**Council of AI · CSOAI Ltd (UK 16939677)**

Live FAQ: [councilof.ai/faq/](https://councilof.ai/faq/).

Machine-readable answers for N-sites and agents. Counts come from
`GET /api/gspc`. This Space does not freeze a table.
"""
    )
    with gr.Tab("FAQ"):
        faq_out = gr.Code(label="faq", language="json")
        gr.Button("Load FAQ").click(faq_door, outputs=faq_out)
        demo.load(faq_door, outputs=faq_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    gr.Markdown(footer())

if __name__ == "__main__":
    demo.launch(mcp_server=True)
