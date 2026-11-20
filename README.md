# DevDocs AI

A production-grade **Retrieval-Augmented Generation (RAG)** system for querying developer
documentation. It ingests PDFs, retrieves relevant passages using a **hybrid dense + sparse**
pipeline with reranking, and generates grounded, cited answers — all behind an authenticated
FastAPI service with per-user document isolation and full tracing.

## Features

- **Hybrid retrieval** — dense vector search ([LanceDB](https://lancedb.com) + sentence-transformers)
  fused with **BM25** sparse search via **Reciprocal Rank Fusion (RRF)**.
- **Reranking** — a cross-encoder reranks fused candidates for higher precision.
- **Metadata extraction & filtering** — chunks carry structured metadata used to scope retrieval.
- **Grounded generation with citations** — answers cite their source document, pages, and chunk IDs.
- **Per-user access control** — JWT auth; retrieval is scoped to the document owner, so users can
  only query their own documents.
- **Caching** — in-memory per-user query cache with TTL to cut latency and cost.
- **Observability** — OpenTelemetry tracing exported to [Arize Phoenix](https://github.com/Arize-ai/phoenix).
- **Evaluation** — scripts to evaluate retrieval and answer quality (faithfulness, relevance).

## Architecture

```
PDF → ingest → chunk + metadata → embeddings (LanceDB) + BM25 index
                                              │
Query ──► dense ─┐                            │
         BM25 ───┴─► RRF fusion ─► rerank ─► top-k chunks ─► LLM ─► cited answer
```

## Tech stack

FastAPI · LanceDB · sentence-transformers · bm25s · OpenAI · PyMuPDF · Arize Phoenix · PyJWT · Pydantic · uv


## Setup

```bash
# Install dependencies
uv sync

# Configure environment (see below)
cp .env.example .env   # then fill in the values
```

### Environment variables

| Variable | Description | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | API key for answer generation | _(required)_ |
| `OPENAI_MODEL` | Chat model for generation | `gpt-4.1-mini` |
| `JWT_SECRET_KEY` | Secret used to sign auth tokens | _(required)_ |
| `PHOENIX_COLLECTOR_ENDPOINT` | OTLP traces endpoint | `http://localhost:6006/v1/traces` |

## Usage

### 1. View traces in Phoenix

The app exports OpenTelemetry traces to [Arize Phoenix](https://github.com/Arize-ai/phoenix).
Start a local Phoenix server (it's already installed via `uv sync`):

```bash
uv run phoenix serve
```

This launches the Phoenix UI at `http://localhost:6006`, which also receives OTLP traces
at `http://localhost:6006/v1/traces` — the default `PHOENIX_COLLECTOR_ENDPOINT`.

> To send traces to a different collector, set `PHOENIX_COLLECTOR_ENDPOINT` in your `.env`.

### 2. Ingest documents

Place PDFs in the raw data directory (`data/raw/`), then run the ingestion pipeline (owner-scoped):

```bash
# Document ingestion and chunking
uv run python scripts/ingest.py --owner-id <user-id> 
# Generate embeddings and save to LanceDB
uv run python scripts/save_embeddings.py
# Build the BM25 index
uv run python scripts/build_bm25_index.py
```

### 3. Run the API

```bash
uv run uvicorn devdocs_ai.api:app --reload
```
Interactive docs are then available at `http://localhost:8000/docs`.
