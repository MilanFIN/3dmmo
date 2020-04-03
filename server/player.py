
import time

class Player():
	def __init__(self, username):
		self.username = username
		self.x = 0
		self.y = 0
		self.state = "idle"
		self.angle = 0
		self.targetAngle = 0
		self.targetX = 0
		self.targetY = 0
		self.map = "0"
		self.mapValid = False
		self.ActionAcknowleged = False

		self.actionTarget = None

		self.lastActionTime = time.clock()
		print(self.lastActionTime)
	def getMapId(self):
		return self.map
	def hasValidMap(self):
		return self.mapValid
	def validateMap(self):
		self.mapValid = True
	def setMap(self, mapId):
		self.map = mapId
		self.mapValid = False
	def tickDone(self):
		self.ActionAcknowleged = False
		if (self.state == "forceidle"):
			self.state = "idle"
	def setAction(self,targetId):
		self.actionTarget = targetId
	def getAction(self):
		return self.actionTarget
	def resetActionTime(self):
		self.lastActionTime = time.clock()
	def getLastActionTime(self):
		return self.lastActionTime

	def forcePosition(self, x, y):
		self.x = x
		self.y = y
		self.state = "forceidle"
