---
library: express
version: "4.18.0"
category: api
item: express.express
type: function
signature: "const app = express()"
keywords: ["express", "server", "app", "framework"]
aliases: ["express app", "create server", "express instance"]
intent: "Create an Express application instance that provides methods for HTTP server creation, middleware, and routing."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://expressjs.com/en/4x/api.html"
source_title: "Express API Documentation"
alternatives:
  - option: "FastAPI"
    reason: "Python async framework with automatic docs."
  - option: "Koa"
    reason: "Lighter Express successor by same team."
  - option: "NestJS"
    reason: "Angular-inspired Node.js framework with DI."
  - option: "Hono"
    reason: "Fast, ultrafast web framework for edge runtimes."
---

# express()

## Signature
```javascript
const express = require('express');
const app = express();
```

## What It Does
Creates an Express application. The app object has methods for:
- Routing: `app.get()`, `app.post()`, etc.
- Middleware: `app.use()`
- View rendering: `app.set()`
- Starting server: `app.listen()`

## Use When
- Building REST APIs with Node.js.
- Creating web servers with routing.
- Adding middleware for logging, parsing, auth.
- Single-page application backends.

## Examples
```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World');
});

app.listen(3000);
```

```javascript
// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Route with params
app.get('/users/:id', (req, res) => {
  const userId = req.params.id;
  res.json({ id: userId });
});

// Query params
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.json({ results: [] });
});
```

```javascript
// POST body
app.post('/users', (req, res) => {
  const user = req.body;
  res.status(201).json(user);
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});
```

```javascript
// Sub-routers
const adminRouter = express.Router();
adminRouter.get('/dashboard', (req, res) => res.send('Admin'));
app.use('/admin', adminRouter);
```

## Returns
Express application instance

## Gotchas / Version Notes
- Middleware order matters - defined before routes.
- Don't forget to parse body with express.json().
- Use `express.Router()` for modular routes.
- 404 handler: app.use((req, res) => res.status(404));
- Error handler: app.use((err, req, res, next) => {...}).

## References
- Express docs: https://expressjs.com/
- Routing: https://expressjs.com/en/guide/routing.html
