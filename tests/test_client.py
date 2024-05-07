import pytest
from unittest.mock import MagicMock, patch
from stomp.exception import ConnectFailedException
from TEM_comms.client import TEMComms, __version__
from TEM_comms.exceptions import NoSuchTopicException
from TEM_comms.msgs.base import BaseMessage


class MockMessage(BaseMessage):
    field1: str


@pytest.fixture
def tem_comm_client():
    with patch("TEM_comms.logging.setup_logging") as mock_logging:
        topics = {"topic1": MockMessage}
        yield TEMComms(
            "test", host="localhost", port=61613, logger=mock_logging.Logger(), topics=topics
        )


@pytest.mark.parametrize(
    "username, password, expected_log",
    [
        (None, None, "Connected to STOMP server."),
        ("user", "pass", "Connected to STOMP server."),
    ],
    ids=["no-auth", "with-auth"],
)
def test_connect(tem_comm_client, username, password, expected_log):
    # Arrange
    tem_comm_client._connection.connect = MagicMock()

    # Act
    tem_comm_client.connect(username=username, password=password)

    # Assert
    tem_comm_client._connection.connect.assert_called_with(
        username=username, password=password, wait=True
    )
    tem_comm_client._logger.info.assert_called_with(expected_log)


@pytest.mark.parametrize(
    "username, password",
    [
        (None, None),
        ("user", "pass"),
    ],
    ids=["connect-fail-no-auth", "connect-fail-with-auth"],
)
def test_connect_failure(tem_comm_client, username, password):
    # Arrange
    tem_comm_client._connection.connect = MagicMock(
        side_effect=ConnectFailedException("Connection failed")
    )
    retry_limit = 1
    tem_comm_client._logger.error = MagicMock()

    # Act & Assert
    with pytest.raises(
        ConnectFailedException, match="Could not connect to server: Connection failed"
    ):
        tem_comm_client.connect(username=username, password=password, retry_limit=retry_limit)

    # Assert the logger was called the same number of times as the retry limit
    assert tem_comm_client._logger.error.call_count == retry_limit


@pytest.mark.parametrize(
    "topic, data, expected_serialized_data",
    [
        ("topic1", {"field1": "value"}, '{"field1":"value"}'),
    ],
    ids=["send-data"],
)
def test_send(tem_comm_client, topic, data, expected_serialized_data):
    
    
    expected_headers = {"service": "test", "version": __version__}
    # Arrange
    tem_comm_client._topics[topic] = MockMessage
    tem_comm_client._connection.send = MagicMock()

    # Act
    tem_comm_client.send(topic, **data)

    # Assert
    tem_comm_client._connection.send.assert_called_with(
        destination=topic, body=expected_serialized_data, headers=expected_headers
    )
    tem_comm_client._logger.debug.assert_called_with(
        f"Sent data to {topic}: {expected_serialized_data}"
    )
@pytest.mark.parametrize(
    "topic, data",
    [
        ("unknown_topic", {"key": "value"}),
    ],
    ids=["send-data-no-such-topic"],
)
def test_send_no_such_topic(tem_comm_client, topic, data):
    # Act & Assert
    with pytest.raises(NoSuchTopicException, match=f"Topic {topic} not defined."):
        tem_comm_client.send(topic, **data)


@pytest.mark.parametrize(
    "topic, callback_name, expected_log",
    [
        ("topic1", "callback", "Subscribed to topic1 with callback."),
    ],
    ids=["subscribe-new-topic"],
)
def test_subscribe(tem_comm_client, topic, callback_name, expected_log):
    # Arrange
    tem_comm_client._topics[topic] = MockMessage
    callback = MagicMock(__name__=callback_name)
    tem_comm_client._connection.subscribe = MagicMock()

    # Act
    tem_comm_client.subscribe(topic, callback)

    # Assert
    assert tem_comm_client._callbacks[topic] == callback
    tem_comm_client._connection.subscribe.assert_called_with(destination=topic, id=topic)
    tem_comm_client._logger.info.assert_called_with(expected_log)


@pytest.mark.parametrize(
    "topic",
    [
        ("unknown_topic"),
    ],
    ids=["subscribe-no-such-topic"],
)
def test_subscribe_no_such_topic(tem_comm_client, topic):
    # Arrange
    callback = MagicMock()

    # Act & Assert
    with pytest.raises(NoSuchTopicException, match=f"Topic {topic} not defined."):
        tem_comm_client.subscribe(topic, callback)


@pytest.mark.parametrize(
    "topic, expected_log",
    [
        ("topic1", "Unsubscribed from topic1."),
    ],
    ids=["unsubscribe-existing-topic"],
)
def test_unsubscribe(tem_comm_client, topic, expected_log):
    # Arrange
    tem_comm_client._callbacks[topic] = ["topic1"]
    tem_comm_client._connection.unsubscribe = MagicMock()

    # Act
    tem_comm_client.unsubscribe(topic)

    # Assert
    assert topic not in tem_comm_client._callbacks
    tem_comm_client._connection.unsubscribe.assert_called_with(id=topic)
    tem_comm_client._logger.info.assert_called_with(expected_log)


def test_disconnect(tem_comm_client):
    # Arrange
    tem_comm_client._connection.is_connected = MagicMock(return_value=True)
    tem_comm_client._connection.disconnect = MagicMock()

    # Act
    tem_comm_client.disconnect()

    # Assert
    tem_comm_client._connection.disconnect.assert_called_once()
    tem_comm_client._logger.info.assert_called_with("Disconnected from STOMP server.")
