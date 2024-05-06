import logging
import time 

import stomp
from typing import Callable, Dict, List
from stomp.utils import Frame
import stomp.exception
import importlib.metadata

from . import exceptions


__version__ = importlib.metadata.version("TEM_comms")


class TEMComms:
    def __init__(
        self,
        service: str,
        host: str = "127.0.0.1",
        port: int = 61616,
        topics: Dict[str, Callable] = None,
        logger: logging.Logger = None,
    ):
        self._service = service
        self._connection = stomp.Connection12([(host, port)],  heartbeats=(10000, 10000))
        self._topics = topics if topics is not None else {}
        self._callbacks: Dict[str, Callable] = {}
        self._connection.set_listener("listener", TEMCommsListener(self._handle_message))
        self._logger = logger if logger is not None else self._configure_logging()

    @staticmethod
    def _configure_logging() -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger

    def connect(
        self,
        username: str = None,
        password: str = None,
        retry_limit: int = 8,
    ):
        """
        Connects to the STOMP server using the provided username and password.

        Args:
            username (str, optional): The username to authenticate with. Defaults to None.
            password (str, optional): The password to authenticate with. Defaults to None.

        Raises:
            stomp.exception.ConnectFailedException: If the connection to the server fails.

        """
        retries = 0
        while retries < retry_limit:
            try:
                self._connection.connect(
                    username=username, password=password, wait=True
                )
                self._logger.info("Connected to STOMP server.")
                break
            except stomp.exception.ConnectFailedException as e:
                self._logger.error(f"Connection failed: {e}. Attempting to reconnect.")
                retries += 1
                time.sleep(1)
                if retries == retry_limit:
                    raise stomp.exception.ConnectFailedException(
                        f"Could not connect to server: {e}"
                    ) from e

    def send(self, topic: str, **data):
        """
        Sends data to the specified topic.

        Args:
            topic (str): The topic to send the data to.
            **data: Keyword arguments representing the data to be sent.

        Raises:
            exceptions.NoSuchTopicException: If the specified topic is not defined.

        """
        self._ensure_topic_exists(topic)
        serialized_data = self._topics[topic](**data).serialize()
        headers = dict(service=self._service, version=__version__)
        self._connection.send(destination=topic, body=serialized_data, headers=headers)
        self._logger.debug(f"Sent data to {topic}: {serialized_data}")

    def _ensure_topic_exists(self, topic: str):
        if topic not in self._topics:
            raise exceptions.NoSuchTopicException(f"Topic {topic} not defined.")

    def _handle_message(self, message_frame: Frame):
        if message_frame.headers.get("version") != __version__:
            raise exceptions.VersionMismatchException
        topic = message_frame.headers["subscription"]
        if topic not in self._topics:
            self._logger.warning(f"Received message for unregistered topic: {topic}")
            return
        message_data = self._topics[topic].deserialize(message_frame.body)
        self._callbacks[topic](message_data)

    def subscribe(self, topic: str, callback: Callable):
        """
        Subscribes to a topic and associates a callback function to handle incoming messages.

        Args:
            topic (str): The topic to subscribe to.
            callback (Callable): The callback function to handle incoming messages.

        Raises:
            NoSuchTopicException: If the specified topic is not defined.

        """
        self._ensure_topic_exists(topic)
        if topic not in self._callbacks:
            self._connection.subscribe(destination=topic, id=topic)
        self._callbacks[topic] = callback
        self._logger.info(f"Subscribed to {topic} with {callback.__name__}.")

    def unsubscribe(self, topic: str):
        self._ensure_topic_exists(topic)
        self._connection.unsubscribe(id=topic)
        self._logger.info(f"Unsubscribed from {topic}.")
        del self._callbacks[topic]

    def disconnect(self):
        if self._connection.is_connected():
            self._connection.disconnect()
            self._logger.info("Disconnected from STOMP server.")


class TEMCommsListener(stomp.ConnectionListener): 
    def __init__(self, callback: Callable):
        self.callback = callback

    def on_message(self, frame):
        self.callback(frame)
