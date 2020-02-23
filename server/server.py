import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os
import threading
import time




from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []
class GameServer(WebSocket):

	def handleMessage(self):
		data = self.data.decode("utf-8")
		print(data)
		self.sendMessage(self.data)
		#for client in clients:
		#	if client != self:
		#		client.sendMessage(self.address[0] + u' - ' + self.data)

	def handleConnected(self):
		print(self.address, 'connected')
		for client in clients:
			client.sendMessage(self.address[0] + u' - connected')
			clients.append(self)

	def handleClose(self):
		clients.remove(self)
		print(self.address, 'closed')
		#for client in clients:
		#	client.sendMessage(self.address[0] + u' - disconnected')

server = SimpleWebSocketServer('', 4000, GameServer)
server.serveforever()



