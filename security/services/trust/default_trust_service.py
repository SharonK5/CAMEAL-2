# security/services/trust/default_trust_service.py
# security/services/trust/default_trust_service.py
from __future__ import annotations

from typing import Any, Optional

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.lifecycle import HealthStatus

from security.trust.trust_engine import TrustEngine
from security.trust.trust_provider import TrustProvider
from security.trust.models import TrustRequest

from .trust_service import TrustService
from .trust_mapper import TrustMapper


class DefaultTrustService(TrustService):
    VERSION = "1.0.0"
    NAME = "default_trust"
    DOMAIN = "trust"

    def __init__(
        self,
        trust_engine: TrustEngine,
        trust_provider: TrustProvider,
    ) -> None:
        super().__init__()
        self._trust_engine = trust_engine
        self._trust_provider = trust_provider
        self._mapper = TrustMapper()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def _on_initialize(self) -> None:
        self._trust_engine.initialize()
        self._trust_provider.initialize()

    def _on_validate(self) -> None:
        self._trust_engine.validate()
        self._trust_provider.validate()

    def _on_start(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        self._trust_engine.shutdown()
        self._trust_provider.shutdown()

    def _on_dispose(self) -> None:
        pass

    def _on_health(self) -> HealthStatus:
        statuses = [
            self._trust_engine.health(),
            self._trust_provider.health(),
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

    def evaluate(
        self,
        context: SecurityContext,
        previous_results: Optional[dict[str, Any]] = None,
    ) -> SecurityDecision:
        """
        Evaluate trust based on the context and optionally aggregated previous results.
        """
        request = TrustRequest(
            identity=context.identity,
            resource=context.resource,
            operation=context.operation,
            metadata=context.metadata,
        )
        # The provider will use previous_results to build signals.
        signals = self._trust_provider.get_signals(request, previous_results=previous_results)
        trust_result = self._trust_engine.evaluate(signals)
        return self._mapper.to_security_decision(trust_result)
