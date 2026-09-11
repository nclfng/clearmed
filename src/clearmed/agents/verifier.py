"""Verifier agent (owner: M3) — LLM-as-judge: is every claim in the draft supported by the atoms?

Owner TODO: calibrate against MedAESQA human labels until Cohen's kappa >= 0.6 / agreement >= 80%,
track omission vs. addition separately, watch for position/verbosity/self-preference bias.
"""
from __future__ import annotations

from ..models import DEFAULT_MODEL, call_model

PROMPT = (
    "Compare DRAFT against ATOMS. Return JSON: "
    '{"faithful": bool, "unsupported_claims": [...], "omissions": [...], "reading_level_ok": bool}. '
    "Be strict: a single unsupported clinical claim means faithful=false."
)


def verify(draft: str, atoms: str, model: str = DEFAULT_MODEL) -> str:
    """Return a JSON verdict string comparing `draft` to `atoms`."""
    return call_model(PROMPT, f"DRAFT:\n{draft}\n\nATOMS:\n{atoms}", model=model)  # dont change, for free / local ollama models to avoid api keys
