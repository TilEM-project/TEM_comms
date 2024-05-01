import stomp
from typing import Callable, Dict, List
from stomp.utils import Frame
import stomp.exception
from TEM_comms import exceptions
from TEM_comms.base_broker import MessageBroker
import logging


class StompMessageBroker(MessageBroker):
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 61616,
        topics: Dict[str, Callable] = None,
        logger: logging.Logger = None,
    ):
        self._connection = stomp.Connection12([(host, port)])
        self._topics = topics if topics is not None else {}
        self._callbacks: Dict[str, List[Callable]] = {}
        self._connection.set_listener("listener", StompListener(self._handle_message))
        self._logger = logger if logger is not None else self._configure_logging()

    def _configure_logging(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger

    def connect(self, username: str = None, password: str = None):
        """
        Connects to the STOMP server using the provided username and password.

        Args:
            username (str, optional): The username to authenticate with. Defaults to None.
            password (str, optional): The password to authenticate with. Defaults to None.

        Raises:
            stomp.exception.ConnectFailedException: If the connection to the server fails.

        """
        try:
            self._connection.connect(username=username, password=password, wait=True)
            self._logger.info("Connected to STOMP server.")
        except stomp.exception.ConnectFailedException as e:
            self._logger.error(f"Connection failed: {e}")
            raise stomp.exception.ConnectFailedException(
                f"Could not connect to server: {e}"
            )

    def add_topic(self, topic_name: str, message_handler: Callable):
        """
        Add a new topic to the StompClient.

        Args:
            topic_name (str): The name of the topic to add.
            message_handler (Callable): The class representing the message for the topic.
        """
        if topic_name in self._topics:
            self._logger.warning(f"Topic {topic_name} is already registered.")
            return
        self._topics[topic_name] = message_handler
        self._callbacks[topic_name] = []
        self._logger.info(f"Added new topic {topic_name}.")

    def remove_topic(self, topic_name: str):
        """
        Removes a topic from the StompClient's internal topic list.

        Args:
            topic_name (str): The name of the topic to be removed.
        """
        if topic_name in self._topics:
            del self._topics[topic_name]
            del self._callbacks[topic_name]
            self._logger.info(f"Removed topic {topic_name}.")
        else:
            self._logger.warning(f"Topic {topic_name} not found.")

    def send(self, topic: str, **data):
        """
        Sends data to the specified topic.

        Args:
            topic (str): The topic to send the data to.
            **data: Keyword arguments representing the data to be sent.

        Raises:
            exceptions.NoSuchTopicException: If the specified topic is not defined.

        """
        serialized_data = self.serialize_data(topic, **data)
        self._connection.send(destination=topic, body=serialized_data)
        self._logger.debug(f"Sent data to {topic}: {serialized_data}")

    def serialize_data(self, topic: str, **data):
        if topic not in self._topics:
            raise exceptions.NoSuchTopicException(f"Topic {topic} not defined.")
        return self._topics[topic](**data).serialize()

    def _handle_message(self, message_frame: Frame):
        topic = message_frame.headers["subscription"]
        if topic not in self._topics:
            self._logger.warning(f"Received message for unregistered topic: {topic}")
            return
        message_data = self._topics[topic].deserialize(message_frame.body)
        for callback in self._callbacks[topic]:
            callback(message_data)

    def subscribe(self, topic: str, callback: Callable):
        """
        Subscribes to a topic and associates a callback function to handle incoming messages.

        Args:
            topic (str): The topic to subscribe to.
            callback (Callable): The callback function to handle incoming messages.

        Raises:
            NoSuchTopicException: If the specified topic is not defined.

        """
        if topic not in self._topics:
            raise exceptions.NoSuchTopicException(f"Topic {topic} not defined.")
        if topic not in self._callbacks:
            self._callbacks[topic] = []  # Initialize empty list if not present
        if not self._callbacks[topic]:
            self._connection.subscribe(destination=topic, id=topic)
        self._callbacks[topic].append(callback)
        self._logger.info(f"Subscribed to {topic} with {callback.__name__}.")

    def unsubscribe(self, topic: str):
        """
        Unsubscribes from a topic, using the subscription topic stored in the callbacks list.

        Args:
            topic (str): The topic to unsubscribe from.
        """
        if topic in self._callbacks and self._callbacks[topic]:
            for subscription_id in self._callbacks[topic]:
                self._connection.unsubscribe(id=subscription_id)
                self._logger.info(
                    f"Unsubscribed from {topic} with ID {subscription_id}."
                )
            del self._callbacks[topic]
        else:
            self._logger.warning(f"No active subscriptions for topic {topic}.")

    def disconnect(self):
        if self._connection.is_connected():
            self._connection.disconnect()
            self._logger.info("Disconnected from STOMP server.")


class StompListener(stomp.ConnectionListener):
    def __init__(self, callback: Callable):
        self.callback = callback

    def on_message(self, frame):
        self.callback(frame)

