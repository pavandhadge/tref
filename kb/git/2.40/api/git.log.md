---
library: git
version: "2.40.0"
category: api
item: git.log
type: command
signature: "git log [options] [revision range]"
keywords: ["log", "history", "commit", "timeline"]
aliases: ["git log", "commit history", "view history"]
intent: "Display commit history, showing commits, their messages, author, date, and changes for current branch."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-log"
source_title: "git-log Documentation"
alternatives:
  - option: "git diff"
    reason: "Shows changes between commits, not history."
  - option: "git show"
    reason: "Shows individual commit details."
---

# git log

## Signature
```bash
git log
git log --oneline --graph
git log -n 5
git log --author="name"
git log --since="2024-01-01"
```

## What It Does
Shows commit history with metadata: hash, author, date, message. Supports filtering by author, date, file, and formatting options.

## Use When
- Viewing commit history.
- Finding when changes were made.
- Investigating bugs (git log -p).
- Understanding project evolution.

## Examples
```bash
git log
```

```bash
git log --oneline
# abc1234 Commit message
# def5678 Another commit
```

```bash
git log --graph --oneline --all
```

```bash
git log -10 --author="Alice"
```

```bash
git log --since="2024-01-01" --until="2024-12-31"
```

```bash
git log --follow file.txt
```

```bash
git log --pretty=format:"%h - %an, %ar : %s"
```

```bash
git log -p file.txt
```

```bash
git log --stat
```

## Returns
Commit history output

## Gotchas / Version Notes
- Use --follow to track file renames.
- -n limits number of commits.
- --graph shows branch structure.
- --pretty for custom formatting.

## References
- git-log docs: https://git-scm.com/docs/git-log
