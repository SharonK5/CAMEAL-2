"""
===============================================================================
Module: security.exceptions

Security exception hierarchy.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations


class SecurityError(Exception):
    """
    Base class for all security-related exceptions.
    """


class AuthenticationError(SecurityError):
    """
    Raised when authentication fails.
    """


class AuthorizationError(SecurityError):
    """
    Raised when authorization fails.
    """


class InvalidCredentialsError(AuthenticationError):
    """
    Username or password is invalid.
    """


class AccountDisabledError(AuthenticationError):
    """
    User account has been disabled.
    """


class SessionExpiredError(AuthenticationError):
    """
    Session has expired.
    """


class PermissionDeniedError(AuthorizationError):
    """
    Required permission is missing.
    """


class InvalidTokenError(AuthenticationError):
    """
    Authentication token is invalid.
    """
