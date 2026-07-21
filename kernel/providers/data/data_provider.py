# kernel/providers/data/data_provider.py
"""
Data provider abstraction.

Provides interfaces for accessing external data sources.
"""

from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union

from ..base.provider import Provider


class DataProvider(Provider):
    """
    Base interface for data providers.

    Data providers abstract access to external data sources:
        - REST APIs
        - GraphQL endpoints
        - Database connections
        - File systems
        - Streaming data sources

    All data providers must support:
        - Fetching data by query
        - Mutating data (create, update, delete)
        - Connection management
        - Health checking

    Examples of implementations:
        - HTTP/API data provider
        - SQL database provider
        - GraphQL client provider
        - File system data provider
        - Streaming data provider (Kafka, etc.)
    """

    @abstractmethod
    def get(self) -> Any:
        """Return the underlying data client or connection."""
        pass

    @abstractmethod
    def fetch(
        self,
        query: Union[str, Dict[str, Any]],
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """
        Fetch data based on a query.

        Args:
            query: The query (SQL string, API endpoint, or query dict).
            params: Optional query parameters.
            **kwargs: Implementation-specific arguments.

        Returns:
            The fetched data (format depends on provider).

        Raises:
            ProviderError: If the fetch operation fails.
        """
        pass

    @abstractmethod
    def mutate(
        self,
        operation: str,
        payload: Dict[str, Any],
        **kwargs
    ) -> Any:
        """
        Perform a mutation operation (create, update, delete).

        Args:
            operation: The operation type ("create", "update", "delete", "upsert").
            payload: The data payload for the mutation.
            **kwargs: Implementation-specific arguments.

        Returns:
            The result of the mutation.

        Raises:
            ProviderError: If the mutation fails.
        """
        pass

    @abstractmethod
    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """
        Execute a structured query (SQL, GraphQL, or similar).

        Args:
            query: The query string.
            variables: Query variables (for parameterized queries).
            **kwargs: Implementation-specific arguments.

        Returns:
            The query results.

        Raises:
            ProviderError: If the query execution fails.
        """
        pass

    @abstractmethod
    def execute(
        self,
        statement: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """
        Execute a statement (SQL DDL, stored procedure, etc.).

        Args:
            statement: The statement to execute.
            params: Optional parameters.
            **kwargs: Implementation-specific arguments.

        Returns:
            The execution result.

        Raises:
            ProviderError: If the execution fails.
        """
        pass
