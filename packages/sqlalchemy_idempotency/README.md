# sqlalchemy-idempotency

Idempotent command handling with payload-hash validation.

```python
from sqlalchemy.orm import Session
from sqlalchemy_idempotency import find_cached_response, store_response, make_idempotency_model

IdempotencyRecord = make_idempotency_model(Base)
# migrate table, then:
cached = find_cached_response(session, scope_key="issue", idempotency_key=key, payload=body)
```
