"""
===============================================================================
Tests for AnalyticsStage
===============================================================================
"""

import pytest
from unittest.mock import Mock

from query.execution import AnalyticsStage, ExecutionContext, ContextKeys
from services.analytics import AnalyticsResult
from query.query_request import QueryRequest
from query.query_intent import QueryIntent


class DescriptiveAnalytics:
    def analyze(self, request, context) -> AnalyticsResult:
        return AnalyticsResult(
            success=True,
            stage="analytics",
            analytics_type="descriptive",
            data={"mean": 4.2, "count": 10, "std": 1.3},
            summary="Descriptive summary of query results",
            insights=("distribution is normal", "no outliers"),
        )


class PredictiveAnalytics:
    def analyze(self, request, context) -> AnalyticsResult:
        return AnalyticsResult(
            success=True,
            stage="analytics",
            analytics_type="predictive",
            data={"forecast": [1.2, 1.5, 1.8, 2.0], "confidence": 0.85},
            summary="Predicted next values for trend",
            insights=("upward trend expected", "seasonality detected"),
        )


class GapAnalytics:
    def analyze(self, request, context) -> AnalyticsResult:
        return AnalyticsResult(
            success=True,
            stage="analytics",
            analytics_type="gap",
            data={
                "gap_type": "compliance",
                "expected": 1.0,
                "actual": 0.85,
                "gap": 0.15,
                "unit": "percent",
            },
            summary="Compliance gap of 15% detected",
            insights=("Policy not fully applied", "correction recommended"),
        )


class SemanticAnalytics:
    def analyze(self, request, context) -> AnalyticsResult:
        return AnalyticsResult(
            success=True,
            stage="analytics",
            analytics_type="semantic",
            data={"similarity": 0.92, "vector_distance": 0.08, "matching_terms": 12},
            summary="High semantic similarity between query and context",
            insights=("query aligns well with retrieved documents",),
        )


class ComparativeAnalytics:
    def analyze(self, request, context) -> AnalyticsResult:
        return AnalyticsResult(
            success=True,
            stage="analytics",
            analytics_type="comparative",
            data={
                "baseline": 0.75,
                "current": 0.82,
                "improvement": 0.07,
                "metric": "accuracy",
            },
            summary="Accuracy improved by 7% over baseline",
            insights=("positive trend",),
        )


def test_descriptive_analytics():
    service = DescriptiveAnalytics()
    stage = AnalyticsStage(service)
    request = QueryRequest(identifier="1", intent=QueryIntent.RETRIEVE, query="test")
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    assert result.analytics_type == "descriptive"
    assert result.data["mean"] == 4.2
    assert "no outliers" in result.insights   # fixed
    stored = context.get(ContextKeys.ANALYTICS_RESULT)
    assert stored is result


def test_predictive_analytics():
    service = PredictiveAnalytics()
    stage = AnalyticsStage(service)
    request = QueryRequest(identifier="1", intent=QueryIntent.RETRIEVE, query="test")
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    assert result.analytics_type == "predictive"
    assert result.data["forecast"] == [1.2, 1.5, 1.8, 2.0]
    assert result.data["confidence"] == 0.85
    stored = context.get(ContextKeys.ANALYTICS_RESULT)
    assert stored is result


def test_gap_analytics():
    service = GapAnalytics()
    stage = AnalyticsStage(service)
    request = QueryRequest(identifier="1", intent=QueryIntent.RETRIEVE, query="test")
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    assert result.analytics_type == "gap"
    assert result.data["gap_type"] == "compliance"
    assert result.data["gap"] == 0.15
    assert "correction recommended" in result.insights
    stored = context.get(ContextKeys.ANALYTICS_RESULT)
    assert stored is result


def test_semantic_analytics():
    service = SemanticAnalytics()
    stage = AnalyticsStage(service)
    request = QueryRequest(identifier="1", intent=QueryIntent.RETRIEVE, query="test")
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    assert result.analytics_type == "semantic"
    assert result.data["similarity"] == 0.92
    assert result.data["matching_terms"] == 12
    stored = context.get(ContextKeys.ANALYTICS_RESULT)
    assert stored is result


def test_comparative_analytics():
    service = ComparativeAnalytics()
    stage = AnalyticsStage(service)
    request = QueryRequest(identifier="1", intent=QueryIntent.RETRIEVE, query="test")
    context = ExecutionContext()

    result = stage.execute(request, context)

    assert result.success
    assert result.analytics_type == "comparative"
    assert result.data["improvement"] == 0.07
    assert "positive trend" in result.insights
    stored = context.get(ContextKeys.ANALYTICS_RESULT)
    assert stored is result


def test_analytics_stage_name():
    service = DescriptiveAnalytics()
    stage = AnalyticsStage(service)
    assert stage.name == "analytics"
