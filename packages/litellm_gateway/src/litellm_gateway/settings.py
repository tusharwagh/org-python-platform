"""Settings for the LiteLLM gateway (explicit dataclass; inject from your app config)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LlmGatewaySettings:
    """Configuration surface required by routing, guardrails, and gateway."""

    agent_mock_llm: bool = True
    llm_provider: str = "groq"
    llm_model: str = "llama-3.3-70b-versatile"
    llm_fallback_enabled: bool = False
    llm_fallback_provider: str = "openai"
    llm_fallback_model: str | None = None
    llm_providers: str = ""
    llm_proxy_url: str | None = None
    llm_proxy_api_key: str | None = None
    llm_cache_enabled: bool = True
    llm_rate_limit_enabled: bool = False
    llm_rate_limit_window_seconds: int = 60
    llm_rate_limit_max: int = 60
    llm_max_prompt_chars: int = 32_000
    llm_max_tokens_cap: int = 4096
    deployment_prefix: str = "app"
    groq_api_key: str | None = None
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    together_api_key: str | None = None
    hf_token: str | None = None
    azure_api_key: str | None = None
    azure_api_base: str | None = None
