extends Spatial

var SPEED = 1.0
var targetX = 0
var targetY = 0
# Declare member variables here. Examples:
# var a = 2
# var b = "text"



# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _physics_process(delta):
	translation.x = targetX
	translation.z = targetY

func setPosition(x, y):
	translation.x = x
	translation.z = y
	targetX = x
	targetY = y

func updatePosition(x, y):
	targetX = x
	targetY = y
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
