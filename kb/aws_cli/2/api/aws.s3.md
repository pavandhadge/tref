---
library: aws_cli
version: "2.15.0"
category: api
item: aws.s3
type: command
signature: "aws s3 <command> [options]"
keywords: ["s3", "storage", "bucket", "object"]
aliases: ["aws s3", "s3 cli", "simple storage service"]
intent: "Manage S3 buckets and objects - upload, download, list, sync with Amazon Simple Storage Service."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/index.html"
source_title: "AWS S3 CLI Documentation"
alternatives:
  - option: "s3transfer library"
    reason: "Python library for S3 transfers."
  - option: "AWS SDK (boto3)"
    reason: "Programmatic access for applications."
---

# AWS S3 Commands

## Signature
```bash
aws s3 cp s3://bucket/key local-file
aws s3 ls s3://bucket/
aws s3 sync local-dir s3://bucket/
aws s3 mb s3://bucket-name
```

## What It Does
Manage S3 (Simple Storage Service) from command line. Upload, download, list, sync files. Manage buckets and access.

## Use When
- Uploading files to S3.
- Downloading from S3.
- Syncing directories.
- Managing buckets.

## Examples
```bash
# List buckets
aws s3 ls
```

```bash
# List objects
aws s3 ls s3://my-bucket/
aws s3 ls s3://my-bucket/prefix/
```

```bash
# Copy file to S3
aws s3 cp myfile.txt s3://my-bucket/
aws s3 cp myfile.txt s3://my-bucket/backup/
```

```bash
# Copy from S3
aws s3 cp s3://my-bucket/data.csv ./
```

```bash
# Sync directories
aws s3 sync ./local-dir s3://my-bucket/
aws s3 sync s3://my-bucket/backup ./local-backup
```

```bash
# Make bucket
aws s3 mb s3://new-bucket-name
```

```bash
# Remove bucket
aws s3 rb s3://empty-bucket
aws s3 rb s3://bucket --force  # force delete
```

```bash
# Remove object
aws s3 rm s3://my-bucket/old-file.txt
```

```bash
# Presigned URL
aws s3 presign s3://my-bucket/file.txt --expires-in 3600
```

```bash
# Website configuration
aws s3 website s3://my-bucket \
  --index-document index.html \
  --error-document error.html
```

## Returns
Success output or error

## Gotchas / Version Notes
- Use --region for specific region.
- --recursive for directories.
- Use --exclude/--include with sync.
- s3:// URI scheme for paths.

## References
- AWS S3 CLI: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/index.html
