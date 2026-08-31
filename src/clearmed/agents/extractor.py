"""Extractor agent (owner: M1) — pull clinical "atoms" (facts + types) from the source document.

Owner TODO: structured-output prompting, schema enforcement, unit tests on 10 notes,
score recall/precision against MedAESQA "nuggets".
"""
from __future__ import annotations

from ..models import DEFAULT_MODEL, call_model

PROMPT = (
    "Extract every clinically meaningful fact from the SOURCE as a JSON list of atoms, each with "
    '{"text": ..., "type": ...} where type is one of: diagnosis, medication, lab_value, procedure, '
    "instruction. Do not add facts that are not in the SOURCE. Return only the JSON list."
)


def extract(source: str, model: str = DEFAULT_MODEL) -> str:
    """Return a JSON string: a list of {text, type} atoms found in `source`."""
    return call_model(PROMPT, f"SOURCE:\n{source}", model=model)
