# security/audit/audit_provider.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from .models import AuditEvent, AuditRequest, AuditResult


class AuditProvider(ABC):
    """
    Base interface for audit providers.

    Audit providers are responsible for persisting or forwarding audit
    events to a storage backend (database, file system, SIEM, message bus,
    cloud logging service, etc.).

    They expose a uniform lifecycle and health interface so they can be
    managed consistently by the CAMEAL Service Framework.
    """

    PROVIDER_NAME = "AuditProvider"
    PROVIDER_VERSION = "1.0.0"

    @property
    def provider_name(self) -> str:
        return self.PROVIDER_NAME

    @property
    def provider_version(self) -> str:
        return self.PROVIDER_VERSION

    @abstractmethod
    def record(self, request: AuditRequest, event: AuditEvent) -> AuditResult:
        """
        Persist an audit event.

        Args:
            request: Original audit request.
            event: Fully constructed audit event.

        Returns:
            AuditResult describing the persistence outcome.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """Initialize provider resources."""
        pass

    def shutdown(self) -> None:
        """Release provider resources."""
        pass

    def validate(self) -> None:
        """Validate provider configuration."""
        pass

    def health(self) -> bool:
        """Return provider health."""
        return True

    def clear_cache(self) -> None:
        """Clear any provider caches."""
        pass

    def metadata(self) -> Dict[str, Any]:
        """Return provider metadata for diagnostics."""
        return {
            "provider_name": self.provider_name,
            "provider_version": self.provider_version,
        }
