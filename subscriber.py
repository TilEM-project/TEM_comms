from TEM_comms import TEM_comms

connection = TEM_comms()
connection.connect()

def callback(data):
    print(data)

connection.subscribe("buffer.status", callback)

while True:
    pass