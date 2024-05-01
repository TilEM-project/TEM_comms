from TEM_comms.stomp_message_broker import StompMessageBroker
import time
from TEM_comms.logging import setup_logging
from TEM_comms.msgs import topics

logger = setup_logging("publisher")

connection = StompMessageBroker(topics=topics, logger=logger)
connection.connect()

while True:
    connection.send("tile.statistics.focus", tile_id="test", focus=11.2)
    time.sleep(1)
