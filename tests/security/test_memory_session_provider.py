from security.identity.memory_session_provider import MemorySessionProvider
from security.identity.session import Session


def test_create_session():

    provider = MemorySessionProvider()

    session = Session(username="sharon")

    provider.create(session)

    assert provider.exists(session.session_id)


def test_get_session():

    provider = MemorySessionProvider()

    session = Session(username="sharon")

    provider.create(session)

    assert provider.get(session.session_id) == session


def test_delete_session():

    provider = MemorySessionProvider()

    session = Session(username="sharon")

    provider.create(session)

    provider.delete(session.session_id)

    assert provider.get(session.session_id) is None
