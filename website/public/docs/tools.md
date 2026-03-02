# Tools & Dependencies

## Python Runtime

- Python `>=3.11`
- `typer`, `rich` (CLI UX)
- `fastembed` (embeddings)
- `faiss-cpu` (vector search)
- `httpx` (network/update)
- `pyyaml`, `python-frontmatter` (KB parsing)

## Website Stack

- React + TypeScript
- Vite
- Tailwind CSS
- lucide-react icons

## Retrieval Stack

- Embedding model: `BAAI/bge-small-en-v1.5`
- Index: FAISS inner-product over normalized vectors
- Ranking: semantic score + lexical overlap + intent section boost

## Operational Tooling

- `scripts/build_index.py`
- `scripts/validate_kb.py`
- `scripts/regression_eval.py`
- GitHub Actions workflows for CI and index artifact build/signing

## Security/Trust Controls

- Release checksum verification
- Optional cosign signature verification
- Freshness policy: `strict`, `warn`, `offline-only`
- Remote endpoint override via `tref remote set`
