# AI Engineer Learning & Build Roadmap

This repository documents my end-to-end journey to becoming a **production-ready AI Engineer**.
The focus is not on demos or tutorials, but on **building reliable, testable, and deployable LLM systems**.

Each phase builds on the previous one and produces concrete artifacts.

---

## Phase 0 — LLM Fundamentals (Baseline Reset)

**Goal:** Understand LLM behavior without abstractions.

### What I built
- Raw Python scripts calling LLM APIs
- Structured JSON outputs (no free-form text)
- Basic logging for tokens, latency, and failures

### Key learnings
- Token limits and context windows
- Determinism vs creativity
- Why structured outputs matter in production

📁 Folder: `phase_0_llm_basics/`

---

## Phase 1 — LangChain Core (Deterministic Pipelines)

**Goal:** Use LangChain as an orchestration tool, not a crutch.

### What I learned
- PromptTemplate
- Chat models
- Pydantic output parsers
- Runnable pipelines (`|` operator)

### What I built
- Deterministic LLM pipelines
- Parallel execution (summary + keywords)
- Output validation and retries

📁 Folder: `phase_1_langchain_core/`

---

## Phase 2 — Retrieval Augmented Generation (RAG)

**Goal:** Build explainable, debuggable RAG systems.

### Concepts covered
- Embeddings and similarity search
- Chunking strategies and their impact
- Hallucination failure modes

### What I built
- Document loaders and text splitters
- FAISS-based vector store
- Retrieval + answer synthesis pipeline
- Source citation and fallback responses

📁 Folder: `phase_2_rag/`

---

## Phase 3 — Evaluation & Reliability

**Goal:** Measure quality instead of guessing.

### What I built
- Golden evaluation dataset
- Prompt/version comparison scripts
- Hallucination and refusal tracking
- Structured output validation

### Why this matters
Most GenAI systems fail silently.
This phase ensures improvements are **measurable and repeatable**.

📁 Folder: `phase_3_evaluation/`

---

## Phase 4 — Production AI Engineering

**Goal:** Ship an AI service, not a notebook.

### What I built
- FastAPI backend
- Async and streaming LLM responses
- Caching for embeddings and LLM calls
- Rate limits, timeouts, and retries
- Deployed service with a public endpoint

📁 Folder: `phase_4_production_api/`

---

## Phase 5 — Agents & Tool Use (Controlled)

**Goal:** Use agents only where they make sense.

### What I learned
- Tool calling and ReAct pattern
- Guardrails and bounded reasoning
- Failure recovery

### What I built
- Agent calling custom Python tools
- Explicit step limits
- Safe stopping conditions

📁 Folder: `phase_5_agents/`

---

## Phase 6 — Framework Independence

**Goal:** Prove system-level understanding.

### What I did
- Reimplemented one RAG / agent flow without LangChain
- Compared complexity, control, and debuggability

This phase ensures I understand the **architecture**, not just the framework.

📁 Folder: `phase_6_framework_free/`

---

## Tech Stack
- Python
- FastAPI
- LangChain
- Chroma
- Pydantic
- AsyncIO

---

## Design Principles Followed
- Structured outputs over free text
- Explicit failure handling
- Measurable improvements
- Production-first mindset

---

## Status
🚧 Actively building and iterating  
📌 Focus: reliability, cost control, and system clarity

---

## Next Steps
- Improve evaluation coverage
- Add cost dashboards
- Explore multi-modal inputs
