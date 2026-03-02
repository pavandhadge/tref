---
library: fastapi
version: "0.100.0"
category: api
item: fastapi.FastAPI
type: class
signature: "app = FastAPI(title, version, docs_url, ...) "
keywords: ["fastapi", "app", "framework", "web"]
aliases: ["create app", "FastAPI instance", "ASGI app"]
intent: "Create the main FastAPI application instance that handles routing, middleware, and request processing."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://fastapi.tiangolo.com/reference/fastapi/"
source_title: "FastAPI Reference"
alternatives:
  - option: "Flask"
    reason: "Lightweight WSGI framework, simpler but less features."
  - option: "Django"
    reason: "Full-stack framework with ORM and admin panel."
  - option: "AIOHTTP"
    reason: "Async HTTP client/server without routing."
---

# FastAPI

## Signature
```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
```

## What It Does
Creates an ASGI application instance. Provides automatic OpenAPI schema generation, interactive docs (Swagger UI), request validation, dependency injection, and async support out of the box.

## Use When
- Building REST APIs with Python.
- Need automatic documentation and validation.
- High-performance async endpoints required.
- Microservices with OpenAPI integration.

## Examples
```python
from fastapi import FastAPI

app = FastAPI(title="Hello API")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True

@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "status": "created"}
```

```python
# With dependency injection
from fastapi import Depends

async def get_db():
    return db

@app.get("/users/")
def get_users(db = Depends(get_db)):
    return db.query(User).all()
```

## Returns
FastAPI application instance (ASGI app)

## Gotchas / Version Notes
- Uses Pydantic for data validation.
- Supports async def and sync def endpoints.
- Automatic OpenAPI documentation at /docs.
- Requires Uvicorn or similar ASGI server to run.
- Middleware order matters for request processing.

## References
- FastAPI docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/
