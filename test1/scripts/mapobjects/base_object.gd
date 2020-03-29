extends StaticBody


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var _actionType = ""

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


func setPos(x, y):
	translation.x = int(x)
	translation.z = int(y)

func setAction(action):
	_actionType = action

func action():
	return _actionType
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
