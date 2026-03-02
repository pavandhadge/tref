---
library: docker
version: "26.1.0"
category: api
item: docker.run
type: command
signature: "docker run [OPTIONS] IMAGE [COMMAND] [ARG...]"
keywords: ["docker run", "container", "image", "port mapping"]
last_updated: "2025-03-02"
---

# docker.run

## Signature
```python
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

## Parameters
- -d: Run container in detached mode.
- -p: Publish container port(s) to host.
- --name: Set container name.

## Examples
```python
docker run --name web -p 8080:80 -d nginx:latest
```

## Gotchas / Version Notes
- Detached containers exit if main process exits.
- Prefer explicit tag instead of floating `latest` for reproducibility.
