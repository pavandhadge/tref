---
library: docker
version: "20.10.0"
category: api
item: docker.exec
type: command
signature: "docker exec [OPTIONS] CONTAINER COMMAND [ARG...]"
keywords: ["exec", "run", "command", "inside container"]
aliases: ["docker exec", "run in container", "shell into container"]
intent: "Execute a command inside a running container, commonly used to get shell access or run debug commands."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.docker.com/engine/reference/commandline/exec/"
source_title: "docker exec reference"
alternatives:
  - option: "docker attach"
    reason: "Attach to container's main process."
  - option: "docker run"
    reason: "Start new container for command."
---

# docker exec

## Signature
```bash
docker exec -it container bash
docker exec -it container sh
docker exec container ls /app
docker exec -d container background-command
```

## What It Does
Runs a new command in running container. Creates new process (not attached to container's main process). Most common: getting interactive shell.

## Use When
- Getting shell inside container.
- Running debug commands.
- Checking configuration.
- Running one-off tasks.

## Examples
```bash
docker exec -it mycontainer bash
```

```bash
docker exec -it mycontainer sh
```

```bash
docker exec mycontainer ls -la
```

```bash
docker exec -e VAR=value mycontainer env
```

```bash
docker exec -d mycontainer tail -f /var/log/app.log
```

```bash
docker exec --workdir /app mycontainer npm test
```

## Returns
Command output

## Gotchas / Version Notes
- -i keeps STDIN open.
- -t allocates pseudo-TTY.
- Container must be running.
- Use sh if bash not available.
- --user to run as specific user.

## References
- docker exec: https://docs.docker.com/engine/reference/commandline/exec/
