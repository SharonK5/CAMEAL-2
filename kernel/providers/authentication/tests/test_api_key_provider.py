# kernel/providers/authentication/tests/test_api_key_provider.py
import pytest

from kernel.providers.authentication.implementations.api_key_provider import APIKeyProvider
from kernel.lifecycle import HealthStatus


class TestAPIKeyProvider:
    @pytest.fixture
    def provider(self):
        return APIKeyProvider({"key1": "user1", "key2": "user2"})

    def test_initial_state(self, provider):
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_start_stop(self, provider):
        provider.start()
        assert provider.health() == HealthStatus.HEALTHY
        provider.stop()
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_authenticate_valid(self, provider):
        provider.start()
        result = provider.authenticate({"api_key": "key1"})
        assert result["success"] is True
        assert result["user_id"] == "user1"

        provider.stop()

    def test_authenticate_invalid(self, provider):
        provider.start()
        result = provider.authenticate({"api_key": "invalid"})
        assert result["success"] is False

        provider.stop()

    def test_generate_token(self, provider):
        provider.start()
        key = provider.generate_token("newuser")
        assert key is not None
        assert key in provider._valid_keys
        assert provider._valid_keys[key] == "newuser"

        provider.stop()

    def test_revoke_token(self, provider):
        provider.start()
        key = provider.generate_token("user3")
        assert provider.verify_token(key)["valid"] is True

        provider.revoke_token(key)
        result = provider.verify_token(key)
        assert result["valid"] is False

        provider.stop()
