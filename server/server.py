#from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import tornado.websocket
import tornado.ioloop
import json
import uuid

from multiprocessing import Process, Queue

from controller import *

clients = {}
messageInQue = Queue()
messageOutQue = Queue()


def updateClients():

	while (not messageOutQue.empty()):
		msg = messageOutQue.get()
		if ("user" in msg):
			if (msg["user"] in clients):
				uid = msg["user"]
				del msg["user"]
				clients[uid].write_message(msg)

	#for uid in clients:
	#	clients[uid].write_message("asd")

class MessageHandler(tornado.websocket.WebSocketHandler):

	def check_origin(self, origin):
		return True
	def open(self):
		self.uuid = str(uuid.uuid4())

		while True:
			if (self.uuid in clients):
				self.uuid =  uuid.uuid4()
			else:
				break
		clients[self.uuid] = self
		
	def on_message(self, message):
		parsed_msg = json.loads(message)
		if (type(parsed_msg) is not dict):
			return
		else:
			parsed_msg["user"] = self.uuid
			messageInQue.put(parsed_msg)
		
	def on_close(self):
		msg = {"user":self.uuid, "action":"logout"}
		messageInQue.put(msg)
		clients.pop(self.uuid, None)



def make_app():
	return tornado.web.Application([
		(r"/", MessageHandler),
	])

def main():
	app = make_app()
	http_server = tornado.httpserver.HTTPServer(app
												#,
												#ssl_options = {
												#    "certfile": os.path.join("certs/domain-crt.txt"),
												#    "keyfile": os.path.join("certs/domain-key.txt"),
												#}
	)
	http_server.listen(9998)
	
	


	controller = Process(target=startController, args=(messageInQue, messageOutQue))
	controller.start()



	updateTimer = tornado.ioloop.PeriodicCallback(updateClients, 1000, jitter=0)
	updateTimer.start()
	tornado.ioloop.IOLoop.current().start()
	controller.join()

if __name__ == "__main__":
	main()
