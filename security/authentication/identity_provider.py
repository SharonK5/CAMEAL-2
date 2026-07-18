from abc import ABC, abstractmethod
from typing import Optional
from security.authentication.models import Identity


class IdentityProvider(ABC):
    @abstractmethod
    def get_identity(self, identity_id: str) -> Optional[Identity]: ...
    @abstractmethod
    def get_identity_by_username(self, username: str) -> Optional[Identity]: ...
    @abstractmethod
    def get_identity_by_system_id(self, system_id: str) -> Optional[Identity]: ...

    def health(self) -> bool:
        return True


class DefaultIdentityProvider(IdentityProvider):
    def __init__(self) -> None:
        self._identities: dict[str, Identity] = {}

    def add_identity(self, identity: Identity) -> None:
        self._identities[identity.username] = identity

    def get_identity(self, identity_id: str) -> Optional[Identity]:
        for ident in self._identities.values():
            if str(ident.identity_id) == identity_id:
                return ident
        return None

    def get_identity_by_username(self, username: str) -> Optional[Identity]:
        return self._identities.get(username)

    def get_identity_by_system_id(self, system_id: str) -> Optional[Identity]:
        for ident in self._identities.values():
            if ident.system_id == system_id:
                return ident
        return None
