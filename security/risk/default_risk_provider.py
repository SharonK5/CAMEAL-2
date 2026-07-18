# security/risk/default_risk_provider.py
from __future__ import annotations

from typing import Tuple

from .risk_provider import RiskProvider
from .models import RiskFactor, RiskFactorType, RiskRequest


class DefaultRiskProvider(RiskProvider):
    """
    Default development implementation.

    Returns a single low-risk factor for any request.
    """

    PROVIDER_NAME = "DefaultRiskProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_factors(self, request: RiskRequest) -> Tuple[RiskFactor, ...]:
        return (
            RiskFactor(
                name="default_factor",
                factor_type=RiskFactorType.CUSTOM,
                score=0.10,
                weight=1.0,
                description="Default development risk factor.",
                metadata={
                    "identity": request.identity,
                    "resource": request.resource,
                    "operation": request.operation,
                },
            ),
        )
