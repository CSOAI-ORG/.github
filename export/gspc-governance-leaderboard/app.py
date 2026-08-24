import gradio as gr
import json
import os
from huggingface_hub import hf_hub_download

RESULTS_REPO = os.environ.get("RESULTS_REPO", "csoai/gspc-leaderboard-results")
RESULTS_FILE = "results.jsonl"

def load_results():
    rows = []
    try:
        path = hf_hub_download(repo_id=RESULTS_REPO, filename=RESULTS_FILE, repo_type="dataset")
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    except Exception as e:
        rows = [{"subject": "(loading)", "measured_axes": 0, "total_axes": 14, "as_of": "—", "evidence_url": str(e)}]
    return rows

def build_table():
    rows = load_results()
    headers = ["Subject", "Measured", "Total", "As of", "Evidence"]
    data = []
    for r in rows:
        data.append([
            r.get("subject", ""),
            r.get("measured_axes", ""),
            r.get("total_axes", 14),
            r.get("as_of", ""),
            r.get("evidence_url", ""),
        ])
    return data

with gr.Blocks(title="GSPC Governance Leaderboard") as demo:
    gr.Markdown("""
# GSPC Governance Leaderboard

**Council of AI · CSOAI Ltd (UK #16939677)**

First dedicated governance leaderboard we could find on Hugging Face (searched 2026-08-24).

- Measurement only — not certification
- Renders signed measurement state from [`csoai/gspc-leaderboard-results`](https://huggingface.co/datasets/csoai/gspc-leaderboard-results)
- Submit via PR on the results dataset (maintainer review before merge)
- Scores are never sold
""")
    table = gr.Dataframe(
        headers=["Subject", "Measured", "Total", "As of", "Evidence"],
        datatype=["str", "number", "number", "str", "markdown"],
        interactive=False,
    )
    refresh = gr.Button("Refresh")
    refresh.click(fn=build_table, outputs=table)
    demo.load(fn=build_table, outputs=table)

if __name__ == "__main__":
    demo.launch()
