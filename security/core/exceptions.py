# security/core/exceptions.py
"""
Core exceptions for the Security subsystem.

These exceptions define the common error hierarchy shared across
all security domain modules and application services.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class SecurityError(Exception):
    """
    Base class for all security-related exceptions.

    Attributes:
        code: Optional machine‑readable error code.
        details: Optional structured context.
    """

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {super().__str__()}"
        return super().__str__()


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------

class SecurityValidationError(SecurityError):
    """Raised when validation of input or configuration fails."""

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        field: Optional[str] = None,
    ) -> None:
        if field:
            message = f"{field}: {message}"
            if code is None:
                code = "VALIDATION_ERROR"
        super().__init__(message, code=code, details=details)


class SecurityConfigurationError(SecurityError):
    """Raised when a security component is incorrectly configured."""

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        component: Optional[str] = None,
    ) -> None:
        if component:
            message = f"{component}: {message}"
            if code is None:
                code = "CONFIGURATION_ERROR"
        super().__init__(message, code=code, details=details)


# ----------------------------------------------------------------------
# Domain
# ----------------------------------------------------------------------

class SecurityDomainError(SecurityError):
    """Raised when a security domain invariant is violated."""


class AuthenticationError(SecurityDomainError):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        identity: Optional[str] = None,
    ) -> None:
        if identity:
            message = f"Identity '{identity}': {message}"
            if code is None:
                code = "AUTHENTICATION_FAILED"
        super().__init__(message, code=code, details=details)


class AuthorizationError(SecurityDomainError):
    """Raised when authorization fails."""

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        resource: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> None:
        if resource and permission:
            message = f"{resource}: {permission} - {message}"
        elif resource:
            message = f"{resource}: {message}"
        elif permission:
            message = f"{permission}: {message}"
        if code is None:
            code = "AUTHORIZATION_FAILED"
        super().__init__(message, code=code, details=details)


class PolicyError(SecurityDomainError):
    """Raised during policy evaluation."""


class RiskEvaluationError(SecurityDomainError):
    """Raised during risk evaluation."""


class TrustEvaluationError(SecurityDomainError):
    """Raised during trust computation."""


class AuditError(SecurityDomainError):
    """Raised during audit operations."""


# ----------------------------------------------------------------------
# Infrastructure
# ----------------------------------------------------------------------

class SecurityInfrastructureError(SecurityError):
    """Raised when an infrastructure component fails."""


class SecurityStorageError(SecurityInfrastructureError):
    """Raised when persistence fails."""


class SecurityCommunicationError(SecurityInfrastructureError):
    """Raised when communication with external systems fails."""
