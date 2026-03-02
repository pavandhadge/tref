---
library: curl
version: "7.81.0"
category: api
item: curl.http
type: command
signature: "curl [options] URL"
keywords: ["curl", "http", "request", "api"]
aliases: ["http client", "download", "api call"]
intent: "Transfer data from/to servers using various protocols, primarily HTTP/HTTPS for API testing and file downloads."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://curl.se/docs/manpage.html"
source_title: "curl Documentation"
alternatives:
  - option: "wget"
    reason: "Recursive downloads, older protocol support."
  - option: "httpie"
    reason: "Human-friendly HTTP client."
  - option: "fetch"
    reason: "BSD, simpler but less options."
---

# curl

## Signature
```bash
curl [options] URL
curl -X METHOD -H "Header: value" -d "data" URL
```

## What It Does
Command-line HTTP client. Supports HTTP/HTTPS/FTP/FTPS/SCP/SFTP. Make requests, download files, test APIs, interact with web services.

## Use When
- Testing APIs.
- Downloading files.
- Debugging HTTP issues.
- Automating web requests.

## Examples
```bash
curl https://api.example.com/data
```

```bash
# POST request
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

```bash
# With headers
curl -H "Authorization: Bearer token" \
  -H "Accept: application/json" \
  https://api.example.com/protected
```

```bash
# Form data
curl -X POST -d "username=alice" -d "password=secret" \
  https://example.com/login
```

```bash
# Download file
curl -O https://example.com/file.zip
curl -o custom.zip https://example.com/file.zip
```

```bash
# Follow redirects
curl -L https://short.url/abc
```

```bash
# Verbose
curl -v https://example.com
curl --verbose https://example.com
```

```bash
# With cookies
curl -b "session=abc123" https://example.com
curl -c cookies.txt https://example.com
```

```bash
# Upload file
curl -X POST -F "file=@document.pdf" \
  https://example.com/upload
```

## Returns
Server response (or downloads to file)

## Gotchas / Version Notes
- Use -k for insecure (self-signed certs).
- -s for silent (no progress).
- -o for output file, -O for original name.
- Escape special chars in data.
- Use @filename for file data.

## References
- curl docs: https://curl.se/docs/manpage.html
