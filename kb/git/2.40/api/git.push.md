---
library: git
version: "2.40.0"
category: api
item: git.push
type: command
signature: "git push [remote] [branch] [--force] [--tags]"
keywords: ["push", "upload", "remote", "upload commits"]
aliases: ["git push", "upload to remote", "send commits"]
intent: "Upload local branch commits to a remote repository, updating remote refs and objects."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://git-scm.com/docs/git-push"
source_title: "git-push Documentation"
alternatives:
  - option: "git push --force-with-lease"
    reason: "Safer force push that checks for upstream changes."
  - option: "git pull --rebase"
    reason: "Pull and rebase instead of merge."
---

# git push

## Signature
```bash
git push <remote> <branch>
git push -u origin main
git push --force
git push --tags
```

## What It Does
Uploads local branch commits to remote repository. Updates remote branch references and transfers objects. Can set upstream with -u flag.

## Use When
- Sharing commits with collaborators.
- Publishing feature branches.
- Syncing local and remote repositories.
- After making local commits.

## Examples
```bash
git push origin main
```

```bash
git push -u origin feature/login
```

```bash
git push origin --tags
```

```bash
git push --force
```

```bash
git push --force-if-includes
```

```bash
git push origin :feature/old
```

## Returns
Success message or error

## Gotchas / Version Notes
- --force overwrites remote, can lose commits.
- --force-with-lease is safer.
- --set-upstream/-u sets default upstream.
- Use --delete to remove remote branches.
- Configure default remote with push.default.

## References
- git-push docs: https://git-scm.com/docs/git-push
