# agent-desk-starter

Generic LangGraph HITL desk primitives extracted from LMS-AI.

```python
from agent_desk import compile_sop_graph, DeskSession, SessionStore, PseudonymMap

graph = compile_sop_graph()
store = SessionStore()
session = store.create(operator_id="staff-1")
```

Domain-specific coordinator, tools, and slots remain in your application.
