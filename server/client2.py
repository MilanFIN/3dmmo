

from websocket import create_connection
import json
import time

ws = create_connection("ws://localhost:4000")#create_connection("ws://localhost:4000")


message = {"action":"login", "username":"name2", "password":"passwd"}
message = json.dumps(message)
ws.send(message)
while True:
	print (ws.recv())



ws.close()