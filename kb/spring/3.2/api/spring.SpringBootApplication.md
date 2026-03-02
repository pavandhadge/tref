---
library: spring
version: "3.2.0"
category: api
item: spring.SpringBootApplication
type: annotation
signature: "@SpringBootApplication"
keywords: ["springboot", "application", "main", "boot"]
aliases: ["Spring Boot main", "boot application", "app entry point"]
intent: "Main Spring Boot application class annotation that combines @Configuration, @EnableAutoConfiguration, and @ComponentScan."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/SpringBootApplication.html"
source_title: "SpringBootApplication Documentation"
alternatives:
  - option: "Manual Spring config"
    reason: "Traditional XML/Java config without auto-configuration."
  - option: "Spring Initializr"
    reason: "Project generator, not a code annotation."
---

# @SpringBootApplication

## Signature
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

## What It Does
Main Spring Boot application class annotation. Combines three annotations:
- @Configuration: Marks class as bean definition source
- @EnableAutoConfiguration: Enables Spring Boot auto-configuration
- @ComponentScan: Enables component scanning in current package

## Use When
- Creating Spring Boot application entry point.
- Enabling auto-configuration.
- Scanning components in default package hierarchy.

## Examples
```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

```java
// Customizing with properties
@SpringBootApplication(
    scanBasePackages = {"com.example", "org.acme"},
    exclude = {DataSourceAutoConfiguration.class}
)
public class Application { }
```

```java
// Programmatically configure
public static void main(String[] args) {
    SpringApplication app = new SpringApplication(MyApplication.class);
    app.setBannerMode(Banner.Mode.OFF);
    app.run(args);
}
```

```java
// CommandLineRunner example
@SpringBootApplication
public class Application implements CommandLineRunner {
    
    @Autowired
    private DataService dataService;
    
    @Override
    public void run(String... args) throws Exception {
        dataService.process();
    }
}
```

## Returns
Boot application entry point

## Gotchas / Version Notes
- Spring Boot 3.x requires Java 17+.
- Uses jakarta.* namespace (javax.* deprecated).
- Custom exclusions with exclude attribute.
- scanBasePackages to change scanning.
- Application runs in isolated app context.

## References
- SpringBootApplication: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/SpringBootApplication.html
- Getting started: https://spring.io/guides/gs/spring-boot/
