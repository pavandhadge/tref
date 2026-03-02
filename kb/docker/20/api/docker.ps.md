---
library: docker
version: "20.10.0"
category: api
item: docker.ps
type: command
signature: "docker ps [OPTIONS]"
keywords: ["ps", "list", "containers", "running"]
aliases: ["docker ps", "list containers", "show containers"]
intent: "List running containers, showing container ID, image, command, ports, and status."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.docker.com/engine/reference/commandline/ps/"
source_title: "docker ps reference"
alternatives:
  - option: "docker container ls"
    reason: "Same command, newer syntax."
  - option: "docker stats"
    reason: "Shows live resource usage."
---

# docker ps

## Signature
```bash
docker ps
docker ps -a
docker ps -l
docker ps --filter "name=web"
docker ps --format "{{.Names}}: {{.Status}}"
```

## What It Does
Lists containers. By default shows only running containers. Use -a for all containers including stopped.

## Use When
- Finding container IDs.
- Checking if container is running.
- Getting container names for other commands.
- Monitoring container status.

## Examples
```bash
docker ps
```

```bash
docker ps -a
```

```bash
docker ps -l
```

```bash
docker ps --filter "status=exited"
```

```bash
docker ps --filter "ancestor=nginx"
```

```bash
docker ps -q
```

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## Returns
Container list table

## Gotchas / Version Notes
- -a shows stopped containers.
- -l shows last created.
- -q returns only IDs.
- Use --format for custom output.
- Combine with grep for filtering.

## References
- docker ps: https://docs.docker.com/engine/reference/commandline/ps/
