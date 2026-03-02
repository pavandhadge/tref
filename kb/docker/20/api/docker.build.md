---
library: docker
version: "20.10.0"
category: api
item: docker.build
type: command
signature: "docker build [OPTIONS] PATH | URL | -"
keywords: ["build", "image", "dockerfile", "containerize"]
aliases: ["build image", "docker buildx", "build container"]
intent: "Build a Docker image from a Dockerfile and a context directory."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.docker.com/engine/reference/commandline/build/"
source_title: "docker build reference"
alternatives:
  - option: "docker buildx"
    reason: "Advanced builder with multi-platform support and caching."
  - option: "BuildKit"
    reason: "Next-generation build backend with parallel execution."
---

# docker.build

## Signature
```bash
docker build [OPTIONS] PATH | URL | -
docker build -t myapp:latest .
docker build -f Dockerfile.prod .
```

## What It Does
Reads the Dockerfile in the specified context (directory), executes instructions to create a Docker image, and tags it with a name. Each instruction in Dockerfile creates a layer.

## Use When
- Creating custom container images for applications.
- Building images from Dockerfiles in CI/CD pipelines.
- Packaging applications for deployment.

## Examples
```bash
docker build -t myapp:latest .
```

```bash
docker build -t myapp:1.0 -f Dockerfile.prod .
```

```bash
docker build --build-arg VERSION=1.0 -t myapp .
```

```bash
docker build --no-cache -t myapp .
```

```bash
docker build -t myapp --target production .
```

## Returns
Creates Docker image

## Gotchas / Version Notes
- Context is the root for ADD/COPY instructions.
- Use `.dockerignore` to exclude files from context.
- Layer caching speeds up rebuilds when unchanged.
- `--no-cache` ignores cache for fresh builds.
- Multi-stage builds reduce final image size.

## References
- docker build docs: https://docs.docker.com/engine/reference/commandline/build/
- Best practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
