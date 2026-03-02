---
library: git
version: "2.44.0"
category: api
item: git.branch
type: command
signature: "git branch [--all] [--list] [<branchname>]"
keywords: ["branch", "new branch", "switch", "checkout", "git"]
aliases: ["create branch", "new branch", "switch branch"]
intent: "Create, list, rename, or delete branches in a Git repository."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-branch"
source_title: "git-branch Documentation"
alternatives:
  - option: "git switch -c <name>"
    reason: "Modern and clear create+switch flow."
  - option: "git checkout -b <name>"
    reason: "Works on older Git versions and widely used."
  - option: "git worktree add -b <name> <path> <start-point>"
    reason: "Work on multiple branches in separate directories."
---

# git.branch

## Signature
```bash
git branch [--all] [--list] [<branchname>]
```

## What It Does
Manages branches: create, list, move, and delete branch references.

## Use When
- You need to create a new local branch.
- You need to inspect branch lists and tracking status.
- You need to rename or remove branches.

## Examples
```bash
# create branch only (stay on current branch)
git branch feature/login-flow
```

```bash
# create and switch in one step
git switch -c feature/login-flow
```

```bash
# older equivalent: create and switch
git checkout -b feature/login-flow
```

```bash
# create local branch tracking remote
git switch -c feature/login-flow --track origin/feature/login-flow
```

## Alternatives
- `git switch -c <name>` is the modern, clearer create+switch command.
- `git checkout -b <name>` is widely supported and works on older Git versions.
- `git worktree add -b <name> <path> <start-point>` for parallel branch work in separate directory.

## Gotchas / Version Notes
- `git branch <name>` does not switch to the new branch.
- Use descriptive branch names and avoid rebasing shared branch history.
- Branch deletion with `-D` is forceful; use `-d` when possible.

## References
- git-branch docs: https://git-scm.com/docs/git-branch
- git-switch docs: https://git-scm.com/docs/git-switch
- git-checkout docs: https://git-scm.com/docs/git-checkout
