import configparser

class GameObject():
	def __init__(self, properties):
		#map specific data, unique
		self.type = properties["type"]
		self.x = int(properties["x"])
		self.y = int(properties["y"])

		self.config = configparser.ConfigParser()
		data = {}
		with open("./objects/"+self.type+".cfg") as fp:
			self.config.readfp(fp)
			sections = self.config.sections()
			data = dict(self.config.items(sections[0]))

		#object specific data, per object
		self.radius = data["radius"]
		self.block = data["block"]
		self.name = data["name"]
		self.action = data["action"]

		if (self.action == "changemap"):
			self.targetMap = data["targetmap"]
			self.exitX = data["exitx"]
			self.exitY = data["exity"]


		self.data = {}
		self.data["x"] = self.x
		self.data["y"] = self.y
		self.data["type"] = self.type
		self.data["action"] = self.action


	def getData(self):
		return self.data