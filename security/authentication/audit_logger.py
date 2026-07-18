from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class AuditLogger(ABC):
    @abstractmethod
    def log_authentication(
        self,
        identity_id: Optional[str],
        success: bool,
        method: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        pass

    def health(self) -> bool:
        return True


class DefaultAuditLogger(AuditLogger):
    def log_authentication(
        self,
        identity_id: Optional[str],
        success: bool,
        method: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        # Stub: print to stdout for testing; in production, would write to a real audit store.
        print(f"[AUDIT] identity={identity_id or 'anonymous'} success={success} method={method} details={details}")
