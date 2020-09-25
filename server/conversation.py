import configparser
from gameobject import *
import json


class Conversation():
	def __init__(self, id):
		self.messages = ["test", "test2"]
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

