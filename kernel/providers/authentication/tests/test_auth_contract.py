# kernel/providers/authentication/tests/test_auth_contract.py
"""
Contract tests for authentication providers.
"""

import pytest
from kernel.providers.authentication.auth_provider import AuthProvider
from kernel.providers.authentication.implementations import JWTProvider


class TestAuthContract:
    def test_provider_interface(self):
        provider = JWTProvider(secret="test")
        assert isinstance(provider, AuthProvider)

    def test_required_methods(self):
        provider = JWTProvider(secret="test")
        assert hasattr(provider, "authenticate")
        assert callable(provider.authenticate)
        assert hasattr(provider, "generate_token")
        assert callable(provider.generate_token)
        assert hasattr(provider, "verify_token")
        assert callable(provider.verify_token)
        assert hasattr(provider, "revoke_token")
        assert callable(provider.revoke_token)
        assert hasattr(provider, "authorize")
        assert callable(provider.authorize)
