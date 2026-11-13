from devdocs_ai.auth.token import (
    create_access_token,
    decode_access_token,
)

user_id = "test-user-123"

# Create token
token = create_access_token(user_id)
print("JWT created!")

# Decode and verify token
payload = decode_access_token(token)

assert payload["sub"] == user_id
assert "iat" in payload
assert "exp" in payload

print("JWT verification passed!")
print("User ID:", payload["sub"])

# Test tampered token
tampered_token = token[:-5] + "abcde"

try:
    decode_access_token(tampered_token)
    raise AssertionError("Tampered token should be rejected.")
except Exception as exc:  # noqa: BLE001
    import jwt

    assert isinstance(exc, jwt.InvalidTokenError)

print("Tampered token rejection passed!")

print("\nAll JWT tests passed!")
