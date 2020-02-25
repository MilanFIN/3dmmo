from multiprocessing import Process, Queue
from time import sleep

class Controller:
	def __init__(self):
		self.authorizedUsers = {}
		self.unAuthUsers = {}
		self.outBoundMessages = []

	def newMessage(self, message):
		print(message)

		if ("user" in message):
			if (message["user"] in self.authorizedUsers):
				pass
				#user is logged in, can handle message as normal
			elif (message["user"] not in self.unAuthUsers):

				#user has just connected, feed to login service
				pass
		pass
		#figure out what keys it contains here
		#key is uuid, if not in auth, then add to unauth
		#if in auth, check action and shoot to comms or game sim
	def getOutBoundMessages(self):
		messages = []
		messages.append({"uuid":"?", "stuff":"here"})
		return messages#actually return outboundmessages


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

		outbound = controller.getOutBoundMessages()
		if (len(outbound) != 0):
			idle = False
			for i in outbound:
				outQ.put(i)
		if (idle):
			sleep(0.1)
