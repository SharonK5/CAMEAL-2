from dataclasses import dataclass
from typing import Optional

from .permissions import Permission
from .user import User


@dataclass(slots=True, frozen=True)
class AuthorizationResult:
    """
    Result of an authorization decision.
    """

    allowed: bool

    user: Optional[User] = None

    permission: Optional[Permission] = None

    message: str = ""
