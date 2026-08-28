"""ClaimGuard — Hugging Face Space + MCP door.

Thin living-board claim check + verify_card proxy.
Full CLI lives in products/claimguard. MCP claimguard.check is not on the worker yet.
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

from door_kit import THEME, footer, living_totals, verify_card
from mcp_client import SITES, check_claim as _check_claim, pretty


def check_claim(claim: str) -> str:
    """Audit a natural-language claim against the living GSPC board.

    Rejects a full-board-measured overclaim, '16 measured axes', Elo-as-grade,
    and certification language. Numeric 'N measured' must match live totals.measured_axes.

    Args:
        claim: The sentence to audit (marketing copy, README line, AEO answer).

    Returns:
        PASS/FAIL findings plus live public_count. Not certification.
    """
    return pretty(_check_claim(claim))


with gr.Blocks(title="ClaimGuard — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# ClaimGuard
**Council of AI · CSOAI Ltd (UK 16939677)**

Honesty surface: [councilof.ai/honesty/](https://councilof.ai/honesty/).
Verify a card: [gspc-verify](https://councilof.ai/gspc-verify/).

This Space MCP-exports a **thin living-board claim check** and `verify_card`.
It does not replace the CLI. It does not certify.

Living counts: `GET https://councilof.ai/api/gspc`. Never freeze a full-board measured claim.
"""
    )
    with gr.Tab("Check claim"):
        claim = gr.Textbox(
            label="Claim",
            placeholder="22 axis · 15 measured",
            lines=3,
        )
        claim_out = gr.Code(label="check_claim", language="json")
        gr.Button("Check against living board").click(
            check_claim, inputs=claim, outputs=claim_out
        )
    with gr.Tab("Verify card"):
        card = gr.Textbox(label="Card JSON or URL", lines=6)
        card_out = gr.Code(label="verify_card", language="json")
        gr.Button("Verify (live MCP)").click(verify_card, inputs=card, outputs=card_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    gr.Markdown(f"{footer()} · [Honesty]({SITES['honesty']})")

if __name__ == "__main__":
    demo.launch(mcp_server=True)
