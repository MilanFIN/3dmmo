extends Label


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var messages = []

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func addMessageBatch(messageList): #{u:name, m:message}
	for i in messageList:
		if ("u" in i and "m" in i):
			messages.append(i["u"] + ": " + i["m"])
	
	if (len(messages) > 8):
		messages = messages.slice(len(messages)-9, len(messages)-1)


	text = ""
	for i in messages:
		text += i + "\n"
# Called every frame. 'delta' is the elapsed time since the previous frame.:
#func _process(delta):
#	pass
