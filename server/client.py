

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
	time.sleep(2)
	x += 1

x = 0
while x < 1:

	message = {"action":"moving", "x":"0", "y":"0", "targetx":"10", "targety":"10"}
	message = json.dumps(message)
	ws.send(message)	
	ws.recv()
	time.sleep(5)
	x += 1
x = 0
while x < 100:

	message = {"action":"idle", "x":"0", "y":"0", "targetx":"10", "targety":"10"}
	message = json.dumps(message)
	ws.send(message)	
	ws.recv()
	time.sleep(5)
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