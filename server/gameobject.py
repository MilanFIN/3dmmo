import configparser

class StaticObject():
	def __init__(self, properties):
		#map specific data, unique
		self.type = properties["type"]
		self.x = int(properties["x"])
		self.y = int(properties["y"])

		self.config = configparser.ConfigParser()
		data = {}

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


	def getData(self):
		return self.data