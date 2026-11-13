import sqlite3
from datetime import UTC, datetime
from uuid import uuid4

from devdocs_ai.auth.database import get_connection
from devdocs_ai.auth.password import hash_password, verify_password


def create_user(email: str, password: str) -> dict:
    email = email.strip().lower()

    if not email:
        raise ValueError("Email cannot be empty.")

    user_id = str(uuid4())
    password_hash = hash_password(password)
    created_at = datetime.now(UTC).isoformat()

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (id, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, email, password_hash, created_at),
            )
    except Exception as exc:
        if isinstance(exc, sqlite3.IntegrityError):
            raise ValueError("An account with this email already exists.") from exc  # noqa: TRY004
        raise

    return {
        "id": user_id,
        "email": email,
        "created_at": created_at,
    }


def get_user_by_email(email: str) -> dict | None:
    email = email.strip().lower()

    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        ).fetchone()

    return dict(row) if row else None


def authenticate_user(email: str, password: str) -> dict | None:
    user = get_user_by_email(email)

    if user is None:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return {
        "id": user["id"],
        "email": user["email"],
        "created_at": user["created_at"],
    }


def get_user_by_id(user_id: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    return dict(row) if row else None
