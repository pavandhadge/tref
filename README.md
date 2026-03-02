# tref

`tref` is an offline-first terminal helper and Python library for versioned developer references.

## CLI

```bash
tref pandas@2.2 "groupby multiple columns agg mean"
tref "pandas@2.2 groupby multiple columns agg mean"
tref "how to rebase current branch safely"   # auto-detects library when possible
tref update --strict-verify
tref status
tref remote show
tref remote set --releases-api-url https://api.github.com/repos/myorg/my-kb/releases/latest
tref build-index ./kb --output ~/.tref/custom
```

## Python API

```python
from tref import ask

result = ask("groupby multiple columns agg mean", library="pandas", version="2.2")
print(result["results"][0]["citation"])
```

## Goals

- Grounded retrieval against curated markdown KB files.
- Exact `library@version` targeting.
- Auto-detection of library from plain query when unambiguous.
- 100% offline after first index sync.
- Lightweight runtime (`fastembed + faiss-cpu`, no torch).
- Verified update path with SHA256 checksum asset support.

## Production Notes

- `tref update --strict-verify` requires a checksum asset (default `tref-indexes.tar.gz.sha256`).
- `tref --strict-fresh ...` fails closed when freshness/update verification cannot be ensured.
- `tref status` reports freshness and verification state.
- Remote source endpoints can be changed with `tref remote set ...`.
