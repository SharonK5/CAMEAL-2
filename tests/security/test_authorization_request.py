from security.identity.authorization_request import AuthorizationRequest
from security.identity.permissions import Permission
from security.identity.user import User


def test_create_request():

    user = User(username="sharon")

    request = AuthorizationRequest(
        user=user,
        permission=Permission.READ,
    )

    assert request.user == user
    assert request.permission == Permission.READ
