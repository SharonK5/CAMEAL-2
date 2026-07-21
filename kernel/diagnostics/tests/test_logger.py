# kernel/diagnostics/tests/test_logger.py
import pytest
from kernel.diagnostics.base.logger import Logger


def test_log_event():
    logger = Logger(log_limit=3)
    event = type("Event", (), {"event_type": "log.info", "payload": {"message": "Hello"}})()
    logger.record(event)
    logs = logger.get_logs()
    assert len(logs) == 1
    assert logs[0]["type"] == "log.info"
    assert logs[0]["message"] == "Hello"


def test_log_filter():
    logger = Logger()
    logger.record(type("Event", (), {"event_type": "log.info", "payload": {"msg": "info"}})())
    logger.record(type("Event", (), {"event_type": "log.error", "payload": {"msg": "error"}})())
    logs = logger.get_logs(level="info")
    assert len(logs) == 1
    assert logs[0]["msg"] == "info"


def test_log_limit():
    logger = Logger(log_limit=2)
    for i in range(5):
        logger.record(type("Event", (), {"event_type": "log.info", "payload": {"id": i}})())
    logs = logger.get_logs()
    assert len(logs) == 2
    assert logs[0]["id"] == 3
    assert logs[1]["id"] == 4


def test_clear():
    logger = Logger()
    logger.record(type("Event", (), {"event_type": "log.info"})())
    assert len(logger.get_logs()) == 1
    logger.clear()
    assert len(logger.get_logs()) == 0
