"""
===============================================================================
Tests for query.query_intent
===============================================================================
"""

from query.query_intent import QueryIntent


def test_unique_values():

    values = {intent.value for intent in QueryIntent}

    assert len(values) == len(QueryIntent)


def test_retrieve_exists():

    assert QueryIntent.RETRIEVE.name == "RETRIEVE"


def test_monitor_exists():

    assert QueryIntent.MONITOR.name == "MONITOR"


def test_evaluate_exists():

    assert QueryIntent.EVALUATE.name == "EVALUATE"


def test_accountability_exists():

    assert QueryIntent.ACCOUNTABILITY.name == "ACCOUNTABILITY"


def test_learning_exists():

    assert QueryIntent.LEARN.name == "LEARN"


def test_adaptation_exists():

    assert QueryIntent.ADAPT.name == "ADAPT"
