import configparser
from gameobject import *
import json

class StaticMap():
	def __init__(self, name):
		self.name = name
		
		self.statics = {}

		self.config = configparser.ConfigParser()
		self.config.read_file(open("./maps/static/"+name+".cfg"))

		sections = self.config.sections()

		for i in sections:
			obj = StaticObject(dict(self.config.items(i)))
			self.statics[i] = obj

	def getMap(self):
		mapData = {}
		for i in self.statics:
			mapData[i] = self.statics[i].getData()
		return json.dumps(mapData)
		
	def __checkPlayerCollisionForObjects(self, player):
		x = player.x
		y = player.y
		return False

	def getStaticObjectById(self, objId):
		if (objId in self.statics):
			return self.statics[objId]
		else:
			return None
		