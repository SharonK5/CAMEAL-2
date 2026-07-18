from abc import ABC, abstractmethod
from security.authentication.models import Credentials, AuthenticationResult, Identity, IdentityType
from uuid import uuid4
from datetime import datetime, timezone


class Authenticator(ABC):
    @abstractmethod
    def authenticate(self, credentials: Credentials) -> AuthenticationResult:
        pass

    def health(self) -> bool:
        return True


class DefaultAuthenticator(Authenticator):
    """Default stub authenticator for testing."""
    def __init__(self, default_password: str = "password") -> None:
        self._default_password = default_password

    def authenticate(self, credentials: Credentials) -> AuthenticationResult:
        if credentials.credential_type == "PASSWORD":
            if credentials.value and len(credentials.value) >= 3:
                identity = Identity(
                    identity_id=uuid4(),
                    username="testuser",
                    identity_type=IdentityType.USER,
                    email="test@example.com",
                    full_name="Test User",
                    roles=("user",),
                    permissions=("read",),
                    created_at=datetime.now(timezone.utc),
                    enabled=True,
                )
                return AuthenticationResult(
                    success=True,
                    identity=identity,
                    message="Authentication successful (stub).",
                    evidence=({"source": "stub", "detail": "password accepted"},),
                )
            else:
                return AuthenticationResult(
                    success=False,
                    message="Invalid credentials (stub).",
                    error_code="INVALID_CREDENTIALS",
                )
        else:
            identity = Identity(
                identity_id=uuid4(),
                username="system",
                identity_type=IdentityType.SYSTEM,
                created_at=datetime.now(timezone.utc),
            )
            return AuthenticationResult(
                success=True,
                identity=identity,
                message=f"Stub authentication for {credentials.credential_type}.",
            )
