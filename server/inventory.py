

class Inventory():
	def __init__(self):
		self.MAXSIZE = 10
		self.items = []
		self.changed = False
	def getItems(self):
		return self.items
	def addItem(self, item):
		if (len(self.items) < self.MAXSIZE):
			self.items.append(item)
			self.changed = True
			return True
		else:
			return False

		self.items.append(item)
	def removeItem(self, item):
		if (item in self.items):
			self.items.remove(item)
			self.changed = True
			return True
		else:
			return False
	def hasChanged(self):
		return self.changed
	def tickDone(self):
		self.changed = False