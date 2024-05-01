from TEM_comms.stomp_message_broker import StompMessageBroker
from TEM_comms.msgs import topics
from TEM_comms.logging import setup_logging

logger = setup_logging("subscriber")



connection = StompMessageBroker(topics=topics, logger=logger)
connection.connect()


def callback(data):
    print(data)

connection.subscribe("tile.statistics.focus", callback)

while True:
    pass
