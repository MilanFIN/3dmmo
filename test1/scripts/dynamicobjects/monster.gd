extends "res://scripts/dynamicobjects/base_dynamic.gd"

var lastHp = 0

# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	#initialize health bar to display full hp at first
	var healthBar = get_node("HealthBar")
	healthBar.setHp(1,1)

func setHp(hp, maxHp):
	if (hp != lastHp):
		var healthBar = get_node("HealthBar")
		healthBar.setHp(hp, maxHp)
		lastHp = hp


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
