# security/trust/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple
from uuid import UUID, uuid4

from security.core.exceptions import SecurityValidationError


class TrustLevel(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    MAXIMUM = "MAXIMUM"


class TrustSignalType(str, Enum):
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    POLICY = "POLICY"
    RISK = "RISK"
    AUDIT = "AUDIT"
    BEHAVIOR = "BEHAVIOR"
    REPUTATION = "REPUTATION"
    HISTORICAL = "HISTORICAL"


@dataclass(frozen=True, slots=True)
class Provenance:
    source_type: str
    source_id: str
    version: str
    authority: Optional[str] = None
    jurisdiction: Optional[str] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    checksum: Optional[str] = None
    generated_at: Optional[datetime] = None
    evidence_uri: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.source_type.strip():
            raise SecurityValidationError("source_type cannot be empty.")
        if not self.source_id.strip():
            raise SecurityValidationError("source_id cannot be empty.")
        if not self.version.strip():
            raise SecurityValidationError("version cannot be empty.")
        if self.generated_at is not None and self.generated_at.tzinfo is None:
            raise SecurityValidationError("generated_at must be timezone-aware.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_type": self.source_type,
            "source_id": self.source_id,
            "version": self.version,
            "authority": self.authority,
            "jurisdiction": self.jurisdiction,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "checksum": self.checksum,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "evidence_uri": self.evidence_uri,
        }


@dataclass(frozen=True, slots=True)
class TrustSignal:
    # Required fields first
    signal_type: TrustSignalType
    score: float              # 0.0 to 1.0
    source: str               # human-readable source name
    provenance: Provenance

    # Optional fields with defaults
    signal_id: UUID = field(default_factory=uuid4)
    weight: float = 1.0
    reliability: float = 1.0  # 0.0 to 1.0
    valid_from: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: Optional[datetime] = None
    description: Optional[str] = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise SecurityValidationError("score must be between 0 and 1.")
        if self.weight <= 0:
            raise SecurityValidationError("weight must be positive.")
        if not 0.0 <= self.reliability <= 1.0:
            raise SecurityValidationError("reliability must be between 0 and 1.")
        if not self.source.strip():
            raise SecurityValidationError("source cannot be empty.")
        if not isinstance(self.signal_type, TrustSignalType):
            raise SecurityValidationError("signal_type must be a TrustSignalType.")
        if not isinstance(self.provenance, Provenance):
            raise SecurityValidationError("provenance must be a Provenance instance.")
        if self.valid_from.tzinfo is None:
            raise SecurityValidationError("valid_from must be timezone-aware.")
        if self.valid_until is not None and self.valid_until.tzinfo is None:
            raise SecurityValidationError("valid_until must be timezone-aware.")
        if self.valid_until is not None and self.valid_until <= self.valid_from:
            raise SecurityValidationError("valid_until must be after valid_from.")
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata))
        )

    @property
    def effective_score(self) -> float:
        if self.is_expired:
            return 0.0
        return self.score * self.weight * self.reliability

    @property
    def is_expired(self) -> bool:
        if self.valid_until is None:
            return False
        return datetime.now(timezone.utc) > self.valid_until

    @property
    def age_seconds(self) -> float:
        return (datetime.now(timezone.utc) - self.valid_from).total_seconds()

    def to_dict(self) -> dict[str, Any]:
        return {
            "signal_id": str(self.signal_id),
            "signal_type": self.signal_type.value,
            "score": self.score,
            "weight": self.weight,
            "reliability": self.reliability,
            "effective_score": self.effective_score,
            "source": self.source,
            "provenance": self.provenance.to_dict(),
            "valid_from": self.valid_from.isoformat(),
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "is_expired": self.is_expired,
            "age_seconds": self.age_seconds,
            "description": self.description,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class TrustRequest:
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


@dataclass(frozen=True, slots=True)
class TrustEvidence:
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


@dataclass(frozen=True, slots=True)
class TrustResult:
    # Required fields first
    overall_score: float
    trust_level: TrustLevel

    # Optional fields with defaults
    request_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    signals: Tuple[TrustSignal, ...] = ()
    rationale: str = ""
    confidence: float = 1.0
    evidence: Tuple[TrustEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.overall_score <= 1.0:
            raise SecurityValidationError("overall_score must be between 0 and 1.")
        if not isinstance(self.trust_level, TrustLevel):
            raise SecurityValidationError("trust_level must be a TrustLevel.")
        if not 0.0 <= self.confidence <= 1.0:
            raise SecurityValidationError("confidence must be between 0 and 1.")
        if self.created_at.tzinfo is None:
            raise SecurityValidationError("created_at must be timezone-aware.")
        rationale = self.rationale.strip()
        object.__setattr__(self, "rationale", rationale)
        object.__setattr__(self, "signals", tuple(self.signals))
        object.__setattr__(self, "evidence", tuple(self.evidence))

        if any(not isinstance(s, TrustSignal) for s in self.signals):
            raise SecurityValidationError("All signals must be TrustSignal instances.")
        if any(not isinstance(e, TrustEvidence) for e in self.evidence):
            raise SecurityValidationError("All evidence items must be TrustEvidence instances.")

    @property
    def is_high_trust(self) -> bool:
        return self.trust_level in (TrustLevel.HIGH, TrustLevel.MAXIMUM)

    @property
    def is_acceptable(self) -> bool:
        return self.trust_level in (TrustLevel.MEDIUM, TrustLevel.HIGH, TrustLevel.MAXIMUM)

    @property
    def total_weight(self) -> float:
        return sum(s.weight for s in self.signals)

    @property
    def total_effective_score(self) -> float:
        return sum(s.effective_score for s in self.signals)

    @property
    def signal_count(self) -> int:
        return len(self.signals)

    @property
    def highest_signal(self) -> Optional[TrustSignal]:
        if not self.signals:
            return None
        return max(self.signals, key=lambda s: s.effective_score)

    @property
    def expired_signals(self) -> Tuple[TrustSignal, ...]:
        return tuple(s for s in self.signals if s.is_expired)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": str(self.request_id),
            "created_at": self.created_at.isoformat(),
            "overall_score": self.overall_score,
            "trust_level": self.trust_level.value,
            "signals": [s.to_dict() for s in self.signals],
            "rationale": self.rationale,
            "confidence": self.confidence,
            "evidence": [e.to_dict() for e in self.evidence],
            "total_weight": self.total_weight,
            "total_effective_score": self.total_effective_score,
            "signal_count": self.signal_count,
            "expired_count": len(self.expired_signals),
        }
