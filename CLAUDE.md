# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (uses UV)
uv sync

# Run the app (queries the graph with a sample question)
python main.py

# Ingest documents into Chroma vector store (one-time setup)
python ingestion.py

# Run all tests
pytest

# Run tests with verbose output
pytest graph/chains/tests/test_chains.py -v

# Format code
black .
isort .
```

## Environment Setup

Requires a `.env` file with:
- `ANTHROPIC_API_KEY` — Claude LLM access
- `VOYAGE_API_KEY` — Voyage AI embeddings (`voyage-4-lite` model)
- `TAVILY_API_KEY` — Web search fallback
- `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, `LANGSMITH_TRACING` — optional tracing

Run `ingestion.py` before `main.py` to populate the `.chroma` vector store.

## Architecture

This is an **Agentic RAG** pipeline built with **LangGraph**. The graph routes questions, retrieves documents, grades their relevance, generates answers, and validates them — looping back if quality checks fail.

### Graph Flow

```
Question → [route_question] → vectorstore or websearch
              ↓
          [retrieve] → Chroma vector store
              ↓
          [grade_documents] → filter irrelevant docs; set web_search flag
              ↓
          [decide_to_generate] → add web results if web_search=True
              ↓
          [generate] → Claude Haiku with retrieved context
              ↓
          [grade_generation_v_documents_and_question]
              ├─ hallucination? → loop back to [generate]
              ├─ doesn't answer question? → [websearch]
              └─ good answer → END
```

### Key Components

| Layer | Location | Purpose |
|---|---|---|
| State | `graph/state.py` | `GraphState` Pydantic model: `question`, `generation`, `web_search`, `documents` |
| Graph | `graph/graph.py` | LangGraph workflow with conditional edges and routing logic |
| Nodes | `graph/nodes/` | `retrieve`, `grade_documents`, `generate`, `web_search` — each mutates `GraphState` |
| Chains | `graph/chains/` | LangChain chains (prompt + LLM): router, generation, retrieval grader, hallucination grader, answer grader |
| Ingestion | `ingestion.py` | Loads URLs via `WebBaseLoader`, splits with `RecursiveCharacterTextSplitter` (250 tokens), stores in Chroma |
| Constants | `graph/consts.py` | Node name constants used as graph edge identifiers |

### LLM Usage

All chains use **Claude Haiku** (`claude-haiku-4-5-20251001` or equivalent). Graders use structured output via `.with_structured_output()` with Pydantic models (`GradeDocuments`, `GradeHallucinations`, `GradeAnswer`). The router uses a `RouteQuery` structured output with `datasource` field (`"websearch"` or `"vectorstore"`).

### Vector Store

Chroma persists to `./.chroma`. Embeddings use Voyage AI (`voyage-4-lite`). The retriever is initialized once in `graph/nodes/retrieve.py` and reused across graph invocations.
