

class Player():
	def __init__(self, username):
		self.username = username
		self.x = 0
		self.y = 0
		self.state = "idle"
		self.angle = 0
		self.targetAngle = 0