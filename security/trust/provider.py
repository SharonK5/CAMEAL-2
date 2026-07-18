# security/trust/provider.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from .models import TrustRequest, TrustSignal


class TrustProvider(ABC):
    """
    Base interface for all Trust providers.

    A Trust provider supplies TrustSignal objects for a given request.
    """

    PROVIDER_NAME = "TrustProvider"
    PROVIDER_VERSION = "1.0.0"

    @property
    def provider_name(self) -> str:
        return self.PROVIDER_NAME

    @property
    def provider_version(self) -> str:
        return self.PROVIDER_VERSION

    @abstractmethod
    def get_signals(self, request: TrustRequest) -> Tuple[TrustSignal, ...]:
        """
        Retrieve trust signals for this request.
        """
        raise NotImplementedError

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def validate(self) -> None:
        pass

    def health(self) -> bool:
        return True

    def clear_cache(self) -> None:
        pass

    def metadata(self) -> Dict[str, Any]:
        return {
            "provider_name": self.provider_name,
            "provider_version": self.provider_version,
        }
