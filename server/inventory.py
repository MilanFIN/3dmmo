

class Inventory():
	def __init__(self):
		self.MAXSIZE = 20
		self.items = [""] * self.MAXSIZE
		self.changed = False
	def getItems(self):
		return self.items
	def addItem(self, item):
		for i in range (len(self.items)):
			if (self.items[i] == ""):
				self.items[i] = item
				self.changed = True
				return True

		return False

	def removeItem(self, item):
		for i in range (len(items)):
			if (self.items[i] == item):
				self.items[i] = ""
				self.changed = True
				return True
		return False
	def hasChanged(self):
		return self.changed
	def tickDone(self):
		self.changed = False