from multiprocessing import Process, Queue
from time import sleep

from auth import *
from gamelogic import *
from messagelogic import *


class Controller:
	def __init__(self):
		self.authorizedUsers = []
		self.unAuthUsers = []

		self.authInQue = Queue()
		self.authOutQue = Queue()

		self.auth = Process(target=startAuthService, args=(self.authInQue, self.authOutQue))
		self.auth.start()

		self.gameInQue = Queue()
		self.gameOutQue = Queue()

		self.game = Process(target=startGameLogic, args=(self.gameInQue, self.gameOutQue))
		self.game.start()

		self.msgInQue = Queue()
		self.msgOutQue = Queue()

		self.msgLogic = Process(target=startMessageLogic, args=(self.msgInQue, self.msgOutQue))
		self.msgLogic.start()

	def newMessage(self, message):

		if ("user" in message):
			if (message["user"] in self.authorizedUsers and "action" in message):

				action = message["action"]
				if (action == "logout"):
					self.authorizedUsers.remove(message["user"])
					self.authInQue.put(message)
					self.gameInQue.put(message)
					self.msgInQue.put(message)


				if (action == "idle" or action == "turning" or action == "moving"):
					self.gameInQue.put(message)
				if (action == "message"):
					self.msgInQue.put(message)
				pass
				#user is logged in, can handle message as normal
			else:
				if (message["action"] == "login"):
					self.authInQue.put(message)
				#user has just connected, feed to login service
				pass
		pass
		#figure out what keys it contains here
		#key is uuid, if not in auth, then add to unauth
		#if in auth, check action and shoot to comms or game sim
	def tick(self):
		messages = []

		roundCount = 0
		while (roundCount < 200):
			if (self.authOutQue.empty()):
				break
			roundCount += 1
			message = self.authOutQue.get()
			if (message["auth"] == "accepted"):
				#print("NEW LOGIN:")
				#print(message)
				self.gameInQue.put(message)
				self.msgInQue.put(message)

				messages.append(message)
				self.authorizedUsers.append(message["user"])
			elif (message["auth"] == "rejected"):
				messages.append(message)

		roundCount = 0
		while (roundCount < 1000):
			if (self.gameOutQue.empty()):
				break
			roundCount += 1
			message = self.gameOutQue.get()
			messages.append(message)


		roundCount = 0
		while (roundCount < 1000):
			if (self.msgOutQue.empty()):
				break
			roundCount += 1
			message = self.msgOutQue.get()
			messages.append(message)


		return messages


def startController(inQ, outQ):
	controller = Controller()
	while True:
		idle = True
		messages = 0
		while (messages < 200):
			if (inQ.empty()):
				break
			msg = inQ.get()
			controller.newMessage(msg)
			messages += 1
			idle = False

		outbound = controller.tick()
		if (len(outbound) != 0):
			idle = False
			for i in outbound:
				outQ.put(i)
		if (idle):
			sleep(0.05)
