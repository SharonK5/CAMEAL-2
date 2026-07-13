from kernel.request import Request


def test_request_creation():
    """Test creation of a valid Request."""

    request = Request(
        action="search",
        payload={"query": "climate"},
    )

    assert request.action == "search"
    assert request.payload["query"] == "climate"

    # The implementation uses correlation_id
    assert request.correlation_id is not None

    # Timestamp should be automatically generated
    assert request.timestamp is not None

    # Defaults
    assert request.priority == 100
    assert request.source == "unknown"


def test_request_to_dict():
    """Test serialization."""

    request = Request(
        action="analyse",
        payload={"x": 1},
        metadata={"source": "unit-test"},
    )

    data = request.to_dict()

    assert data["action"] == "analyse"
    assert data["payload"]["x"] == 1
    assert data["metadata"]["source"] == "unit-test"

    assert "correlation_id" in data
    assert "timestamp" in data
