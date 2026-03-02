---
library: terraform
version: "1.9.0"
category: api
item: terraform.module
type: block
signature: "module \"name\" { source, ... }"
keywords: ["module", "reusable", "component", "template"]
aliases: ["terraform module", "reusable infrastructure", "IaC module"]
intent: "Group and reuse infrastructure configuration as a modular component with inputs and outputs."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://developer.hashicorp.com/terraform/language/modules"
source_title: "Terraform Module Documentation"
alternatives:
  - option: "Terragrunt"
    reason: "Orchestration and composition tool for Terraform."
  - option: "separate tf files"
    reason: "Manual file organization without encapsulation."
  - option: "Child modules"
    reason: "Terminology for modules called by root module."
---

# Module

## Signature
```hcl
module "vpc" {
  source = "./modules/vpc"
  
  cidr_block = "10.0.0.0/16"
  name       = "production"
}
```

## What It Does
Groups infrastructure into reusable components. Modules encapsulate resources, accept input variables, and expose output values. Enables code reuse and separation of concerns.

## Use When
- Reusing infrastructure patterns across projects.
- Organizing complex infrastructure into components.
- Creating reusable infrastructure templates.
- Team-based infrastructure development.

## Examples
```hcl
module "ec2_instance" {
  source = "terraform-aws-modules/ec2-instance/aws"
  
  name           = "web-server"
  instance_type  = "t3.micro"
  ami            = "ami-12345"
  
  tags = {
    Environment = "production"
  }
}
```

```hcl
# Child module: modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
}

# Child module: modules/vpc/outputs.tf  
output "vpc_id" {
  value = aws_vpc.main.id
}
```

```hcl
# Parent: outputs.tf references module output
module "vpc" {
  source = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
```

```hcl
# Module with count
module "servers" {
  source = "./compute"
  
  count = 3
  name  = "server-${count.index}"
}
```

## Returns
Module block instantiates reusable configuration

## Gotchas / Version Notes
- Use `source` to specify module location (local, registry, git).
- Module outputs must be explicitly declared.
- Use `providers` to pass provider configs.
- Module versions recommended (ref= tag/branch).
- Use `for_each` with maps for dynamic instances.

## References
- Modules: https://developer.hashicorp.com/terraform/language/modules
- Module registry: https://registry.terraform.io/
