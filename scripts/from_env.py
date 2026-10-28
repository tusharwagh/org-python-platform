#!/usr/bin/env python3
"""Load repo .env and construct package settings from environment variables."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _settings_class(package: str, settings_file: str, class_name: str):
    path = ROOT / "packages" / package / "src" / package / settings_file
    module = _load_module(f"{package}.{settings_file.removesuffix('.py')}", path)
    return getattr(module, class_name)


def load_dotenv_file(path: Path | None = None) -> Path | None:
    """Load .env from repo root. Returns the path loaded, or None if missing."""
    env_path = path or ROOT / ".env"
    if not env_path.is_file():
        return None

    try:
        from dotenv import load_dotenv
    except ImportError as exc:
        raise RuntimeError("Install dev deps: make dev-install (requires python-dotenv)") from exc

    load_dotenv(env_path, override=False)
    return env_path


def _optional_str(name: str) -> str | None:
    value = os.getenv(name)
    if value is None or not value.strip():
        return None
    return value.strip()


def _str(name: str, default: str) -> str:
    value = os.getenv(name)
    return default if value is None else value.strip()


def _bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return int(raw)


def llm_gateway_settings():
    LlmGatewaySettings = _settings_class("litellm_gateway", "settings.py", "LlmGatewaySettings")

    return LlmGatewaySettings(
        agent_mock_llm=_bool("AGENT_MOCK_LLM", True),
        llm_provider=_str("LLM_PROVIDER", "groq"),
        llm_model=_str("LLM_MODEL", "llama-3.3-70b-versatile"),
        llm_fallback_enabled=_bool("LLM_FALLBACK_ENABLED", False),
        llm_fallback_provider=_str("LLM_FALLBACK_PROVIDER", "openai"),
        llm_fallback_model=_optional_str("LLM_FALLBACK_MODEL"),
        llm_providers=_str("LLM_PROVIDERS", ""),
        llm_proxy_url=_optional_str("LLM_PROXY_URL"),
        llm_proxy_api_key=_optional_str("LLM_PROXY_API_KEY"),
        llm_cache_enabled=_bool("LLM_CACHE_ENABLED", True),
        llm_rate_limit_enabled=_bool("LLM_RATE_LIMIT_ENABLED", False),
        llm_rate_limit_window_seconds=_int("LLM_RATE_LIMIT_WINDOW_SECONDS", 60),
        llm_rate_limit_max=_int("LLM_RATE_LIMIT_MAX", 60),
        llm_max_prompt_chars=_int("LLM_MAX_PROMPT_CHARS", 32_000),
        llm_max_tokens_cap=_int("LLM_MAX_TOKENS_CAP", 4096),
        deployment_prefix=_str("DEPLOYMENT_PREFIX", "app"),
        groq_api_key=_optional_str("GROQ_API_KEY"),
        openai_api_key=_optional_str("OPENAI_API_KEY"),
        anthropic_api_key=_optional_str("ANTHROPIC_API_KEY"),
        together_api_key=_optional_str("TOGETHER_API_KEY"),
        hf_token=_optional_str("HF_TOKEN"),
        azure_api_key=_optional_str("AZURE_API_KEY"),
        azure_api_base=_optional_str("AZURE_API_BASE"),
    )


def langfuse_tracing_settings():
    LangfuseTracingSettings = _settings_class(
        "langfuse_tracing", "settings.py", "LangfuseTracingSettings"
    )

    return LangfuseTracingSettings(
        langfuse_public_key=_optional_str("LANGFUSE_PUBLIC_KEY"),
        langfuse_secret_key=_optional_str("LANGFUSE_SECRET_KEY"),
        langfuse_host=_optional_str("LANGFUSE_HOST"),
    )


def jwt_settings():
    JwtSettings = _settings_class("fastapi_platform", "jwt.py", "JwtSettings")

    secret = _optional_str("APP_SECRET_KEY")
    if not secret:
        raise ValueError("APP_SECRET_KEY is required for JwtSettings")
    return JwtSettings(
        app_secret_key=secret,
        jwt_algorithm=_str("JWT_ALGORITHM", "HS256"),
        jwt_access_token_expire_minutes=_int("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60),
    )


def _secret_keys() -> set[str]:
    return {
        "GROQ_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "TOGETHER_API_KEY",
        "HF_TOKEN",
        "AZURE_API_KEY",
        "LLM_PROXY_API_KEY",
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY",
        "APP_SECRET_KEY",
        "GITHUB_TOKEN",
        "TWINE_PASSWORD",
    }


def _env_file_keys(path: Path) -> list[str]:
    keys: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            keys.append(line.split("=", 1)[0].strip())
    return keys


def check_env() -> int:
    env_path = ROOT / ".env"
    if not env_path.is_file():
        print(f"no .env file at {env_path} — run: make env-init", file=sys.stderr)
        return 1

    loaded = load_dotenv_file(env_path)
    assert loaded is not None

    print(f"loaded {loaded.relative_to(ROOT)}")

    for key in _env_file_keys(env_path):
        value = os.getenv(key)
        if value is None:
            print(f"  {key}=<unset>")
        elif key in _secret_keys():
            print(f"  {key}=***")
        else:
            print(f"  {key}={value}")

    llm_gateway_settings()
    print("  LlmGatewaySettings: ok")

    langfuse_tracing_settings()
    print("  LangfuseTracingSettings: ok")

    if os.getenv("APP_SECRET_KEY"):
        jwt_settings()
        print("  JwtSettings: ok")
    else:
        print("  JwtSettings: skipped (APP_SECRET_KEY unset)")

    return 0


if __name__ == "__main__":
    raise SystemExit(check_env())
