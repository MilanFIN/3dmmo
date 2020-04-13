extends Panel

const Item = preload("res://scripts/item.gd");

var style = StyleBoxFlat.new();
const SIZE = 34
var mouseOver = false

func _ready():
	# The Panel doc tells you which style names there are
	rect_min_size = Vector2(SIZE, SIZE)

	rect_size = Vector2(SIZE, SIZE)

	style.set_border_width_all(2)
	set('custom_styles/panel', style)
	set_process(true)
	#style.bg_color = Color("#000000")
	style.border_color = Color("#000000")
	
	
	mouse_filter = Control.MOUSE_FILTER_PASS;
	connect("mouse_entered", self, "_on_mouse_entered")
	connect("mouse_exited", self, "_on_mouse_exited")

func setItem(itemname, iconpath):
	var item = Item.new(itemname, iconpath)
	add_child(item)
	print(item.name)

func clearItem():
	for i in get_children():
		remove_child(i)
		i.free()


func _on_mouse_entered():
	mouseOver = true


func _on_mouse_exited():
	mouseOver = false

func _input(event):
	if event is InputEventMouseButton and event.is_pressed():
		if mouseOver == true:
			print("Clicked On Object")
			var player = get_tree().get_root().get_node("gamecontroller/level/playership")
			player.setNextAction("inventory", "drop", name)

			
			#var player = get_node("./level/playership")

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
