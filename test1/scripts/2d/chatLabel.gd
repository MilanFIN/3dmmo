extends Spatial


const MAXLENGTH = 80
const MAXAGE = 5.0
var msgAge = 0.0



# Called when the node enters the scene tree for the first time.
func _ready():
	var label = get_node("Viewport/Control/Panel/Label")
	label.text = ""

func _process(delta):
	#rotate towards camera
	var camera = get_viewport().get_camera()
	var point = camera.global_transform.origin
	var mesh = get_node("MeshInstance")
	#mesh.look_at(Vector3(point.x, point.y, point.z), Vector3.UP)
	look_at(point - translation, Vector3.DOWN)
	
	#keepalive for the latest msg
	var label = get_node("Viewport/Control/Panel/Label")
	if (label.text != ""):
		msgAge += delta
		if (msgAge >= MAXAGE):
			label.text = ""

func setMessage(msg):
	if (len(msg) > MAXLENGTH):
		msg = msg.left(MAXLENGTH)
	var label = get_node("Viewport/Control/Panel/Label")
	label.text = msg
	msgAge = 0.0

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
