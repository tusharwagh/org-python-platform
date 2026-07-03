# langfuse-tracing

Structured audit logging with optional Langfuse spans.

```python
from langfuse_tracing import LangfuseTracing, LangfuseTracingSettings

tracing = LangfuseTracing(LangfuseTracingSettings(
    langfuse_public_key="pk-...",
    langfuse_secret_key="sk-...",
))
with tracing.tool_span(tool_name="search", session_id="s1", operator_id="op1", agent_id="desk"):
    ...
```
