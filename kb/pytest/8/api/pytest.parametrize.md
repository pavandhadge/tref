---
library: pytest
version: "8.0.0"
category: api
item: pytest.parametrize
type: decorator
signature: "@pytest.mark.parametrize(argnames, argvalues)"
keywords: ["parametrize", "test cases", "data driven", "multiple inputs"]
aliases: ["parametrize", "data driven tests", "test parameters"]
intent: "Run a test function multiple times with different argument values, generating multiple test cases from a single test function."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.pytest.org/en/8.0.0/reference/reference.markers.html#pytest.mark.parametrize"
source_title: "pytest.mark.parametrize Documentation"
alternatives:
  - option: "pytest.generate_tests"
    reason: "Dynamic test generation with custom logic."
  - option: "for loop in test"
    reason: "Less elegant, harder to identify failures."
  - option: "subtests package"
    reason: "Continue after failures, report individually."
---

# pytest.mark.parametrize

## Signature
```python
@pytest.mark.parametrize("arg1,arg2", [(val1a, val2a), (val1b, val2b)])
def test_function(arg1, arg2):
    ...

@pytest.mark.parametrize("arg", values, ids=lambda x: f"test_{x}")
def test_single(arg):
    ...
```

## Parameters
- argnames: Comma-separated string or list of argument names.
- argvalues: Iterable of argument values (list of tuples if multiple args).
- ids: Custom test IDs for readability.
- indirect: Pass args to fixture instead of test function.

## What It Does
Creates multiple test runs from a single test function. Each tuple in argvalues generates a separate test case. Test names include parameter values for easy identification.

## Use When
- Testing same logic with multiple input values.
- Testing boundary conditions.
- Data-driven testing scenarios.
- API endpoint testing with different payloads.

## Examples
```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
```

```python
@pytest.mark.parametrize("username,password,valid", [
    ("admin", "password123", True),
    ("user", "wrong", False),
    ("", "", False),
])
def test_login(username, password, valid):
    result = authenticate(username, password)
    assert result.is_valid == valid
```

```python
@pytest.mark.parametrize("status_code", [200, 201, 204], ids=["ok", "created", "no_content"])
def test_response(status_code):
    response = api.call(status_code)
    assert response.status_code == status_code
```

```python
# With custom IDs
@pytest.mark.parametrize("input,output", [
    (1, "one"),
    (2, "two"),
], ids=["number_one", "number_two"])
def test_number_to_word(input, output):
    assert convert(input) == output
```

```python
# Nested parametrize
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [10, 20])
def test_combinations(a, b):
    # Runs 4 times: (1,10), (1,20), (2,10), (2,20)
    assert a + b > 0
```

## Returns
Creates multiple test functions

## Gotchas / Version Notes
- Multiple @pytest.mark.parametrize decorators multiply test cases.
- Use ids for readable test names in output.
- Can parametrize fixtures with indirect.
- Exception in any test case fails entire test run.
- Combine with pytest fixtures for complex setups.

## References
- parametrize docs: https://docs.pytest.org/en/8.0.0/reference/reference.markers.html#pytest.mark.parametrize
- Examples: https://docs.pytest.org/en/8.0.0/example/parametrize.html
