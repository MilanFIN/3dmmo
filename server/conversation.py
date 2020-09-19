import configparser
from gameobject import *
import json


class Conversation():
	def __init__(self, id):
		self.messages = ["test", "test2"]
		self.currentMessage = 0
		self.newMessage = True
	def getMessage(self):
		if (self.newMessage):
			self.newMessage = False
			return self.messages[self.currentMessage]
		else:
			return ""
	def advanceConversation(self):
		self.currentMessage += 1
		if (self.currentMessage >= len(self.messages)):
			self.newMessage = True
			self.currentMessage = len(self.messages) - 1
