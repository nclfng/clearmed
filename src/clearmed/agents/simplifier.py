"""Simplifier agent (owner: M2) — rewrite the source in plain language, grounded by RAG.

Owner TODO: wire `retrieval.retrieve()` into the prompt, measure retrieval hit quality,
tune against the PLABA professional<->plain gold pairs.
"""
from __future__ import annotations

from ..models import DEFAULT_MODEL, call_model

PROMPT = (
    "Rewrite the SOURCE for a patient at an 8th-grade reading level using ONLY the extracted ATOMS. "
    "Use the plain-language DEFINITIONS provided. Add nothing that is not in ATOMS."
)


def simplify(source: str, atoms: str, definitions: str = "", model: str = DEFAULT_MODEL) -> str:
    """Return a patient-friendly draft of `source` constrained to `atoms`."""
    user = f"SOURCE:\n{source}\n\nATOMS:\n{atoms}\n\nDEFINITIONS:\n{definitions or '(none yet)'}"
    return call_model(PROMPT, user, model=model)
