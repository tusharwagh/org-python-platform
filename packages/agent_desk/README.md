# agent-desk-starter

Generic LangGraph HITL desk primitives: SOP graph skeleton, in-memory sessions, privacy/redaction helpers.

```python
from agent_desk import compile_sop_graph, DeskSession, SessionStore, PseudonymMap

graph = compile_sop_graph()
store = SessionStore()
session = store.create(operator_id="operator-1")
```

Coordinators, tools, domain slots, and durable stores belong in your application.
