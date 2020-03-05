#extends Spatial
extends KinematicBody


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
	#print(state)

	if (state == "idle"):
		#translation.x = x
		#translation.z = y
		pass
	if (state == "turning"):
		#translation.x = x
		#translation.z = y
		var difference = angle - targetAngle
		if (abs(difference) < 2):
			state == "idle"
		elif (difference < 0):
			#meshNode.rotate_y(deg2rad(ROTSPEED))
			angle += ROTSPEED
		elif (difference > 0):
			#meshNode.rotate_y(deg2rad(-ROTSPEED))
			angle -= ROTSPEED
	elif (state == "moving"):
		
		var direction = Vector3(target.x-translation.x, 0, target.y-translation.z).normalized()
		
		move_and_slide(direction*SPEED)
		var locationDifference = abs(target.x-translation.x)+abs(target.y-translation.z)
		if (locationDifference < 0.5):
			state = "idle"
			translation.x = target.x
			translation.z = target.y
			print(translation, " ", target)
			
		
	
	

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
		angle = float(data["angle"])
		var newTarget = Vector2(data["targetx"],data["targety"])
		if (target != newTarget):
			x = float(data["x"])
			y = float(data["y"])
			target = newTarget


	pass
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
