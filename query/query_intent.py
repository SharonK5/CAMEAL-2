"""
===============================================================================
Module: query.query_intent

Query Intent.

Defines the supported governance query intents within CAMEAL.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from enum import Enum, auto


class QueryIntent(Enum):
    """
    Enumeration of supported CAMEAL query intents.
    """

    # ------------------------------------------------------------------
    # Knowledge Retrieval
    # ------------------------------------------------------------------

    RETRIEVE = auto()
    SEARCH = auto()

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    ANALYZE = auto()
    SUMMARIZE = auto()
    COMPARE = auto()
    DIAGNOSE = auto()
    ASSESS = auto()

    # ------------------------------------------------------------------
    # Governance
    # ------------------------------------------------------------------

    MONITOR = auto()
    EVALUATE = auto()
    ACCOUNTABILITY = auto()
    LEARN = auto()
    ADAPT = auto()

    # ------------------------------------------------------------------
    # Decision Support
    # ------------------------------------------------------------------

    RECOMMEND = auto()
    REPORT = auto()
    PREDICT = auto()
    SIMULATE = auto()

    # ------------------------------------------------------------------
    # Enterprise
    # ------------------------------------------------------------------

    SERVICE = auto()
    EXECUTE = auto()

    # ------------------------------------------------------------------
    # AI
    # ------------------------------------------------------------------

    RAG = auto()
    LLM = auto()
