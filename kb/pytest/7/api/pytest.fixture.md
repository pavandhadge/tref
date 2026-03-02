---
library: pytest
version: "7.4.0"
category: api
item: pytest.fixture
type: decorator
signature: "@pytest.fixture(scope, params, autouse)"
keywords: ["fixture", "setup", "teardown", "dependency injection"]
aliases: ["pytest fixture", "test fixture", "setup function"]
intent: "Define reusable test fixtures that provide setup and teardown for tests, enabling dependency injection and reducing duplication."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.pytest.org/en/7.4.0/reference/fixtures.html"
source_title: "Pytest Fixtures Documentation"
alternatives:
  - option: "unittest setUp/tearDown"
    reason: "Class-based testing framework approach."
  - option: "setup_module"
    reason: "Module-level setup for multiple tests."
  - option: "conftest.py shared fixtures"
    reason: "Share fixtures across multiple test files."
---

# pytest.fixture

## Signature
```python
@pytest.fixture(scope="function", params=None, autouse=False, name=None)
def my_fixture():
    # setup
    yield value
    # teardown
```

## Parameters
- scope: "function", "class", "module", "package", "session".
- params: List of parameters for parametrized fixtures.
- autouse: Run automatically without explicit reference.
- name: Custom fixture name if different from function name.

## What It Does
Creates reusable setup and teardown functions for tests. Uses yield to separate setup from teardown. Supports dependency injection - fixtures can depend on other fixtures.

## Use When
- Creating test data or resources needed by multiple tests.
- Managing database connections or API clients.
- Cleaning up after tests (files, processes).
- Sharing common test configuration.

## Examples
```python
@pytest.fixture
def user():
    return {"name": "test", "email": "test@example.com"}
```

```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

```python
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
```

```python
@pytest.fixture
def user(db_connection):
    user = create_user(db_connection)
    yield user
    delete_user(db_connection, user.id)
```

```python
@pytest.fixture(params=["admin", "guest"])
def role(request):
    return request.param
```

```python
@pytest.fixture(autouse=True)
def reset_config():
    # Runs before every test
    load_default_config()
    yield
    restore_original_config()
```

## Returns
Fixture function that yields value to test

## Gotchas / Version Notes
- Use `yield` for teardown code after test runs.
- Exception in teardown marks test as failed.
- `request` fixture provides test context.
- Fixtures in conftest.py are auto-discovered.
- Scope affects how often fixture is created.

## References
- Fixtures docs: https://docs.pytest.org/en/7.4.0/reference/fixtures.html
- conftest: https://docs.pytest.org/en/7.4.0/reference/conftest.html
