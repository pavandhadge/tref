---
library: django
version: "4.2.0"
category: api
item: django.views
type: view
signature: "def view(request): return HttpResponse"
keywords: ["view", "request", "response", "http"]
aliases: ["Django view", "HTTP view", "endpoint"]
intent: "Handle HTTP requests and return HTTP responses. Views are the core of Django's request/response processing."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.djangoproject.com/en/4.2/topics/http/views/"
source_title: "Django Views Documentation"
alternatives:
  - option: "Class-based views (CBV)"
    reason: "Reusable view classes with mixins for common patterns."
  - option: "Django REST Framework views"
    reason: "API-specific views with serialization."
  - option: "Async views"
    reason: "Async handling for I/O-bound operations."
---

# Django Views

## Signature
```python
from django.http import HttpResponse

def my_view(request):
    return HttpResponse("Hello")
```

## What It Does
A view is a callable that takes a Web request and returns a Web response. Can be a function (FBV) or class (CBV). Contains business logic and returns HttpResponse, JsonResponse, or render().

## Use When
- Processing HTTP requests.
- Returning HTML, JSON, or other content.
- Handling forms and user input.
- Integrating with models for CRUD operations.

## Examples
```python
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello World")
```

```python
from django.shortcuts import render, get_object_or_404
from .models import Article

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'article.html', {'article': article})
```

```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def api_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'data': []})
```

```python
# Class-based view
from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
```

```python
# Async view (Django 3.1+)
import asyncio
from django.http import JsonResponse

async def async_view(request):
    await asyncio.sleep(1)
    return JsonResponse({'message': 'Hello async'})
```

## Returns
HttpResponse, JsonResponse, or render() result

## Gotchas / Version Notes
- First parameter is always `request` (HttpRequest object).
- Must return HttpResponse or similar.
- Use `@require_http_methods` for method restrictions.
- CBVs provide reusable patterns for common operations.
- Async views require ASGI server (uvicorn, etc.).

## References
- Django views: https://docs.djangoproject.com/en/4.2/topics/http/views/
- CBV docs: https://docs.djangoproject.com/en/4.2/topics/class-based-views/
