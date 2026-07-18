# security/authorization/default_authorizer.py
"""
Default permissive implementation of the Authorizer interface.
"""

from .authorizer import Authorizer
from .models import (
    AuthorizationRequest,
    AuthorizationResult,
    AuthorizationDecisionType,
    AuthorizationEvidence,
    AuthorizationReasonCode,
)
from security.services.base.lifecycle import HealthStatus


class DefaultAuthorizer(Authorizer):
    ENGINE_NAME = "DefaultAuthorizer"
    ENGINE_VERSION = "1.0.0"

    def __init__(self) -> None:
        super().__init__()

    @property
    def engine_name(self) -> str:
        return self.ENGINE_NAME

    @property
    def engine_version(self) -> str:
        return self.ENGINE_VERSION

    def evaluate(self, request: AuthorizationRequest) -> AuthorizationResult:
        return AuthorizationResult(
            decision=AuthorizationDecisionType.ALLOW,
            confidence=1.0,
            rationale="Authorization allowed by the default permissive authorizer.",
            evidence=(
                AuthorizationEvidence(
                    source=self.ENGINE_NAME,
                    description="Default authorizer evaluation – always allows.",
                    attributes={
                        "engine_version": self.ENGINE_VERSION,
                        "reason_code": AuthorizationReasonCode.DEFAULT_ALLOW.value,
                        "policy_evaluated": False,
                        "constraint_evaluated": False,
                        "risk_evaluated": False,
                        "request_identity": request.identity,
                        "request_resource": request.resource,
                        "request_operation": request.operation,
                        "request_id": str(request.request_id),
                        "default_engine": True,
                    },
                ),
            ),
        )

    def health(self) -> HealthStatus:
        return HealthStatus.HEALTHY

    def validate(self) -> None:
        pass
