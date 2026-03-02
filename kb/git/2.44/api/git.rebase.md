---
library: git
version: "2.44.0"
category: api
item: git.rebase
type: command
signature: "git rebase [--onto <newbase>] [<upstream> [<branch>]]"
keywords: ["rebase", "history", "squash", "git"]
last_updated: "2025-03-02"
---

# git.rebase

## Signature
```python
git rebase [--onto <newbase>] [<upstream> [<branch>]]
```

## Parameters
- --onto: Rebase commits onto a specific base.
- upstream: Commit where replay starts.
- branch: Branch to rebase (defaults to current branch).

## Examples
```python
git checkout feature
git rebase main
```

## Gotchas / Version Notes
- Avoid rebasing shared/public history.
- Resolve conflicts and continue with `git rebase --continue`.
