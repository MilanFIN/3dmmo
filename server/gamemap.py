import configparser
from gameobject import *
import json

class GameMap():
	def __init__(self, name):
		self.name = name
		
		self.statics = {}
		self.config = configparser.ConfigParser()
		self.config.read_file(open("./maps/static/"+name+".cfg"))
		sections = self.config.sections()
		for i in sections:
			obj = StaticObject(dict(self.config.items(i)))
			self.statics[i] = obj

		self.dynamics = {}
		self.config = configparser.ConfigParser()
		self.config.read_file(open("./maps/dynamic/"+name+".cfg"))
		sections = self.config.sections()
		for i in sections:
			obj = DynamicObject(dict(self.config.items(i)))
			self.dynamics[i] = obj

	def __checkPlayerCollisionForObjects(self, player):
		x = player.x
		y = player.y
		return False

	def getStaticMap(self):
		mapData = {}
		for i in self.statics:
			mapData[i] = self.statics[i].getData()
		return json.dumps(mapData)
		
	def getStaticObjectById(self, objId):
		if (objId in self.statics):
			return self.statics[objId]
		else:
			return None

	def getDynamicObjectById(self, objId):
		if (objId in self.dynamics):
			return self.dynamics[objId]
		else:
			return None
	
	def getDynamicMap(self):
		mapData = {}
		for i in self.dynamics:
			if (self.dynamics[i].visible):
				mapData[i] = self.dynamics[i].getData()
		return json.dumps(mapData)
	

	def getDynamicObjects(self):
		return self.dynamics.values()
		