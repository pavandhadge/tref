---
library: git
version: "2.40.0"
category: api
item: git.pull
type: command
signature: "git pull [remote] [branch] [--rebase]"
keywords: ["pull", "fetch merge", "download", "sync"]
aliases: ["git pull", "fetch and merge", "update local"]
intent: "Fetch changes from remote and merge them into current branch, synchronizing local repository with remote."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-pull"
source_title: "git-pull Documentation"
alternatives:
  - option: "git fetch + git merge"
    reason: "Separate steps give more control."
  - option: "git fetch + git rebase"
    reason: "Linear history, no merge commits."
---

# git pull

## Signature
```bash
git pull
git pull origin main
git pull --rebase origin main
git pull --ff-only
```

## What It Does
Combines git fetch and git merge. Fetches changes from remote and integrates them into current branch. May create merge commit if diverged.

## Use When
- Syncing with remote changes.
- Updating local branch with remote.
- Before pushing to avoid conflicts.

## Examples
```bash
git pull
```

```bash
git pull origin main
```

```bash
git pull --rebase origin main
```

```bash
git pull --ff-only
```

## Returns
Merge results or error

## Gotchas / Version Notes
- Creates merge commit by default.
- --rebase for linear history.
- --ff-only fails if not fast-forward.
- Configure rebase behavior with pull.rebase.
- May cause conflicts needing resolution.

## References
- git-pull docs: https://git-scm.com/docs/git-pull
