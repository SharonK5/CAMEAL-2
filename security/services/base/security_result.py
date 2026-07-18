# security/services/base/security_result.py
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Optional, Dict
from uuid import uuid4

from .exceptions import ServiceValidationError


@dataclass(frozen=True, slots=True)
class SecurityResult:
    success: bool
    message: str

    data: Optional[Any] = None
    error_code: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    result_id: str = field(default_factory=lambda: str(uuid4()))

    details: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.message.strip():
            raise ServiceValidationError("message cannot be empty.")
        if self.timestamp.tzinfo is None:
            raise ServiceValidationError("timestamp must be timezone-aware.")
        if not isinstance(self.details, Mapping):
            raise ServiceValidationError("details must be a Mapping.")

        object.__setattr__(
            self,
            "details",
            MappingProxyType(dict(self.details))
        )

    def __hash__(self) -> int:
        return hash((
            self.success,
            self.message,
            self.error_code,
            self.timestamp,
            self.result_id,
        ))

    @classmethod
    def ok(
        cls,
        data: Any = None,
        message: str = "Success",
        details: Optional[Mapping[str, Any]] = None,
    ) -> "SecurityResult":
        return cls(success=True, message=message, data=data, details=details or {})

    @classmethod
    def error(
        cls,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Mapping[str, Any]] = None,
        data: Any = None,
    ) -> "SecurityResult":
        return cls(
            success=False,
            message=message,
            error_code=error_code,
            details=details or {},
            data=data,
        )

    @property
    def failed(self) -> bool:
        return not self.success

    def with_updates(self, **changes) -> "SecurityResult":
        return replace(self, **changes)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error_code": self.error_code,
            "details": dict(self.details),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecurityResult":
        required = {"success", "message"}
        missing = required - set(data.keys())
        if missing:
            raise ServiceValidationError(f"Missing required fields: {', '.join(sorted(missing))}")

        success = data["success"]
        if not isinstance(success, bool):
            raise ServiceValidationError("success must be a boolean.")

        timestamp = None
        if "timestamp" in data and data["timestamp"] is not None:
            try:
                dt = datetime.fromisoformat(data["timestamp"])
                if dt.tzinfo is None:
                    raise ServiceValidationError("timestamp must be timezone-aware.")
                timestamp = dt
            except ValueError as e:
                raise ServiceValidationError(f"Invalid timestamp: {data['timestamp']!r}") from e

        return cls(
            success=success,
            message=data["message"],
            data=data.get("data"),
            error_code=data.get("error_code"),
            details=data.get("details", {}),
            timestamp=timestamp or datetime.now(timezone.utc),
            result_id=data.get("result_id", str(uuid4())),
        )

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:
        status = "OK" if self.success else "ERROR"
        return f"SecurityResult({status}, message={self.message!r})"

    def __str__(self) -> str:
        return f"SecurityResult({self.message})"
