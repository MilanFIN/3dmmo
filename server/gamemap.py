import configparser
from gameobject import *
import json

class GameMap():
	def __init__(self, name):
		self.name = name
		
		self.objects = {}

		self.config = configparser.ConfigParser()

		with open("./maps/"+name+".cfg") as fp:
			self.config.readfp(fp)
			sections = self.config.sections()

			for i in sections:
				obj = GameObject(dict(self.config.items(i)))
				self.objects[i] = obj

	def getMap(self):
		mapData = {}
		for i in self.objects:
			mapData[i] = self.objects[i].getData()
		return json.dumps(mapData)
		
	def __checkPlayerCollisionForObjects(self, player):
		x = player.x
		y = player.y
		return False