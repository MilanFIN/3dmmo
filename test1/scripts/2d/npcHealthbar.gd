extends Spatial

var _delta = 0.0

# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _process(delta):
	pass
	var camera = get_viewport().get_camera()
	var point = camera.global_transform.origin
	var mesh = get_node("MeshInstance")
	#mesh.look_at(Vector3(point.x, point.y, point.z), Vector3.UP)
	look_at(point - translation, Vector3.UP)

	print(camera.get_global_transform().basis.z)

	
func setHp(hp, maxHp):
	var fraction = float(hp)/maxHp
	var green = get_node("Viewport/Control/Panel/green")
	var red = get_node("Viewport/Control/Panel/red")
	var maxWidth = red.rect_size.x
	green.rect_size.x = maxWidth * fraction


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
