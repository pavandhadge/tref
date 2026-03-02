---
library: pydantic
version: "2.0.0"
category: api
item: pydantic.BaseModel
type: class
signature: "class Model(BaseModel): field: type"
keywords: ["pydantic", "validation", "model", "schema"]
aliases: ["pydantic model", "data validation", "schema"]
intent: "Define data models with type hints that automatically validate, serialize, and deserialize data at runtime."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.pydantic.dev/latest/"
source_title: "Pydantic Documentation"
alternatives:
  - option: "dataclasses"
    reason: "Built-in, less validation features."
  - option: "marshmallow"
    reason: "Serialization/deserialization, older."
  - option: "attrs"
    reason: "Simple class definitions with features."
---

# BaseModel

## Signature
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int
    email: str | None = None
```

## Parameters
- Field: Additional field configuration (default, description, validation).
- Config: Model-wide configuration class.

## What It Does
Validates data at runtime based on type hints. Generates schemas (JSON Schema), serialization, deserialization, and error messages automatically.

## Use When
- API request/response validation.
- Configuration parsing.
- Data transformation.
- Type-safe data models.

## Examples
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int = Field(default=0, ge=0)
    email: str | None = None

# Create
user = User(name="Alice", age=30)
print(user.model_dump())
print(user.model_json_schema())
```

```python
# Validation
try:
    user = User(name="Bob", age=-5)
except ValidationError as e:
    print(e)
```

```python
# Nested models
class Address(BaseModel):
    street: str
    city: str

class Person(BaseModel):
    name: str
    address: Address
```

```python
# Using Field for constraints
class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    tags: list[str] = []
```

```python
# Serialization
json_data = user.model_dump_json()
parsed = User.model_validate_json(json_data)
```

```python
# Model config
class Config(BaseModel):
    model_config = {"str_strip_whitespace": True}
```

## Returns
Validated model instance

## Gotchas / Version Notesantic v
- Pyd2 is faster (Rust core).
- Use | for Union (Python 3.10+).
- Field for constraints.
- model_validate for dict, model_validate_json for JSON.
- Can use validators decorator for custom.

## References
- Pydantic docs: https://docs.pydantic.dev/
