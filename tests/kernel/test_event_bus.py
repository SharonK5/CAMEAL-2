from kernel.event_bus import EventBus


def test_publish_event():

    bus = EventBus()

    received = []

    def handler(event):

        received.append(event)

    bus.subscribe("test", handler)

    bus.publish(
        "test",
        {"value": 1}
    )

    assert len(received) == 1
