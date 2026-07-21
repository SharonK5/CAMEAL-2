# kernel/providers/authentication/tests/test_jwt_provider.py
import pytest
import time

from kernel.providers.authentication.implementations.jwt_provider import JWTProvider
from kernel.lifecycle import HealthStatus

# 32-byte secret to avoid InsecureKeyLengthWarning
TEST_SECRET = "cameal-test-secret-32-bytes-long!!"


class TestJWTProvider:
    @pytest.fixture
    def provider(self):
        return JWTProvider(secret=TEST_SECRET, algorithm="HS256")

    def test_initial_state(self, provider):
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_start_stop(self, provider):
        provider.start()
        assert provider.health() == HealthStatus.HEALTHY
        provider.stop()
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_generate_and_verify(self, provider):
        provider.start()
        token = provider.generate_token("user123", {"role": "admin"})
        assert isinstance(token, str)
        assert len(token) > 0

        payload = provider.verify_token(token)
        assert payload["valid"] is True
        assert payload["user_id"] == "user123"
        assert "role" in payload["payload"]
        assert payload["payload"]["role"] == "admin"

        provider.stop()

    def test_verify_expired(self, provider):
        provider.start()
        provider._expiration_minutes = 1 / 60  # 1 second
        token = provider.generate_token("user123")
        time.sleep(2)

        result = provider.verify_token(token)
        assert result["valid"] is False
        assert "expired" in result["error"]

        provider.stop()

    def test_authenticate_with_password(self, provider):
        provider.start()
        result = provider.authenticate({"username": "testuser", "password": "pass"})
        assert result["success"] is True
        assert result["user_id"] == "testuser"

        result = provider.authenticate({"username": "", "password": ""})
        assert result["success"] is False

        provider.stop()

    def test_revoke_token(self, provider):
        provider.start()
        token = provider.generate_token("user123")
        assert provider.verify_token(token)["valid"] is True

        provider.revoke_token(token)
        result = provider.verify_token(token)
        assert result["valid"] is False
        assert "revoked" in result["error"]

        provider.stop()
