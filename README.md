# tref

`tref` is an offline-first CLI + Python library for versioned developer documentation retrieval.

It answers natural language queries using curated KB files and local FAISS indexes.

## Install

```bash
pip install .
```

## Quick Start

```bash
# explicit versioned query
tref "pandas@2.2 groupby multiple columns agg mean"

# auto-detect library from query
tref "how to safely rebase current branch"

# always-on interactive mode
tref live
```

## Main Commands

```bash
# query
tref [LIB@VER] "query"
tref query [LIB@VER] "query"

# persistent session
tref live

# update + trust
tref update --strict-verify
tref status
tref doctor

# quality + perf
tref eval --index-root /tmp/tref-indexes --min-pass-rate 1.0
tref bench "groupby multiple columns agg mean" --library pandas --version 2.2 --runs 30

# remote source control
tref remote show
tref remote set --releases-api-url https://api.github.com/repos/myorg/my-kb/releases/latest
tref remote reset

# user defaults config
tref config show
tref config set --freshness-policy offline-only --top-k 8 --llm-model llama3.1:8b-instruct
tref config reset

# local KB indexing
tref build-index ./kb --output ~/.tref/custom
```

## Important Flags

- `--json`: machine-readable output
- `--llm`: generate final answer via Ollama
- `--model`: set Ollama model
- `--lang`: prefer examples by language
- `--verbose`: extended output
- `--full-doc`: include full matched document sections
- `--freshness-policy strict|warn|offline-only`
- `--strict-fresh`
- `--no-autodetect`

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
print(payload["guidance"])
```

## Trust Model

- Checksum verification in strict update mode.
- Optional required signature verification.
- Atomic index replacement during updates.
- Freshness/trust/sla status exposed via `tref status`.

## Local Index Layout (Expected by tref)

Local indexes are expected under `TREF_HOME/indexes` (default: `~/.tref/indexes`):

```text
~/.tref/indexes/
  _manifest.json
  pandas/
    2.2/
      index.faiss
      chunks.jsonl
      meta.json
    latest/
      index.faiss
      chunks.jsonl
      meta.json
  git/
    2.44/
      index.faiss
      chunks.jsonl
      meta.json
```

Each `library/version` directory must contain:

- `index.faiss` (vector index)
- `chunks.jsonl` (chunk metadata + text)
- `meta.json` (build metadata)

And the root must contain:

- `_manifest.json` (library/version availability)

## Remote Update Contract (What tref Downloads)

`tref update` expects a release endpoint returning the latest release JSON with assets.

Default asset names:

- `tref-indexes.tar.gz`
- `tref-indexes.tar.gz.sha256`
- `tref-indexes.tar.gz.sig` (optional unless signature is required)

Expected tar content:

- either `_manifest.json` at tar root, or
- one top-level directory containing `_manifest.json`.

Checksum file format:

- first token on first line is SHA256 digest.

## How to Publish Your Own Remote Index Snapshot

1. Build indexes:

```bash
tref build-index ./kb --output ./dist-indexes
```

2. Package snapshot:

```bash
tar -czf tref-indexes.tar.gz -C dist-indexes .
sha256sum tref-indexes.tar.gz | awk '{print $1}' > tref-indexes.tar.gz.sha256
```

3. (Optional) Sign archive:

```bash
cosign sign-blob --key cosign.key --output-signature tref-indexes.tar.gz.sig tref-indexes.tar.gz
```

4. Upload these files as release assets:

- `tref-indexes.tar.gz`
- `tref-indexes.tar.gz.sha256`
- `tref-indexes.tar.gz.sig` (if using signatures)

5. Point tref to your endpoints:

```bash
tref remote set \
  --releases-api-url https://api.github.com/repos/<org>/<repo>/releases/latest \
  --kb-manifest-url https://raw.githubusercontent.com/<org>/<repo>/main/kb/_manifest.json \
  --release-asset-name tref-indexes.tar.gz \
  --release-checksum-asset-name tref-indexes.tar.gz.sha256 \
  --release-signature-asset-name tref-indexes.tar.gz.sig
