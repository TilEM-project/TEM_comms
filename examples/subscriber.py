from TEM_comms import TEM_comms

connection = TEM_comms()
connection.connect()

def callback(data):
    print(data)

connection.subscribe("tile.statistics.focus", callback)

while True:
    pass