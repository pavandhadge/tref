---
library: git
version: "2.44.0"
category: api
item: git.rebase
type: command
signature: "git rebase [--onto <newbase>] [<upstream> [<branch>]]"
keywords: ["rebase", "history", "squash", "git"]
aliases: ["replay commits", "linear history", "interactive rebase"]
intent: "Replay commits onto a new base to keep history linear or rewrite local commits."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-rebase"
source_title: "git-rebase Documentation"
alternatives:
  - option: "git merge <branch>"
    reason: "Preserve branch topology without rewriting history."
  - option: "git cherry-pick <commit>"
    reason: "Replay specific commits only."
  - option: "git pull --rebase"
    reason: "Keep local branch linear while syncing from remote."
---

# git.rebase

## Signature
```bash
git rebase [--onto <newbase>] [<upstream> [<branch>]]
```

## What It Does
Moves a branch by replaying its commits onto another base commit. Useful for linear history and commit cleanup.

## Use When
- You need to update a feature branch onto latest `main`.
- You want to squash/reword local commits before merging.
- You are rewriting local (not shared) history.

## Examples
```bash
git checkout feature
git rebase main
```

```bash
git rebase --onto release/2.0 main feature
```

```bash
git rebase -i HEAD~5
```

```bash
git add <resolved-files>
git rebase --continue
```

## Alternatives
- `git merge main` to preserve original branch topology without rewriting commits.
- `git cherry-pick <commit>` to copy specific commits only.
- `git pull --rebase` for updating a local branch from remote with linear history.

## Gotchas / Version Notes
- Avoid rebasing shared/public history.
- Resolve conflicts and continue with `git rebase --continue`.
- Use `git rebase --abort` to return to pre-rebase state.

## References
- git-rebase docs: https://git-scm.com/docs/git-rebase
- Pro Git book (rebasing): https://git-scm.com/book/en/v2/Git-Branching-Rebasing
