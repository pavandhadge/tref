---
library: kubernetes
version: "1.30.0"
category: api
item: kubectl.get
type: command
signature: "kubectl get <resource> [name] [-o output] [-w] [-l label]"
keywords: ["get", "list", "describe", "show"]
aliases: ["kubectl get", "list resources", "show pods"]
intent: "List, describe, or get one or more resources from the cluster."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get"
source_title: "kubectl get Documentation"
alternatives:
  - option: "kubectl describe"
    reason: "Detailed information about a single resource."
  - option: "kubectl edit"
    reason: "Edit resource configuration directly."
---

# kubectl get

## Signature
```bash
kubectl get <resource> [NAME] [-o OUTPUT] [-w] [--show-labels] [--field-selector=key=value]
```

## What It Does
Retrieves and displays information about Kubernetes resources. Supports various output formats (YAML, JSON, wide, custom columns) and can watch for changes with -w flag.

## Use When
- Listing pods, services, deployments, etc.
- Checking resource status.
- Getting resource details in different formats.
- Watching for changes in real-time.

## Examples
```bash
kubectl get pods
```

```bash
kubectl get pods -o wide
```

```bash
kubectl get pod my-pod -o yaml
```

```bash
kubectl get pods -l app=nginx
```

```bash
kubectl get pods --field-selector=status.phase=Running
```

```bash
kubectl get all --sort-by='.metadata.name'
```

```bash
kubectl get pods -w
```

## Returns
Table, YAML, or JSON output

## Gotchas / Version Notes
- Common resources: pods (po), services (svc), deployments (deploy), namespaces (ns).
- -o jsonpath allows custom output formatting.
- Use -w for watch mode.
- --all-namespaces (-A) for all namespaces.
- --no-headers to omit column headers.

## References
- kubectl get: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get
- Resource types: https://kubernetes.io/docs/reference/kubectl/overview/#resource-types
