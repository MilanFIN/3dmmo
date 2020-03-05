from multiprocessing import Process, Queue
import time
import uuid

TICKRATE = 1

class MessageLogic():
	def __init__(self):
		pass
		self.players = {} # {uid: "username"}
		self.messages = {}
		self.accountMessages = {}
		self.actedPlayers = {}

	def newMessage(self, message):
		if ("user" in message):
			if (message["user"] not in self.players and "auth" in message):
				self.accountMessages[message["user"]] = message
			elif (message["action"] == "logout"):
				self.accountMessages[message["user"]] = message
			else:
				self.messages[message["user"]] = message
				self.actedPlayers[message["user"]] = 1

	def tick(self):

		for uid in self.accountMessages:
			if (uid not in self.players):
				if (self.accountMessages[uid]["auth"] == "accepted"):
					data = self.accountMessages[uid]["data"]
					if ("username" in data):
						player = data["username"]
						self.players[uid] = player
			else:
				if (self.accountMessages[uid]["action"] == "logout"):
					self.players.pop(self.accountMessages[uid]["user"], None)


		##FINISH THIS
		result = []
		for uid in messages:
			if (uid in self.players):
				username = self.players[uid]
				pass
			pass

def startMessageLogic(inQue, outQue):
	msgLogic = MessageLogic()



	while True:
		idle = True
		startTime = time.time()
		while (time.time() - startTime < TICKRATE):
			if (not inQue.empty()):
				msg = inQue.get()
				MessageLogic.newMessage(msg)
				idle = False

		outbound = MessageLogic.tick()

		if (len(outbound) != 0):
			idle = False
			for i in outbound:
				outQue.put(i)
		if (idle):
			time.sleep(TICKRATE)
