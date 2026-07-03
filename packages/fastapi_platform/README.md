# fastapi-platform-kit

Shared FastAPI building blocks extracted from LMS-AI.

```python
from fastapi import FastAPI
from fastapi_platform import register_exception_handlers, health_router

app = FastAPI()
register_exception_handlers(app, debug=False)
app.include_router(health_router)
```
