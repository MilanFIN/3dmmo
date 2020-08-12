#extends Spatial
extends KinematicBody


const SPEED = 500
const ROTSPEED = 140#70
const MAXANGLEDIFF = 5



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

	#print(state)
	if (x != null and y != null):
		translation.x = x
		translation.z = y
		x = null
		y = null

	if (state == "idle"):
		pass

	elif (state == "moving"):
		
		var direction = Vector3(target.x-translation.x, 0, target.y-translation.z).normalized()
		
		var forward = -meshNode.get_global_transform().basis.z
		forward = Vector2(forward.x, forward.z).normalized()
		var planeDir = Vector2(direction.x, direction.z)
	
		var difference = rad2deg( forward.angle_to(planeDir))

		if (difference < -MAXANGLEDIFF):
			meshNode.rotate_y(deg2rad(ROTSPEED*delta))

		elif (difference > MAXANGLEDIFF):
			meshNode.rotate_y(deg2rad(-ROTSPEED*delta))

		move_and_slide(direction*SPEED*delta)
		var locationDifference = abs(target.x-translation.x)+abs(target.y-translation.z)
		if (locationDifference < 0.5):
			state = "idle"
			translation.x = target.x
			translation.z = target.y
			print(translation, " ", target)
			
		
	
func set_name(n):
	.set_name(n)
	get_node("NameLabel").setName(n)


	

func updateState(data):
	#print(data)
	var meshNode = get_node("./Mesh")
	var previousState = state
	state = data["state"]
	if (state == "idle"):
		x = float(data["x"])
		y = float(data["y"])
	elif (state == "moving"):
		var newTarget = Vector2(data["targetx"],data["targety"])

		if (target != newTarget):
			x = null
			y = null
			target = newTarget
	
	if ("override" in data):
		x = float(data["x"])
		y = float(data["y"])



	pass
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
