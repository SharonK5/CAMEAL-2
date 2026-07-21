# kernel/providers/authentication/__init__.py
"""
Authentication provider package.

Provides interfaces and implementations for authentication and authorization.
"""

from .auth_provider import AuthProvider

__all__ = ["AuthProvider"]
