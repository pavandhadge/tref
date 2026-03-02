---
library: kubernetes
version: "1.27.0"
category: api
item: kubectl.apply
type: command
signature: "kubectl apply -f <file.yaml> [--dry-run=client|server]"
keywords: ["apply", "deploy", "create", "update"]
aliases: ["kubectl apply", "deploy manifest", "kubernetes apply"]
intent: "Apply a configuration to a resource from a file or stdin. Creates resources if they don't exist, updates existing resources if they've changed."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply"
source_title: "kubectl apply Documentation"
alternatives:
  - option: "kubectl create"
    reason: "Only creates new resources, fails if already exists."
  - option: "kubectl replace"
    reason: "Replaces entire resource, requires existing one."
  - option: "kubectl patch"
    reason: "Modifies specific fields without full replacement."
---

# kubectl apply

## Signature
```bash
kubectl apply -f <filename.yaml>
kubectl apply -f <directory/>
kubectl apply -k <kustomization-directory>
kubectl apply -f - < <stdin>
```

## Parameters
- -f: File or directory containing YAML/JSON manifests.
- --dry-run: Validate without applying (client/server).
- --server-dry-run: Server-side dry run.
- --prune: Remove resources not in manifest.
- --validate: Validate against schema (default: true).
- -l: Apply to resources matching label selector.
- --field-manager: Name for field ownership.

## What It Does
Creates or updates Kubernetes resources from manifest files. Calculates diff between current state and desired state, then patches the resource. Records change in annotation for tracking.

## Use When
- Deploying applications from YAML manifests.
- GitOps workflows with declarative configurations.
- Updating existing resources without recreation.
- Applying Kustomize or Helm charts.

## Examples
```bash
kubectl apply -f deployment.yaml
```

```bash
kubectl apply -f ./manifests/
```

```bash
kubectl apply -f deployment.yaml --dry-run=client
```

```bash
kubectl apply -f configmap.yaml -o yaml --dry-run=client
```

```bash
# Apply with label selector
kubectl apply -f pod.yaml -l app=myapp
```

## Returns
Success message or error

## Gotchas / Version Notes
- Use `--dry-run=client` to preview changes.
- `--dry-run=server` validates on API server.
- Deleted resources can't be restored with apply (use --prune carefully).
- Three-way merge: existing + changes + manifest.
- Field ownership tracked to prevent conflicts.

## References
- kubectl apply: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply
- Declarative management: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/
