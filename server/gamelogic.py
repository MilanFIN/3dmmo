
from multiprocessing import Process, Queue
from time import sleep
import uuid


class GameLogic():
	def __init__(self):
		pass
		self.players = {}
	def newMessage(self, message):
		print(message)
		pass
	def tick(self):
		pass
		return []

def startGameLogic(inQue, outQue):
	gameLogic = GameLogic()

	while True:
		idle = True
		messages = 0
		while (messages < 200):
			if (inQue.empty()):
				break
			msg = inQue.get()
			gameLogic.newMessage(msg)
			messages += 1
			idle = False

		outbound = gameLogic.tick()
		#gameLogic.emptyOutBound()
		if (len(outbound) != 0):
			idle = False
			for i in outbound:
				outQue.put(i)
		if (idle):
			sleep(0.5)

