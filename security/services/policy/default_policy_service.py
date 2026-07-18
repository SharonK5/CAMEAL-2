# security/services/policy/default_policy_service.py
from __future__ import annotations

from typing import Tuple

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.base.lifecycle import HealthStatus

from security.policy.policy_engine import PolicyEngine
from security.policy.policy_provider import PolicyRepositoryProvider
from security.policy.rule_provider import RuleProvider
from security.policy.models import PolicyRequest

from .policy_service import PolicyService
from .policy_mapper import PolicyMapper


class DefaultPolicyService(PolicyService):
    VERSION = "1.0.0"
    NAME = "default_policy"
    DOMAIN = "policy"

    def __init__(
        self,
        policy_engine: PolicyEngine,
        policy_provider: PolicyRepositoryProvider,
        rule_provider: RuleProvider,
    ) -> None:
        super().__init__()
        self._policy_engine = policy_engine
        self._policy_provider = policy_provider
        self._rule_provider = rule_provider
        self._mapper = PolicyMapper()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def _on_initialize(self) -> None:
        self._policy_engine.initialize()
        self._policy_provider.initialize()
        self._rule_provider.initialize()
        self.load_policies()

    def _on_validate(self) -> None:
        self._policy_engine.validate()
        self._policy_provider.validate()
        self._rule_provider.validate()
        self.validate_policies()

    def _on_start(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        self._policy_engine.shutdown()
        self._policy_provider.shutdown()
        self._rule_provider.shutdown()

    def _on_dispose(self) -> None:
        pass

    def _on_health(self) -> HealthStatus:
        statuses = [
            self._policy_engine.health(),
            self._policy_provider.health(),
            self._rule_provider.health(),
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
    # Core evaluation
    # ------------------------------------------------------------------

    def evaluate(self, context: SecurityContext) -> SecurityDecision:
        request = PolicyRequest(
            identity=context.identity,
            resource=context.resource,
            operation=context.operation,
            metadata=context.metadata,
        )
        policy_result = self._policy_engine.evaluate(request)
        return self._mapper.to_security_decision(policy_result)

    # ------------------------------------------------------------------
    # Policy management
    # ------------------------------------------------------------------

    def load_policies(self) -> None:
        self._policy_engine.load(self._policy_provider.get_policies())

    def reload_policies(self) -> None:
        self._policy_engine.reload()

    def validate_policies(self) -> None:
        # Validate each loaded policy
        for policy in self._policy_engine.list_policies():
            # Policy model already validates on construction
            pass

    def list_policies(self) -> tuple[str, ...]:
        return tuple(p.name for p in self._policy_engine.list_policies())

    def clear_cache(self) -> None:
        self._policy_engine.clear_cache()
        self._policy_provider.clear_cache()
        self._rule_provider.clear_cache()
