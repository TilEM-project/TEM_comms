import pytest
from unittest.mock import MagicMock, patch
from stomp.exception import ConnectFailedException
from TEM_comms.stomp_message_broker import StompMessageBroker
from TEM_comms.exceptions import NoSuchTopicException
from TEM_comms.msgs.base import BaseMessage


class MockMessage(BaseMessage):
    field1: str

@pytest.fixture
def broker():
    with patch("TEM_comms.logging.setup_logging") as mock_logging:
        topics = {"topic1": MockMessage}
        yield StompMessageBroker(
            host="localhost", port=61613, logger=mock_logging.Logger(), topics=topics
        )


@pytest.mark.parametrize(
    "username, password, expected_log",
    [
        (None, None, "Connected to STOMP server."),
        ("user", "pass", "Connected to STOMP server."),
    ],
    ids=["no-auth", "with-auth"],
)
def test_connect(broker, username, password, expected_log):
    # Arrange
    broker._connection.connect = MagicMock()

    # Act
    broker.connect(username=username, password=password)

    # Assert
    broker._connection.connect.assert_called_with(
        username=username, password=password, wait=True
    )
    broker._logger.info.assert_called_with(expected_log)


@pytest.mark.parametrize(
    "username, password",
    [
        (None, None),
        ("user", "pass"),
    ],
    ids=["connect-fail-no-auth", "connect-fail-with-auth"],
)
def test_connect_failure(broker, username, password):
    # Arrange
    broker._connection.connect = MagicMock(
        side_effect=ConnectFailedException("Connection failed")
    )

    # Act & Assert
    with pytest.raises(
        ConnectFailedException, match="Could not connect to server: Connection failed"
    ):
        broker.connect(username=username, password=password)
    broker._logger.error.assert_called_once()


@pytest.mark.parametrize(
    "topic, data, expected_serialized_data",
    [
        ("topic1", {"field1": "value"}, '{"field1":"value"}'),
    ],
    ids=["send-data"],
)
def test_send(broker, topic, data, expected_serialized_data):
    # Arrange
    broker._topics[topic] = MockMessage
    broker._connection.send = MagicMock()

    # Act
    broker.send(topic, **data)

    # Assert
    broker._connection.send.assert_called_with(
        destination=topic, body=expected_serialized_data
    )
    broker._logger.debug.assert_called_with(
        f"Sent data to {topic}: {expected_serialized_data}"
    )


@pytest.mark.parametrize(
    "topic, data",
    [
        ("unknown_topic", {"key": "value"}),
    ],
    ids=["send-data-no-such-topic"],
)
def test_send_no_such_topic(broker, topic, data):
    # Act & Assert
    with pytest.raises(NoSuchTopicException, match=f"Topic {topic} not defined."):
        broker.send(topic, **data)


@pytest.mark.parametrize(
    "topic, callback_name, expected_log",
    [
        ("topic1", "callback", "Subscribed to topic1 with callback."),
    ],
    ids=["subscribe-new-topic"],
)
def test_subscribe(broker, topic, callback_name, expected_log):
    # Arrange
    broker._topics[topic] = MockMessage
    callback = MagicMock(__name__=callback_name)
    broker._connection.subscribe = MagicMock()

    # Act
    broker.subscribe(topic, callback)

    # Assert
    assert callback in broker._callbacks[topic]
    broker._connection.subscribe.assert_called_with(destination=topic, id=topic)
    broker._logger.info.assert_called_with(expected_log)


@pytest.mark.parametrize(
    "topic",
    [
        ("unknown_topic"),
    ],
    ids=["subscribe-no-such-topic"],
)
def test_subscribe_no_such_topic(broker, topic):
    # Arrange
    callback = MagicMock()

    # Act & Assert
    with pytest.raises(NoSuchTopicException, match=f"Topic {topic} not defined."):
        broker.subscribe(topic, callback)


@pytest.mark.parametrize(
    "topic, expected_log",
    [
        ("topic1", "Unsubscribed from topic1."),
    ],
    ids=["unsubscribe-existing-topic"],
)
def test_unsubscribe(broker, topic, expected_log):
    # Arrange
    broker._callbacks[topic] = ["topic1"]
    broker._connection.unsubscribe = MagicMock()

    # Act
    broker.unsubscribe(topic)

    # Assert
    assert topic not in broker._callbacks
    broker._connection.unsubscribe.assert_called_with(id=topic)
    broker._logger.info.assert_called_with(expected_log)


def test_disconnect(broker):
    # Arrange
    broker._connection.is_connected = MagicMock(return_value=True)
    broker._connection.disconnect = MagicMock()

    # Act
    broker.disconnect()

    # Assert
    broker._connection.disconnect.assert_called_once()
    broker._logger.info.assert_called_with("Disconnected from STOMP server.")
