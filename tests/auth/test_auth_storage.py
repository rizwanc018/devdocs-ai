from uuid import uuid4

from devdocs_ai.auth.database import initialize_database
from devdocs_ai.auth.users import (
    authenticate_user,
    create_user,
    get_user_by_email,
)


def main():
    initialize_database()

    email = f"auth-test-{uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"

    # Test user creation
    user = create_user(email, password)
    print("Created user:", user)

    # Test retrieving the user
    stored_user = get_user_by_email(email)
    assert stored_user is not None
    assert stored_user["email"] == email

    # Confirm that the password is stored as a hash
    assert stored_user["password_hash"] != password
    print("Password hashing passed!")

    # Test correct password
    authenticated = authenticate_user(email, password)
    assert authenticated is not None
    print("Correct password authentication passed!")

    # Test incorrect password
    authenticated = authenticate_user(email, "WrongPassword123!")
    assert authenticated is None
    print("Incorrect password rejection passed!")

    # Test duplicate email
    try:
        create_user(email, password)
        raise AssertionError("Duplicate email should have been rejected.")
    except ValueError as exc:
        assert "already exists" in str(exc)

    print("Duplicate email rejection passed!")
    print("\nAll authentication storage tests passed!")


if __name__ == "__main__":
    main()
