from multiprocessing import Process, Queue
from time import sleep

from auth import *
from gamelogic import *


class Controller:
	def __init__(self):
		self.authorizedUsers = {}
		self.unAuthUsers = {}

		self.authInQue = Queue()
		self.authOutQue = Queue()

		self.auth = Process(target=startAuthService, args=(self.authInQue, self.authOutQue))
		self.auth.start()

		self.gameInQue = Queue()
		self.gameOutQue = Queue()

		self.game = Process(target=startGameLogic, args=(self.gameInQue, self.gameOutQue))
		self.game.start()


	def newMessage(self, message):
		if ("user" in message):
			if (message["user"] in self.authorizedUsers):
				pass
				#user is logged in, can handle message as normal
			elif (message["user"] not in self.unAuthUsers):

				self.unAuthUsers[message["user"]] = 1
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
				print("NEW LOGIN:")
				#print(message)
				self.gameInQue.put(message)
				messages.append(message)
			elif (message["auth"] == "rejected"):
				messages.append(message)

		roundCount = 0
		while (roundCount < 1000):
			if (self.gameOutQue.empty()):
				break
			roundCount += 1
			message = self.gameOutQue.get()
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
