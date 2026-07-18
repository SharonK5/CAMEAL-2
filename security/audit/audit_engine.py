# security/audit/audit_engine.py
from abc import ABC, abstractmethod

from .models import AuditEvent, AuditRequest


class AuditEngine(ABC):
    @abstractmethod
    def build_event(self, request: AuditRequest) -> AuditEvent:
        """
        Build an audit event from a request.
        """
        pass

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def validate(self) -> None:
        pass

    def health(self) -> bool:
        return True
