import os
from datetime import UTC, datetime, timedelta

import jwt

ALGORITHM = "HS256"


def get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY")

    if not secret or len(secret) < 32:
        raise RuntimeError(
            "JWT_SECRET_KEY must be configured and at least 32 characters long."
        )

    return secret


def create_access_token(
    user_id: str,
    expires_minutes: int = 30,
) -> str:
    if not user_id:
        raise ValueError("User ID cannot be empty.")

    if expires_minutes <= 0:
        raise ValueError("Token expiration must be positive.")

    now = datetime.now(UTC)

    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }

    return jwt.encode(
        payload,
        get_jwt_secret(),
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        get_jwt_secret(),
        algorithms=[ALGORITHM],
        options={"require": ["sub", "iat", "exp"]},
    )
