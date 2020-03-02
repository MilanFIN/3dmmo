extends Spatial

const SPEED = 5
const ROTSPEED = 1

var angle = 0
var targetAngle = 0
var state = "idle"
var target = Vector2(0,0) #x,z target location
var x = 0
var y = 0

# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _physics_process(delta):
	var meshNode = get_node("./Mesh")
	meshNode.rotation.y = deg2rad(angle)
	
	translation.x = x
	translation.z = y
	
	if (state == "turning"):
		var difference = angle - targetAngle
		if (abs(difference) < 2):
			state == "idle"
		elif (difference < 0):
			#meshNode.rotate_y(deg2rad(ROTSPEED))
			angle += ROTSPEED
		elif (difference > 0):
			#meshNode.rotate_y(deg2rad(-ROTSPEED))
			angle -= ROTSPEED

	
	

func updateState(data):
	#print(data)
	var meshNode = get_node("./Mesh")
	state = data["state"]
	if (state == "idle"):
		angle = float(data["angle"])
	elif (state == "turning"):
		if (targetAngle != data["targetangle"]):
			angle = float(data["angle"])
			targetAngle = float(data["targetangle"])
	elif (state == "moving"):
		x = float(data["x"])
		y = float(data["y"])
		
	pass
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
