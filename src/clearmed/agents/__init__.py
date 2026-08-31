"""One module per agent. Each exposes a single pure function the pipeline calls.

  extractor.extract(source)          -> atoms JSON string
  simplifier.simplify(source, atoms) -> draft
  verifier.verify(draft, atoms)      -> verdict JSON string
  refiner.refine(draft, verdict)     -> corrected draft
  readability.polish(draft)          -> final text
"""
