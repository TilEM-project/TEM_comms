from abc import ABC, abstractmethod
from typing import Callable

class MessageBroker(ABC):

    @abstractmethod
    def connect(self, host: str, port: int, username: str = None, password: str = None):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def subscribe(self, topic: str, callback: Callable):
        pass

    @abstractmethod
    def unsubscribe(self, topic: str):
        pass

    @abstractmethod
    def send(self, topic: str, message: dict):
        pass
