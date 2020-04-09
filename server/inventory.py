

class Inventory():
	def __init__(self):
		self.MAXSIZE = 10
		self.items = []
	def getItems(self):
		return self.items
	def addItem(self, item):
		if (len(self.items) < self.MAXSIZE):
			self.items.append(item)
			return True
		else:
			return False

		self.items.append(item)
	def removeItem(self, item):
		if (item in self.items):
			self.items.remove(item)
			return True
		else:
			return False
		