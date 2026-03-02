---
library: docker
version: "26.1.0"
category: api
item: docker.run
type: command
signature: "docker run [OPTIONS] IMAGE [COMMAND] [ARG...]"
keywords: ["docker run", "container", "image", "port mapping"]
aliases: ["start container", "run image", "container execution"]
intent: "Create and run a container from an image with runtime options."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.docker.com/engine/reference/commandline/run/"
source_title: "docker run reference"
alternatives:
  - option: "docker compose up"
    reason: "Run multi-service applications with declarative config."
  - option: "docker exec -it <container> ..."
    reason: "Run commands inside an already-running container."
  - option: "docker create + docker start"
    reason: "Split creation from startup lifecycle."
---

# docker.run

## Signature
```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

## What It Does
Creates a new container from an image and executes its main process with runtime flags (ports, env, mounts, resources).

## Use When
- You need a one-off container execution.
- You want local service startup from an image.
- You need isolated command execution with mounts/env vars.

## Examples
```bash
docker run --name web -p 8080:80 -d nginx:latest
```

```bash
docker run --rm -it python:3.11-slim python -q
```

```bash
docker run --rm -v "$PWD":/app -w /app node:20 npm test
```

```bash
docker run --cpus=1.5 --memory=1g --pids-limit=256 myorg/worker:2.0.0
```

## Alternatives
- `docker compose up` for multi-service app stacks.
- `docker exec -it <container> ...` to run commands in existing containers.
- `docker create` + `docker start` when you need separate create/start lifecycle.

## Gotchas / Version Notes
- Detached containers exit if main process exits.
- Prefer explicit tag instead of floating `latest` for reproducibility.
- Bind mounts can mask in-image files at the same path.

## References
- docker run docs: https://docs.docker.com/engine/reference/commandline/run/
- Docker run reference (current): https://docs.docker.com/reference/cli/docker/container/run/
