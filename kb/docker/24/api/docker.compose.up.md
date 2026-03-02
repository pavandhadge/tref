---
library: docker
version: "24.0.0"
category: api
item: docker.compose.up
type: command
signature: "docker compose up [OPTIONS] [SERVICE...]"
keywords: ["compose", "docker-compose", "multi-container", "orchestration"]
aliases: ["docker compose start", "start services", "run compose"]
intent: "Create and start containers defined in docker-compose.yml for multi-service applications."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.docker.com/compose/reference/up/"
source_title: "docker compose up reference"
alternatives:
  - option: "docker run"
    reason: "Run single containers manually without orchestration."
  - option: "kubernetes"
    reason: "Production-grade container orchestration at scale."
  - option: "docker swarm"
    reason: "Native clustering and orchestration in Docker."
---

# docker.compose.up

## Signature
```bash
docker compose up [OPTIONS] [SERVICE...]
docker compose up -d
docker compose up --scale web=3
```

## What It Does
Builds, (re)creates, starts, and attaches to containers for services defined in docker-compose.yml. Starts all services by default or specified services only.

## Use When
- Running multi-container applications locally.
- Developing microservices with multiple dependencies.
- Simulating production environment locally.

## Examples
```bash
docker compose up -d
```

```bash
docker compose up --build
```

```bash
docker compose up -d postgres redis
```

```bash
docker compose up --scale web=3 --scale worker=2
```

```bash
docker compose up --env .env.production
```

## Returns
Starts containers in attached mode (or detached with -d)

## Gotchas / Version Notes
- Use `-d` for detached mode in production.
- `--build` forces rebuild of images.
- `docker-compose` (v1) vs `docker compose` (v2) syntax.
- Volumes persist data between restarts.
- Use `docker compose down` to stop and remove containers.

## References
- docker compose up docs: https://docs.docker.com/compose/reference/up/
- Compose file: https://docs.docker.com/compose/compose-file/
