# security/authentication/tests/test_audit_logger.py
import pytest
from security.authentication.audit_logger import DefaultAuditLogger


def test_audit_logger_no_exception():
    logger = DefaultAuditLogger()
    # Just ensure it doesn't raise
    logger.log_authentication(
        identity_id="user123",
        success=True,
        method="login",
        details={"ip": "127.0.0.1"},
    )
    # No assertion needed; we're just checking it doesn't crash.
