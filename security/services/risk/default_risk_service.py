# security/services/risk/default_risk_service.py
from __future__ import annotations

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.lifecycle import HealthStatus

from security.risk.risk_engine import RiskEngine
from security.risk.risk_provider import RiskProvider
from security.risk.models import RiskRequest

from .risk_service import RiskService
from .risk_mapper import RiskMapper


class DefaultRiskService(RiskService):
    VERSION = "1.0.0"
    NAME = "default_risk"
    DOMAIN = "risk"

    def __init__(
        self,
        risk_engine: RiskEngine,
        risk_provider: RiskProvider,
    ) -> None:
        super().__init__()
        self._risk_engine = risk_engine
        self._risk_provider = risk_provider
        self._mapper = RiskMapper()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def _on_initialize(self) -> None:
        self._risk_engine.initialize()
        self._risk_provider.initialize()

    def _on_validate(self) -> None:
        self._risk_engine.validate()
        self._risk_provider.validate()

    def _on_start(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        self._risk_engine.shutdown()
        self._risk_provider.shutdown()

    def _on_dispose(self) -> None:
        pass

    def _on_health(self) -> HealthStatus:
        statuses = [
            self._risk_engine.health(),
            self._risk_provider.health(),
        ]
        return HealthStatus.HEALTHY if all(statuses) else HealthStatus.UNHEALTHY

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def version(self) -> str:
        return self.VERSION

    @property
    def security_domain(self) -> str:
        return self.DOMAIN

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(self, context: SecurityContext) -> SecurityDecision:
        request = RiskRequest(
            identity=context.identity,
            resource=context.resource,
            operation=context.operation,
            metadata=context.metadata,
        )
        factors = self._risk_provider.get_factors(request)
        risk_result = self._risk_engine.evaluate(factors)
        return self._mapper.to_security_decision(risk_result)

    def assess(self, context: SecurityContext) -> SecurityDecision:
        return self.evaluate(context)
