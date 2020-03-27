extends KinematicBody

const SPEED = 500
const ROTSPEED = 70
var velocity = Vector3(0,0,0)


var target = Vector2(0,0) #x,z target location
var difference = 0 #difference between current angle and goal
var state = "idle" #idle, turning, moving
var angle = 0
var targetAngle = 0



func _ready():
	pass

	

func _physics_process(delta):
	var meshNode = get_node("./PlayerMesh")
	var collisionNode = get_node("./CollisionShape")
	collisionNode.rotation = meshNode.rotation
	angle = rad2deg(meshNode.rotation.y)

	#translation = Vector3(-14, translation.y, -14)
	#print(difference)
	
	if (state == "turning"):
		if (difference < 0):
			meshNode.rotate_y(deg2rad(ROTSPEED*delta))
			difference += ROTSPEED*delta
		elif (difference > 0):
			meshNode.rotate_y(deg2rad(-ROTSPEED*delta))
			difference -= ROTSPEED*delta
		if (abs(difference) < 2):
			state = "moving"
	elif (state == "moving"):
		var direction = Vector3(target.x-translation.x, 0, target.y-translation.z).normalized()
		move_and_slide(direction*SPEED*delta)

		if (get_slide_count() != 0):
			state = "idle"

		var locationDifference = abs(target.x-translation.x)+abs(target.y-translation.z)
		if (locationDifference < 0.5):
			state = "idle"



func moveTo(targetLocation):
	var meshNode = get_node("./PlayerMesh")
	var forward = -meshNode.get_global_transform().basis.z
	forward = Vector2(forward.x, forward.z).normalized()

	#translation arvot on kerrottu -1:llä???

	var targetDir = Vector2(targetLocation.x+translation.x, targetLocation.z+translation.z).normalized()


	difference = rad2deg( forward.angle_to(targetDir))
	state = "turning"
	target = -Vector2(targetLocation.x, targetLocation.z)
	
	targetAngle = angle - difference
	
	#print(targetDir)


func _on_hud_mouse_entered():
	var camera = get_node("./Camera")
	camera.disableClick()
	pass # Replace with function body.


func _on_hud_mouse_exited():
	var camera = get_node("./Camera")
	camera.enableClick()
	pass # Replace with function body.
