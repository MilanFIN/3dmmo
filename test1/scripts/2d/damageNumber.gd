extends Spatial


const maxAge = 2.0
var age = 0.0

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	translation.y += 3
	

func _process(delta):
	pass
	var camera = get_viewport().get_camera()
	var point = camera.global_transform.origin
	var mesh = get_node("MeshInstance")
	#mesh.look_at(Vector3(point.x, point.y, point.z), Vector3.UP)
	look_at(point - translation, Vector3.DOWN)
	
	translation.y += delta*2
	
	age += delta
	if (age > maxAge):
		queue_free()
		

func setValue(val):
	get_node("./Viewport/Control/Panel/Label").set_text(val)
	

	

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
