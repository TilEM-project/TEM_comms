import os
import time

from TEM_comms.client import TEMComms
from TEM_comms.logging import setup_logging
from TEM_comms.msgs import topics

logger = setup_logging("publisher")

host = os.environ.get("ARTEMIS_HOST", "127.0.0.1")
port = int(os.environ.get("ARTEMIS_PORT", 61613))

connection = TEMComms("Publisher", host=host, port=port, topics=topics, logger=logger)
connection.connect(username="admin", password="password")

while True:
    connection.send("tile.statistics.focus", tile_id="test", focus=11.2)
    time.sleep(1)
