# ClearMed: A Multi-Agent System for Faithful, Patient-Friendly Medical Explanations

Hospital paperwork (discharge instructions, lab results, care plans) is usually written for other clinicians, not for patients. Most people can't fully understand it, but that's our data! Misreading a dose or missing a follow-up lands patients back in the hospital. That hard-to-read clinical text is what ClearMed takes as input.

We will attempt to rewrite that text in plain language a patient can actually follow. However, AI that rewrites medical text can also *hallucinate*, which can negatively hurt important information. So instead of one AI doing the whole job, ClearMed uses a small team of specialized agents: one pulls out facts, one rewrites them simply, one checks every sentence of the rewrite against the original and flags anything unsupported, one fixes those flags, and one does a final readability pass. The result aims to be both **easy to read** and **traceable to the source document**, and we measure both against human-labeled data.

---

## The Challenge

### The Core Research Question
> If we split the work across a team of specialized agents instead of asking one LLM to do everything, do the explanations come out *both* easier to read *and* more faithful to the source, and **which agents are actually doing the work?**

A single LLM already handles this reasonably well, so is the added structure worth the extra complexity?

### Project Summary
Only about 1 in 10 U.S. adults has the health literacy to comfortably navigate everyday clinical information (National Assessment of Adult Literacy). This **health-literacy gap** has negative consequences, such as misread discharge instructions, misunderstood lab results, and missed medications and follow-up appointments. LLMs are an obvious tool for rewriting this text in plain language, but they are known to **hallucinate**, like inventing a dose, a diagnosis, or an instruction that was never in the source.

ClearMed examines both of these issues, taking de-identified clinical text and running it through a **pipeline of specialized LLM agents** (Extractor, Simplifier, Verifier, Refiner, Readability). This combines retrieval-augmented generation (RAG), source-grounded faithfulness verification, and a bounded refinement loop. The Verifier checks every claim in the rewrite against the original and flags anything unsupported; the Refiner fixes those flags. We build it on public datasets (MTSamples clinical reports, Synthea synthetic records, MedQuAD consumer Q&A, PLABA plain-language pairs) and evaluate faithfulness against the human-annotated **MedAESQA** dataset.

### Success Criteria

**Quantitative system performance**
- **Readability:** ≥80% of outputs at ≤8th-grade reading level (Flesch-Kincaid).
- **Faithfulness:** ≥85% factual fidelity on the human-annotated test set, verified against human labels.
- **Hallucination rate:** <10% of outputs contain a clinically meaningful unsupported claim.
- **Multi-agent vs. single-agent baseline:** ≥15% absolute improvement in faithfulness score.

