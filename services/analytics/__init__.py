"""
===============================================================================
CAMEAL Analytics Services.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from .analytics_result import AnalyticsResult
from .analytics_service import AnalyticsService
from .default_analytics_service import DefaultAnalyticsService

__all__ = [
    "AnalyticsResult",
    "AnalyticsService",
    "DefaultAnalyticsService",
]
