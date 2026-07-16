from security.identity.authentication_request import AuthenticationRequest


def test_request_defaults():

    request = AuthenticationRequest(
        username="sharon",
        password="secret",
    )

    assert request.username == "sharon"

    assert request.source == "unknown"

    assert request.remember_me is False


def test_request_custom():

    request = AuthenticationRequest(
        username="john",
        password="1234",
        remember_me=True,
        source="api",
    )

    assert request.remember_me

    assert request.source == "api"
