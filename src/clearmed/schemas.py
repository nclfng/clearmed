"""The JSON contracts shared between agents. Finalize these in Week 2 (M1 + M3 + M4).

Keeping them in one place means every agent agrees on the shape of `atoms` and `verdict`.
Swap these TypedDicts for pydantic models if you want runtime validation.
"""
from __future__ import annotations

from typing import Literal, TypedDict

AtomType = Literal["diagnosis", "medication", "lab_value", "procedure", "instruction"]


class Atom(TypedDict):
    """One clinically meaningful fact pulled from the source document by the Extractor."""

    text: str
    type: AtomType


class Verdict(TypedDict, total=False):
    """The Verifier's judgment of a draft against the extracted atoms."""

    faithful: bool
    unsupported_claims: list[str]
    omissions: list[str]
    reading_level_ok: bool
