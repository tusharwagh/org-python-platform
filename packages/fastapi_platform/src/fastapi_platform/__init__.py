"""FastAPI platform kit — errors, health, JWT, DB mixins."""

from fastapi_platform.db import TimestampMixin, UUIDPrimaryKeyMixin
from fastapi_platform.errors import AppError, ErrorCode, error_body, register_exception_handlers
from fastapi_platform.health import health_router
from fastapi_platform.jwt import AuthContext, JwtSettings, create_access_token, decode_access_token

__all__ = [
    "AppError",
    "AuthContext",
    "ErrorCode",
    "JwtSettings",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    "create_access_token",
    "decode_access_token",
    "error_body",
    "health_router",
    "register_exception_handlers",
]
