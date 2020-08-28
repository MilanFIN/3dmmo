extends KinematicBody

const SPEED = 500
const ROTSPEED = 140#70
const MAXANGLEDIFF = 5
var velocity = Vector3(0,0,0)


var hp = 10
var maxHp = 10

var target = Vector2(0,0) #x,z target location

var state = "idle" #idle, turning, moving
var angle = 0

var nextActionType = ""
var nextActionTarget = ""
var nextActionObjectType = ""

var currentActionType = ""
var currentActionTarget = ""
var currentActionObjectType = ""

var laserMaterial = SpatialMaterial.new()


var mapRadius = 200

var blockedTiles = []
var allowedTiles = []
var allowedTileIds = {}
var allowedTilePositions = {}
var astar = AStar.new()

var targetList = []


func _ready():
	laserMaterial.flags_unshaded = true
	laserMaterial.flags_use_point_size = true

	

func _physics_process(delta):
	var meshNode = get_node("./PlayerMesh")
	var collisionNode = get_node("./CollisionShape")
	collisionNode.rotation = meshNode.rotation

	
	

	if (state == "moving"):
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

		if (get_slide_count() != 0):
			state = "idle"

		var locationDifference = abs(target.x-translation.x)+abs(target.y-translation.z)
		if (locationDifference < 0.5):

			if (targetList.size() == 0):
				state = "idle"
			else:
				target = Vector2(targetList[0].x, targetList[0].z)
				targetList.remove(0)
	
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


func simplifyPointPath(points):
	var result = [points[0]]
	var xDir = null
	var yDir = null
	for i in range(1, points.size()):
		if (xDir == null and yDir == null):
			xDir = points[i].x - points[i-1].x
			yDir = points[i].z - points[i-1].z
		else:

			if (i != points.size() - 1):
				var newxDir = points[i].x - points[i-1].x
				var newyDir = points[i].z - points[i-1].z

				if (newxDir != xDir or newyDir != yDir):
					result.append(points[i-1])
					xDir = newxDir
					yDir = newyDir
			else:
				result.append(points[i])

	return result


func drawPathPoints(pathPoints):
	var point_size = 5
	var im = ImmediateGeometry.new()
	get_tree().get_root().add_child(im)
	var m = SpatialMaterial.new()
	m.flags_use_point_size = true
	m.params_point_size = point_size
	im.set_material_override(m)
	im.clear()
	im.begin(Mesh.PRIMITIVE_POINTS, null)
	for p in pathPoints: #list of Vector3s
		im.add_vertex(p)
	im.end()




func moveTo(targetLocation):
	

	var clickTarget = -Vector2(targetLocation.x, targetLocation.z)

	#if current translation is actually closer to a blocked tile, we should find the closest free one in random direction
	var currentPosition = Vector3(int(translation.x), 0, int(translation.z))
	if (not (currentPosition  in allowedTileIds)):
		var offset = []
		for x in range(-1, 1):
			for y in range(-1, 1):	
				offset.push_back([x, y])
		offset.shuffle()
		currentPosition.x += offset[0][0]
		currentPosition.z += offset[0][1]
	
	var targetPosition = Vector3(int(clickTarget.x), 0, int(clickTarget.y))

	if (currentPosition in allowedTileIds and targetPosition in allowedTileIds):
		var pathPoints = astar.get_point_path(allowedTileIds[currentPosition], allowedTileIds[targetPosition])

			
		pathPoints = simplifyPointPath(pathPoints)
		pathPoints.remove(0)


		#drawPathPoints(pathPoints)


		state = "moving"
		if (pathPoints.size() >= 1):
			targetList = pathPoints
			target = Vector2(targetList[0].x, targetList[0].z)
			targetList.remove(0)


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

func setHp(newHp, newMaxHp):
	hp = newHp
	maxHp = newMaxHp
	var hpBar = get_tree().get_root().get_node("gamecontroller/level/HUD/HealthBar")
	hpBar.setHp(hp, maxHp)


func showDamage(damageList):
	if (damageList.size() != 0):
		for damage in damageList:
			var damageObject = load("res://assets/2d/damageNumber.tscn")
			var object_instance = damageObject.instance()
			add_child(object_instance)
			object_instance.setValue(damage)




func bakeNavMesh():
	#startshere
	blockedTiles = []
	allowedTiles = []
	allowedTileIds = {}
	allowedTilePositions = {}

	var staticNodes = get_tree().get_root().get_node("gamecontroller/level/StaticMap").get_children()
	for i in staticNodes:
		var radius = i.getRadius()
		#blockedTiles.append(Vector3(i.translation.x,0, i.translation.z))
		for x in range(-radius, radius):
			for y in range(-radius, radius):
				blockedTiles.append(Vector3(i.translation.x+x,0, i.translation.z+y))
	
	#print(blockedTiles)



	var id = 0
	for x in range(-mapRadius, mapRadius):
		for y in range(-mapRadius, mapRadius):
			var point = Vector3(x,0, y)
			if (not( point in blockedTiles)):
				allowedTiles.append(point)
				allowedTileIds[point] = id
				allowedTilePositions[id] = point
				id += 1

	astar.clear()
	for i in (allowedTiles):
		astar.add_point(allowedTileIds[i], i, 1) # Adds the point (1, 0, 0) with weight_scale 4 and id 1

	for x in range(-mapRadius, mapRadius):
		for y in range(-mapRadius, mapRadius):
			var point = Vector3(x,0, y)
			if (point in allowedTileIds):
				for subx in range (-1, 1):
					for suby in range(-1, 1):
						if (subx != 0 || suby != 0):
							var newPoint = Vector3(point.x+subx, 0, point.z+suby)
							if (newPoint in allowedTileIds):
								astar.connect_points(allowedTileIds[point], allowedTileIds[newPoint], true)
		
	#endshere

func _on_hud_mouse_entered():
	var camera = get_node("./Camera")
	camera.disableClick()
	pass # Replace with function body.


func _on_hud_mouse_exited():
	var camera = get_node("./Camera")
	camera.enableClick()
	pass # Replace with function body.
