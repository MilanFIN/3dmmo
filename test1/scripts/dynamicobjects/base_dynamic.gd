extends Spatial

#maximum allowed distance from the new target
const MAXDISTANCE = 3
#maximum strength that the object can be jerked towards the new target
#if the distance is too big
const MAXJERKMULTIPLIER = 5
var speed = 0
var targetX = 0
var targetY = 0
# Declare member variables here. Examples:
# var a = 2
# var b = "text"



# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _physics_process(delta):
	var xDiff = targetX - translation.x
	var yDiff = targetY - translation.z
	
	var direction = Vector2(xDiff, yDiff)
	var totalDiff = direction.length()
	
	
	var dirUnit = direction.normalized()
	
	if (totalDiff < MAXDISTANCE):
		translation.x += delta*dirUnit.x*speed
		translation.z += delta*dirUnit.y*speed
	else:
		translation.x += delta*dirUnit.x*speed * MAXJERKMULTIPLIER
		translation.z += delta*dirUnit.y*speed* MAXJERKMULTIPLIER
	
	
	#translation.x = targetX
	#translation.z = targetY

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
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
