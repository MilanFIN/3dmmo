import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os
import threading
import time
from websocket import create_connection


class GameLoop(tornado.websocket.WebSocketHandler):
	def open(self):
		print("WebSocket opened")

	def on_message(self, message):
		message = json.loads(message)
		print(message)
		self.write_message(u"You said asd")

	def on_close(self):
		print("WebSocket closed")

def make_app():
	return tornado.web.Application([
		(r"/", GameLoop),

	])

def main():
	app = make_app()

	http_server = tornado.httpserver.HTTPServer(app
	)

	http_server.listen(4000)
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()