extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var hp = 10

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	

func drawBar(x, y, width, height):
	var color = Color(1.0, 0.0, 0.0)
	
	draw_line(Vector2(10,10), Vector2(100,10), color)
	
	
func _draw():
	var width = 15*hp
	drawBar(0,0,width,0)


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
