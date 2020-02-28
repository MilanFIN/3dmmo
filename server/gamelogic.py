
from multiprocessing import Process, Queue
from time import sleep
import uuid


class GameLogic():
	def __init__(self):
		pass
		self.players = {}
		self.messages = {}
	def newMessage(self, message):
		if ("user" in message):
			self.messages[message["user"]] = message
	def emptyMessages(self):
		self.messages = {}
	def tick(self):
		#go through all messages, after that figure out the current gamestate for each player
		for uid in self.messages:
			print(self.messages[uid])
			if (uid not in self.players):
				if (self.messages[uid]["auth"] == "accepted"):
					print("should create a player")
		pass
		return [] #this should be a list of dicts of type {"user":uid, data:data}, data should include for example positions by player

def startGameLogic(inQue, outQue):
	gameLogic = GameLogic()

	while True:
		idle = True
		messages = 0
		while (messages < 200):
			if (inQue.empty()):
				break
			msg = inQue.get()
			gameLogic.newMessage(msg)
			messages += 1
			idle = False

		outbound = gameLogic.tick()
		gameLogic.emptyMessages()
		if (len(outbound) != 0):
			idle = False
			for i in outbound:
				outQue.put(i)
		if (idle):
			sleep(0.5)

