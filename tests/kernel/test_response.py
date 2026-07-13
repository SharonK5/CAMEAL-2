from kernel.response import Response


def test_success_response():
    """Test a successful response."""

    response = Response(
        success=True,
        message="OK",
        data={"status": "ok"},
    )

    assert response.success is True
    assert response.message == "OK"
    assert response.data["status"] == "ok"


def test_failure_response():
    """Test a failed response."""

    response = Response(
        success=False,
        message="Invalid request",
    )

    assert response.success is False
    assert response.message == "Invalid request"


def test_response_to_dict():
    """Test serialization."""

    response = Response(
        success=True,
        message="Done",
        data={"value": 42},
        metadata={"module": "unit-test"},
        component="kernel",
        execution_time=0.05,
        correlation_id="abc123",
    )

    data = response.to_dict()

    assert data["success"] is True
    assert data["message"] == "Done"
    assert data["data"]["value"] == 42
    assert data["metadata"]["module"] == "unit-test"
    assert data["component"] == "kernel"
    assert data["execution_time"] == 0.05
    assert data["correlation_id"] == "abc123"

    assert "timestamp" in data