**Verifier agent quality**
- Verifier agrees with human annotators ≥80% of the time on faithfulness labels (target Cohen's κ ≥ 0.6).

**Ablation analysis (research contribution)**
- A complete ablation table showing the marginal contribution of each agent — answers "which agents matter most for faithfulness vs. readability?"

**Comparative analysis**
- Leaderboard across **≥3 local, open-weight models** (all free via Ollama — no paid API), showing faithfulness, readability, latency, and openness tradeoffs.

**Working artifacts**
- Public GitHub repo with reproducible code: the `clearmed` package plus one notebook per contributor.
- Hosted demo (Hugging Face Spaces or Cloud Run) showing per-agent traces and evidence attributions.
- Technical report (~10 pages) including the ablation study, plus a final presentation.
- Portfolio-ready writeup. Each contributor can speak to their owned agent (e.g., *"I designed and validated the Faithfulness Verifier agent against human-annotated medical text"*).

### Other Possible Cool Features (if there's time...)
#### note: if this goes well, i can ask to extend the project into winter to continue working on it!!
- **Multilingual extension** — add Spanish generation with a parallel Verifier, extending access to Spanish-speaking patients.
- **Personalization layer** — adjustable target reading level and tone through the Readability agent.
- **Agent-debate variant** — replace the single Verifier with a two-agent debate; compare against the single-Verifier ablation.
- **Bias & fairness audit** — does the pipeline perform worse on reports involving non-English names, rare conditions, or specific demographic markers?
- **LoRA fine-tuning experiment** — fine-tune a small open model on patient-friendly explanation pairs and compare against prompt-only baselines.
- **Domain expansion** — apply the pipeline to a high-impact subdomain (oncology discharge summaries, post-partum care, pediatric medication labels).
- **Tool-augmented agents** — give the Extractor a UMLS lookup tool and the Verifier a DrugBank lookup tool; measure whether tools improve verification accuracy.
- **Multimodal clinical data integration** — process visual medical assets (radiology images, ECG waveforms) alongside textual records.
- **Real-time guardrail middleware** — deploy the Verifier as an interceptor that flags unverified clinical claims *before* a final answer is shown.
- **Counterfactual explanation visualizer** — an interactive module showing how changing a lab value or history item alters the multi-agent reasoning path.

### Milestones

- **Weeks 1–2 — Foundations:** understand the data, build the eval harness, freeze the gold set, and stand up a single-LLM baseline to beat.
- **Weeks 3–4 — Pipeline:** build the five agents, wire them into the LangGraph pipeline, and calibrate the Verifier against human labels.
- **Weeks 5–6 — Analysis:** ablations (which agents matter?), error analysis, the model leaderboard, then freeze all numbers.
- **After:** technical report, hosted demo, final presentation, portfolio writeups.

> Full week-by-week checklist with per-person owners -> **[PROJECT-PLAN.md](PROJECT-PLAN.md)**. Mirror it on a GitHub Projects board: **Projects** tab -> **New project** -> **Board** -> a column per phase.

---

## Datasets
All datasets are public and either de-identified, synthetic, or expert-curated. **No PHI/PII is involved.** You will not need every dataset for every agent — start with **MedAESQA** (evaluation backbone) plus **MTSamples + PLABA** (the simplification core). See `data/README.md` for exact download steps and licenses.

| Dataset | What it is | Role here | Format / Size | Where |
|---|---|---|---|---|
| **MedAESQA** | 40 health questions × (1 expert + 30 machine answers); 7,651 evidence excerpts; **human accuracy & evidence-support judgments**; expert "nuggets" | **Primary faithfulness eval + Verifier calibration + Extractor gold** | `medaesqa_v1.json`, small (CC BY 4.0) | OSF: https://osf.io/ydbzq · code: https://github.com/deepaknlp/MedAESQA |
| **MTSamples** | ~5,000 de-identified transcribed medical reports | **Source documents** to simplify | text, <50 MB | https://www.mtsamples.com/ (also on Kaggle) |
| **PLABA** | Professional <-> plain-language biomedical text pairs | **Gold pairs** for the Simplifier | JSON/text | https://osf.io/rnpmf/ (Attal et al., *Scientific Data* 2023) |
| **MedQuAD** | ~47k consumer-health Q&A (NIH/NLM) | Consumer-tone eval; RAG grounding | XML/JSON | https://github.com/abachaa/MedQuAD |
| **Synthea** | Fully synthetic patient records | **FHIR** stress test: discharge summaries / care plans | FHIR JSON, generate as needed | https://synthetichealth.github.io/synthea/ |
| **MedlinePlus glossary** | NLM lay-language definitions of medical terms | **RAG knowledge base** for the Simplifier | text/XML | https://medlineplus.gov/ |
| **MedQA / PubMedQA** *(optional)* | Standard medical-QA benchmarks (USMLE-style MCQ / abstract yes-no-maybe) | Optional extra measure of **clinical accuracy** | JSON | github.com/jind11/MedQA · pubmedqa.github.io |

**Start with MedAESQA.** It is the backbone of your evaluation: *expert human faithfulness labels* — exactly what you need to calibrate the Verifier (Cohen's κ target) — plus expert "nuggets" that serve as gold for the Extractor.

> **Scope note:** MedQA / PubMedQA test *clinical reasoning*, a different task shape than simplification/faithfulness. Treat them as **optional** supplementary benchmarks.

**Key details & gotchas**
- **MedAESQA is for *evaluation*, not training** — 40 questions is a rich gold set but too small to fine-tune on. Its 30 machine answers give a built-in good->bad quality spread to test whether your Verifier separates faithful from unfaithful answers.
- **FHIR is nested and verbose** — write a flattener early; never feed raw FHIR to the LLM.
- **MTSamples/Synthea aren't pre-paired for our task** — your ~50-example baseline set is something you *build*; MedAESQA is the one you *download*.
- **Freeze the gold set early** — version MedAESQA + your curated examples and stop editing them. Silently changing your eval set is the #1 way to make all before/after numbers meaningless.
- **Licensing:** MedAESQA is CC BY 4.0 (attribute the paper). PLABA is research-use — cite Attal et al. 2023, do not redistribute. MTSamples is de-identified; handle with care, don't re-post raw records.

---

## Suggested Approach

**ML Problem Type:** LLM / RAG / multi-agent orchestration (conditional text generation + LLM-as-judge evaluation). This is **not** classic supervised learning — there is no single loss to minimize. Your "model" is a *pipeline*; your "training" is prompt design, retrieval design, and calibration against human labels.

**Reference architecture:**
Extractor (atoms) -> Simplifier (+RAG) -> Verifier (LLM-judge) -> Refiner -> Readability, with a **bounded** Refiner<->Verifier loop.

Two decisions that will save weeks:
1. **Use a deterministic DAG, not free-form recursive agent loops.** Open-ended "agents call agents until satisfied" designs are hard to debug, blow through rate limits, and produce non-reproducible traces. Use a fixed sequence for the main flow plus a bounded loop (max 2 passes) for the one place you want iteration (Refiner<->Verifier) — in LangGraph, a `StateGraph` with a conditional edge and a pass counter. A plain ordered Python function is a fine v1 too.
2. **Build the evaluation harness first, before the agents.** You can't improve what you can't measure. A starter lives in `src/clearmed/eval_harness.py`, and the pipeline skeleton in `src/clearmed/pipeline.py`.

**Recommended stack:** see the [tech-stack table](#resources-to-get-started) below. Two things to hold onto: stay vendor-neutral by routing every model through `litellm` so the same pipeline runs across the whole leaderboard, and use `langgraph` (not free-form agent loops) so the DAG and the one bounded Verifier/Refiner loop stay reproducible.

> **💸 Cost policy: this project is 100% free. No API keys, no paid trial credit, no billing — for anyone, ever.** Every model call runs locally through **Ollama** (free, no signup). Do not sign up for a paid Anthropic/OpenAI/Google API account for this project, even to use free trial credit — we're not spending money or relying on time-limited trials. If your laptop can't run a local model, use a free Colab notebook running Ollama instead.

**Evaluation metrics:**
- Readability: Flesch-Kincaid Grade Level (primary), SMOG (secondary), medical-jargon density, output length, refusal rate.
- Faithfulness: the Verifier's score **calibrated against human labels** — report agreement (accuracy and Cohen's κ) vs. MedAESQA's human annotators; track omission and addition (hallucination) separately.
- System tradeoffs: latency and openness per model for the leaderboard (cost is $0 for all — everything runs on free local models).
- Golden rule: every headline number is reported on the *frozen* gold-standard set.

**Suggested per-contributor ownership** (one agent each, end-to-end):

| Agent | Owns | Core skill built |
|---|---|---|
| Extractor | Structured extraction of clinical "atoms" (facts + types) | Structured-output prompting, schema design |
| Simplifier | Plain-language rewriting with RAG grounding | RAG, retrieval design, prompt engineering |
| Verifier | LLM-as-judge faithfulness scoring + human calibration | Evaluation, annotation, inter-rater agreement |
| Refiner | Targeted fixes to flagged passages, bounded loop | Controlled generation, loop design |
| Readability | Grade-level targeting and tone control | Readability metrics, iterative rewriting |

---

## Resources to Get Started
**Problem space:** AHRQ and CDC "health literacy" resources (why ≤8th-grade is the target); studies on discharge-instruction readability.

**Model stack — 100% free, no API keys, no billing, ever:**
- **Ollama** — runs open-weight models locally, completely free, no signup: https://ollama.com/download
- LiteLLM — one interface to every provider, but we point it *only* at local Ollama models: https://docs.litellm.ai/docs/providers/ollama
- LangGraph docs & tutorials — https://langchain-ai.github.io/langgraph/
- **Do not** sign up for Anthropic / OpenAI / Google API accounts for this project, even for free trial credit — we're not spending money or using time-limited trials. Everyone should be able to run every agent for free, indefinitely.

**Recommended tech stack:**

| Layer | Pick | Why |
|---|---|---|
| Language / env | Python 3.10+, virtualenv or Colab | Standard; Colab gives a free GPU if your laptop can't run a local model |
| Model access | `litellm` pointed at `ollama/<model>` | One API shape, but always routes to your free local Ollama server — no keys |
| Models (all 3 for the leaderboard) | small open-weight models via **Ollama** (e.g. `gemma2:2b`, `llama3.2`, `mistral`) | Free, runs on a normal laptop, no GPU strictly required; pick sizes everyone can actually run |
| Orchestration | `langgraph` | State graph = deterministic DAG + one bounded loop, reproducible traces |
| RAG | `chromadb` + an embedding model | Simple local vector store; `sentence-transformers` + `faiss-cpu` as an offline fallback |
| Metrics | `textstat` (readability), `scikit-learn` (Cohen's κ) | Flesch-Kincaid / SMOG, and Verifier-vs-human agreement |
| Data / viz | `pandas`, `numpy`, `matplotlib`, `seaborn`, `datasets` | EDA and every chart in the notebooks |
| Notebooks | JupyterLab + `nbstripout` | All EDA / calibration / ablation work; `nbstripout` keeps diffs reviewable |
| Demo | `gradio` on Hugging Face Spaces (free) | One-file app, free hosting; Cloud Run if you want a cloud-native target |
| Repo | GitHub + Projects board | Code review on small PRs; board mirrors [PROJECT-PLAN.md](PROJECT-PLAN.md) |

**Other docs & tutorials:**
- `textstat` readability library — https://pypi.org/project/textstat/
- ChromaDB (RAG) — https://docs.trychroma.com/
- Hugging Face Spaces + Gradio (demo) — https://huggingface.co/docs/hub/spaces

**Concepts to search:** LLM-as-a-judge (and its position/verbosity/self-preference biases); faithfulness / hallucination evaluation in summarization (FaithBench as a touchstone); Cohen's κ / inter-annotator agreement; FHIR basics (Condition, MedicationRequest, Procedure, CarePlan).

**Starter code (this repo):** the `clearmed` package in `src/` (`pipeline.py`, `eval_harness.py`, `agents/`), the stub notebooks in `notebooks/`, and `requirements.txt`.

---

## What's in This Repository

```
clearmed/
├── README.md               - you are here
├── PROJECT-PLAN.md          - 6-week checklist, per-person owners
├── TEAM-NOTES.md            - how this team works + what to get out of it (read first)
├── requirements.txt         - dependencies
├── pyproject.toml           - `pip install -e .` -> makes `clearmed` importable
│
├── src/clearmed/         - the package: all shared, reusable code
│   ├── models.py            - one wrapper for every model provider (litellm)
│   ├── schemas.py           - the atom / verdict JSON contracts
│   ├── retrieval.py         - ChromaDB glossary index (RAG for the Simplifier)
│   ├── eval_harness.py      - readability + faithfulness metrics
│   ├── pipeline.py          - the LangGraph graph wiring the agents together
│   └── agents/              - one module per agent
│       ├── extractor.py     ·  simplifier.py  ·  verifier.py
│       └── refiner.py       ·  readability.py
│
├── notebooks/               - one per person; EDA / calibration / ablations / analysis
│   ├── 01_data_eda.ipynb            (M1)   04_leaderboard_ablations.ipynb (M4)
│   ├── 02_retrieval.ipynb           (M2)   05_readability.ipynb          (M5)
│   └── 03_verifier_calibration.ipynb (M3)   06_error_analysis.ipynb      (shared)
│
├── app/demo.py              - Gradio demo (Hugging Face Spaces / Cloud Run)
└── data/                    - datasets live here (see data/README.md)
```

**How it fits together:** `pipeline.py` imports each `agents/*.py`, which import `models.py` for LLM calls and `schemas.py` for the data shapes. Notebooks and `app/demo.py` `import` from the `clearmed` package rather than redefining logic — so the heavy code has one home and the notebooks stay focused on data + visuals.

Jump to: [README.md](README.md) · [PROJECT-PLAN.md](PROJECT-PLAN.md) · [TEAM-NOTES.md](TEAM-NOTES.md) · [src/clearmed/](src/clearmed) · [notebooks/](notebooks) · [app/demo.py](app/demo.py) · [data/](data) · [requirements.txt](requirements.txt) · [pyproject.toml](pyproject.toml)

---

## Team Members

| Name | GitHub Handle | Contribution |
|------|---------------|--------------|
| | | |

---

## Setup and Installation

1. Read [TEAM-NOTES.md](TEAM-NOTES.md) first — how we work and what to get out of the quarter.
2. Clone the repo, make a virtual environment (or use Colab), then `pip install -r requirements.txt` and `pip install -e .` (the second puts the `clearmed` package on your path).
3. **Install [Ollama](https://ollama.com/download)** and pull a small local model, e.g. `ollama pull gemma2:2b`. This is completely free — no API key, no signup, no billing. **We are not using any paid API or trial credit for this project**; everyone runs models locally (or on free Colab if your laptop can't handle it). Leave Ollama running, then run `python -m clearmed.pipeline` for one successful local call.
4. Download MedAESQA (see `data/README.md`); skim MTSamples and generate a few Synthea patients.
5. Run `python -m clearmed.eval_harness` and skim `src/clearmed/pipeline.py` to see the pipeline shape.
6. `nbstripout --install` in the repo so notebook diffs stay clean.
7. Set up the team GitHub Projects board.
8. Claim an agent — Extractor / Simplifier / Verifier / Refiner / Readability — and take the matching notebook.

---

## License
This project is licensed under the MIT License.
