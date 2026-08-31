# ClearMed — Project Plan & Checklist

Every box we need to tick, laid out across **6 weeks** and split among the five agent owners.
Pair this with a GitHub Projects board (one column per phase); this file is the master list, the board is the working queue.
New to the team? Read [TEAM-NOTES.md](TEAM-NOTES.md) first — how we work and what to get out of the quarter.

- **`[ ]`** = not started · **`[~]`** = in progress · **`[x]`** = done
- Weeks are a guide, not a contract. Weeks marked _(lighter week)_ are deliberately less loaded — use them to catch up, review each other's work, or breathe.
- "Owner" = the person accountable for the box, not necessarily the only person working on it.
- 6 weeks is tight. Scope is deliberately cut to fit: ~30 curated examples (not 50), 3 models on the leaderboard, demo is optional. The **report, presentation, and final polish are not in the weekly plan** — see [Afterwards](#afterwards-on-your-own-time).

---

## Team roles

Each person owns **one agent end-to-end** (prompt, schema, tools, tests, writeup) plus **one cross-cutting hat**, and drives **one notebook**.

| Person | Agent owned | Cross-cutting hat | Notebook |
|---|---|---|---|
| _M1_ | **Extractor** — clinical "atoms" (facts + types) | **Data lead** — dataset downloads, EDA, FHIR flattener | `01_data_eda.ipynb` |
| _M2_ | **Simplifier** — plain-language rewrite + RAG | **Retrieval lead** — the ChromaDB glossary index | `02_retrieval.ipynb` |
| _M3_ | **Verifier** — LLM-as-judge faithfulness scoring | **Eval lead** — the shared harness + the frozen gold set | `03_verifier_calibration.ipynb` |
| _M4_ | **Refiner** — targeted fixes, bounded loop | **Experiments lead** — leaderboard, ablations, cost/latency logging | `04_leaderboard_ablations.ipynb` |
| _M5_ | **Readability** — grade-level + tone control | **Integration lead** — wires the pipeline together, owns the demo | `05_readability.ipynb` |

`06_error_analysis.ipynb` is shared (Phase 3). Fill in real names/handles in the README team table once claimed.

---

## Success criteria

From the README. Numbers are reported **only on the frozen gold set**.

**System performance**
- [ ] ≥80% of outputs at ≤8th-grade reading level (Flesch-Kincaid)
- [ ] ≥85% factual fidelity on the human-annotated test set
- [ ] <10% of outputs contain a clinically meaningful unsupported claim
- [ ] Multi-agent beats single-agent baseline by ≥15% absolute on faithfulness

**Verifier quality**
- [ ] Verifier agrees with human annotators ≥80% of the time (Cohen's κ ≥ 0.6)

**Research contribution**
- [ ] Complete ablation table — marginal contribution of each agent to faithfulness vs. readability
- [ ] Leaderboard across ≥3 models (≥1 API + open weights): faithfulness, readability, latency, cost, openness
- [ ] Error analysis: which content types hallucinate most, which agent catches them

**Artifacts** (repo + notebooks land in the 6 weeks; report/demo/presentation come [afterwards](#afterwards-on-your-own-time))
- [ ] Public GitHub repo, reproducible, one notebook per person
- [ ] Technical report (~10 pages) including the ablation study
- [ ] Hosted demo with per-agent traces + evidence attributions
- [ ] Final presentation
- [ ] Each contributor has a portfolio writeup for their agent

---

## Standing habits (every week)

- [ ] **Weekly team meeting** — each person gives a short, prepared update: what I accomplished this week, what I'm doing next, what's blocking me. Not a status roundtable — come with it ready.
- [ ] **Every update has a visual.** A chart, a table, a screenshot, a before/after example, a trace — no walls of text. If you can't show it, you probably can't explain it yet.
- [ ] Move your board cards; open a PR per finished chunk (small PRs > big ones).
- [ ] Never edit the frozen gold set — propose changes, M3 versions them.
- [ ] Log every model run (model, params, cost, latency) to the shared results sheet.
- [ ] Read at least one paper related to your agent; add a 2-3 sentence takeaway to the shared reading doc (see [TEAM-NOTES.md](TEAM-NOTES.md)).

---

## Phase 1 — Foundations & Single-Agent Baseline (Weeks 1–2)

Goal: everyone can call a model, the data is understood, the eval harness runs, and there's a **single-LLM baseline** to beat.

### Week 1 — Setup, data, metrics
- [ ] **All:** clone repo; `pip install -r requirements.txt && pip install -e .`; run `python -m clearmed.pipeline` for one successful model call
- [ ] **All:** claim your agent + notebook in the README team table
- [ ] **M5:** create the GitHub Projects board (one column per phase), seed it from this file
- [ ] **M1:** download MedAESQA + confirm it loads; download MTSamples; quick EDA in `01_data_eda.ipynb` (report types, length, the 30 machine answers' quality spread, expert "nuggets")
- [ ] **M1:** write the FHIR flattener (M4 generates ~15 Synthea patients as input) — never feed raw FHIR to the LLM
- [ ] **M2:** download PLABA + MedQuAD; skim ~10 professional<->plain pairs in `02_retrieval.ipynb`
- [ ] **M3:** finalize the eval harness (`src/clearmed/eval_harness.py`): Flesch-Kincaid, SMOG, jargon density, length, refusal rate — documented I/O
- [ ] **M3:** write the task spec + "what faithful means" rubric in `docs/`
- [ ] **M4 + M1 + M3:** lock the atom / verdict JSON schemas (`src/clearmed/schemas.py`)

### Week 2 — Baseline + frozen gold set  _(lighter week)_
- [ ] **M5 + M1:** curate ~30 hand-picked (source -> ideal explanation) examples
- [ ] **M3:** freeze v1 gold set = MedAESQA slice + the ~30 curated examples; **tag it in git**
- [ ] **M5:** run the single-LLM baseline (no agents) over the gold set; record readability + a rough faithfulness read in `05_readability.ipynb`
- [ ] **M2:** pick the embedding model + chunking; stand up an empty ChromaDB index
- [ ] **All:** retro — schema right? rubric usable? adjust before building agents

**Phase 1 exit check**
- [ ] Everyone made a real model call · [ ] harness runs on the gold set · [ ] gold set frozen & tagged · [ ] baseline numbers recorded

---

## Phase 2 — Multi-Agent Pipeline & Verifier Calibration (Weeks 3–4)

Goal: the five-agent LangGraph pipeline runs end-to-end and the Verifier is **calibrated against human labels**.

### Week 3 — Build your agent, wire the graph
- [ ] **M1:** Extractor — flesh out `agents/extractor.py`; unit-test on 10 notes
- [ ] **M2:** Simplifier — `agents/simplifier.py` consuming `atoms`; build + populate the ChromaDB index over the MedlinePlus glossary + lay-health guidelines; wire `retrieval.retrieve()` in
- [ ] **M3:** Verifier — `agents/verifier.py` scoring faithfulness / omission / addition / reading-level
- [ ] **M4:** Refiner — `agents/refiner.py` ("fix only what's flagged"); add cost + latency logging to every node
- [ ] **M5:** Readability — `agents/readability.py`; assemble + smoke-test the full graph (`pipeline.py`), confirm the bounded loop stops at 2
- [ ] **All:** first end-to-end run on 5 examples; eyeball outputs together

### Week 4 — Verifier calibration + first comparison
- [ ] **M3:** map MedAESQA human accuracy / evidence-support labels onto the Verifier's output; run it over the 30 machine answers; compute accuracy + Cohen's κ
- [ ] **M3:** iterate the Verifier prompt until **κ ≥ 0.6 / ≥80% agreement**; document what moved the needle (charts in `03_verifier_calibration.ipynb`)
- [ ] **M1:** score Extractor recall/precision against MedAESQA "nuggets"
- [ ] **M4:** run pipeline vs. single-LLM baseline on the full gold set across **3 models** via `litellm`; results in `04_leaderboard_ablations.ipynb`
- [ ] **M5:** pipeline emits a per-agent trace (atoms, draft, verdict) for each run
- [ ] **All:** read ~10 pipeline outputs each; note failure patterns in a shared doc; retro

**Phase 2 exit check**
- [ ] Pipeline runs end-to-end on 3 models · [ ] Verifier κ ≥ 0.6 · [ ] multi-agent vs. baseline numbers exist · [ ] traces captured

---

## Phase 3 — Ablations, Error Analysis & Leaderboard (Weeks 5–6)

Goal: answer *which agents matter* and *where it fails*, then freeze the numbers.

### Week 5 — Ablations + error analysis
- [ ] **M4:** ablation harness — drop one agent at a time (skip Extractor / Verifier / Refiner / Readability / RAG), re-run on the gold set
- [ ] **M4:** ablation table — marginal Δ for each agent on faithfulness AND readability
- [ ] **M3:** categorize hallucinations by content type (lab values, drug names, procedures, instructions) in `06_error_analysis.ipynb`
- [ ] **M1:** which errors originate at extraction vs. simplification?
- [ ] **M2:** do RAG-grounded terms hallucinate less than ungrounded ones? quantify
- [ ] **M1 / M2 / M5:** each write 3–4 sentences interpreting your agent's ablation result — is it pulling its weight?

### Week 6 — Leaderboard + freeze  _(lighter week)_
- [ ] **M4:** final leaderboard — faithfulness, readability, latency, cost, openness across all 3 models
- [ ] **M3:** compute every success-criteria number on the frozen gold set; **lock them** — no more gold-set or prompt changes
- [ ] **M1:** every notebook runs top-to-bottom from a clean checkout
- [ ] **M2:** `data/README.md` + repo README final pass — reproducible from zero
- [ ] **All:** retro; confirm each success-criteria box above is ticked or explicitly noted as missed; divide up report sections for afterwards

**Phase 3 exit check**
- [ ] Ablation table done · [ ] error analysis written · [ ] leaderboard done · [ ] all numbers frozen · [ ] repo reproducible from zero

---

## Afterwards (on your own time)

Not scheduled into the 6 weeks — the team does these after the core work is frozen, at whatever pace works.

- [ ] **Technical report (~10 pages)** — M5 assembles; each person writes their method + agent + ablation/error findings; M3 owns the results section; one editing pass by everyone
- [ ] **Final presentation** — build the deck from the report's figures; rehearse once
- [ ] **Hosted demo** — M5 deploys `app/demo.py` to Hugging Face Spaces or Cloud Run (per-agent traces, faithfulness scores, flagged passages); test on a fresh machine
- [ ] **Portfolio paragraph** — each person: *"I designed and validated the ___ agent against ___"*
- [ ] **Tag `v1.0`** — check the demo link, repo, and report all point at each other
- [ ] _(optional)_ arXiv draft
