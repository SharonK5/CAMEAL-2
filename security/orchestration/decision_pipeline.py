# security/orchestration/decision_pipeline.py
from __future__ import annotations

import time
from typing import Dict, Optional, Any
from datetime import datetime, timezone
from uuid import uuid4  # ADDED

from security.services.base.security_context import SecurityContext
from security.services.base.security_decision import SecurityDecision
from security.services.authentication.authentication_service import AuthenticationService
from security.services.authorization.authorization_service import AuthorizationService
from security.services.policy.policy_service import PolicyService
from security.services.risk.risk_service import RiskService
from security.services.audit.audit_service import AuditService
from security.services.trust.trust_service import TrustService

from .models import (
    OrchestrationContext,
    ServiceResult,
    OrchestrationResult,
    Provenance,
    EvidenceBundle,
)
from .decision_fusion import DecisionFusion
from .recommendation_engine import RecommendationEngine


class DecisionPipeline:
    """
    Orchestrates the full security decision pipeline.
    """

    def __init__(
        self,
        authentication_service: AuthenticationService,
        authorization_service: AuthorizationService,
        policy_service: PolicyService,
        risk_service: RiskService,
        audit_service: AuditService,
        trust_service: TrustService,
        service_versions: Dict[str, str] = None,
        engine_names: Dict[str, str] = None,
        engine_versions: Dict[str, str] = None,
        fusion_engine: Optional[DecisionFusion] = None,
        recommendation_engine: Optional[RecommendationEngine] = None,
    ) -> None:
        self._services = {
            "authentication": authentication_service,
            "authorization": authorization_service,
            "policy": policy_service,
            "risk": risk_service,
            "audit": audit_service,
            "trust": trust_service,
        }
        self._service_versions = service_versions or {}
        self._engine_names = engine_names or {}
        self._engine_versions = engine_versions or {}
        self._fusion = fusion_engine or DecisionFusion()
        self._recommendation = recommendation_engine or RecommendationEngine()

    def _get_provenance(self, name: str) -> Provenance:
        service = self._services[name]
        return Provenance(
            service_name=name,
            service_version=self._service_versions.get(name, "1.0.0"),
            engine_name=self._engine_names.get(name, getattr(service, "name", "unknown")),
            engine_version=self._engine_versions.get(name, getattr(service, "version", "1.0.0")),
        )

    def _run_service(self, name: str, context: SecurityContext, orch_ctx: OrchestrationContext) -> ServiceResult:
        start = time.perf_counter()
        try:
            if name == "authentication":
                decision = self._services[name].authenticate(context)
            elif name == "authorization":
                decision = self._services[name].authorize(context)
            elif name == "policy":
                decision = self._services[name].evaluate(context)
            elif name == "risk":
                decision = self._services[name].evaluate(context)
            elif name == "audit":
                decision = self._services[name].log_event(context)
            elif name == "trust":
                # Build aggregated inputs for trust
                inputs = self._build_trust_inputs(orch_ctx)
                decision = self._services[name].evaluate(context, previous_results=inputs)
            else:
                raise ValueError(f"Unknown service: {name}")
        except Exception as e:
            decision = SecurityDecision.deny(f"{name} failed", confidence=0.0)
            return ServiceResult(
                provenance=self._get_provenance(name),
                decision=decision,
                execution_time_ms=int((time.perf_counter() - start) * 1000),
                error=str(e),
            )

        return ServiceResult(
            provenance=self._get_provenance(name),
            decision=decision,
            execution_time_ms=int((time.perf_counter() - start) * 1000),
        )

    def _build_trust_inputs(self, ctx: OrchestrationContext) -> Dict[str, Any]:
        inputs = {}
        for name, result in ctx.service_results.items():
            if name != "trust":
                inputs[name] = {
                    "decision": result.decision.decision.value,
                    "confidence": result.decision.confidence,
                    "rationale": result.decision.rationale,
                }
        return inputs

    def execute(self, context: SecurityContext, correlation_id: Optional[str] = None) -> OrchestrationResult:
        orch_ctx = OrchestrationContext(
            identity=context.identity,
            resource=context.resource,
            operation=context.operation,
            metadata=context.metadata,
            correlation_id=correlation_id or str(uuid4()),  # FIXED: uuid4 now imported
        )

        decision_trace = []

        # Run each service in order
        for name in ["authentication", "authorization", "policy", "risk", "audit", "trust"]:
            result = self._run_service(name, context, orch_ctx)
            orch_ctx = orch_ctx.add_service_result(name, result)
            decision_trace.append(f"{name.capitalize()}: {result.decision.decision.value} (conf={result.decision.confidence:.2f})")

        # Fusion
        final, escalation_reasons, confidence = self._fusion.fuse(orch_ctx)
        decision_trace.append(f"Fusion: {final.value} (conf={confidence:.2f})")

        # Recommendations
        recommendations = self._recommendation.generate(orch_ctx, final, escalation_reasons)

        # Build evidence bundle
        evidence_bundle = EvidenceBundle(
            service_results=orch_ctx.service_results,
            provenance={name: result.provenance for name, result in orch_ctx.service_results.items()},
            timestamps={name: datetime.now(timezone.utc) for name in orch_ctx.service_results.keys()},
            overall_confidence=confidence,
        )

        return OrchestrationResult(
            decision=final,
            confidence=confidence,
            rationale=f"Final decision: {final.value}. {', '.join([r.value for r in escalation_reasons])}" if escalation_reasons else f"Final decision: {final.value}.",
            request_id=orch_ctx.request_id,
            created_at=datetime.now(timezone.utc),
            correlation_id=orch_ctx.correlation_id,
            evidence_bundle=evidence_bundle,
            decision_trace=tuple(decision_trace),
            escalation_reasons=escalation_reasons,
        )
