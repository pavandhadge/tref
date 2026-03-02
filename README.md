# tref

`tref` is an offline-first terminal helper and Python library for versioned developer references.

## Install

```bash
pip install .
```

## CLI

```bash
# explicit library@version
tref pandas@2.2 "groupby multiple columns agg mean"

# plain query with library auto-detection
tref "how to rebase current branch safely"

# strict trust/freshness mode (fail closed)
tref --freshness-policy strict --strict-fresh "docker run port mapping"

# offline-only mode (no network)
tref --freshness-policy offline-only "pandas groupby agg"

# update indexes with strict verification
tref update --strict-verify

# status + diagnostics
tref status
tref doctor

# benchmark hot query latency
tref bench "groupby multiple columns agg mean" --library pandas --version 2.2 --runs 30

# remote endpoint configuration
tref remote show
tref remote set --releases-api-url https://api.github.com/repos/myorg/my-kb/releases/latest

# build custom index from kb path
tref build-index ./kb --output ~/.tref/custom
```

## Python API

```python
from tref import ask

result = ask(
    "groupby multiple columns agg mean",
    library="pandas",
    version="2.2",
    freshness_policy="strict",
)
print(result["provenance"])
```

## Core Capabilities

- Grounded retrieval against curated markdown KB files.
- One index per `library@version`.
- Auto-detection when query is unambiguous; ambiguity returns explicit error candidates.
- Freshness policy modes: `strict`, `warn`, `offline-only`.
- Provenance in every response: build hash, KB commit, embedding model, policy.
- Verified update pipeline: checksum verification and optional signature verification (`cosign verify-blob`).
- Atomic index update with rollback safety.
- Lightweight hybrid retrieval (semantic + lexical overlap rerank).
- Bench + doctor commands for production operations.

## Production Trust Model

- Default verification uses SHA256 checksum asset.
- Optional signature verification is enabled when `TREF_COSIGN_KEY_PATH` is set and signature asset exists.
- Strict modes fail closed when verification/freshness guarantees cannot be met.

## Environment Variables

- `TREF_HOME`
- `TREF_KB_MANIFEST_URL`
- `TREF_RELEASES_API`
- `TREF_RELEASE_ASSET`
- `TREF_RELEASE_CHECKSUM_ASSET`
- `TREF_RELEASE_SIGNATURE_ASSET`
- `TREF_UPDATE_STRICT_VERIFY`
- `TREF_MAX_INDEX_AGE_DAYS`
- `TREF_FRESHNESS_POLICY`
- `TREF_COSIGN_KEY_PATH`
- `TREF_COSIGN_BIN`
