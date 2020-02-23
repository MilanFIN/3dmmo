

from websocket import create_connection
import json

ws = create_connection("ws://localhost:4000")#create_connection("ws://localhost:4000")


message = {"posx":"100", "posy":"100"}
message = json.dumps(message)
ws.send(message)
print (ws.recv())
ws.close()