---
library: git
version: "2.40.0"
category: api
item: git.diff
type: command
signature: "git diff [options] [<commit>] [--] <path>"
keywords: ["diff", "changes", "difference", "compare"]
aliases: ["git diff", "show changes", "compare commits"]
intent: "Show changes between commits, working tree, staged area, or files for review and understanding modifications."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-diff"
source_title: "git-diff Documentation"
alternatives:
  - option: "git log -p"
    reason: "Shows changes in commit history."
  - option: "git show"
    reason: "Shows single commit changes."
---

# git diff

## Signature
```bash
git diff
git diff --staged
git diff HEAD
git diff main..feature
git diff --stat
```

## What It Does
Shows uncommitted changes, differences between commits, or between commits and working tree. Supports various output formats.

## Use When
- Reviewing changes before commit.
- Checking what modified.
- Comparing branches.
- Understanding what changed in commits.

## Examples
```bash
git diff
```

```bash
git diff --staged
```

```bash
git diff HEAD
```

```bash
git diff main..feature
```

```bash
git diff --stat
```

```bash
git diff --name-only
```

```bash
git diff file.txt
```

```bash
git diff HEAD~5 HEAD
```

```bash
git diff -w file.txt
```

```bash
git diff --color-words
```

## Returns
Diff output

## Gotchas / Version Notes
- --staged shows staged changes.
- HEAD shows all uncommitted.
- Use --name-only for just files.
- Use -w to ignore whitespace.
- --check checks for conflicts.

## References
- git-diff docs: https://git-scm.com/docs/git-diff
