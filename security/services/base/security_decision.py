# security/services/base/security_decision.py
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Optional, Tuple, Dict, List
from uuid import UUID, uuid4

from .exceptions import ServiceValidationError


class DecisionType(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    ABSTAIN = "ABSTAIN"


@dataclass(frozen=True, slots=True)
class Evidence:
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    evidence_id: UUID = field(default_factory=uuid4)

    data: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ServiceValidationError("evidence source cannot be empty.")
        if self.timestamp.tzinfo is None:
            raise ServiceValidationError("timestamp must be timezone-aware.")
        if not isinstance(self.data, Mapping):
            raise ServiceValidationError("evidence data must be a Mapping.")

        object.__setattr__(
            self,
            "data",
            MappingProxyType(dict(self.data))
        )

    def __hash__(self) -> int:
        # Exclude evidence_id from hash (content-based)
        return hash((self.source, self.timestamp, tuple(self.data.items())))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "data": dict(self.data),
            "timestamp": self.timestamp.isoformat(),
            "evidence_id": str(self.evidence_id),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Evidence":
        try:
            timestamp = datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None
            if timestamp is not None and timestamp.tzinfo is None:
                raise ServiceValidationError("timestamp must be timezone-aware.")
            evidence_id = UUID(data["evidence_id"]) if "evidence_id" in data else None
        except (ValueError, KeyError) as e:
            raise ServiceValidationError(f"Invalid evidence data: {e}") from e

        return cls(
            source=data["source"],
            data=data.get("data", {}),
            timestamp=timestamp or datetime.now(timezone.utc),
            evidence_id=evidence_id or uuid4(),
        )

    def __repr__(self) -> str:
        return f"Evidence(source={self.source!r}, evidence_id={self.evidence_id!r})"


@dataclass(frozen=True, slots=True)
class SecurityDecision:
    decision: DecisionType
    confidence: float
    rationale: str

    decision_source: Optional[str] = None
    evidence: Tuple[Evidence, ...] = ()
    recommendations: Tuple[str, ...] = ()
    applied_policies: Tuple[str, ...] = ()
    applied_rules: Tuple[str, ...] = ()
    execution_time_ms: Optional[int] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    decision_id: UUID = field(default_factory=uuid4)

    audit_metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ServiceValidationError("confidence must be between 0 and 1.")
        if not self.rationale.strip():
            raise ServiceValidationError("rationale cannot be empty.")
        if self.decision in (DecisionType.ALLOW, DecisionType.DENY) and not self.evidence:
            raise ServiceValidationError("evidence must be provided for ALLOW or DENY decisions.")
        if not isinstance(self.evidence, tuple):
            raise ServiceValidationError("evidence must be a tuple.")
        if not isinstance(self.recommendations, tuple):
            raise ServiceValidationError("recommendations must be a tuple.")
        if not isinstance(self.applied_policies, tuple):
            raise ServiceValidationError("applied_policies must be a tuple.")
        if not isinstance(self.applied_rules, tuple):
            raise ServiceValidationError("applied_rules must be a tuple.")
        if self.created_at.tzinfo is None:
            raise ServiceValidationError("created_at must be timezone-aware.")
        if not isinstance(self.audit_metadata, Mapping):
            raise ServiceValidationError("audit_metadata must be a Mapping.")

        if any(not isinstance(e, Evidence) for e in self.evidence):
            raise ServiceValidationError("all evidence items must be Evidence instances.")
        if any(not isinstance(r, str) for r in self.recommendations):
            raise ServiceValidationError("recommendations must contain strings.")
        if any(not isinstance(p, str) for p in self.applied_policies):
            raise ServiceValidationError("applied_policies must contain strings.")
        if any(not isinstance(r, str) for r in self.applied_rules):
            raise ServiceValidationError("applied_rules must contain strings.")

        object.__setattr__(
            self,
            "audit_metadata",
            MappingProxyType(dict(self.audit_metadata))
        )

    def __hash__(self) -> int:
        # Exclude decision_id and audit_metadata; include evidence (which now has consistent hash)
        return hash((
            self.decision,
            self.confidence,
            self.rationale,
            self.decision_source,
            self.evidence,
            self.recommendations,
            self.applied_policies,
            self.applied_rules,
            self.execution_time_ms,
            self.created_at,
        ))

    @property
    def is_allowed(self) -> bool:
        return self.decision == DecisionType.ALLOW

    @property
    def is_denied(self) -> bool:
        return self.decision == DecisionType.DENY

    @property
    def is_abstained(self) -> bool:
        return self.decision == DecisionType.ABSTAIN

    @property
    def confidence_level(self) -> str:
        if self.confidence == 0.0:
            return "NONE"
        if self.confidence <= 0.25:
            return "LOW"
        if self.confidence <= 0.50:
            return "MEDIUM"
        if self.confidence <= 0.75:
            return "HIGH"
        if self.confidence < 1.0:
            return "VERY_HIGH"
        return "MAXIMUM"

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)

    @property
    def has_recommendations(self) -> bool:
        return bool(self.recommendations)

    @property
    def evidence_sources(self) -> set[str]:
        return {e.source for e in self.evidence}

    def with_updates(self, **changes) -> "SecurityDecision":
        return replace(self, **changes)

    def add_evidence(self, evidence: Evidence) -> "SecurityDecision":
        if not isinstance(evidence, Evidence):
            raise ServiceValidationError("evidence must be an Evidence instance.")
        return self.with_updates(
            evidence=self.evidence + (evidence,)
        )

    def add_recommendation(self, recommendation: str) -> "SecurityDecision":
        if not isinstance(recommendation, str) or not recommendation.strip():
            raise ServiceValidationError("recommendation must be a non-empty string.")
        return self.with_updates(
            recommendations=self.recommendations + (recommendation,)
        )

    def to_dict(self) -> Dict[str, Any]:
        sorted_evidence = sorted(self.evidence, key=lambda e: e.source)
        return {
            "decision_id": str(self.decision_id),
            "decision": self.decision.value,
            "confidence": self.confidence,
            "confidence_level": self.confidence_level,
            "rationale": self.rationale,
            "decision_source": self.decision_source,
            "evidence": [e.to_dict() for e in sorted_evidence],
            "recommendations": sorted(self.recommendations),
            "applied_policies": list(self.applied_policies),
            "applied_rules": list(self.applied_rules),
            "execution_time_ms": self.execution_time_ms,
            "audit_metadata": dict(self.audit_metadata),
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecurityDecision":
        required = {"decision", "confidence", "rationale"}
        missing = required - set(data.keys())
        if missing:
            raise ServiceValidationError(f"Missing required fields: {', '.join(sorted(missing))}")

        try:
            decision = DecisionType(data["decision"])
        except (KeyError, ValueError) as e:
            raise ServiceValidationError(f"Invalid decision: {data.get('decision')!r}") from e

        confidence = data["confidence"]
        if not isinstance(confidence, (int, float)) or not (0.0 <= confidence <= 1.0):
            raise ServiceValidationError("confidence must be a number between 0 and 1.")

        created_at = None
        if "created_at" in data and data["created_at"] is not None:
            try:
                dt = datetime.fromisoformat(data["created_at"])
                if dt.tzinfo is None:
                    raise ServiceValidationError("created_at must be timezone-aware.")
                created_at = dt
            except ValueError as e:
                raise ServiceValidationError(f"Invalid created_at: {data['created_at']!r}") from e

        decision_id = None
        if "decision_id" in data and data["decision_id"] is not None:
            try:
                decision_id = UUID(data["decision_id"])
            except ValueError as e:
                raise ServiceValidationError(f"Invalid decision_id: {data['decision_id']!r}") from e

        evidence_list: List[Evidence] = []
        evidence_data = data.get("evidence", [])
        if not isinstance(evidence_data, list):
            raise ServiceValidationError("evidence must be a list of dicts.")
        for item in evidence_data:
            if not isinstance(item, dict):
                raise ServiceValidationError("each evidence item must be a dict.")
            evidence_list.append(Evidence.from_dict(item))

        return cls(
            decision=decision,
            confidence=confidence,
            rationale=data["rationale"],
            decision_source=data.get("decision_source"),
            evidence=tuple(evidence_list),
            recommendations=tuple(data.get("recommendations", [])),
            applied_policies=tuple(data.get("applied_policies", [])),
            applied_rules=tuple(data.get("applied_rules", [])),
            execution_time_ms=data.get("execution_time_ms"),
            audit_metadata=data.get("audit_metadata", {}),
            created_at=created_at or datetime.now(timezone.utc),
            decision_id=decision_id or uuid4(),
        )

    def __repr__(self) -> str:
        return (
            f"SecurityDecision(decision={self.decision.value}, "
            f"confidence={self.confidence:.2f}, "
            f"evidence_count={len(self.evidence)})"
        )

    def __str__(self) -> str:
        return (
            f"SecurityDecision({self.decision.value}, "
            f"conf={self.confidence:.2f}, {self.rationale[:50]}...)"
        )
