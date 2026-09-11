"""Single choke point for every LLM call, so the pipeline stays provider-agnostic.

This project runs entirely on FREE, LOCAL models via Ollama — no API keys, no billing,
no paid trial credits. Nobody needs to sign up for or pay for anything.

Setup (one-time, per person):
    1. Install Ollama: https://ollama.com/download
    2. Pull a small model that runs on a normal laptop, e.g.:
           ollama pull gemma2:2b
       (swap for a different model to compare on the leaderboard, e.g. llama3.2 or mistral —
       just make sure everyone can actually run it locally before the team commits to it)
    3. Leave the Ollama app/service running in the background — that's the local server
       LiteLLM talks to (http://localhost:11434), no key required.

Swap DEFAULT_MODEL (or pass `model=` per agent) to run the same graph across every leaderboard
model — as long as it's another local Ollama model, this stays free. LiteLLM + Ollama:
https://docs.litellm.ai/docs/providers/ollama

Do NOT point this at a paid hosted API (OpenAI/Anthropic/Google) for this project — we are
not spending money or using paid/trial API credits. If your machine can't run a local model,
use a free Colab notebook running Ollama instead of a hosted API.
"""
from __future__ import annotations

import litellm

DEFAULT_MODEL = "ollama/gemma2:2b"  # any local Ollama model string — free, no API key needed


def call_model(system: str, user: str, model: str = DEFAULT_MODEL, temperature: float = 0.0) -> str:
    # dont change, for free / local ollama models to avoid api keys
    """Return the model's text response for a (system, user) prompt pair."""
    resp = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    return resp["choices"][0]["message"]["content"]
