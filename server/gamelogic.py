
from multiprocessing import Process, Queue
import time
import uuid
import random
import math

from player import *
from gamemap import *
from itemhandler import *


TICKRATE = 0.5


class GameLogic():
	def __init__(self):
		pass
		self.players = {} # {uid: Player}
		self.gameMessages = {}
		self.accountMessages = {}

		self.maps = {}
		self.maps["0"] = GameMap("0")
		self.maps["1"] = GameMap("1")


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
				if ("auth" in self.accountMessages[uid]):
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


		#go through all messages, change player positions and change next actions for players
		for uid in self.gameMessages:
			if (uid in self.players):
				msg = self.gameMessages[uid]
				player = self.players[uid]
				if ("action" in msg):
					
					#MOVEMENT
					if (msg["action"] == "idle" and "x" in msg and "y" in msg):
						player.x = float(msg["x"])
						player.y = float(msg["y"])
						player.setState("idle")
					elif (msg["action"] == "moving" and "x" in msg and "y" in msg and "targetx" in msg and "targety" in msg):
						if (player.targetX != msg["targetx"] or player.targetY != msg["targety"]):
							player.clearNextAction()
						player.x = float(msg["x"])
						player.y = float(msg["y"])
						player.targetX = msg["targetx"]
						player.targetY = msg["targety"]
						player.setState("moving")

				#SET NEXT ACTIONS TO PLAYERS
				if ("acttarget" in msg and "actobject" in msg and "acttype" in msg):
					targetId = msg["acttarget"]
					if (msg["actobject"] == "static"):
						mapId = player.getMapId()
						target = self.maps[mapId].getStaticObjectById(targetId)
						if (target != None):
							if (target.action == msg["acttype"]):
								timeDiff = time.time() - player.getLastActionTime()
								if (timeDiff > 1):
									player.setNextAction("static", target.action, targetId)
					elif (msg["actobject"] == "inventory"):
						if (msg["acttarget"].isdigit()):# item index should be a number
							player.setNextAction("inventory", msg["acttype"], msg["acttarget"])
					elif (msg["actobject"] == "dynamic"):
						mapId = player.getMapId()
						target = self.maps[mapId].getDynamicObjectById(targetId)
						if (target != None):
							if (target.action == msg["acttype"]):
								timeDiff = time.time() - player.getLastActionTime()
								if (timeDiff > 1):
									player.setNextAction("dynamic", target.action, targetId)
					elif (msg["actobject"] == "conversation"):
							timeDiff = time.time() - player.getLastActionTime()
							if (timeDiff > 1):
								player.setNextAction("conversation", msg["acttype"], None)

		self.gameMessages = {}	

		
		# go throught players and handle each players action
		for uid in self.players:
			player = self.players[uid]
			if (player.hasNextAction()):
				if (player.nextActionObjectType == "static"):
					player.stopSpeaking()

					target = self.maps[player.getMapId()].getStaticObjectById(player.nextActionTargetId)
					deltaX = abs(target.x - player.x)
					deltaY = abs(target.y - player.y)
					if (deltaX + deltaY < target.actionDistance):
						player.resetActionTime()
						actionType = target.action
						if (actionType == "changemap"):
							player.setDoneAction("static", actionType, player.nextActionTargetId)
							player.setMap(target.targetMap)
							player.forceState("idle", target.exitX, target.exitY)
							player.clearNextAction()
						elif (actionType == "mine"):
							player.setDoneAction("static", actionType, player.nextActionTargetId)
							hitOdds = random.random()
							if (hitOdds < target.probability):
								drop = target.drop
								if (itemhandler.itemExists(drop)):
									addedItem = player.inventory.addItem(drop)
									if (not addedItem):
										print("inventory full")
								player.forceState("idle")
								player.clearNextAction()
				elif (player.nextActionObjectType == "inventory"):
					player.stopSpeaking()

					if (player.nextActionType == "drop"):
						player.setDoneAction("inventory", player.nextActionType, player.nextActionTargetId)
						player.inventory.removeByIndex(int(player.nextActionTargetId))
						player.clearNextAction()
				elif (player.nextActionObjectType == "dynamic"):
					player.stopSpeaking()
					if (player.nextActionType == "attack"):
						player.resetActionTime()
						player.setDoneAction("dynamic", player.nextActionType, player.nextActionTargetId)
						player.setAttackTarget(player.nextActionTargetId, "dynamic")
						player.clearNextAction()
					elif (player.nextActionType == "speak"):
						player.stopSpeaking()
						conversationTarget = self.maps[player.getMapId()].getDynamicObjectById(player.nextActionTargetId)
						player.speak(conversationTarget.conversation, conversationTarget.name)
						player.resetActionTime()
						player.setDoneAction("dynamic", player.nextActionType, player.nextActionTargetId)
						player.clearNextAction()
				elif (player.nextActionObjectType == "conversation"):
					if (player.nextActionType == "next"):
						player.resetActionTime()
						player.setDoneAction("conversation", player.nextActionType, player.nextActionTargetId)
						player.advanceConversation()
						player.clearNextAction()
					if (player.nextActionType == "stop"):
						player.resetActionTime()
						player.setDoneAction("conversation", player.nextActionType, player.nextActionTargetId)
						player.stopSpeaking()
						player.clearNextAction()




		#handle player attacks
		for uid in self.players:
			player = self.players[uid]
			if (player.attackTarget != ""):
				if (player.attackTargetType == "dynamic"):
					mapId = player.getMapId()
					targetId = player.attackTarget
					target = self.maps[mapId].getDynamicObjectById(targetId)
					attacked = False
					if (targetId != None):

						distance = math.sqrt( ((target.x-player.x)**2)+((target.y-player.y)**2) )
						if (distance < 20):
							maxDamage = player.getAttack()
							damage = random.randint(0,maxDamage)
							attacked = target.takeDamage(damage, uid) #false if enemy dies
					if (not attacked):
						player.clearAttackTarget()


		#update dynamic objects
		for m in self.maps:
			dobjs = self.maps[m].getDynamicObjects()
			for d in dobjs:
				#maybe move updating to after handing attacking, so we can deal with movement
				d.update()
				if (d.action == "attack"):
					if (d.attackTarget != ""):
						attacked = False
						#npc has been attacked by the player
						if (d.attackTarget in self.players):
							#should check if
							player = self.players[uid]
							pass #should check distance  to player and if map is the same
							if (m == player.getMapId()):
								distance = math.sqrt( ((d.x-player.x)**2)+((d.y-player.y)**2) )
								if (distance < 20):
									maxDamage = d.getAttack()
									damage = random.randint(0,maxDamage)

									attacked = player.takeDamage(damage)
								
						if (not attacked):
							#cannot attack player anymore

							print("forget target")

							d.forgetAttackTarget()




		#make a dict with each player's gamestate
		playerStates = {}
		for uid in self.players:
			player = self.players[uid]
			playerState = {}
			playerState["username"] = player.username
			playerState["x"] = player.x
			playerState["y"] = player.y
			playerState["state"] = player.state
			playerState["mapId"] = player.getMapId()


			playerState["hp"] = {}
			playerState["hp"]["hp"] = player.getHp()
			playerState["hp"]["maxhp"] = player.getMaxHp()

			playerState["dmghist"] = player.damageHistory

			playerState["speaking"] = player.speaking
			playerState["conv"] = player.getConversation()

			"""
			print(player.hp)
			player.hp -= 1
			if (player.hp <= 0):
				player.resetHp()
			"""


			if (player.state == "moving"):
				playerState["x"] = player.x
				playerState["y"] = player.y
				playerState["targetx"] = player.targetX
				playerState["targety"] = player.targetY
			
			if (player.hasDoneAction()):
				playerState["actobject"] = player.doneActionObjectType
				playerState["acttype"] = player.doneActionType
				playerState["acttarget"] = player.doneActionTargetId
			if (player.overrideState == True):
				playerState["override"] = "1"
			if (player.inventory.hasChanged()):
				playerState["inv"] = player.inventory.getItems()


			playerStates[player.username] = playerState

		#set the data to be sent to players
		result = []
		for uid in self.players:
			player = self.players[uid]
			playerdata = {}
			for i in playerStates:
				mapId = player.getMapId()
				if (playerStates[i]["mapId"] == mapId):
					playerdata[i] =  playerStates[i]
			dynamicdata = self.maps[player.getMapId()].getDynamicMap()
			res = {"user":uid, "data":{"playerdata":playerdata, "dynamicdata":dynamicdata}, "type":"game"}
			result.append(res)
			
			#handle map changes and the player initialization with the default map
			player = self.players[uid]
			if (not player.hasValidMap()):
				#print("not valid")
				player.validateMap()
				mapId = player.getMapId()
				mapJSON = self.maps[mapId].getStaticMap()
				res1 = {"user":uid, "data":mapJSON, "type":"map"}
				result.append(res1)

				
		#tell player objects to clean up tick related stuff
		for uid in self.players:
			self.players[uid].tickDone()

		for m in self.maps:
			dobjs = self.maps[m].getDynamicObjects()
			for d in dobjs:
				#maybe move updating to after handing attacking, so we can deal with movement
				d.tickDone()


		#print(result)
		return result #this should be a list of dicts of type {"user":uid, data:data}, data should include for example positions by player

def startGameLogic(inQue, outQue):
	gameLogic = GameLogic()



	while True:
		idle = True
		startTime = time.time()
		while (time.time() - startTime < TICKRATE):
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
			time.sleep(TICKRATE/10)

