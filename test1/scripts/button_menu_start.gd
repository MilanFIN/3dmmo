extends Button


func _ready():
	pass


func _on_button_menu_start_pressed():
	var addrs = get_node("../AddressField").get_text()
	var port = get_node("../PortField").get_text()
	#print(addrs)
	global.address = addrs
	global.port = port
	get_tree().change_scene("res://assets/gamecontroller.tscn")


	pass # Replace with function body.
