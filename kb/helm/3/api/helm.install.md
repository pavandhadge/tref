---
library: helm
version: "3.14.0"
category: api
item: helm.install
type: command
signature: "helm install [NAME] [CHART] [flags]"
keywords: ["install", "deploy", "chart", "release"]
aliases: ["helm install", "deploy chart", "release"]
intent: "Install a Helm chart to Kubernetes cluster, creating a release with specified configuration."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://helm.sh/docs/helm/helm_install/"
source_title: "helm install Documentation"
alternatives:
  - option: "kubectl apply"
    reason: "Raw YAML, no templating."
  - option: "Kustomize"
    reason: "Native Kubernetes overlay tool."
---

# helm install

## Signature
```bash
helm install my-release bitnami/nginx
helm install --values values.yaml my-release ./chart
helm install my-release oci://registry.chart.io/chart
```

## What It Does
Installs Helm chart as release. Creates resources from chart templates with provided values. Names release for tracking.

## Use When
- Deploying applications.
- Installing packages (Prometheus, etc.).
- Testing charts locally.
- Production deployments.

## Examples
```bash
helm install my-release bitnami/nginx
```

```bash
helm install my-release ./my-chart
```

```bash
helm install my-release ./chart --set image.tag=v1.0
```

```bash
helm install my-release ./chart --values custom-values.yaml
```

```bash
# Dry run
helm install --dry-run --debug my-release ./chart
```

```bash
# Wait for resources
helm install my-release ./chart --wait --timeout 5m
```

```bash
# Create namespace
helm install my-release ./chart --namespace my-ns --create-namespace
```

```bash
# Reuse values on upgrade
helm install my-release ./chart --reuse-values
```

## Returns
Release info

## Gotchas / Version Notes
- Name is required (or use --generate-name).
- --set for command-line values.
- --values for file.
- --dry-run to test.
- Use --namespace for scoped install.

## References
- helm install: https://helm.sh/docs/helm/helm_install/
