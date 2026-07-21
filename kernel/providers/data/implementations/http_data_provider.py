import logging
# kernel/providers/data/implementations/http_data_provider.py
"""
HTTP/REST API data provider.

Provides access to HTTP-based data sources (REST APIs, etc.).
"""

import json
import requests
from typing import Any, Dict, List, Optional, Union

from ..data_provider import DataProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError

logger = logging.getLogger(__name__)


class HTTPDataProvider(DataProvider):
    """
    HTTP/REST API data provider.

    This provider abstracts HTTP-based data access:
        - REST APIs
        - JSON APIs
        - Custom HTTP endpoints

    Features:
        - Configurable base URL
        - Authentication (API key, Bearer token, Basic auth)
        - Headers and timeout configuration
        - Retry logic (optional)

    Usage:
        provider = HTTPDataProvider(
            base_url="https://api.example.com",
            auth_type="bearer",
            auth_token="my-token"
        )
        provider.start()
        data = provider.fetch("/users", params={"page": 1})
        provider.stop()
    """

    def __init__(
        self,
        base_url: str,
        auth_type: str = "none",
        auth_token: Optional[str] = None,
        auth_username: Optional[str] = None,
        auth_password: Optional[str] = None,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the HTTP data provider.

        Args:
            base_url: The base URL for all requests.
            auth_type: Authentication type ("none", "bearer", "basic", "api_key").
            auth_token: Token for bearer authentication.
            auth_username: Username for basic authentication.
            auth_password: Password for basic authentication.
            default_headers: Headers to include with every request.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries.
        """
        self._base_url = base_url.rstrip("/")
        self._auth_type = auth_type
        self._auth_token = auth_token
        self._auth_username = auth_username
        self._auth_password = auth_password
        self._default_headers = default_headers or {}
        self._timeout = timeout
        self._max_retries = max_retries
        self._session = None
        self._initialized = False

    def get(self) -> Any:
        """Return the underlying requests Session."""
        return self._session

    def start(self) -> None:
        """
        Initialize the HTTP session.

        Raises:
            ProviderInitializationError: If initialization fails.
        """
        try:
            self._session = requests.Session()
            self._session.headers.update(self._default_headers)

            # Configure authentication
            if self._auth_type == "bearer" and self._auth_token:
                self._session.headers.update({
                    "Authorization": f"Bearer {self._auth_token}"
                })
            elif self._auth_type == "basic" and self._auth_username and self._auth_password:
                self._session.auth = (self._auth_username, self._auth_password)
            elif self._auth_type == "api_key" and self._auth_token:
                self._session.headers.update({
                    "X-API-Key": self._auth_token
                })

            self._initialized = True
            logger.info(f"HTTP data provider initialized for {self._base_url}")
        except Exception as e:
            raise ProviderInitializationError(f"Failed to initialize HTTP provider: {e}") from e

    def stop(self) -> None:
        """Close the HTTP session."""
        if self._session:
            self._session.close()
        self._session = None
        self._initialized = False

    def health(self) -> HealthStatus:
        """
        Check health by making a lightweight request.

        Returns:
            HealthStatus.HEALTHY if the base URL is reachable.
        """
        if not self._initialized or self._session is None:
            return HealthStatus.UNHEALTHY

        try:
            response = self._session.head(self._base_url, timeout=5)
            if response.status_code < 500:
                return HealthStatus.HEALTHY
            return HealthStatus.DEGRADED
        except requests.exceptions.RequestException:
            return HealthStatus.UNHEALTHY

    def fetch(
        self,
        query: Union[str, Dict[str, Any]],
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """
        Fetch data via HTTP GET.

        Args:
            query: The endpoint path or a dict with endpoint and parameters.
            params: Query parameters.
            **kwargs: Additional arguments (headers, timeout, etc.).

        Returns:
            The parsed response data (JSON or text).

        Raises:
            ProviderError: If the request fails.
        """
        if not self._initialized or self._session is None:
            raise ProviderError("Provider not initialized")

        # Handle dict query format
        if isinstance(query, dict):
            endpoint = query.get("endpoint", "/")
            params = query.get("params", params or {})
        else:
            endpoint = query
            params = params or {}

        url = f"{self._base_url}{endpoint}"
        timeout = kwargs.get("timeout", self._timeout)

        try:
            response = self._session.get(
                url,
                params=params,
                timeout=timeout,
                **{k: v for k, v in kwargs.items() if k not in ["timeout"]}
            )
            response.raise_for_status()

            # Parse JSON if applicable
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            return response.text

        except requests.exceptions.RequestException as e:
            raise ProviderError(f"HTTP fetch failed: {e}") from e

    def mutate(
        self,
        operation: str,
        payload: Dict[str, Any],
        **kwargs
    ) -> Any:
        """
        Perform a mutation via HTTP.

        Maps operations to HTTP methods:
            - "create" → POST
            - "update" → PUT
            - "delete" → DELETE
            - "patch" → PATCH
            - "upsert" → PUT

        Args:
            operation: The operation type.
            payload: The data payload.
            **kwargs: Additional arguments (headers, timeout, endpoint, etc.).

        Returns:
            The parsed response data.

        Raises:
            ProviderError: If the mutation fails.
        """
        if not self._initialized or self._session is None:
            raise ProviderError("Provider not initialized")

        endpoint = kwargs.get("endpoint", "/")
        url = f"{self._base_url}{endpoint}"
        timeout = kwargs.get("timeout", self._timeout)

        method = kwargs.get("method", {
            "create": "POST",
            "update": "PUT",
            "delete": "DELETE",
            "patch": "PATCH",
            "upsert": "PUT",
        }.get(operation, "POST"))

        try:
            response = self._session.request(
                method=method,
                url=url,
                json=payload,
                timeout=timeout,
                **{k: v for k, v in kwargs.items() if k not in ["timeout", "endpoint", "method"]}
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            return response.text

        except requests.exceptions.RequestException as e:
            raise ProviderError(f"HTTP mutation failed: {e}") from e

    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """
        Execute a structured query (GraphQL, etc.).

        This implementation supports GraphQL queries.

        Args:
            query: The query string (GraphQL, SQL, etc.).
            variables: Query variables.
            **kwargs: Additional arguments.

        Returns:
            The query results.

        Raises:
            ProviderError: If the query execution fails.
        """
        if not self._initialized or self._session is None:
            raise ProviderError("Provider not initialized")

        endpoint = kwargs.get("endpoint", "/")
        url = f"{self._base_url}{endpoint}"

        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        timeout = kwargs.get("timeout", self._timeout)

        try:
            response = self._session.post(
                url,
                json=payload,
                timeout=timeout,
                **{k: v for k, v in kwargs.items() if k not in ["timeout", "endpoint"]}
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise ProviderError(f"Query execution failed: {e}") from e

    def execute(
        self,
        statement: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """
        Execute a statement.

        For HTTP providers, this may be a raw POST request with a statement body.

        Args:
            statement: The statement to execute (may be SQL, command, etc.).
            params: Optional parameters.
            **kwargs: Additional arguments.

        Returns:
            The execution result.

        Raises:
            ProviderError: If execution fails.
        """
        if not self._initialized or self._session is None:
            raise ProviderError("Provider not initialized")

        endpoint = kwargs.get("endpoint", "/")
        url = f"{self._base_url}{endpoint}"

        payload = {"statement": statement}
        if params:
            payload["params"] = params

        timeout = kwargs.get("timeout", self._timeout)

        try:
            response = self._session.post(
                url,
                json=payload,
                timeout=timeout,
                **{k: v for k, v in kwargs.items() if k not in ["timeout", "endpoint"]}
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise ProviderError(f"Statement execution failed: {e}") from e
