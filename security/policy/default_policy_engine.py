# security/policy/default_policy_engine.py
from typing import Tuple

from .policy_engine import PolicyEngine
from .models import PolicyRequest, PolicyResult, PolicyDecisionType, PolicyEvidence, Policy


class DefaultPolicyEngine(PolicyEngine):
    ENGINE_NAME = "DefaultPolicyEngine"
    ENGINE_VERSION = "1.0.0"
    _policies: Tuple[Policy, ...] = ()

    def evaluate(self, request: PolicyRequest) -> PolicyResult:
        return PolicyResult(
            decision=PolicyDecisionType.ALLOW,
            confidence=1.0,
            rationale="Policy allowed by default engine.",
            evidence=(
                PolicyEvidence(
                    source=self.ENGINE_NAME,
                    description="Default policy engine always allows.",
                    details={
                        "engine_version": self.ENGINE_VERSION,
                        "request_identity": request.identity,
                        "request_resource": request.resource,
                        "request_operation": request.operation,
                    },
                ),
            ),
        )

    def load(self, policies: Tuple[Policy, ...]) -> None:
        self._policies = policies

    def reload(self) -> None:
        pass

    def list_policies(self) -> Tuple[Policy, ...]:
        return self._policies

    def get_policy(self, policy_id: str) -> Policy:
        for p in self._policies:
            if str(p.policy_id) == policy_id:
                return p
        raise ValueError(f"Policy {policy_id} not found.")

    def clear_cache(self) -> None:
        pass

    def health(self) -> bool:
        return True
