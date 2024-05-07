import os

from TEM_comms.client import TEMComms
from TEM_comms.msgs import topics
from TEM_comms.logging import setup_logging

logger = setup_logging("subscriber")

host = os.environ.get("ARTEMIS_HOST", "127.0.0.1")
port = int(os.environ.get("ARTEMIS_PORT", 61613))


def handle_focus_message(message):
    logger.info(f"Received focus message: {message}")


connection = TEMComms("Subscriber", host=host, port=port, topics=topics, logger=logger)
connection.connect(username="admin", password="password")
connection.subscribe("tile.statistics.focus", handle_focus_message)

while True:
    pass
