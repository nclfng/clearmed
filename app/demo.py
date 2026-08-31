"""ClearMed demo app (owner: M5) — Gradio UI for Hugging Face Spaces / Cloud Run.

Paste a de-identified clinical note, run the pipeline, and show the final explanation plus the
per-agent trace (atoms, draft, verdict, flagged passages) and evidence attributions.

Run locally:  python app/demo.py
Deploy:       push this file + requirements.txt to a Hugging Face Space (SDK: gradio)
"""
from __future__ import annotations

import gradio as gr

from clearmed.pipeline import build_graph

GRAPH = build_graph()


def run(source: str):
    result = GRAPH.invoke({"source": source})
    trace = f"ATOMS:\n{result.get('atoms', '')}\n\nVERDICT:\n{result.get('verdict', '')}"
    return result.get("final", ""), trace


demo = gr.Interface(
    fn=run,
    inputs=gr.Textbox(lines=12, label="De-identified clinical note"),
    outputs=[gr.Textbox(label="Patient-friendly explanation"), gr.Textbox(label="Per-agent trace")],
    title="ClearMed",
    description="Faithful, patient-friendly medical explanations from a multi-agent pipeline.",
)

if __name__ == "__main__":
    demo.launch()
