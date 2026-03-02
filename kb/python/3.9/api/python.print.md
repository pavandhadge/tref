---
library: python
version: "3.9.0"
category: api
item: python.print
type: function
signature: "print(*objects, sep=' ', end='\\n', file=sys.stdout, flush=False)"
keywords: ["print", "output", "display", "console"]
aliases: ["print function", "output to console", "print to stdout"]
intent: "Output objects to the standard output stream with customizable separator, end character, and file destination."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/library/functions.html#print"
source_title: "print function documentation"
alternatives:
  - option: "sys.stdout.write()"
    reason: "More control over output, no automatic newlines or formatting."
  - option: "logging module"
    reason: "Structured logging with levels and configuration for production apps."
  - option: "f-strings"
    reason: "String formatting within expressions for variable interpolation."
---

# print

## Signature
```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

## Parameters
- *objects: Any number of objects to print.
- sep: String inserted between values, default a space.
- end: String appended after the last value, default a newline.
- file: A file-like object with write method, default sys.stdout.
- flush: Whether to forcibly flush the stream, default False.

## What It Does
Prints the values to a stream, or to sys.stdout by default. Converts objects to strings and writes them separated by sep and followed by end.

## Use When
- Debugging and displaying output during development.
- Simple console output without logging requirements.
- Displaying results to users in CLI applications.

## Examples
```python
print("Hello, World!")
```

```python
print("Name:", "Alice", "Age:", 30, sep=" | ")
```

```python
print("Loading...", end="\r")
print("Done!")
```

```python
with open("output.txt", "w") as f:
    print("Written to file", file=f)
```

## Returns
None

## Gotchas / Version Notes
- In Python 2, print was a statement. Use function syntax in Python 3.
- The flush parameter is useful for real-time output without buffering.
- Use sys.stderr for error messages.

## References
- Python print docs: https://docs.python.org/3/library/functions.html#print
- f-strings: https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals
