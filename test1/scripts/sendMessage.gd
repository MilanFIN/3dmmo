extends Button


var message = ""

# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _pressed():
	var textField = get_node("../InputField")
	var msg = textField.get_text()
	textField.clear()

	if (msg != ""):
		message = msg



# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
