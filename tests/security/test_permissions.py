from security.permissions import Permission


def test_permissions_exist():

    assert Permission.READ.value == "read"

    assert Permission.ADMIN.value == "admin"
