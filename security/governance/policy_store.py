"""
===============================================================================
Module: security.policy_store
===============================================================================
"""

from __future__ import annotations

from security.identity.permissions import Permission
from .policy import Policy
from security.identity.roles import Role


class PolicyStore:
    """
    Repository of authorization policies.
    """

    def __init__(self) -> None:

        self._policies = {

            Role.SYSTEM_ADMIN:
                Policy(
                    role=Role.SYSTEM_ADMIN,
                    permissions=frozenset(Permission),
                ),

            Role.AI_ADMINISTRATOR:
                Policy(
                    role=Role.AI_ADMINISTRATOR,
                    permissions=frozenset({

                        Permission.READ,
                        Permission.WRITE,
                        Permission.QUERY,
                        Permission.ANALYZE,
                        Permission.CONFIGURE,
                        Permission.REVIEW,

                    }),
                ),

            Role.GOVERNANCE_OFFICER:
                Policy(
                    role=Role.GOVERNANCE_OFFICER,
                    permissions=frozenset({

                        Permission.READ,
                        Permission.WRITE,
                        Permission.REVIEW,
                        Permission.GOVERN,
                        Permission.QUERY,

                    }),
                ),

            Role.RESEARCHER:
                Policy(
                    role=Role.RESEARCHER,
                    permissions=frozenset({

                        Permission.READ,
                        Permission.QUERY,
                        Permission.ANALYZE,
                        Permission.EXPORT,

                    }),
                ),

            Role.ANALYST:
                Policy(
                    role=Role.ANALYST,
                    permissions=frozenset({

                        Permission.READ,
                        Permission.QUERY,
                        Permission.ANALYZE,

                    }),
                ),

            Role.OPERATOR:
                Policy(
                    role=Role.OPERATOR,
                    permissions=frozenset({

                        Permission.READ,
                        Permission.WRITE,
                        Permission.INGEST,

                    }),
                ),

            Role.API_CLIENT:
                Policy(
                    role=Role.API_CLIENT,
                    permissions=frozenset({

                        Permission.READ,
                        Permission.QUERY,

                    }),
                ),

            Role.REVIEWER:
                Policy(
                    role=Role.REVIEWER,
                    permissions=frozenset({

                        Permission.READ,
                        Permission.REVIEW,

                    }),
                ),

            Role.GUEST:
                Policy(
                    role=Role.GUEST,
                    permissions=frozenset({

                        Permission.READ,

                    }),
                ),
        }

    def get(self, role: Role) -> Policy | None:

        return self._policies.get(role)
