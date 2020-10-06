import configparser
import json
import math
import time

class GameObject():
	def __init__(self, properties):
		self.type = properties["type"]
		self.x = float(properties["x"])
		self.y = float(properties["y"])

		self.data = {}

	def getData(self):
		return self.data


class StaticObject(GameObject):
	def __init__(self, properties):

		super().__init__(properties)

		#map specific data, unique

		self.config = configparser.ConfigParser()
		#data = {}

		self.config.read_file(open("./objects/static/"+self.type+".cfg"))

		sections = self.config.sections()
		data = dict(self.config.items(sections[0]))

		#data that every object should have
		self.radius = data["radius"]
		self.block = data["block"]
		self.name = data["name"]
		self.action = data["action"]

		#if object has an action, it has a minimum distance to activate
		if (self.action != "none"):
			self.actionDistance = int(data["actiondistance"])

		#details that are specific to the action type
		if (self.action == "changemap"):
			self.targetMap = properties["targetmap"] #data["targetmap"]
			self.exitX = properties["exitx"] #data["exitx"]
			self.exitY = properties["exity"] #data["exity"]
		
		elif (self.action == "mine"):
			self.probability = float(data["probability"])
			self.drop = data["drop"]


		self.data = {}
		self.data["x"] = self.x
		self.data["y"] = self.y
		self.data["type"] = self.type
		self.data["action"] = self.action
		self.data["radius"] = self.radius




class DynamicObject(GameObject):
	def __init__(self, properties):
		super().__init__(properties)



		self.config = configparser.ConfigParser()
		data = {}

		self.config.read_file(open("./objects/dynamic/"+self.type+".cfg"))

		sections = self.config.sections()
		data = dict(self.config.items(sections[0]))

		#data that every object should have
		self.name = data["name"]
		self.action = data["action"]
		self.visible = True
		self.speed = 0
		self.radius = data["radius"]


		self.moving = False
		self.waypoints = []
		self.targetWaypoint = 0

		if ("waypoints" in properties):
			self.moving = True
			self.speed = float(data["speed"])
			points = json.loads(properties["waypoints"])
			for w in points:
				x, y = w.split(",")
				x = float(x)
				y = float(y)
				self.waypoints.append({"x":x, "y":y})

		if (self.action == "attack"):
			#aggressive npc, must have hp etch
			self.hp = int(data["hp"])
			self.maxHp = self.hp
			#uid
			self.attackTarget = ""
			self.deathTime = time.time()
			self.respawnDelay = int(data["respawn"])
			self.damageHistory = []

		if (self.action == "speak"):
			self.conversation = data["conversation"]

		self.data = {}
		self.data["x"] = self.x
		self.data["y"] = self.y
		self.data["type"] = self.type
		self.data["action"] = self.action
		self.data["speed"] = self.speed
		self.data["radius"] = self.radius

	def update(self):

		move = self.moving
		if (self.action == "attack"):
			if (self.hp <= 0):

				if (time.time() - self.deathTime > self.respawnDelay):
					self.hp = self.maxHp
					self.visible = True
				else:
					self.visible = False
			pass
			if (self.attackTarget != ""):
				move = False


		if (move):
			target = self.waypoints[self.targetWaypoint]
			xDir = target["x"] - self.x
			yDir = target["y"] - self.y
			total = math.sqrt(xDir**2 + yDir**2)
			if (xDir != 0):
				xDir = xDir/total*self.speed
			if (yDir != 0):
				yDir = yDir/total*self.speed
			self.x += xDir
			self.y += yDir

			xDiff = abs(self.x - target["x"])
			yDiff = abs(self.y - target["y"])

			if (xDiff <= abs(xDir) and yDiff <= abs(yDir)):
				self.x = target["x"]
				self.y = target["y"]
				self.targetWaypoint += 1
				if (self.targetWaypoint == len(self.waypoints)):
					self.targetWaypoint = 0
			self.data["x"] = self.x
			self.data["y"] = self.y
		if (self.action == "attack"):
			if (self.hp <= 0):

				if (time.time() - self.deathTime > self.respawnDelay):
					self.hp = self.maxHp
					self.visible = True
				else:
					self.visible = False
			pass

	def takeDamage(self, damage, target):
		if (self.action != "attack"):
			return
		if (damage < 0):
			return
		self.hp -= damage
		if (damage != 0):
			self.damageHistory.append(str(damage))
		if (self.hp <= 0):
			#we died...
			self.attackTarget = ""
			self.deathTime = time.time()
			return False
		else:
			self.attackTarget = target
			return True


	def forgetAttackTarget(self):
		self.attackTarget = ""

	def getAttack(self):
		return 1

	def getData(self):
		if (self.action == "attack"):
			self.data["hp"] = self.hp
			self.data["mhp"] = self.maxHp
			self.data["dmghist"] = self.damageHistory
		return self.data

	def tickDone(self):
		if (self.action == "attack"):
			self.damageHistory = []
