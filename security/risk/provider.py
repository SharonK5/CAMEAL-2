# security/risk/provider.py
from __future__ import annotations

from abc import ABC
from typing import Any, Dict


class RiskProviderBase(ABC):
    """
    Base class for all Risk providers.

    Provides a uniform lifecycle, metadata, and health contract.
    """

    PROVIDER_NAME = "RiskProvider"
    PROVIDER_VERSION = "1.0.0"

    @property
    def provider_name(self) -> str:
        return self.PROVIDER_NAME

    @property
    def provider_version(self) -> str:
        return self.PROVIDER_VERSION

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
        """Clear any internal caches."""
        pass

    def metadata(self) -> Dict[str, Any]:
        """Return provider metadata."""
        return {
            "provider_name": self.provider_name,
            "provider_version": self.provider_version,
        }
