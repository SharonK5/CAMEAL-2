"""
===============================================================================
Module: services.analytics.analytics_service

Abstract Analytics Service.

Defines the contract implemented by all analytics services.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from abc import abstractmethod

from services.service import Service

from query.execution.execution_context import ExecutionContext
from query.query_request import QueryRequest
from .analytics_result import AnalyticsResult


class AnalyticsService(Service):
    """
    Abstract analytics service.
    """

    @abstractmethod
    def analyze(
        self,
        request: QueryRequest,
        context: ExecutionContext,
    ) -> AnalyticsResult:
        """
        Perform analytics.
        """
