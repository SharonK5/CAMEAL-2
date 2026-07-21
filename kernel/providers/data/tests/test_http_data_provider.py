# kernel/providers/data/tests/test_http_data_provider.py
import pytest
from unittest.mock import Mock, patch
import requests  # <-- add this

from kernel.providers.data.implementations.http_data_provider import HTTPDataProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderError


class TestHTTPDataProvider:
    @pytest.fixture
    def provider(self):
        return HTTPDataProvider(
            base_url="https://api.example.com",
            timeout=5,
        )

    def test_initial_state(self, provider):
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_start_stop(self, provider):
        provider.start()
        assert provider._initialized is True
        provider.stop()
        assert provider._initialized is False
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_fetch_success(self, provider):
        provider.start()
        with patch.object(provider._session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": "test"}
            mock_response.headers = {"content-type": "application/json"}
            mock_get.return_value = mock_response

            result = provider.fetch("/test")
            assert result == {"data": "test"}
            mock_get.assert_called_once()
        provider.stop()

    def test_mutate_success(self, provider):
        provider.start()
        with patch.object(provider._session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"success": True}
            mock_response.headers = {"content-type": "application/json"}
            mock_request.return_value = mock_response

            result = provider.mutate(
                "create",
                {"id": "1", "name": "test"},
                endpoint="/items"
            )
            assert result == {"success": True}
            mock_request.assert_called_once()
        provider.stop()

    def test_fetch_failure(self, provider):
        provider.start()
        with patch.object(provider._session, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
            with pytest.raises(ProviderError):
                provider.fetch("/test")
        provider.stop()
