from security.audit import AuditEvent


def test_create_audit_event():

    event = AuditEvent(
        action="LOGIN"
    )

    assert event.action == "LOGIN"

    assert event.success

    assert event.event_id is not None


def test_metadata():

    event = AuditEvent(
        action="QUERY",
        metadata={"document": "policy.pdf"},
    )

    assert event.metadata["document"] == "policy.pdf"
