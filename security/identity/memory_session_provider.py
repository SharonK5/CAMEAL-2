from .session import Session
from .session_provider import SessionProvider


class MemorySessionProvider(SessionProvider):

    def __init__(self):

        self._sessions: dict[str, Session] = {}

    def create(self, session: Session) -> None:

        self._sessions[session.session_id] = session

    def get(self, session_id: str) -> Session | None:

        return self._sessions.get(session_id)

    def delete(self, session_id: str) -> None:

        self._sessions.pop(session_id, None)

    def exists(self, session_id: str) -> bool:

        return session_id in self._sessions
