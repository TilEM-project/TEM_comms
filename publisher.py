from TEM_comms import TEM_comms
import time

connection = TEM_comms()
connection.connect()

while True:
    connection.send("buffer.status", queue_length=1, free_space=2, upload_rate=3)
    time.sleep(1)