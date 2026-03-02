---
library: terraform
version: "1.5.0"
category: api
item: terraform.resource
type: block
signature: "resource \"type\" \"name\" { config }"
keywords: ["resource", "infrastructure", "provision", "deploy"]
aliases: ["terraform resource", "infrastructure as code", "IaC resource"]
intent: "Define infrastructure resources that Terraform manages - computes, networks, databases, or any cloud resource."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://developer.hashicorp.com/terraform/language/resources"
source_title: "Terraform Resource Documentation"
alternatives:
  - option: "AWS CloudFormation"
    reason: "AWS-native, JSON/YAML templating."
  - option: "Pulumi"
    reason: "Infrastructure as code with general-purpose languages."
  - option: "Ansible"
    reason: "Procedural configuration management."
---

# Resource

## Signature
```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t2.micro"
  tags = {
    Name = "web-server"
  }
}
```

## What It Does
Declares a resource of the specified type with a local name. Terraform manages the lifecycle: create, read, update, delete (CRUD). Each resource has configuration options for the cloud provider.

## Use When
- Creating cloud resources (EC2, S3, RDS, etc.).
- Managing infrastructure state.
- Reproducible infrastructure deployments.
- Multi-cloud resource provisioning.

## Examples
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
  
  tags = {
    Environment = "production"
  }
}
```

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}
```

```hcl
resource "null_resource" "example" {
  triggers = {
    always = timestamp()
  }
  
  provisioner "local-exec" {
    command = "echo Hello"
  }
}
```

```hcl
resource "aws_security_group" "web" {
  name = "web-sg"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Returns
Resource block creates/manages infrastructure

## Gotchas / Version Notes
- Provider must be configured before use.
- Use `depends_on` for implicit dependencies.
- Use `lifecycle` blocks for create_before_destroy, etc.
- `count` and `for_each` for multiple resources.
- `data` sources read existing resources.

## References
- Resources: https://developer.hashicorp.com/terraform/language/resources
- Providers: https://developer.hashicorp.com/terraform/language/providers
