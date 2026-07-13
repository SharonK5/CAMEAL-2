from security.session import Session


def test_session_creation():

    session = Session(username="sharon")

    assert session.username == "sharon"
    assert session.active
    assert session.session_id is not None


def test_session_expiry():

    session = Session(username="sharon")

    assert not session.is_expired()


def test_touch():

    session = Session(username="sharon")

    before = session.last_activity

    session.touch()

    assert session.last_activity >= before
