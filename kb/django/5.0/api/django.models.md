---
library: django
version: "5.0.0"
category: api
item: django.models
type: model
signature: "class ModelName(models.Model):"
keywords: ["model", "database", "orm", "schema"]
aliases: ["Django model", "ORM model", "database model"]
intent: "Define database schema and ORM operations. Each model maps to a database table and provides methods for CRUD operations."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.djangoproject.com/en/5.0/topics/db/models/"
source_title: "Django Models Documentation"
alternatives:
  - option: "Django ORM with raw SQL"
    reason: "Complex queries not easily expressed in ORM."
  - option: "SQLAlchemy"
    reason: "Python SQL toolkit for other frameworks."
  - option: "Tortoise ORM"
    reason: "Async ORM for asyncio applications."
---

# Django Models

## Signature
```python
from django.db import models

class ModelName(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

## What It Does
Define database tables as Python classes. Each attribute is a database field. Models provide ORM methods: `.objects.create()`, `.save()`, `.filter()`, etc. Migrations convert models to SQL schema.

## Use When
- Defining database schema.
- CRUD operations on database records.
- Complex queries with Q objects and aggregations.
- Database-agnostic code (works with PostgreSQL, MySQL, SQLite, etc.).

## Examples
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
```

```python
# Creating
article = Article.objects.create(title="Hello", content="World")

# Reading
articles = Article.objects.filter(published=True)
article = Article.objects.get(pk=1)

# Updating
article.title = "New Title"
article.save()

# Deleting
article.delete()
```

```python
# Complex queries
from django.db.models import Q, Count

articles = Article.objects.filter(
    Q(author=request.user) | Q(published=True)
).annotate(
    comment_count=Count('comments')
).order_by('-created')
```

```python
# Relationships
author.articles.all()  # reverse relation
article.author.username  # forward relation
```

## Returns
Model class with ORM methods

## Gotchas / Version Notes
- Always add `__str__` method.
- Use `on_delete` for ForeignKey (CASCADE, PROTECT, etc.).
- `auto_now_add` vs `auto_now` for DateTimeField.
- Run `makemigrations` and `migrate` after model changes.
- Use `select_related`, `prefetch_related` for optimization.

## References
- Django Models: https://docs.djangoproject.com/en/5.0/topics/db/models/
- QuerySet API: https://docs.djangoproject.com/en/5.0/ref/models/querysets/
