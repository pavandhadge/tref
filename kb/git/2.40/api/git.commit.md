---
library: git
version: "2.40.0"
category: api
item: git.commit
type: command
signature: "git commit [-m <message>] [-a] [--amend] [-S]"
keywords: ["commit", "save", "snapshot", "changes"]
aliases: ["git commit", "save changes", "record changes"]
intent: "Record changes to the repository by creating a new commit with a snapshot of staged files."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-commit"
source_title: "git-commit Documentation"
alternatives:
  - option: "git add + git commit"
    reason: "Explicit staging before commit for more control."
  - option: "git stash"
    reason: "Temporarily save changes without committing."
  - option: "git commit --amend"
    reason: "Modify the last commit instead of creating new one."
---

# git.commit

## Signature
```bash
git commit [-m <message>] [-a] [--amend] [--no-verify] [-S] [-s]
```

## What It Does
Takes all changes that have been staged with `git add` and creates a new commit snapshot. Each commit has a unique SHA-1 hash, author information, message, and optional GPG signature.

## Use When
- Saving a coherent set of changes with a descriptive message.
- Creating a checkpoint in your project history.
- Preparing changes for sharing via push or pull requests.

## Examples
```bash
git commit -m "Add user authentication feature"
```

```bash
git add .
git commit -m "Fix bug in login form validation"
```

```bash
git commit --amend -m "Updated commit message"
```

```bash
git commit -a -m "Commit all modified tracked files"
```

```bash
git commit -S -m "Signed commit for verification"
```

## Returns
Creates a new commit object

## Gotchas / Version Notes
- Requires staged changes (use `git add` first).
- Empty commit message is not allowed.
- Use `--amend` carefully on shared branches.
- GPG signing requires configured GPG key.
- `-a` auto-stages modified tracked files (not new files).

## References
- git-commit docs: https://git-scm.com/docs/git-commit
- Pro Git book: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
