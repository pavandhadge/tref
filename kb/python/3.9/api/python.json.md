---
library: python
version: "3.9.0"
item: python.jsoncategory: api

type: module
signature: "json.dumps(obj), json.loads(s), json.load(fp)"
keywords: ["json", "serialize", "deserialize", "parse"]
aliases: ["json parsing", "json encoding", "json decoding"]
intent: "Encode Python objects to JSON strings and decode JSON strings back to Python objects for data interchange."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/library/json.html"
source_title: "json Module"
alternatives:
  - option: "pickle"
    reason: "Python object serialization, supports arbitrary objects."
  - option: "orjson"
    reason: "Faster JSON, supports dataclasses, datetime."
  - option: "ujson"
    reason: "Ultra-fast JSON parser/writer."
---

# JSON

## Signature
```python
import json

json.dumps(obj, indent=None)      # to string
json.loads(s)                     # from string
json.dump(obj, fp)                # to file
json.load(fp)                     # from file
```

## What It Does
Convert between JSON (JavaScript Object Notation) and Python data structures. Supports dict, list, str, int, float, bool, None.

## Use When
- API requests/responses.
- Configuration files.
- Data exchange between systems.
- Log files.

## Examples
```python
# Serialize to string
data = {"name": "Alice", "age": 30, "active": True}
json_str = json.dumps(data)  # '{"name": "Alice", "age": 30, ...}'
pretty = json.dumps(data, indent=2)  # formatted
```

```python
# Deserialize from string
json_str = '{"name": "Bob", "scores": [1, 2, 3]}'
data = json.loads(json_str)  # {'name': 'Bob', 'scores': [1, 2, 3]}
```

```python
# File operations
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r") as f:
    data = json.load(f)
```

```python
# Custom encoding
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def user_encoder(obj):
    if isinstance(obj, User):
        return {"name": obj.name, "age": obj.age}
    raise TypeError

json.dumps(user, default=user_encoder)

# Or use JSONEncoder subclass
class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)

json.dumps(user, cls=UserEncoder)
```

```python
# Custom decoding
def user_decoder(d):
    if "name" in d and "age" in d:
        return User(d["name"], d["age"])
    return d

data = json.loads(json_str, object_hook=user_decoder)
```

## Returns
String (dumps/loads) or None (dump/load)

## Gotchas / Version Notes
- Keys must be strings in JSON (dict keys converted).
- No support for tuples (converted to arrays).
- Use ensure_ascii=False for non-ASCII.
- For dates, use custom encoder or isoformat.

## References
- json docs: https://docs.python.org/3/library/json.html
