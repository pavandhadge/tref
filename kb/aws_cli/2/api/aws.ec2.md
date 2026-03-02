---
library: aws_cli
version: "2.15.0"
category: api
item: aws.ec2
type: command
signature: "aws ec2 <command> [options]"
keywords: ["ec2", "virtual server", "instance", "cloud"]
aliases: ["aws ec2", "virtual machines", "compute"]
intent: "Manage EC2 instances - create, start, stop, terminate, and manage virtual servers in AWS cloud."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/index.html"
source_title: "AWS EC2 CLI Documentation"
alternatives:
  - option: "AWS Console"
    reason: "Web UI, not command-line."
  - option: "Terraform"
    reason: "Infrastructure as code."
---

# AWS EC2 Commands

## Signature
```bash
aws ec2 run-instances --image-id ami-xxx --instance-type t3.micro
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-xxx
aws ec2 stop-instances --instance-ids i-xxx
```

## What It Does
Create and manage virtual servers (instances) in AWS. Launch, start, stop, terminate, monitor EC2 instances.

## Use When
- Launching servers.
- Managing instance lifecycle.
- Getting instance status.
- Creating AMIs.

## Examples
```bash
# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-key-pair \
  --security-group-ids sg-xxx \
  --subnet-id subnet-xxx
```

```bash
# List instances
aws ec2 describe-instances
aws ec2 describe-instances --instance-ids i-1234567890abcdef0
```

```bash
# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

```bash
# Stop instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
```

```bash
# Terminate instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

```bash
# Create key pair
aws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > MyKeyPair.pem
```

```bash
# Create security group
aws ec2 create-security-group \
  --group-name my-sg \
  --description "My security group"
```

```bash
# Add rule to security group
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp --port 22 --cidr 0.0.0.0/0
```

## Returns
JSON output with instance details

## Gotchas / Version Notes
- Requires key pair for SSH access.
- Security group controls access.
- Use --query to filter output.
- Use tags for organization.
- Instance types have different costs.

## References
- AWS EC2 CLI: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/index.html
