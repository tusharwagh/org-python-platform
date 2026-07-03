"""LiteLLM global configuration."""

from __future__ import annotations

from litellm_gateway.settings import LlmGatewaySettings


def configure_litellm(settings: LlmGatewaySettings) -> None:
    """Apply optional LiteLLM global settings (no-op when mock mode)."""
    if settings.agent_mock_llm:
        return
    try:
        import litellm

        litellm.suppress_debug_info = True
    except ImportError:
        pass
