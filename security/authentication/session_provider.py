from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from security.authentication.models import Identity, Session, Credentials


class SessionProvider(ABC):
    @abstractmethod
    def requires_session(self, credentials: Credentials) -> bool:
        pass

    @abstractmethod
    def create_session(self, identity: Identity, ttl_seconds: int = 3600) -> Session:
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Session]:
        pass

    @abstractmethod
    def refresh_session(self, session_id: str) -> Optional[Session]:
        pass

    @abstractmethod
    def revoke_session(self, session_id: str) -> bool:
        pass

    def health(self) -> bool:
        return True


class DefaultSessionProvider(SessionProvider):
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def requires_session(self, credentials: Credentials) -> bool:
        # By default, all credentials require a session, but this can be overridden.
        # For simplicity, always return True.
        return True

    def create_session(self, identity: Identity, ttl_seconds: int = 3600) -> Session:
        now = datetime.now(timezone.utc)
        session = Session(
            session_id=uuid4(),
            identity_id=identity.identity_id,
            expires_at=now + timedelta(seconds=ttl_seconds),
            created_at=now,
            last_activity=now,
        )
        self._sessions[str(session.session_id)] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def refresh_session(self, session_id: str) -> Optional[Session]:
        session = self._sessions.get(session_id)
        if session and not session.is_revoked and not session.is_expired():
            # Create a new session with extended expiry
            now = datetime.now(timezone.utc)
            new_session = Session(
                session_id=session.session_id,
                identity_id=session.identity_id,
                expires_at=now + timedelta(seconds=3600),
                created_at=session.created_at,
                last_activity=now,
                ip_address=session.ip_address,
                user_agent=session.user_agent,
                is_revoked=False,
                metadata=session.metadata,
            )
            self._sessions[str(session.session_id)] = new_session
            return new_session
        return None

    def revoke_session(self, session_id: str) -> bool:
        session = self._sessions.get(session_id)
        if session:
            new_session = Session(
                session_id=session.session_id,
                identity_id=session.identity_id,
                expires_at=session.expires_at,
                created_at=session.created_at,
                last_activity=session.last_activity,
                ip_address=session.ip_address,
                user_agent=session.user_agent,
                is_revoked=True,
                metadata=session.metadata,
            )
            self._sessions[str(session.session_id)] = new_session
            return True
        return False
