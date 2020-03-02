

from websocket import create_connection
import json
import time

ws = create_connection("ws://localhost:4000")#create_connection("ws://localhost:4000")




message = {"action":"login", "username":"name", "password":"passwd"}
message = json.dumps(message)
ws.send(message)

time.sleep(1)


x = 0
while x < 1:

	message = {"action":"turning", "angle":"0.0", "targetangle":"120.0"}
	message = json.dumps(message)
	ws.send(message)	
	ws.recv()
	time.sleep(1)
	x += 1
"""
x = 0
while True:

	message = {"action":"idle", "angle":str(x)}
	message = json.dumps(message)
	ws.send(message)	
	ws.recv()
	time.sleep(1)
	x += 10



x = 0
"""
ws.close()