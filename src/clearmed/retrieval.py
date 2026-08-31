"""RAG index for the Simplifier (owner: M2).

Build a ChromaDB collection over the MedlinePlus lay-language glossary + authoritative lay-health
guidelines, then `retrieve()` plain-language definitions for the terms in a source document.

Owner TODO: pick an embedding model (hosted vs. sentence-transformers), chunking strategy,
build + persist the index, measure retrieval hit quality.
"""
from __future__ import annotations

PERSIST_DIR = "data/chroma"
COLLECTION = "medlineplus_glossary"


def build_index(docs: list[str]) -> None:
    """Embed `docs` and persist a ChromaDB collection to PERSIST_DIR. Not implemented yet."""
    raise NotImplementedError("M2: build the ChromaDB glossary index here (Week 3-4).")


def retrieve(query: str, k: int = 5) -> list[str]:
    """Return the top-`k` plain-language definition snippets for `query`. Not implemented yet."""
    raise NotImplementedError("M2: query the ChromaDB collection here.")
