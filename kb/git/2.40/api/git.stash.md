---
library: git
version: "2.40.0"
category: api
item: git.stash
type: command
signature: "git stash [push|pop|list|drop] [options]"
keywords: ["stash", "save", "temporary", "work in progress"]
aliases: ["git stash", "save changes", "temporary commit"]
intent: "Temporarily save uncommitted changes to switch branches without committing, allowing clean working directory."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-stash"
source_title: "git-stash Documentation"
alternatives:
  - option: "git add + temporary commit"
    reason: "Creates actual commit, shows in history."
  - option: "git worktree"
    reason: "Multiple working directories."
---

# git stash

## Signature
```bash
git stash push -m "message"
git stash pop
git stash list
git stash drop
git stash clear
```

## What It Does
Saves uncommitted changes (staged and unstaged) to stash stack. Working directory becomes clean. Later restore changes with pop or apply.

## Use When
- Switching branches with uncommitted work.
- Pulling changes when have local modifications.
- Temporarily setting aside experimental changes.
- Saving work-in-progress.

## Examples
```bash
git stash push -m "WIP: login feature"
```

```bash
git stash list
# stash@{0}: WIP on main: abc123 message
# stash@{1}: another stash
```

```bash
git stash pop
```

```bash
git stash apply stash@{0}
```

```bash
git stash drop stash@{0}
```

```bash
git stash clear
```

```bash
git stash -p  # stash specific files
```

```bash
git stash branch new-branch stash@{0}
```

## Returns
Success or error

## Gotchas / Version Notes
- Only tracks tracked files.
- Use -u for untracked files.
- Use -a for all files including ignored.
- Pop applies and removes from stash.
- Apply keeps stash for reuse.

## References
- git-stash docs: https://git-scm.com/docs/git-stash
