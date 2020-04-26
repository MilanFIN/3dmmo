import configparser
import json
import math

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
			self.targetMap = data["targetmap"]
			self.exitX = data["exitx"]
			self.exitY = data["exity"]
		
		elif (self.action == "mine"):
			self.probability = float(data["probability"])
			self.drop = data["drop"]


		self.data = {}
		self.data["x"] = self.x
		self.data["y"] = self.y
		self.data["type"] = self.type
		self.data["action"] = self.action




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
		self.speed = 0


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


		self.data = {}
		self.data["x"] = self.x
		self.data["y"] = self.y
		self.data["type"] = self.type
		self.data["action"] = self.action
		self.data["speed"] = self.speed
	
	def update(self):
		if (self.moving):
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

