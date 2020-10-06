from gameobject import *


class Conversation():
	def __init__(self, id, playerName, opponent):

		filename = "./conversations/" + str(id) + ".cfg"
		self.unparsedMessages = []
		self.messages = []
		with open(filename) as f:
			self.unparsedMessages = f.readlines() 
		for m in self.unparsedMessages:
			parsedMessage = m.replace("{player}", playerName)
			parsedMessage = parsedMessage.replace("{opponent}", opponent)
			self.messages.append(parsedMessage)
		self.currentMessage = 0
		self.newMessage = True
		self.stillSpeaking = True
	def getMessage(self):
		if (self.newMessage):
			self.newMessage = False
			return self.messages[self.currentMessage]
		else:
			return ""
	def advance(self):
		self.currentMessage += 1
		self.newMessage = True

		if (self.currentMessage >= len(self.messages)):
			self.currentMessage = ""
			self.stillSpeaking = False
		return self.stillSpeaking

