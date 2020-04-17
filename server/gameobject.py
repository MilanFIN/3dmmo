import configparser
import json

class GameObject():
	def __init__(self, properties):
		self.type = properties["type"]
		self.x = int(properties["x"])
		self.y = int(properties["y"])

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
		self.speed = data["speed"]


		self.moving = False
		if ("waypoints" in properties):
			self.moving = True
			self.waypoints = json.loads(properties["waypoints"])


		self.data = {}
		self.data["x"] = self.x
		self.data["y"] = self.y
		self.data["type"] = self.type
		self.data["action"] = self.action
	
	def update(self):
		if (self.moving):
			for w in self.waypoints:
				print(w)
			if (self.x < 100):
				self.x += 0.5
		self.data["x"] = self.x
