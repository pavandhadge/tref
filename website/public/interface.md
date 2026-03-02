# tref CLI Interface & Commands

`tref` is an offline-first, versioned developer reference CLI.

## Core Query

- `tref <query>`
- `tref <library@version> "query"`

Examples:

```bash
tref "pandas@2.2 groupby multiple columns agg mean"
tref "git@2.44 create a new branch and switch"
```

## Main Commands

- `tref query [LIB@VER] QUERY`
  - Default query command (auto-inserted when omitted).
- `tref update [--strict-verify]`
  - Pull latest index snapshot from release assets.
- `tref status`
  - Show freshness, trust, and remote configuration.
- `tref doctor`
  - Local diagnostics summary.
- `tref bench QUERY --library LIB --version VER --runs N`
  - Local latency/memory benchmark.
- `tref eval --index-root PATH --min-pass-rate 1.0`
  - Regression gate using golden queries.
- `tref build-index KB_PATH --output OUT`
  - Build local FAISS indexes from KB markdown.
- `tref remote show|set|reset`
  - Manage remote endpoints/asset names.

## Configuration (No Inline Env Needed)

For normal usage, configure once and reuse:

```bash
tref remote set --releases-api-url <url> --kb-manifest-url <url>
tref remote show
```

Trust policy and related settings can be maintained in your local `tref` config/state rather than passed on every command.

## Important Flags

- `--json`: machine-readable output for agents.
- `--verbose`: show extended preview/sections.
- `--full-doc`: dump full matched doc sections.
- `--lang <language>`: prefer examples by language (`bash`, `python`, `jsx`, ...).
- `--freshness-policy strict|warn|offline-only`: runtime freshness behavior.
- `--no-autodetect`: disable library auto-detection.

## Output Contract (Human Mode)

A normal successful query can show:

1. Header: `library@version • item`
2. Optional version notice if requested vs resolved differs
3. Description
4. Signature
5. Parameters (when present)
6. Returns (when present)
7. Gotchas / cautions
8. Examples (2 in normal mode)
9. References
10. Source metadata
11. Other good options (structured alternatives)
12. Notices (freshness/trust/version mapping)

## Python API

```python
from tref import ask

payload = ask(
    "groupby multiple columns agg mean",
    library="pandas",
    version="2.2",
    json_mode=True,
    freshness_policy="strict",
)
```
