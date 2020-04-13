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
				if (message["user"] not in self.actedPlayers and "data" in message):
					self.messages[message["user"]] = message
					self.actedPlayers[message["user"]] = 1

	def tick(self):

		for uid in self.accountMessages:
			if (uid not in self.players):
				if ("auth" in self.accountMessages[uid]):
					if (self.accountMessages[uid]["auth"] == "accepted"):
						data = self.accountMessages[uid]["data"]
						if ("username" in data):
							player = data["username"]
							self.players[uid] = player
			else:
				if (self.accountMessages[uid]["action"] == "logout"):
					self.players.pop(self.accountMessages[uid]["user"], None)

		self.accountMessages.clear()

		##FINISH THIS
		messageBatch = []
		for uid in self.messages:
			if (uid in self.players):
				username = self.players[uid]
				message = self.messages[uid]["data"]
				messageBatch.append({"u": username, "m":message})
				pass
			pass

		self.actedPlayers.clear()
		self.messages.clear()


		result = []

		if (len(messageBatch) != 0):
			for uid in self.players:
				res = {"user":uid, "data":messageBatch, "type":"message"}
				result.append(res)


		return result



def startMessageLogic(inQue, outQue):
	msgLogic = MessageLogic()

	while True:
		idle = True
		startTime = time.time()
		while (time.time() - startTime < TICKRATE):
			if (not inQue.empty()):
				msg = inQue.get()
				msgLogic.newMessage(msg)
				idle = False

		outbound = msgLogic.tick()

		if (len(outbound) != 0):
			idle = False
			for i in outbound:
				outQue.put(i)
		if (idle):
			time.sleep(TICKRATE)
