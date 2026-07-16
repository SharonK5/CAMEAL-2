"""
===============================================================================
Tests for security.risk_level
===============================================================================
"""

from security.core.risk_level import RiskLevel


def test_ordering():

    assert RiskLevel.LOW < RiskLevel.MODERATE
    assert RiskLevel.MODERATE < RiskLevel.HIGH
    assert RiskLevel.HIGH < RiskLevel.CRITICAL


def test_higher_than():

    assert RiskLevel.CRITICAL.higher_than(RiskLevel.HIGH)
    assert not RiskLevel.LOW.higher_than(RiskLevel.MODERATE)


def test_at_least():

    assert RiskLevel.HIGH.at_least(RiskLevel.MODERATE)
    assert RiskLevel.MODERATE.at_least(RiskLevel.MODERATE)
    assert not RiskLevel.LOW.at_least(RiskLevel.HIGH)
