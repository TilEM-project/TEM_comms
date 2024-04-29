import stomp
from . import exceptions
from . import msgs

class TEM_comms:
    topics = {
        "buffer.status": msgs.buffer.status,
        "camera.command": msgs.camera.command,
        "camera.image": msgs.camera.image,
        "camera.settings": msgs.camera.settings,
        "camera.status": msgs.camera.status,
        "scope.command": msgs.scope.command,
        "scope.status": msgs.scope.status,
        "stage.aperture.command": msgs.stage.aperture.command,
        "stage.aperture.status": msgs.stage.aperture.status,
        "stage.motion.command": msgs.stage.motion.command,
        "stage.motion.status": msgs.stage.motion.status,
        "stage.rotation.command": msgs.stage.rotation.command,
        "stage.rotation.status": msgs.stage.rotation.status,
        "tile.jpeg": msgs.tile.jpeg,
        "tile.minimap": msgs.tile.minimap,
        "tile.processed": msgs.tile.processed,
        "tile.raw": msgs.tile.raw,
        "tile.statistics.focus": msgs.tile.statistics.focus,
        "tile.statistics.histogram": msgs.tile.statistics.histogram,
        "tile.statistics.min_max_mean": msgs.tile.statistics.min_max_mean,
        "tile.transform": msgs.tile.transform,
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