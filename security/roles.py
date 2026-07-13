"""
System roles.
"""

from enum import Enum


class Role(str, Enum):
    """
    Built-in system roles.
    """

    SYSTEM_ADMIN = "system_admin"

    AI_ADMINISTRATOR = "ai_administrator"

    GOVERNANCE_OFFICER = "governance_officer"

    REVIEWER = "reviewer"

    RESEARCHER = "researcher"

    ANALYST = "analyst"

    OPERATOR = "operator"

    API_CLIENT = "api_client"

    GUEST = "guest"