```

## User Defaults via Config File (Cross-Platform)

`tref` supports persistent defaults in a config file.

Default config path:

- Linux: `~/.tref/config.json`
- macOS: `~/.tref/config.json`
- Windows: `%USERPROFILE%\\.tref\\config.json`
- Docker/CI: `${TREF_HOME}/config.json` (set `TREF_HOME` explicitly if needed)

Set/read defaults with CLI:

```bash
tref config show
tref config set --freshness-policy offline-only --top-k 8 --example-language bash
tref config set --releases-api-url https://api.github.com/repos/<org>/<repo>/releases/latest
```

Example `config.json`:

```json
{
  "freshness_policy": "offline-only",
  "top_k": 8,
  "llm_model": "llama3.1:8b-instruct",
  "example_language": "bash",
  "update_strict_verify": true,
  "require_signature": false,
  "releases_api_url": "https://api.github.com/repos/myorg/my-kb/releases/latest",
  "kb_manifest_url": "https://raw.githubusercontent.com/myorg/my-kb/main/kb/_manifest.json",
  "release_asset_name": "tref-indexes.tar.gz",
  "release_checksum_asset_name": "tref-indexes.tar.gz.sha256",
  "release_signature_asset_name": "tref-indexes.tar.gz.sig"
}
```

Precedence order:

1. environment variables
2. `config.json`
3. `remote.json` (for remote-specific overrides)
4. built-in defaults

## KB Authoring (for humans and other models)

Use `docs/kb_schema_v2.md` as the source of truth.

### Required frontmatter keys

- `library`, `version`, `category`, `item`, `type`
- `signature`, `keywords`, `intent`
- `last_updated`, `schema_version`, `source_url`, `source_title`
- `alternatives` (list of `{option, reason}`)
- optional: `aliases`

`schema_version` must be `"2.0"`.

### Required sections (exact names)

1. `## Signature`
2. `## What It Does`
3. `## Use When`
4. `## Examples`
5. `## Alternatives`
6. `## Gotchas / Version Notes`
7. `## References`

### Minimal KB file template

```md
---
library: git
version: "2.44.0"
category: api
item: git.branch
type: command
signature: "git branch [--all] [--list] [<branchname>]"
keywords: ["git", "branch", "create branch"]
aliases: ["new branch", "switch branch"]
intent: "Create, list, rename, or delete branches."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-branch"
source_title: "git-branch Documentation"
alternatives:
  - option: "git switch -c <name>"
    reason: "Modern create+switch flow."
  - option: "git checkout -b <name>"
    reason: "Compatible with older Git versions."
---

# git.branch

## Signature
```bash
git branch [--all] [--list] [<branchname>]
```

## What It Does
Manages branch references.

## Use When
- You need a new local branch.

## Examples
```bash
git switch -c feature/login-flow
```

## Alternatives
- `git checkout -b <name>` for older Git clients.

## Gotchas / Version Notes
- `git branch <name>` does not switch to the new branch.

## References
- git docs: https://git-scm.com/docs/git-branch
```

### LLM authoring prompt (copy/paste)

Use this with any model generating KB files:

```text
Generate exactly one markdown KB file for tref schema v2.0.
Follow required frontmatter keys and required section names exactly.
No missing fields. No extra sections. No prose outside the markdown file.
Use accurate signature/version/source URL.
Use fenced code blocks with correct language tags.
alternatives frontmatter must be list of {option, reason}.
```

### Validate and build

```bash
python scripts/validate_kb.py kb
tref build-index kb --output /tmp/tref-indexes
```

## Environment Variables

- `TREF_HOME`
- `TREF_KB_MANIFEST_URL`
- `TREF_RELEASES_API`
- `TREF_RELEASE_ASSET`
- `TREF_RELEASE_CHECKSUM_ASSET`
- `TREF_RELEASE_SIGNATURE_ASSET`
- `TREF_UPDATE_STRICT_VERIFY`
- `TREF_REQUIRE_SIGNATURE`
- `TREF_MAX_INDEX_AGE_DAYS`
- `TREF_FRESHNESS_POLICY`
- `TREF_COSIGN_KEY_PATH`
- `TREF_COSIGN_BIN`
