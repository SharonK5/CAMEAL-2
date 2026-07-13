"""
Abstract session provider.
"""

from abc import ABC, abstractmethod

from .session import Session


class SessionProvider(ABC):

    @abstractmethod
    def create(self, session: Session) -> None:
        ...

    @abstractmethod
    def get(self, session_id: str) -> Session | None:
        ...

    @abstractmethod
    def delete(self, session_id: str) -> None:
        ...

    @abstractmethod
    def exists(self, session_id: str) -> bool:
        ...
