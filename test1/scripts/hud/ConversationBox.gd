extends Panel


# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func setVisible(visibility):
	visible = visibility
	if (visibility == false):
		_on_ConversationBox_mouse_exited()



func _on_ConversationBox_mouse_entered():
	get_tree().get_root().get_node("gamecontroller/level/playership/Camera").disableClick()


func _on_ConversationBox_mouse_exited():
	get_tree().get_root().get_node("gamecontroller/level/playership/Camera").enableClick()


func _on_NextButton_pressed():
	var player = get_tree().get_root().get_node("gamecontroller/level/playership")
	player.setNextAction("conversation", "next", "none")
