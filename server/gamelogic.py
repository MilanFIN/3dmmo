
from multiprocessing import Process, Queue
import time
import uuid
from player import *


class GameLogic():
	def __init__(self):
		pass
		self.players = {} # {uid: Player}
		self.gameMessages = {}
		self.accountMessages = {}
	def newMessage(self, message):
		if ("user" in message):
			if (message["user"] not in self.players and "auth" in message):
				self.accountMessages[message["user"]] = message
			elif (message["action"] == "logout"):
				self.accountMessages[message["user"]] = message
			else:
				self.gameMessages[message["user"]] = message
	def emptyMessages(self):
		self.gameMessages = {}
	def tick(self):

		#go through all messages and create the players, still needs delete?
		for uid in self.accountMessages:
			if (uid not in self.players):
				if (self.accountMessages[uid]["auth"] == "accepted"):
					#print("creating a player")
					data = self.accountMessages[uid]["data"]
					if ("username" in data):
						player = Player(data["username"])
						self.players[uid] = player
			else:
				if (self.accountMessages[uid]["action"] == "logout"):
					self.players.pop(self.accountMessages[uid]["user"], None)


		self.accountMessages = {}


		#go through all messages, and change their state accordingly
		for uid in self.gameMessages:
			if (uid in self.players):
				msg = self.gameMessages[uid]
				player = self.players[uid]
				if ("action" in msg):
					#idling
					if (msg["action"] == "idle" and "angle" in msg):
						player.angle = float(msg["angle"])
						player.state = "idle"
						print("idling")
					elif (msg["action"] == "turning" and "angle" in msg and "targetangle" in msg):
						player.angle = float(msg["angle"])
						player.targetAngle = float(msg["targetangle"])
						player.state = "turning"
						print("turning")



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
			playerState["angle"] = str(player.angle)
			if (player.state == "turning"):
				playerState["targetangle"] = player.targetAngle

			playerStates[player.username] = playerState

		result = []
		for uid in self.players:
			res = {"user":uid, "data":playerStates}
			result.append(res)


		#print(result)
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

