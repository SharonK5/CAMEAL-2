# security/risk/risk_provider.py
from __future__ import annotations

from abc import abstractmethod
from typing import Tuple

from .provider import RiskProviderBase
from .models import RiskFactor, RiskRequest


class RiskProvider(RiskProviderBase):
    """
    Base interface for all Risk providers.

    Risk providers collect or compute risk factors from one or more
    sources such as:

        • Identity
        • Device
        • Location
        • Historical behaviour
        • Threat intelligence
        • AI anomaly detection
        • Repository metadata
        • Policy violations

    The provider does not perform scoring. It only supplies
    RiskFactor objects to the RiskEngine.
    """

    PROVIDER_NAME = "RiskProvider"
    PROVIDER_VERSION = "1.0.0"

    @abstractmethod
    def get_factors(self, request: RiskRequest) -> Tuple[RiskFactor, ...]:
        """
        Retrieve all risk factors relevant to a request.

        Args:
            request: Risk evaluation request.

        Returns:
            Tuple[RiskFactor, ...]
        """
        raise NotImplementedError
