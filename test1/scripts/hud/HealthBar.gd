extends Node2D

const X = 10
const Y = 10
const HEIGHT = 20


var hp = 10
var maxHp = 10
var maxWidth = 200



# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	

func drawBar(width):
	var color = PoolColorArray([Color(1.0, 0.0, 0.0)])
	var points = PoolVector2Array()
	points.push_back(Vector2(X,Y))
	points.push_back(Vector2(X+width,Y))
	points.push_back(Vector2(X+width,Y+HEIGHT))
	points.push_back(Vector2(X,Y+HEIGHT))

	draw_polygon(points, color)
	#draw_line(Vector2(10,10), Vector2(100,10), color)
	
	
func _draw():
	var width = hp/maxHp*maxWidth
	drawBar(width)

func _process(delta):
	update()

func setHp(health, maxHealth):
	hp = health
	maxHp = maxHealth


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
