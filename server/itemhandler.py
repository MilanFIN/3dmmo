import configparser
from item import *


class ItemHandler():
	def __init__(self):
		self.items ={}
		self.config = configparser.ConfigParser()
		self.config.read_file(open('./items/items.cfg'))


		for section in self.config.sections():
			for (key, value) in self.config.items(section):
				item = Item(section)
				self.items[section] = item
				print(section)
				print(key)
				print (value)

	def itemExists(self, itemName):
		if (itemName in self.items):
			return True
		else:
			return False

itemhandler = ItemHandler()