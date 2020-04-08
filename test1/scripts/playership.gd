extends KinematicBody

const SPEED = 500
const ROTSPEED = 70
var velocity = Vector3(0,0,0)


var target = Vector2(0,0) #x,z target location
var difference = 0 #difference between current angle and goal
var state = "idle" #idle, turning, moving
var angle = 0
var targetAngle = 0
var nextActionType = ""
var nextActionTarget = ""
var nextActionObjectType = ""

var currentActionType = ""
var currentActionTarget = ""
var currentActionObjectType = ""

var laserMaterial = SpatialMaterial.new()
func _ready():
	laserMaterial.flags_unshaded = true
	laserMaterial.flags_use_point_size = true

	

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
	
	if (currentActionType == "mine"):
		var laser = get_node("./Laser")
		laserMaterial.albedo_color = Color.orange
		var targetPos = Vector3(0,0,0)
		var mapRoot = get_tree().get_root().get_node("gamecontroller/level/StaticMap")
		if (mapRoot.has_node(currentActionTarget)):
			var target = mapRoot.get_node(currentActionTarget)
			targetPos = target.translation - translation
		laser.set_material_override(laserMaterial)
		laser.clear()
		laser.begin(Mesh.PRIMITIVE_LINE_STRIP, null)
		laser.add_vertex(Vector3(0,0,0))
		laser.add_vertex(targetPos)
		laser.end()

	else:
		var laser = get_node("./Laser")
		laser.clear()


func moveTo(targetLocation):
	var meshNode = get_node("./PlayerMesh")
	var forward = meshNode.get_global_transform().basis.z
	forward = Vector2(forward.x, forward.z).normalized()

	#translation arvot on kerrottu -1:llä???

	var targetDir = Vector2(targetLocation.x+translation.x, targetLocation.z+translation.z).normalized()


	difference = rad2deg( forward.angle_to(targetDir))
	state = "turning"
	target = -Vector2(targetLocation.x, targetLocation.z)
	
	targetAngle = angle - difference

func nextAction():
	if (nextActionType != "" and nextActionTarget != "" and nextActionObjectType != ""):
		return true
	else:
		return false

func setNextAction(objtype, actiontype, target):
	nextActionType = actiontype
	nextActionTarget = target
	nextActionObjectType = objtype

func clearNextAction():
	nextActionType = ""
	nextActionTarget = ""
	nextActionObjectType = ""
	
func setCurrentAction(objtype, actiontype, target):
	currentActionType = actiontype
	currentActionTarget = target
	currentActionObjectType = objtype

func clearCurrentAction():
	currentActionType = ""
	currentActionTarget = ""
	currentActionObjectType = ""

func forceState(newState, x = null, y = null):
	if (x != null):
		translation.x = float(x)
	if (y != null):
		translation.z = float(y)
	state = newState


func _on_hud_mouse_entered():
	var camera = get_node("./Camera")
	camera.disableClick()
	pass # Replace with function body.


func _on_hud_mouse_exited():
	var camera = get_node("./Camera")
	camera.enableClick()
	pass # Replace with function body.
