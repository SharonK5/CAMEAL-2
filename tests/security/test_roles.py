from security.roles import Role


def test_roles_exist():

    assert Role.SYSTEM_ADMIN.value == "system_admin"

    assert Role.GUEST.value == "guest"
