import configparser

class GameObject():
	def __init__(self, properties):
		#map specific data, unique
		self.type = properties["type"]
		self.x = properties["x"]
		self.y = properties["y"]

		self.config = configparser.ConfigParser()
		data = {}
		with open("./objects/"+self.type+".cfg") as fp:
			self.config.readfp(fp)
			sections = self.config.sections()
			data = dict(self.config.items(sections[0]))

		#object specific data, per object
		self.radius = data["radius"]
		self.model = data["model"]
		self.block = data["block"]
		self.name = data["name"]
