from security.authorization_result import AuthorizationResult


def test_success():

    result = AuthorizationResult(
        success=True,
        message="Allowed",
    )

    assert result.success
    assert result.message == "Allowed"


def test_failure():

    result = AuthorizationResult(
        success=False,
        message="Denied",
    )

    assert not result.success
    assert result.message == "Denied"
