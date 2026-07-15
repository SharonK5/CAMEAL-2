"""
===============================================================================
Module: query.query

Abstract Query.

Defines the base contract for all CAMEAL query types.

A Query represents a governance request for knowledge, analysis,
evaluation, monitoring, accountability, learning, adaptation,
diagnostics, AI reasoning, or enterprise services.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .query_intent import QueryIntent


class Query(ABC):
    """
    Abstract base class for all CAMEAL queries.
    """

    @property
    @abstractmethod
    def identifier(self) -> str:
        """
        Unique query identifier.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def intent(self) -> QueryIntent:
        """
        Primary query intent.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def source(self) -> str:
        """
        Originating actor or system.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Human-readable query description.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Query specification version.
        """
        raise NotImplementedError
