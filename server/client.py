

from websocket import create_connection
import json

ws = create_connection("ws://localhost:4000")#create_connection("ws://localhost:4000")


message = {"action":"login", "username":"name", "password":"passwd"}
message = json.dumps(message)
ws.send(message)
print (ws.recv())
ws.close()