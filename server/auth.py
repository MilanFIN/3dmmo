from multiprocessing import Process, Queue
from time import sleep




class AuthService:
	def __init__(self):
		self.OutBoundMessages = []
	def newMessage(self, message):
		#self.OutBoundMessages.append("user";)
		if ("action" in message and "username" in message and "password" in message):
			response = {}
			response["user"] = message["user"]
			response["auth"] = "accepted"
			response["data"] = {"username": message["username"]}
			self.OutBoundMessages.append(response)

		else:
			response = {}
			response["user"] = message["user"]
			response["auth"] = "rejected"
			self.OutBoundMessages.append(response)
		pass
	def getOutBoundMessages(self):
		return self.OutBoundMessages
	def emptyOutBound(self):
		self.OutBoundMessages = []


def startAuthService(inQue, outQue):
	auth = AuthService()

	while True:
		idle = True
		messages = 0
		while (messages < 200):
			if (inQue.empty()):
				break
			msg = inQue.get()
			auth.newMessage(msg)
			messages += 1
			idle = False

		outbound = auth.getOutBoundMessages()
		auth.emptyOutBound()
		if (len(outbound) != 0):
			idle = False
			for i in outbound:
				outQue.put(i)
		if (idle):
			sleep(0.5)


