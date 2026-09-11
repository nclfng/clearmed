"""The ClearMed pipeline as a LangGraph state graph (owner: M4, integrates everyone's agent).

Shape the SME review asked for: a deterministic DAG, not open-ended recursion, with ONE bounded
loop (Verifier <-> Refiner, hard cap of MAX_REFINE_PASSES).

    Extractor -> Simplifier -> [Verifier <-> Refiner x<=2] -> Readability

Run:  python -m clearmed.pipeline   (needs Ollama installed + running locally — see models.py; no API key)
LangGraph docs: https://langchain-ai.github.io/langgraph/
"""
from __future__ import annotations

from typing import TypedDict

from .agents import extractor, readability, refiner, simplifier, verifier

MAX_REFINE_PASSES = 2  # the ONLY loop in the system


class PipelineState(TypedDict, total=False):
    source: str          # input: the original clinical text
    atoms: str           # Extractor output
    definitions: str     # retrieval output fed to the Simplifier
    draft: str           # current patient-friendly draft
    verdict: str         # Verifier output
    refine_passes: int   # loop counter
    final: str           # output: Readability result


def _extract(state: PipelineState) -> PipelineState:
    return {"atoms": extractor.extract(state["source"])}


def _simplify(state: PipelineState) -> PipelineState:
    draft = simplifier.simplify(state["source"], state["atoms"], state.get("definitions", ""))
    return {"draft": draft, "refine_passes": 0}


def _verify(state: PipelineState) -> PipelineState:
    return {"verdict": verifier.verify(state["draft"], state["atoms"])}


def _refine(state: PipelineState) -> PipelineState:
    draft = refiner.refine(state["draft"], state["verdict"])
    return {"draft": draft, "refine_passes": state.get("refine_passes", 0) + 1}


def _readability(state: PipelineState) -> PipelineState:
    return {"final": readability.polish(state["draft"])}


def _route_after_verify(state: PipelineState) -> str:
    """Bounded loop: refine again only if unfaithful AND under the pass cap."""
    faithful = '"faithful": true' in state.get("verdict", "").lower()
    if faithful or state.get("refine_passes", 0) >= MAX_REFINE_PASSES:
        return "readability"
    return "refiner"


def build_graph():
    from langgraph.graph import END, START, StateGraph

    g = StateGraph(PipelineState)
    g.add_node("extractor", _extract)
    g.add_node("simplifier", _simplify)
    g.add_node("verifier", _verify)
    g.add_node("refiner", _refine)
    g.add_node("readability", _readability)

    g.add_edge(START, "extractor")
    g.add_edge("extractor", "simplifier")
    g.add_edge("simplifier", "verifier")
    g.add_conditional_edges("verifier", _route_after_verify, ["refiner", "readability"])
    g.add_edge("refiner", "verifier")  # back to the judge; refine_passes caps the loop
    g.add_edge("readability", END)
    return g.compile()


if __name__ == "__main__":
    print("Extractor -> Simplifier -> [Verifier <-> Refiner x<=2] -> Readability")
    graph = build_graph()
    # result = graph.invoke({"source": "<paste a de-identified clinical note>"})
    # print(result["final"])
