from TEM_comms import TEM_comms
import time

connection = TEM_comms('publisher')
connection.connect()

while True:
    connection.send("tile.statistics.focus", tile_id="test", focus=11.2)
    time.sleep(1)