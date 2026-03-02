---
library: jest
version: "28.1.0"
category: api
item: jest.test
type: function
signature: "test(name, fn, timeout) / it(name, fn, timeout)"
keywords: ["test", "it", "spec", "test case"]
aliases: ["jest test", "test block", "spec function"]
intent: "Define a single test case within a test suite, with optional timeout and asynchronous support."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://jestjs.io/docs/api#testname-fn-timeout"
source_title: "Jest test API Documentation"
alternatives:
  - option: "describe block"
    reason: "Groups related tests, not individual test cases."
  - option: "test.each"
    reason: "Parametrized tests for multiple inputs."
  - option: "it.each"
    reason: "Alias for test.each with same functionality."
---

# test / it

## Signature
```javascript
test(name, fn, timeout);
it(name, fn, timeout);
```

## Parameters
- name: String describing what the test verifies.
- fn: Test function (synchronous or async/Promise).
- timeout: Optional timeout in milliseconds (default: 5000ms).

## What It Does
Creates a test case. The test passes if the function doesn't throw, fails if it throws an error. Supports async functions, Promises, and callbacks. `it` is an alias for `test`.

## Use When
- Writing individual test assertions.
- Testing synchronous and asynchronous code.
- Creating parametrized tests with test.each.

## Examples
```javascript
test('adds 1 + 2 to equal 3', () => {
  expect(1 + 2).toBe(3);
});
```

```javascript
it('should fetch user', async () => {
  const user = await fetchUser(1);
  expect(user.id).toBe(1);
});
```

```javascript
test('promises resolve', () => {
  return expect(Promise.resolve('ok')).resolves.toBe('ok');
});
```

```javascript
test('rejects with error', () => {
  return expect(Promise.reject(new Error('fail'))).rejects.toThrow('fail');
});
```

```javascript
test('callback style', (done) => {
  getData((err, data) => {
    expect(err).toBeNull();
    expect(data).toBeDefined();
    done();
  });
});
```

```javascript
test('timeout extended', async () => {
  await longRunningOperation();
}, 10000);
```

## Returns
undefined (registers test case)

## Gotchas / Version Notes
- Use `expect` for assertions.
- Async tests must return Promise or use callback.
- Use `.only` to run single test: `test.only()`.
- Use `.skip` to skip: `test.skip()`.
- Test timeout default is 5 seconds.

## References
- Jest API: https://jestjs.io/docs/api#testname-fn-timeout
- Expect: https://jestjs.io/docs/expect
