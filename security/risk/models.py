# security/risk/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError


class RiskLevel(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskFactorType(str, Enum):
    IP_REPUTATION = "IP_REPUTATION"
    USER_BEHAVIOR = "USER_BEHAVIOR"
    RESOURCE_SENSITIVITY = "RESOURCE_SENSITIVITY"
    HISTORICAL_PATTERN = "HISTORICAL_PATTERN"
    LOCATION = "LOCATION"
    DEVICE = "DEVICE"
    TIME = "TIME"
    RATE_LIMITING = "RATE_LIMITING"
    ANOMALY = "ANOMALY"
    POLICY = "POLICY"
    AUTHORIZATION = "AUTHORIZATION"
    AUTHENTICATION = "AUTHENTICATION"
    LLM = "LLM"
    RAG = "RAG"
    EVIDENCE = "EVIDENCE"
    TRUST = "TRUST"
    COMPLIANCE = "COMPLIANCE"
    PRIVACY = "PRIVACY"
    GOVERNANCE = "GOVERNANCE"
    CUSTOM = "CUSTOM"


# ------------------------------------------------------------------
# Risk Request
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class RiskRequest:
    identity: str
    resource: str
    operation: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.identity.strip():
            raise SecurityValidationError("Identity cannot be empty.")
        if not self.resource.strip():
            raise SecurityValidationError("Resource cannot be empty.")
        if not self.operation.strip():
            raise SecurityValidationError("Operation cannot be empty.")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "resource": self.resource,
            "operation": self.operation,
            "metadata": dict(self.metadata),
        }


# ------------------------------------------------------------------
# Risk Evidence
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class RiskEvidence:
    source: str
    description: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attributes: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise SecurityValidationError("Evidence source cannot be empty.")
        if not self.description.strip():
            raise SecurityValidationError("Evidence description cannot be empty.")
        if self.timestamp.tzinfo is None:
            raise SecurityValidationError("timestamp must be timezone-aware.")
        object.__setattr__(
            self,
            "attributes",
            MappingProxyType(dict(self.attributes))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "attributes": dict(self.attributes),
        }


# ------------------------------------------------------------------
# Risk Factor (field ordering fixed)
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class RiskFactor:
    name: str
    factor_type: RiskFactorType
    score: float
    factor_id: UUID = field(default_factory=uuid4)
    weight: float = 1.0
    description: Optional[str] = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SecurityValidationError("Risk factor name cannot be empty.")
        if not isinstance(self.factor_type, RiskFactorType):
            raise SecurityValidationError("factor_type must be a RiskFactorType.")
        if not 0.0 <= self.score <= 1.0:
            raise SecurityValidationError("score must be between 0 and 1.")
        if self.weight <= 0:
            raise SecurityValidationError("weight must be positive.")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight

    def to_dict(self) -> dict[str, Any]:
        return {
            "factor_id": str(self.factor_id),
            "name": self.name,
            "factor_type": self.factor_type.value,
            "score": self.score,
            "weight": self.weight,
            "weighted_score": self.weighted_score,
            "description": self.description,
            "metadata": dict(self.metadata),
        }


# ------------------------------------------------------------------
# Risk Result
# ------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class RiskResult:
    overall_score: float
    risk_level: RiskLevel
    request_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    factors: Tuple[RiskFactor, ...] = ()
    rationale: str = ""
    confidence: float = 1.0
    evidence: Tuple[RiskEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.overall_score <= 1.0:
            raise SecurityValidationError("overall_score must be between 0 and 1.")
        if not isinstance(self.risk_level, RiskLevel):
            raise SecurityValidationError("risk_level must be a RiskLevel.")
        if not 0.0 <= self.confidence <= 1.0:
            raise SecurityValidationError("confidence must be between 0 and 1.")
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        rationale = self.rationale.strip()
        object.__setattr__(self, "rationale", rationale)
        object.__setattr__(self, "factors", tuple(self.factors))
        object.__setattr__(self, "evidence", tuple(self.evidence))

        if any(not isinstance(f, RiskFactor) for f in self.factors):
            raise SecurityValidationError("All factors must be RiskFactor instances.")
        if any(not isinstance(e, RiskEvidence) for e in self.evidence):
            raise SecurityValidationError("All evidence items must be RiskEvidence instances.")

    @property
    def is_high_risk(self) -> bool:
        return self.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)

    @property
    def is_acceptable(self) -> bool:
        return self.risk_level in (RiskLevel.NONE, RiskLevel.LOW)

    @property
    def total_weight(self) -> float:
        return sum(f.weight for f in self.factors)

    @property
    def factor_count(self) -> int:
        return len(self.factors)

    @property
    def highest_factor(self) -> Optional[RiskFactor]:
        if not self.factors:
            return None
        return max(self.factors, key=lambda f: f.score)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": str(self.request_id),
            "created_at": self.created_at.isoformat(),
            "overall_score": self.overall_score,
            "risk_level": self.risk_level.value,
            "factors": [f.to_dict() for f in self.factors],
            "rationale": self.rationale,
            "confidence": self.confidence,
            "evidence": [e.to_dict() for e in self.evidence],
            "total_weight": self.total_weight,
            "factor_count": self.factor_count,
        }
