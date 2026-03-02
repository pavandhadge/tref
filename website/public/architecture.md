# tref Architecture

`tref` is a local retrieval system for curated, versioned documentation snapshots.

## High-Level Flow

1. Parse query + optional `library@version`
2. Resolve version (exact/compatible/latest fallback)
3. Load local index for `library/version`
4. Retrieve via semantic + lexical hybrid rank
5. Apply intent-aware reranking by section
6. Build structured response
7. Render CLI or JSON

## Core Modules

- `tref/indexer.py`
  - Validates KB schema and builds chunked FAISS indexes.
- `tref/retrieval.py`
  - Loads FAISS index + chunk metadata; performs hybrid + intent-aware retrieval.
- `tref/api.py`
  - Orchestrates detection, version resolution, retrieval, and guidance shaping.
- `tref/updater.py`
  - Secure snapshot update pipeline with checksum/signature verification and atomic swaps.
- `tref/kb.py`
  - Manifest loading, library detection hints, version resolution.
- `tref/cli.py`
  - Human-readable presentation and command routing.

## Data Artifacts

Per `library/version` index:

- `index.faiss`
- `chunks.jsonl`
- `meta.json`

Global:

- `_manifest.json`
- update state cache with verification metadata

## Trust Model

- Checksum verification in strict update mode.
- Optional required signature verification (policy-driven runtime config).
- Freshness and trust are surfaced in status/output notices.
- Atomic index replacement protects against partial updates.

## Quality Gates

- KB schema validation (`scripts/validate_kb.py`)
- Golden-query regression suite (`scripts/regression_eval.py`)
- CI gate via `tref eval --min-pass-rate`
