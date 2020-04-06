
import time

class Player():
	def __init__(self, username):
		self.username = username
		self.x = 0
		self.y = 0
		self.state = "idle"
		self.overrideState = False
		self.angle = 0
		self.targetAngle = 0
		self.targetX = 0
		self.targetY = 0
		self.map = "0"
		self.mapValid = False
		self.actionAcknowleged = None
		self.acknowlegedTarget = None

		self.actionTarget = None
		

		self.lastActionTime = time.clock()
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
		self.actionAcknowleged = None
		self.overrideState = False
	def setAction(self,targetId):
		self.actionTarget = targetId
	def getAction(self):
		return self.actionTarget
	def resetActionTime(self):
		self.lastActionTime = time.clock()
	def getLastActionTime(self):
		return self.lastActionTime

	def forceState(self, state, x = None, y = None):
		if (x != None):
			self.x = x
		if (y != None):
			self.y = y
		self.state = state
		self.overrideState = True

	def ackAction(self, action, target):
		self.actionAcknowleged = action
		self.acknowlegedTarget = target
		pass