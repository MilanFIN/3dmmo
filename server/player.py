
import time
from inventory import *

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


		self.maxHp = 10
		self.hp = 10


		self.nextActionTargetId = ""
		self.nextActionType = ""
		self.nextActionObjectType = ""

		self.doneActionTargetId = ""
		self.doneActionType = ""
		self.doneActionObjectType = ""


		self.actionTarget = None


		self.inventory = Inventory()
		

		self.lastActionTime = time.time()

		self.attackTarget = ""
		self.attackTargetType = ""
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
		self.doneActionTargetId = ""
		self.doneActionType = ""
		self.doneActionObjectType = ""
		self.overrideState = False
		self.inventory.tickDone()

	def forceState(self, state, x = None, y = None):
		if (x != None):
			self.x = x
		if (y != None):
			self.y = y
		self.state = state
		self.overrideState = True


	def hasNextAction(self):
		if (self.nextActionTargetId != "" and self.nextActionType != "" and self.nextActionObjectType != ""):
			return True
		else:
			return False

	def setNextAction(self, objtype, acttype, targetid):
		self.nextActionTargetId = targetid
		self.nextActionType = acttype
		self.nextActionObjectType = objtype

	def clearNextAction(self):
		self.nextActionTargetId = ""
		self.nextActionType = ""
		self.nextActionObjectType = ""


	def hasDoneAction(self):
		if (self.doneActionTargetId != "" and self.doneActionType != "" and self.doneActionObjectType != ""):
			return True
		else:
			return False

	def setDoneAction(self, objtype, acttype, targetid):
		self.doneActionTargetId = targetid
		self.doneActionType = acttype
		self.doneActionObjectType = objtype

	def resetActionTime(self):
		self.lastActionTime = time.time()
	def getLastActionTime(self):
		return self.lastActionTime

	def setAttackTarget(self, target, targetType):
		self.attackTarget = target
		self.attackTargetType = targetType

	def clearAttackTarget(self):
		self.attackTarget = ""
		self.attackTargetType = ""


	def getAttack(self):
		return 1

	def getHp(self):
		return self.hp
	def getMaxHp(self):
		return self.maxHp
	def resetHp(self):
		self.hp = self.maxHp