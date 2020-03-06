

from websocket import create_connection
import json
import time

ws = create_connection("ws://localhost:4000")#create_connection("ws://localhost:4000")




message = {"action":"login", "username":"name", "password":"passwd"}
message = json.dumps(message)
ws.send(message)

time.sleep(1)

ws.send(json.dumps({"action":"message", "data":"asd"}))



x = 0
while True:
	print(ws.recv())
	time.sleep(1)



x = 0

ws.close()