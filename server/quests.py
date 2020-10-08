import os


class Quest():
	def __init__(self, questFile):
		unparsedLines = []
		with open(questFile) as f:
			lines = f.readlines() 
			for line in lines:
				if (line[:1] != "#"):
					unparsedLines.append(line.replace('\n', ''))
		currentSection = ""
		self.name = ""
		self.steps = [] #list of {action:"", target:"", desc:""}
		print(unparsedLines)
		for line in unparsedLines:
			if (currentSection == ""):
				if (line == "QUEST"):
					currentSection = line
			elif (currentSection == "QUEST"):
				if (line == "STEPS"):
					currentSection = line
				else:
					self.name = line
			elif (currentSection == "STEPS"):
				lineSteps = line.split(";")
				if (len(lineSteps) == 3):
					step = {
						"action": lineSteps[0],
						"target": lineSteps[1],
						"desc": lineSteps[2]
					}
					self.steps.append(step)

		print(self.steps)
		



class QuestApi():
	def __init__(self):
		self.quests = {}
		filenames = os.listdir("./quests/")
		for f in filenames:
			self.quests[f.strip(".cfg")] = Quest("./quests/"+f)
		pass


