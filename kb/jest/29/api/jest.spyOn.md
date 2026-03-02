---
library: jest
version: "29.7.0"
category: api
item: jest.spyOn
type: function
signature: "jest.spyOn(object, methodName, accessType)"
keywords: ["spy", "mock", "spyOn", "monitor"]
aliases: ["create spy", "method monitoring", "partial mock"]
intent: "Create a mock function that wraps the specified method, allowing you to track calls and optionally mock implementation while leaving other methods unchanged."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://jestjs.io/docs/jest-object#jestspyonobject-methodname-accesstype"
source_title: "jest.spyOn Documentation"
alternatives:
  - option: "jest.fn()"
    reason: "Creates standalone mock function, not wrapping existing method."
  - option: "jest.mock()"
    reason: "Mocks entire module at import time."
  - option: "manual mock"
    reason: "Create __mocks__ folder with manual mock implementation."
---

# jest.spyOn

## Signature
```javascript
const spy = jest.spyOn(object, 'methodName');
const spy = jest.spyOn(object, 'methodName', 'get'); // or 'set'
```

## Parameters
- object: Object containing method to spy on.
- methodName: Name of method to spy on.
- accessType: Optional - 'get' or 'set' for getters/setters.

## What It Does
Wraps an existing method with a mock function. Tracks all calls, arguments, and instances. Unlike jest.fn(), only replaces the specified method - other methods of the object remain unchanged.

## Use When
- Testing that a method is called with specific arguments.
- Temporarily replacing a method implementation.
- Testing callbacks or event handlers.
- Mocking getters/setters.

## Examples
```javascript
const obj = {
  getData: () => 'real data',
  process: (x) => x * 2,
};

test('spies on method', () => {
  const spy = jest.spyOn(obj, 'getData');
  
  obj.getData();
  
  expect(spy).toHaveBeenCalled();
  expect(obj.getData()).toBe('real data'); // still returns real
  
  spy.mockReturnValue('mocked');
  expect(obj.getData()).toBe('mocked'); // now mocked
  
  spy.mockRestore();
  expect(obj.getData()).toBe('real data'); // restored
});
```

```javascript
test('tracks arguments', () => {
  const spy = jest.spyOn(obj, 'process');
  
  obj.process(5);
  obj.process(10);
  
  expect(spy).toHaveBeenCalledTimes(2);
  expect(spy).toHaveBeenCalledWith(5);
  expect(spy).toHaveBeenCalledWith(10);
});
```

```javascript
test('mock implementation', () => {
  jest.spyOn(console, 'log').mockImplementation(() => {});
  
  // console.log now does nothing
  console.log('silent');
  
  jest.restoreAllMocks(); // cleanup
});
```

## Returns
Mock spy function

## Gotchas / Version Notes
- Use `mockRestore()` to restore original method.
- Use `mockImplementation()` to change behavior temporarily.
- Works with getters/setters using accessType parameter.
- After Jest 29, returns jest.SpiedMethod type.
- Don't forget to restore spies in afterEach.

## References
- jest.spyOn: https://jestjs.io/docs/jest-object#jestspyonobject-methodname-accesstype
- Mock functions: https://jestjs.io/docs/mock-functions
