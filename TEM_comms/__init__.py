import stomp
from . import exceptions
from . import msgs

class TEM_comms:
    topics = {
        "buffer.status": msgs.buffer.status
    }

    def __init__(self, host="127.0.0.1", port=61616):
        self.connection = stomp.Connection12([(host, port)])
        self.connection.set_listener("listener", TEM_comm_listener(self.callback)) 
        self.callbacks = { topic:[] for topic in self.topics.keys() }
    
    def connect(self, username=None, password=None):
        self.connection.connect(username=username, password=password)
    
    def send(self, topic, **data):
        if topic not in self.topics:
            raise exceptions.NoSuchTopicException
        self.connection.send(topic, self.topics[topic](**data).serialize())

    def callback(self, frame):
        topic = frame.headers["subscription"]
        data = self.topics[topic].deserialize(frame.body)
        for callback in self.callbacks[topic]:
            callback(data)
    
    def subscribe(self, topic, callback):
        if topic not in self.topics:
            raise exceptions.NoSuchTopicException
        if not len(self.callbacks[topic]):
            self.connection.subscribe(topic, topic)
        self.callbacks[topic].append(callback)


class TEM_comm_listener(stomp.ConnectionListener):
    def __init__(self, callback):
        self.callback = callback

    def on_message(self, frame):
        self.callback(frame)