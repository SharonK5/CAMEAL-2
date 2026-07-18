# security/policy/provider.py
from __future__ import annotations

from abc import ABC
from typing import Any, Dict


class PolicyProvider(ABC):
    """
    Base class for all Policy providers.

    Defines the common lifecycle, validation, health,
    metadata, and cache management contract.
    """

    PROVIDER_NAME = "PolicyProvider"
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
        """Clear any provider caches."""
        pass

    def metadata(self) -> Dict[str, Any]:
        return {
            "provider_name": self.provider_name,
            "provider_version": self.provider_version,
        }
