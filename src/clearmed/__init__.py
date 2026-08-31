"""ClearMed — multi-agent system for faithful, patient-friendly medical explanations.

Shared code lives here and is imported by the notebooks in ``notebooks/`` and the demo in ``app/``.
Layout:
  models.py       - one wrapper around every model provider (litellm)
  schemas.py      - the atom / verdict JSON contracts shared between agents
  agents/         - one module per agent (Extractor, Simplifier, Verifier, Refiner, Readability)
  pipeline.py     - the LangGraph graph that wires the agents together
  retrieval.py    - the ChromaDB glossary index for the Simplifier's RAG
  eval_harness.py - readability + faithfulness metrics (build this first)
"""

__version__ = "0.0.1"
