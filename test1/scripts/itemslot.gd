extends Panel

const Item = preload("res://scripts/item.gd");

var style = StyleBoxFlat.new();
const SIZE = 34

func _ready():
	# The Panel doc tells you which style names there are
	rect_min_size = Vector2(SIZE, SIZE)

	rect_size = Vector2(SIZE, SIZE)

	style.set_border_width_all(2)
	set('custom_styles/panel', style)
	set_process(true)
	#style.bg_color = Color("#000000")
	style.border_color = Color("#000000")



func setItem(itemname, iconpath):
	var item = Item.new(itemname, iconpath)
	add_child(item)
	print(item.name)

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
