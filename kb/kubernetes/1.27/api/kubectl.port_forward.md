---
library: kubernetes
version: "1.27.0"
category: api
item: kubectl.port_forward
type: command
signature: "kubectl port-forward TYPE/NAME [LOCAL_PORT:]REMOTE_PORT"
keywords: ["port-forward", "tunnel", "local", "access"]
aliases: ["kubectl port-forward", "access pod", "database tunnel"]
intent: "Forward local port to Kubernetes pod or service, enabling access to running containers from local machine."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#port-forward"
source_title: "kubectl port-forward Documentation"
alternatives:
  - option: "kubectl exec"
    reason: "Execute commands inside pod."
  - option: "kubectl proxy"
    reason: "Proxy to Kubernetes API server."
---

# kubectl port-forward

## Signature
```bash
kubectl port-forward pod/my-pod 8080:80
kubectl port-forward service/my-service 8080:80
kubectl port-forward deployment/my-app 5432:5432
```

## What It Does
Forwards local port to pod/service. Creates tunnel for accessing containerized applications locally. Useful for debugging, databases, web UIs.

## Use When
- Accessing pod ports locally.
- Debugging web apps.
- Connecting to databases in cluster.
- Testing services locally.

## Examples
```bash
# Forward to pod
kubectl port-forward pod/my-pod 8080:80
```

```bash
# Forward to deployment
kubectl port-forward deployment/my-app 8080:8080
```

```bash
# Forward to statefulset
kubectl port-forward statefulset/postgres 5432:5432
```

```bash
# Random local port
kubectl port-forward pod/my-pod :80
```

```bash
# Multiple ports
kubectl port-forward pod/my-pod 8080:80 9090:90
```

```bash
# Address binding
kubectl port-forward --address 0.0.0.0 pod/my-pod 8080:80
```

## Returns
Forwards until interrupted

## Gotchas / Version Notes
- Connection stays open while running.
- Use different local port if conflict.
- Works with pods, services, deployments.
- Use -n for specific namespace.

## References
- kubectl port-forward: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#port-forward
