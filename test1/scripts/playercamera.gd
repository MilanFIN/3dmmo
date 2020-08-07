extends Camera

var previousMouseLocation = Vector2(0, 0)
var mouseLocation = Vector2(0,0)
var mouseMoved = false
var mouseInitialized = false
var velocity = Vector3(0,0,0)
var zoomDirection = ""
const ZOOMSPEED = 1
const MINDIST = 5
const MAXDIST = 100
const MOVEPLANESIZE = 1
var canClick = true

func _ready():
	pass
	var node = get_node("../PlayerMesh")
	var up = get_global_transform().basis.y
	look_at(node.translation, up)
	translate_object_local(Vector3(0.0, 0.0, 10)) # initial zoom

func _physics_process(delta):
	#print(cameraLocation, previousCameraLocation)
	var node = get_node("../PlayerMesh")
	if (mouseMoved):
		var mouseMovement = mouseLocation - previousMouseLocation

		#print(mouseMovement)
		mouseMoved = false
		previousMouseLocation = mouseLocation
		
		var targetDir = node.translation - translation
		var distance = targetDir.length()
		translate_object_local(Vector3(0.0, 0.0, -distance)) # temporary zoom in
		rotate_y(deg2rad(-mouseMovement.x))
		var upDir = Vector3(1,0,0)
		rotate_object_local(upDir, deg2rad(-mouseMovement.y))
		var newDir = -get_global_transform().basis.z
		translate_object_local(Vector3(0.0, 0.0, distance)) # tzoom out
	else: #this happens when mouse is moved without pressing the middle mouse button
		# after last movement
		mouseInitialized = false


	if (zoomDirection == "forward"):
		if (abs(node.translation.x - translation.x) + abs(node.translation.y - translation.y) + abs(node.translation.z - translation.z) > MINDIST):
			var dir = -get_global_transform().basis.z
			translation += dir * ZOOMSPEED
			mouseInitialized = false

	elif (zoomDirection == "back"):
		if (abs(node.translation.x - translation.x) + abs(node.translation.y - translation.y) + abs(node.translation.z - translation.z) < MAXDIST):
			var dir = get_global_transform().basis.z
			translation += dir * ZOOMSPEED
			mouseInitialized = false
	velocity = Vector3(0,0,0)
	zoomDirection = ""
	orthonormalize() # repair precision errors


	

func _input(event):
   # Mouse in viewport coordinates
	if event is InputEventMouseButton:
		#print("Mouse Click/Unclick at: ", event.position)
		pass
		#print(get_global_mouse_position())
	if (Input.is_action_pressed("ui_middlemouse")):
		if event is InputEventMouseMotion:
			if (mouseInitialized):
				mouseLocation = event.position
				mouseMoved = true
			else:
				mouseInitialized = true
				mouseMoved = true
				mouseLocation = event.position
				previousMouseLocation = event.position
			pass
	if (event.is_action_pressed("ui_mousewheelup")):
		var dir = -get_global_transform().basis.z
		zoomDirection = "forward"
		#velocity = SPEED * dir
	if (event.is_action_pressed("ui_mousewheeldown")):
		var dir = get_global_transform().basis.z
		zoomDirection = "back"
	if (event.is_action_pressed("ui_mouseleft")):
		if (canClick):
			var position2D = get_viewport().get_mouse_position()
			var point1 = Vector3(-MOVEPLANESIZE,0,-MOVEPLANESIZE)
			var point2 = Vector3(-MOVEPLANESIZE,0,MOVEPLANESIZE)
			var point3 = Vector3(MOVEPLANESIZE,0,-MOVEPLANESIZE)
			var dropPlane = Plane(point1, point2, point3)
			var position3D = dropPlane.intersects_ray(project_ray_origin(position2D),project_ray_normal(position2D))
			if (position3D != null):
				#figure out if the click collides with another object or not
				
				var nodeClicked = false


				if (not nodeClicked):
					var mapRoot = get_tree().get_root().get_node("gamecontroller/level/StaticMap")
					for i in mapRoot.get_children():
						var collShape = i.get_node("./CollisionShape")
						var radius = collShape.shape.radius
						if((i.translation - position3D).length() < radius):
							var actionType = i.action()
							var actionTarget = i.name
							if (actionType != "none"):
								print("actiontype", actionType)
								get_parent().setNextAction("static", actionType, actionTarget)
								nodeClicked = true
								break

				if (not nodeClicked):
					var dynamicRoot = get_tree().get_root().get_node("gamecontroller/level/DynamicMap")
					for i in dynamicRoot.get_children():
						var radius = i.getRadius()
						if ((i.translation - position3D).length()  < radius):
							var actionType = i.action()
							var actionTarget = i.name
							print(actionType, " ", actionTarget)
							get_parent().setNextAction("dynamic", actionType, actionTarget)
							nodeClicked = true
							break

				if (not nodeClicked):
					get_parent().clearNextAction()
					get_parent().clearCurrentAction()


					
				var up = Vector3(0,1,0)
				position3D = -position3D
				get_parent().moveTo(position3D)


func disableClick():
	canClick = false

func enableClick():
	canClick = true
