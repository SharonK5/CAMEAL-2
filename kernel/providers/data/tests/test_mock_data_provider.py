# kernel/providers/data/tests/test_mock_data_provider.py
import pytest

from kernel.providers.data.implementations.mock_data_provider import MockDataProvider
from kernel.lifecycle import HealthStatus


class TestMockDataProvider:
    @pytest.fixture
    def provider(self):
        return MockDataProvider()

    def test_initial_state(self, provider):
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_start_stop(self, provider):
        provider.start()
        assert provider.health() == HealthStatus.HEALTHY
        provider.stop()
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_create(self, provider):
        provider.start()
        result = provider.mutate("create", {"id": "1", "name": "test"})
        assert result["success"] is True
        assert result["id"] == "1"

        data = provider.fetch({"id": "1"})
        assert data["id"] == "1"
        assert data["name"] == "test"

        provider.stop()

    def test_update(self, provider):
        provider.start()
        provider.mutate("create", {"id": "1", "name": "test"})
        provider.mutate("update", {"id": "1", "name": "updated"})

        data = provider.fetch({"id": "1"})
        assert data["name"] == "updated"

        provider.stop()

    def test_delete(self, provider):
        provider.start()
        provider.mutate("create", {"id": "1", "name": "test"})
        result = provider.mutate("delete", {"id": "1"})
        assert result["success"] is True

        with pytest.raises(Exception):
            provider.fetch({"id": "1"})

        provider.stop()

    def test_query(self, provider):
        provider.start()
        provider.mutate("create", {"id": "1", "name": "test", "type": "a"})
        provider.mutate("create", {"id": "2", "name": "test2", "type": "b"})
        provider.mutate("create", {"id": "3", "name": "test3", "type": "a"})

        results = provider.query("", variables={"type": "a"})
        assert len(results) == 2
        assert any(r["id"] == "1" for r in results)
        assert any(r["id"] == "3" for r in results)

        provider.stop()
