# kernel/providers/data/implementations/mock_data_provider.py
"""
Mock data provider for testing.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from ..data_provider import DataProvider
from ....lifecycle import HealthStatus
from ...base.exceptions import ProviderError

logger = logging.getLogger(__name__)


class MockDataProvider(DataProvider):
    """
    Mock data provider for testing.

    This provider stores data in memory and is useful for testing
    without external dependencies.
    """

    def __init__(self) -> None:
        self._data = {}
        self._initialized = False

    def get(self) -> Any:
        return self._data

    def start(self) -> None:
        self._data = {}
        self._initialized = True

    def stop(self) -> None:
        self._data = {}
        self._initialized = False

    def health(self) -> HealthStatus:
        if not self._initialized:
            return HealthStatus.UNHEALTHY
        return HealthStatus.HEALTHY

    def fetch(
        self,
        query: Union[str, Dict[str, Any]],
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        if not self._initialized:
            raise ProviderError("Provider not initialized")

        if isinstance(query, dict):
            item_id = query.get("id")
            if item_id:
                if item_id in self._data:
                    return self._data[item_id]
                raise KeyError(f"Item with id '{item_id}' not found")
            return list(self._data.values())
        return list(self._data.values())

    def mutate(
        self,
        operation: str,
        payload: Dict[str, Any],
        **kwargs
    ) -> Any:
        if not self._initialized:
            raise ProviderError("Provider not initialized")

        item_id = payload.get("id")
        if not item_id:
            raise ProviderError("Payload must include 'id' field")

        if operation == "create" or operation == "upsert":
            self._data[item_id] = payload
            return {"success": True, "id": item_id, "operation": operation}

        elif operation == "update":
            if item_id in self._data:
                self._data[item_id].update(payload)
                return {"success": True, "id": item_id, "operation": operation}
            else:
                raise ProviderError(f"Item with id '{item_id}' not found")

        elif operation == "delete":
            if item_id in self._data:
                del self._data[item_id]
                return {"success": True, "id": item_id, "operation": operation}
            else:
                raise ProviderError(f"Item with id '{item_id}' not found")

        else:
            raise ProviderError(f"Unknown operation: {operation}")

    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        if not self._initialized:
            raise ProviderError("Provider not initialized")

        if variables:
            filters = variables
            results = []
            for item in self._data.values():
                matches = True
                for key, value in filters.items():
                    if key in item and item[key] != value:
                        matches = False
                        break
                if matches:
                    results.append(item)
            return results
        return list(self._data.values())

    def execute(
        self,
        statement: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        if not self._initialized:
            raise ProviderError("Provider not initialized")
        return {"success": True, "statement": statement, "params": params}
