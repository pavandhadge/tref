---
library: docker
version: "20.10.0"
category: api
item: docker.pull
type: command
signature: "docker pull [OPTIONS] NAME[:TAG|@DIGEST]"
keywords: ["pull", "download", "image", "fetch"]
aliases: ["docker pull", "download image", "fetch image"]
intent: "Download a Docker image from a registry, making it available locally for creating containers."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.docker.com/engine/reference/commandline/pull/"
source_title: "docker pull reference"
alternatives:
  - option: "docker build"
    reason: "Build from Dockerfile instead."
  - option: "docker load"
    reason: "Load from tarball."
---

# docker pull

## Signature
```bash
docker pull nginx:latest
docker pull python:3.11-slim
docker pull myregistry.io/myimage:v1.0
```

## What It Does
Downloads image layers from registry. If not specified, pulls from Docker Hub. Supports specific tags, digests, and all tags.

## Use When
- Getting base images.
- Updating local images.
- Pulling private images.
- Before docker run if image not local.

## Examples
```bash
docker pull nginx
```

```bash
docker pull nginx:latest
```

```bash
docker pull python:3.11-slim
```

```bash
docker pull --all-tags nginx
```

```bash
docker pull myregistry.io/myapp:v1.0
```

## Returns
Layer download progress

## Gotchas / Version Notes
- Default registry is Docker Hub.
- Use specific tags for reproducibility.
- :latest is often outdated.
- Pulls all layers even if some exist.

## References
- docker pull: https://docs.docker.com/engine/reference/commandline/pull/
