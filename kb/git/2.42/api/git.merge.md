---
library: git
version: "2.42.0"
category: api
item: git.merge
type: command
signature: "git merge <branch> [--no-ff] [--squash] [--abort]"
keywords: ["merge", "branch", "combine", "integration"]
aliases: ["merge branches", "combine branches", "git merge"]
intent: "Join two or more development histories together by integrating changes from one branch into another."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-merge"
source_title: "git-merge Documentation"
alternatives:
  - option: "git rebase"
    reason: "Reapply commits on top of another branch for linear history."
  - option: "git cherry-pick"
    reason: "Apply specific commits from one branch to another."
---

# git.merge

## Signature
```bash
git merge <branch> [--no-ff] [--squash] [--abort] [--no-commit]
```

## What It Does
Integrates changes from specified branch into the current branch. Creates a merge commit unless fast-forward is possible. Preserves complete history of both branches.

## Use When
- Combining feature branches back into main.
- Integrating changes from develop into release branches.
- Pulling remote changes with `git pull` (which calls merge).

## Examples
```bash
git checkout main
git merge feature/login
```

```bash
git merge feature/login --no-ff
```

```bash
git merge origin/main --no-commit
# Review changes before committing
```

```bash
# Abort a merge in progress
git merge --abort
```

```bash
git merge feature/login --squash
# Combine all commits into one
```

## Returns
Creates merge commit on success

## Gotchas / Version Notes
- `--no-ff` always creates merge commit, preserving branch history.
- `--squash` combines changes without merge history.
- Conflicts require manual resolution then `git add` + `git commit`.
- Use `--abort` to cancel problematic merges.
- Fast-forward merge possible when no divergent commits.

## References
- git-merge docs: https://git-scm.com/docs/git-merge
- Pro Git branching: https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
