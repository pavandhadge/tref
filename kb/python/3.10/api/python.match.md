---
library: python
version: "3.10.0"
category: api
item: python.match
type: statement
signature: "match subject: case pattern1: ... case pattern2: ..."
keywords: ["match", "pattern matching", "switch", "case"]
aliases: ["match statement", "pattern matching", "switch case"]
intent: "Match a subject expression against one or more patterns, similar to switch-case in other languages."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/tutorial/controlflow.html#match-statements"
source_title: "match statement documentation"
alternatives:
  - option: "if-elif-else chains"
    reason: "Traditional conditional flow for simple cases."
  - option: "dictionary mapping"
    reason: "Map values to functions or results."
---

# match

## Signature
```python
match subject:
    case pattern1:
        # code
    case pattern2:
        # code
    case _:
        # default
```

## What It Does
Evaluates the subject expression and compares it against patterns in case blocks. The first matching pattern's block executes. Supports literal patterns, wildcard, or-patterns, as-patterns, and class patterns.

## Use When
- Replacing long if-elif-else chains with cleaner pattern matching.
- Parsing structured data like JSON or AST nodes.
- Implementing state machines.

## Examples
```python
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return "Unknown"
```

```python
match point:
    case (x, y):
        print(f"Point at {x}, {y}")
    case {"type": "circle", "radius": r}:
        print(f"Circle with radius {r}")
```

```python
match command.split():
    case ["quit"]:
        print("Goodbye!")
    case ["go", direction]:
        print(f"Going {direction}")
    case _:
        print("Unknown command")
```

## Returns
None (executes code blocks)

## Gotchas / Version Notes
- Only available in Python 3.10+.
- The wildcard case `_` matches anything and must be last.
- Use `case _ as name:` to capture the subject.

## References
- PEP 634: https://peps.python.org/pep-0634/
- Pattern matching tutorial: https://docs.python.org/3/tutorial/controlflow.html#match-statements
