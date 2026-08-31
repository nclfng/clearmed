"""Readability agent (owner: M5) — final pass to hit the target grade level and tone.

Owner TODO: hit Flesch-Kincaid <= 8 on >= 80% of outputs without dropping or adding any fact;
optional personalization (adjustable target level / tone).
"""
from __future__ import annotations

from ..models import DEFAULT_MODEL, call_model

PROMPT = (
    "Polish the DRAFT to a Flesch-Kincaid grade level of 8 or below while preserving every fact. "
    "Do not introduce new clinical content. Keep a calm, plain, reassuring tone."
)


def polish(draft: str, model: str = DEFAULT_MODEL) -> str:
    """Return the final, grade-level-targeted version of `draft`."""
    return call_model(PROMPT, f"DRAFT:\n{draft}", model=model)
