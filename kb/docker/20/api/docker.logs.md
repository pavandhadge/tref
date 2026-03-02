---
library: docker
version: "20.10.0"
category: api
item: docker.logs
type: command
signature: "docker logs [OPTIONS] CONTAINER"
keywords: ["logs", "output", "stdout", "stderr"]
aliases: ["docker logs", "view logs", "container output"]
intent: "Fetch container logs, showing stdout and stderr from the container's main process for debugging."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.docker.com/engine/reference/commandline/logs/"
source_title: "docker logs reference"
alternatives:
  - option: "docker-compose logs"
    reason: "Logs from docker-compose services."
  - option: "docker inspect"
    reason: "Detailed container info including log path."
---

# docker logs

## Signature
```bash
docker logs container
docker logs -f container
docker logs --tail 100 container
docker logs --timestamps container
```

## What It Does
Retrieves logs written to stdout/stderr by container. Shows historical logs from container start. Use -f to follow.

## Use When
- Debugging container issues.
- Checking application output.
- Monitoring startup errors.
- Following live logs.

## Examples
```bash
docker logs mycontainer
```

```bash
docker logs -f mycontainer
```

```bash
docker logs --tail 100 mycontainer
```

```bash
docker logs --timestamps mycontainer
```

```bash
docker logs --since 1h mycontainer
```

```bash
docker logs --until 30m mycontainer
```

## Returns
Container log output

## Gotchas / Version Notes
- Shows both stdout and stderr.
- Use -f to follow live.
- --tail limits lines shown.
- Use --timestamps for timestamps.
- May miss early logs if ring buffer full.

## References
- docker logs: https://docs.docker.com/engine/reference/commandline/logs/
