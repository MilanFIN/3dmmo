extends KinematicBody

const SPEED = 5
const ROTSPEED = 1
var velocity = Vector3(0,0,0)


var target = Vector2(0,0) #x,z target location
var difference = 0 #difference between current angle and goal
var state = "idle" #idle, turning, moving


func _ready():
	pass
	
	

func _physics_process(delta):
	var meshNode = get_node("./PlayerMesh")
	#translation = Vector3(-14, translation.y, -14)
	#print(difference)
	
	if (state == "turning"):
		if (difference < 0):
			meshNode.rotate_y(deg2rad(ROTSPEED))
			difference += ROTSPEED
		elif (difference > 0):
			meshNode.rotate_y(deg2rad(-ROTSPEED))
			difference -= ROTSPEED
		if (abs(difference) < 2):
			state = "moving"
	elif (state == "moving"):
		var direction = Vector3(target.x-translation.x, 0, target.y-translation.z).normalized()
		move_and_slide(direction*SPEED)
		var locationDifference = abs(target.x-translation.x)+abs(target.y-translation.z)
		if (locationDifference < 0.5):
			state = "idle"


	"""
	#print("phyx")
	if (Input.is_action_pressed("ui_right")):
		#velocity.x = SPEED
		rotate_y(deg2rad(-ROTSPEED))
		#$MeshInstance.rotate_y(0.05)
	if (Input.is_action_pressed("ui_left")):
		#velocity.x = -SPEED
		rotate_y(deg2rad(ROTSPEED))
	
	if (Input.is_action_pressed("ui_up")):
		#velocity.z = -SPEED
		var dir = -get_global_transform().basis.z
		velocity = SPEED * dir
		print(get_viewport().get_mouse_position())
		#print(get_viewport().get_global_mouse_position())d

	move_and_slide(velocity)
	
	velocity.x = lerp(velocity.x, 0, 0.1)
	velocity.z = lerp(velocity.z, 0, 0.1)

	pass
	"""

func moveTo(targetLocation):
	var meshNode = get_node("./PlayerMesh")
	var forward = -meshNode.get_global_transform().basis.z
	forward = Vector2(forward.x, forward.z).normalized()

	#translation arvot on kerrottu -1:llä???

	var targetDir = Vector2(targetLocation.x+translation.x, targetLocation.z+translation.z).normalized()


	difference = rad2deg( forward.angle_to(targetDir))
	state = "turning"
	target = -Vector2(targetLocation.x, targetLocation.z)
	#print(targetDir)