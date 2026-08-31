"""Refiner agent (owner: M4) — fix only what the Verifier flagged. No free rewriting.

Owner TODO: keep edits minimal and localized, design the bounded loop, confirm it converges
within 2 passes on the gold set.
"""
from __future__ import annotations

from ..models import DEFAULT_MODEL, call_model

PROMPT = (
    "Given DRAFT and VERDICT, produce a corrected draft that removes the unsupported claims and "
    "restores the omissions, changing nothing else. If VERDICT says faithful=true, return DRAFT "
    "unchanged."
)


def refine(draft: str, verdict: str, model: str = DEFAULT_MODEL) -> str:
    """Return a corrected draft addressing the issues in `verdict`."""
    return call_model(PROMPT, f"DRAFT:\n{draft}\n\nVERDICT:\n{verdict}", model=model)
