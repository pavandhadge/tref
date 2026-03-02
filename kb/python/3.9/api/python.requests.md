---
library: python
version: "3.9.0"
category: api
item: python.requests
type: module
signature: "requests.get(url, params, headers), requests.post(url, data, json)"
keywords: ["requests", "http", "api", "web"]
aliases: ["http requests", "api calls", "web requests"]
intent: "Simple HTTP library for making web requests, supporting GET, POST, PUT, DELETE with automatic JSON handling."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python-requests.org/en/latest/"
source_title: "Requests Library"
alternatives:
  - option: "httpx"
    reason: "Async support, HTTP/2, similar API."
  - option: "urllib"
    reason: "Built-in, more complex but no dependencies."
  - option: "aiohttp"
    reason: "Async-only, for high concurrency."
---

# Requests

## Signature
```python
import requests

response = requests.get(url, params={}, headers={})
response = requests.post(url, data={}, json={}, headers={})
```

## What It Does
HTTP library for Python. Simplifies making HTTP requests with automatic encoding, connection pooling, JSON decoding, and session management.

## Use When
- Calling REST APIs.
- Web scraping.
- Downloading files.
- Testing HTTP endpoints.

## Examples
```python
# GET request
response = requests.get("https://api.example.com/users")
print(response.status_code)
print(response.json())

# With parameters
params = {"page": 1, "limit": 10}
response = requests.get("https://api.example.com/users", params=params)
```

```python
# POST request
data = {"name": "Alice", "email": "alice@example.com"}
response = requests.post("https://api.example.com/users", json=data)

# With headers
headers = {"Authorization": "Bearer token"}
response = requests.get("https://api.example.com/protected", headers=headers)
```

```python
# Response methods
response.text          # raw text
response.json()        # parsed JSON
response.status_code   # HTTP status
response.headers       # response headers
response.cookies      # cookies
response.raise_for_status()  # raise for 4xx/5xx
```

```python
# Session for persistence
session = requests.Session()
session.headers.update({"Authorization": "Bearer token"})
response = session.get("https://api.example.com/data")

# File uploads
files = {"file": open("document.pdf", "rb")}
response = requests.post("https://api.example.com/upload", files=files)
```

## Returns
Response object

## Gotchas / Version Notes
- Response.json() raises if not valid JSON.
- Use timeout to prevent hanging.
- Session for multiple requests (connection pooling).
- Don't commit secrets in code.

## References
- Requests docs: https://docs.python-requests.org/
