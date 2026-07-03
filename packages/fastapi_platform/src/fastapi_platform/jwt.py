from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from jose import JWTError, jwt


@dataclass(frozen=True, slots=True)
class JwtSettings:
    app_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60


@dataclass(frozen=True, slots=True)
class AuthContext:
    subject: str
    role: str
    tenant_id: str | None = None


def create_access_token(
    settings: JwtSettings,
    subject: str,
    role: str,
    *,
    tenant_id: str | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "exp": expire,
    }
    if tenant_id is not None:
        payload["tenant_id"] = tenant_id
    return jwt.encode(payload, settings.app_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(settings: JwtSettings, token: str) -> AuthContext:
    try:
        payload = jwt.decode(token, settings.app_secret_key, algorithms=[settings.jwt_algorithm])
        subject = payload.get("sub")
        role_raw = payload.get("role")
        if not subject or not role_raw:
            raise JWTError("Missing claims")
        return AuthContext(
            subject=str(subject),
            role=str(role_raw),
            tenant_id=payload.get("tenant_id"),
        )
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


def parse_uuid(value: str) -> UUID:
    return UUID(value)
