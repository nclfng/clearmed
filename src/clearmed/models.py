"""Single choke point for every LLM call, so the pipeline stays provider-agnostic.

Swap DEFAULT_MODEL (or pass `model=` per agent) to run the same graph across every leaderboard
model. LiteLLM model strings: https://docs.litellm.ai/docs/providers
Set the API key that matches your model, e.g. OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY.
"""
from __future__ import annotations

import litellm

DEFAULT_MODEL = "gpt-4o-mini"  # any LiteLLM model string


def call_model(system: str, user: str, model: str = DEFAULT_MODEL, temperature: float = 0.0) -> str:
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
