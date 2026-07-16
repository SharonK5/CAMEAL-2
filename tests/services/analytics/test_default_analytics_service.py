import pytest

from services.analytics import DefaultAnalyticsService


def test_name():

    service = DefaultAnalyticsService()

    assert service.name == "analytics"


def test_initialize():

    service = DefaultAnalyticsService()

    service.initialize()

    assert service.initialized is True


def test_shutdown():

    service = DefaultAnalyticsService()

    service.initialize()

    service.shutdown()

    assert service.initialized is False


def test_requires_initialization():

    service = DefaultAnalyticsService()

    with pytest.raises(RuntimeError):

        service.analyze(None, None)


def test_analyze():

    service = DefaultAnalyticsService()

    service.initialize()

    result = service.analyze(
        None,
        None,
    )

    assert result.success

    assert result.summary == "Analytics completed."
