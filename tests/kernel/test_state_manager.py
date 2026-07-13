from kernel.state_manager import StateManager


def test_state_update():
    """Test updating a value within a section."""

    state = StateManager()

    state.update(
        "session",
        "user",
        "Sharon",
    )

    session = state.get("session")

    assert session["user"] == "Sharon"


def test_snapshot():
    """Test snapshot creation."""

    state = StateManager()

    snapshot = state.snapshot()

    assert isinstance(snapshot, dict)

    assert "session" in snapshot
    assert "workflow" in snapshot
