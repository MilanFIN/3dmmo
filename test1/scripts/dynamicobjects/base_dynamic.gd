extends Spatial

#maximum allowed distance from the new target
const MAXDISTANCE = 3
#maximum strength that the object can be jerked towards the new target
#if the distance is too big
const MAXJERKMULTIPLIER = 5
const ROTSPEED = 70
var speed = 0
var radius = 1
var actionType = ""

var targetX = 0
var targetY = 0
# Declare member variables here. Examples:
# var a = 2
# var b = "text"



# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _physics_process(delta):
	
	if (speed != 0):
		var meshNode = get_node("./MeshInstance")
		
		var xDiff = targetX - translation.x
		var yDiff = targetY - translation.z
		
		var direction = Vector2(xDiff, yDiff)
	
		var totalDiff = direction.length()
		
		
		var dirUnit = direction.normalized()
		
	
		var forward = -meshNode.get_global_transform().basis.z
		forward = Vector2(forward.x, forward.z).normalized()
		var angleDiff = forward.angle_to(dirUnit)
		
	
		if (angleDiff < 0):
			meshNode.rotate_y(deg2rad(ROTSPEED*delta))
		else:
			meshNode.rotate_y(deg2rad(-ROTSPEED*delta))
		#meshNode.rotate_y(deg2rad(ROTSPEED*delta))
	
		if (totalDiff < MAXDISTANCE):
			translation.x += delta*dirUnit.x*speed
			translation.z += delta*dirUnit.y*speed
		else:
			translation.x += delta*dirUnit.x*speed * MAXJERKMULTIPLIER
			translation.z += delta*dirUnit.y*speed* MAXJERKMULTIPLIER
		
	

func setPosition(x, y):
	translation.x = x
	translation.z = y
	targetX = x
	targetY = y

func updatePosition(x, y):
	targetX = x
	targetY = y

func setSpeed(s):
	speed = float(s) / global.tickrate

func setRadius(r):
	radius = float(r)

func getRadius():
	return radius

func setAction(a):
	actionType = a

func action():
	return actionType

#predefinition for derived classes
func setHp(hp, maxHp):
	pass
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
