# security/services/authentication/default_authentication_service.py
from __future__ import annotations

from typing import Any, Dict, Optional

from security.services.base.security_context import SecurityContext
from security.services.base.security_result import SecurityResult
from security.services.base.lifecycle import HealthStatus

from security.authentication.authenticator import Authenticator
from security.authentication.audit_logger import AuditLogger
from security.authentication.identity_provider import IdentityProvider
from security.authentication.models import Credentials, CredentialType
from security.authentication.session_provider import SessionProvider

from .authentication_service import AuthenticationService


class DefaultAuthenticationService(AuthenticationService):
    """
    Default implementation of the Authentication Service.

    Orchestrates authentication domain components and returns
    standardised SecurityResult objects.
    """

    def __init__(
        self,
        authenticator: Authenticator,
        identity_provider: IdentityProvider,
        session_provider: SessionProvider,
        audit_logger: AuditLogger,
    ) -> None:
        super().__init__()  # Important: initializes BaseService
        self._authenticator = authenticator
        self._identity_provider = identity_provider
        self._session_provider = session_provider
        self._audit_logger = audit_logger

    # ------------------------------------------------------------------
    # Service lifecycle (required by base Service)
    # ------------------------------------------------------------------

    def _on_initialize(self) -> None:
        pass

    def _on_validate(self) -> None:
        pass

    def _on_start(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        pass

    def _on_dispose(self) -> None:
        pass

    def _on_health(self) -> HealthStatus:
        if (self._authenticator.health()
            and self._identity_provider.health()
            and self._session_provider.health()
            and self._audit_logger.health()):
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNHEALTHY

    @property
    def name(self) -> str:
        return "default_authentication"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def security_domain(self) -> str:
        return "authentication"

    # ------------------------------------------------------------------
    # Private orchestration helper
    # ------------------------------------------------------------------

    def _process_authentication(
        self,
        credentials: Credentials,
        method: str,
        audit_details: Optional[Dict[str, Any]] = None,
    ) -> SecurityResult:
        domain_result = self._authenticator.authenticate(credentials)

        identity_id = str(domain_result.identity.identity_id) if domain_result.identity else None
        self._audit_logger.log_authentication(
            identity_id=identity_id,
            success=domain_result.success,
            method=method,
            details=audit_details or {},
        )

        if not domain_result.success:
            return SecurityResult.error(
                message=domain_result.message or "Authentication failed.",
                error_code=domain_result.error_code,
                details={"evidence": [dict(e) for e in domain_result.evidence]},
            )

        session = None
        if self._session_provider.requires_session(credentials):
            if domain_result.identity:
                session = self._session_provider.create_session(domain_result.identity)
            else:
                return SecurityResult.error(
                    message="Authentication succeeded but identity is missing.",
                    error_code="INTERNAL_ERROR",
                )

        return SecurityResult.ok(
            data=domain_result,
            message=domain_result.message,
            details={"session_id": str(session.session_id) if session else None},
        )

    # ------------------------------------------------------------------
    # Public authentication methods
    # ------------------------------------------------------------------

    def authenticate(self, context: SecurityContext) -> SecurityResult:
        cred_type_str = context.metadata.get("credential_type", "password")
        try:
            cred_type = CredentialType(cred_type_str.upper())
        except ValueError:
            cred_type = CredentialType.PASSWORD

        credentials = Credentials(
            credential_type=cred_type,
            value=context.metadata.get("credential_value", ""),
        )
        return self._process_authentication(
            credentials=credentials,
            method="authenticate",
            audit_details={"credential_type": cred_type.value},
        )

    def authenticate_user(self, username: str, credential: str) -> SecurityResult:
        credentials = Credentials(
            credential_type=CredentialType.PASSWORD,
            value=credential,
        )
        return self._process_authentication(
            credentials=credentials,
            method="authenticate_user",
            audit_details={"username": username},
        )

    def authenticate_system(self, system_id: str, secret: str) -> SecurityResult:
        credentials = Credentials(
            credential_type=CredentialType.API_KEY,
            value=secret,
        )
        return self._process_authentication(
            credentials=credentials,
            method="authenticate_system",
            audit_details={"system_id": system_id},
        )

    def authenticate_token(self, token: str) -> SecurityResult:
        credentials = Credentials(
            credential_type=CredentialType.TOKEN,
            value=token,
        )
        return self._process_authentication(
            credentials=credentials,
            method="authenticate_token",
        )

    def authenticate_api_key(self, api_key: str) -> SecurityResult:
        credentials = Credentials(
            credential_type=CredentialType.API_KEY,
            value=api_key,
        )
        return self._process_authentication(
            credentials=credentials,
            method="authenticate_api_key",
        )

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def refresh_session(self, session_id: str) -> SecurityResult:
        session = self._session_provider.refresh_session(session_id)
        if session:
            return SecurityResult.ok(
                data={"session_id": str(session.session_id)},
                message="Session refreshed.",
            )
        else:
            return SecurityResult.error(
                message="Session not found or expired.",
                error_code="SESSION_INVALID",
            )

    def logout(self, session_id: str) -> SecurityResult:
        if self._session_provider.revoke_session(session_id):
            return SecurityResult.ok(message="Session terminated.")
        else:
            return SecurityResult.error(
                message="Session not found.",
                error_code="SESSION_NOT_FOUND",
            )

    # ------------------------------------------------------------------
    # Identity verification
    # ------------------------------------------------------------------

    def verify_identity(self, identity: str) -> SecurityResult:
        found = (
            self._identity_provider.get_identity_by_username(identity)
            or self._identity_provider.get_identity_by_system_id(identity)
        )
        if found:
            return SecurityResult.ok(
                data=found,
                message="Identity verified.",
            )
        else:
            return SecurityResult.error(
                message=f"Identity '{identity}' not found.",
                error_code="IDENTITY_NOT_FOUND",
            )
