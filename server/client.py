

from websocket import create_connection
import json
import time

ws = create_connection("ws://localhost:4000")#create_connection("ws://localhost:4000")


message = {"action":"login", "username1":"name", "password":"passwd"}
message = json.dumps(message)
ws.send(message)
x = 0
while x < 1:
	print (ws.recv())
	x +=1


message = {"action":"login", "username":"name", "password":"passwd"}
message = json.dumps(message)
ws.send(message)
x = 0
while x < 5:
	print (ws.recv())
	x +=1

ws.close()