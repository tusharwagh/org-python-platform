# litellm-gateway

LiteLLM Router gateway extracted from LMS-AI `shared/llm/`.

```python
from litellm_gateway import LlmGateway, LlmGatewaySettings

settings = LlmGatewaySettings(
    agent_mock_llm=False,
    groq_api_key="gsk_...",
    llm_provider="groq",
    llm_model="llama-3.3-70b-versatile",
)
gateway = LlmGateway.from_settings(settings)
result = gateway.complete(
    messages=[{"role": "user", "content": "Hello"}],
    purpose="demo",
)
print(result.endpoint.provider, result.cost_usd)
```
