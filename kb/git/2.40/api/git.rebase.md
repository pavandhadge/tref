---
library: git
version: "2.40.0"
category: api
item: git.rebase
type: command
signature: "git rebase <upstream> [branch]"
keywords: ["rebase", "reapply", "history", "linear"]
aliases: ["git rebase", "rewrite history", "move commits"]
intent: "Reapply commits on top of another base tip, creating linear history without merge commits."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-rebase"
source_title: "git-rebase Documentation"
alternatives:
  - option: "git merge"
    reason: "Creates merge commit, preserves full history."
  - option: "git cherry-pick"
    reason: "Apply specific commits, not rebase entire branch."
---

# git rebase

## Signature
```bash
git rebase main
git rebase -i HEAD~3
git rebase --onto newbase oldbase
git rebase --abort
git rebase --continue
```

## What It Does
Replays commits on top of another commit. Moves branch to new base, creating new commits with different hashes. Produces linear history.

## Use When
- Updating feature branch with latest main.
- Cleaning up commit history (squash, reorder).
- Creating linear project history.
- Before merging PR.

## Examples
```bash
git checkout feature
git rebase main
```

```bash
# Interactive rebase
git rebase -i HEAD~3

# Commands in rebase todo:
# pick   = use commit
# reword = change message
# edit   = stop to amend
# squash = combine with previous
# drop   = remove commit
```

```bash
# Abort rebase in progress
git rebase --abort
```

```bash
# Continue after resolving conflicts
git add .
git rebase --continue
```

## Returns
Success or conflicts

## Gotchas / Version Notes
- NEVER rebase public/shared commits.
- Changes commit SHAs.
- Conflicts need resolution then --continue.
- Use --onto for complex rebases.
- git rebase -i for history cleanup.

## References
- git-rebase docs: https://git-scm.com/docs/git-rebase
