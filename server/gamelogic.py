
from multiprocessing import Process, Queue
import time
import uuid
from player import *


class GameLogic():
	def __init__(self):
		pass
		self.players = {}
		self.gameMessages = {}
		self.accountMessages = {}
	def newMessage(self, message):
		if ("user" in message):
			if (message["user"] in self.players):
				self.gameMessages[message["user"]] = message
			else:
				self.accountMessages[message["user"]] = message
	def emptyMessages(self):
		self.gameMessages = {}
	def tick(self):

		#go through all messages and create the players, still needs delete?
		for uid in self.accountMessages:
			if (uid not in self.players):
				if (self.accountMessages[uid]["auth"] == "accepted"):
					print("creating a player")
					data = self.accountMessages[uid]["data"]
					if ("username" in data):
						player = Player(data["username"])
						self.players[uid] = player
		self.accountMessages = {}


		#go through all messages, and change their state accordingly
		for uid in self.gameMessages:
			#print(self.gameMessages[uid])
			pass
		self.gameMessages = {}	


		#make a list of each players restricted gamestate, player specific stuff would be added later
		playerStates = {}
		for uid in self.players:
			player = self.players[uid]
			playerState = {}
			playerState["username"] = player.username
			playerState["x"] = player.x
			playerState["y"] = player.y
			playerState["state"] = player.state

			playerStates[player.username] = playerState

		result = []
		for uid in self.players:
			res = {"user":uid, "data":playerStates}
			result.append(res)


		print(result)
		return result #this should be a list of dicts of type {"user":uid, data:data}, data should include for example positions by player

def startGameLogic(inQue, outQue):
	gameLogic = GameLogic()



	while True:
		idle = True
		startTime = time.time()
		while (time.time() - startTime < 0.5):
			if (not inQue.empty()):
				msg = inQue.get()
				gameLogic.newMessage(msg)
				idle = False

		outbound = gameLogic.tick()
		gameLogic.emptyMessages()
		if (len(outbound) != 0):
			idle = False
			for i in outbound:
				outQue.put(i)
		if (idle):
			time.sleep(0.5)

