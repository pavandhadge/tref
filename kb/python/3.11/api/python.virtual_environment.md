---
library: python
version: "3.11.0"
category: api
item: python.virtual_environment
type: tool
signature: "python -m venv [options] <env_dir>"
keywords: ["venv", "virtual environment", "isolation", "environment"]
aliases: ["create venv", "virtualenv", "python environment"]
intent: "Create isolated Python environments with their own site-packages directories."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/library/venv.html"
source_title: "venv documentation"
alternatives:
  - option: "poetry"
    reason: "Dependency management and packaging tool with built-in venv support."
  - option: "pipenv"
    reason: "Combines pip and venv with Pipfile for dependency management."
  - option: "uv"
    reason: "Fast Python package installer and resolver written in Rust."
---

# venv

## Signature
```bash
python -m venv [options] <env_dir>
```

## What It Does
Creates virtual environments that isolate Python projects from system packages. Each environment has its own Python executable and site-packages directory.

## Use When
- Managing dependencies for multiple projects with conflicting requirements.
- Keeping project dependencies separate from system Python.
- Creating reproducible development environments.

## Examples
```bash
python -m venv myenv
```

```bash
python -m venv venv --system-site-packages
```

```bash
source myenv/bin/activate  # Linux/macOS
myenv\\Scripts\\activate  # Windows
```

```python
# Using venv programmatically
import venv
venv.create("myenv", with_pip=True)
```

## Returns
None (creates directory structure)

## Gotchas / Version Notes
- Python 3.3+ includes venv by default.
- Use `--system-site-packages` to include system packages.
- Activate script location differs by OS.
- Delete the directory to remove the environment.

## References
- venv docs: https://docs.python.org/3/library/venv.html
- Virtual environments guide: https://docs.python.org/3/tutorial/venv.html
