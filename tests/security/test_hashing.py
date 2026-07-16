from security.integrity.hashing import HashingService


def test_hash_password():

    hashed = HashingService.hash_password(
        "cameal123"
    )

    assert hashed != "cameal123"

    assert "$" in hashed


def test_verify_password():

    password = "secure-password"

    hashed = HashingService.hash_password(password)

    assert HashingService.verify_password(
        password,
        hashed,
    )


def test_invalid_password():

    password = "correct"

    hashed = HashingService.hash_password(password)

    assert not HashingService.verify_password(
        "incorrect",
        hashed,
    )


def test_unique_salts():

    password = "same-password"

    first = HashingService.hash_password(password)

    second = HashingService.hash_password(password)

    assert first != second
