from security.authentication_result import AuthenticationResult
from security.user import User


def test_success_result():

    user = User(
        username="sharon",
        roles={"admin"},
    )

    result = AuthenticationResult(
        success=True,
        user=user,
    )

    assert result.success

    assert result.user == user


def test_failure_result():

    result = AuthenticationResult(
        success=False,
        message="Invalid credentials",
    )

    assert not result.success

    assert result.user is None
