---
library: spring
version: "3.0.0"
category: api
item: spring.RestController
type: annotation
signature: "@RestController @RequestMapping"
keywords: ["restcontroller", "api", "endpoint", "web"]
aliases: ["REST controller", "Spring REST", "API controller"]
intent: "Create RESTful API endpoints in Spring, combining @Controller and @ResponseBody for JSON/XML responses."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html"
source_title: "RestController Documentation"
alternatives:
  - option: "@Controller + @ResponseBody"
    reason: "Separate controller and response body annotation."
  - option: "Spring WebFlux"
    reason: "Reactive web framework for async operations."
  - option: "Spring MVC"
    reason: "Traditional synchronous web framework."
---

# @RestController

## Signature
```java
@RestController
@RequestMapping("/api")
public class UserController {
    
    @GetMapping("/users")
    public List<User> getUsers() { ... }
    
    @PostMapping("/users")
    public User createUser(@RequestBody User user) { ... }
}
```

## What It Does
Specialized version of @Controller. Automatically applies @ResponseBody to all methods, so return values are written to HTTP response body (usually as JSON). Base for building REST APIs.

## Use When
- Creating RESTful APIs.
- Building JSON/XML endpoints.
- Microservices with HTTP interfaces.
- CRUD operations via HTTP.

## Examples
```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    
    private final UserService userService;
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public User createUser(@RequestBody @Valid User user) {
        return userService.save(user);
    }
    
    @PutMapping("/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody User user) {
        user.setId(id);
        return userService.save(user);
    }
    
    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) {
        userService.deleteById(id);
    }
}
```

```java
// With response entity
@GetMapping("/users")
public ResponseEntity<List<User>> getUsers() {
    return ResponseEntity.ok(users);
}
```

```java
// Exception handling
@ExceptionHandler(UserNotFoundException.class)
public ResponseEntity<ErrorResponse> handleNotFound(UserNotFoundException ex) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(new ErrorResponse(ex.getMessage()));
}
```

## Returns
REST endpoint handlers

## Gotchas / Version Notes
- Spring 6.x uses jakarta.* imports (javax.* removed).
- @Valid triggers Bean Validation.
- Use @PathVariable for URL parameters.
- Use @RequestBody for request body.
- @RestControllerAdvice for global exception handling.

## References
- @RestController: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html
- Building REST services: https://spring.io/guides/tutorials/rest/
