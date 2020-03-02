extends Node

var address = 0
var port = 0
var ws
var timer
var loggedIn = false
var outBoundMessage = {}
var username = global.username
var otherPlayers = []


func _ready():
	address = global.address
	port = global.port
	
	ws = WebSocketClient.new()
	ws.connect("connection_established", self, "_connection_established")
	ws.connect("connection_closed", self, "_connection_closed")
	ws.connect("connection_error", self, "_connection_error")

	ws.connect("data_received", self, "_data_received")
	var url = "ws://"+address+":"+port
	print("Connecting to " + url)
	ws.connect_to_url(url)
	
	
	
	timer = Timer.new()
	timer.connect("timeout",self,"sendState") 
	timer.set_wait_time(0.5)
	
	#timeout is what says in docs, in signals
	#self is who respond to the callback
	#_on_timer_timeout is the callback, can have any name
	add_child(timer) #to process
	timer.start() #to start



func _connection_established(protocol):
	print("Connection established with protocol: ", protocol)
	var d = {"action":"login","username":global.username, "password":global.password}
	ws.get_peer(1).put_packet(JSON.print(d).to_ascii())
func _connection_closed():
	print("Connection closed")

func _connection_error():
	print("Connection error")

func _physics_process(delta):
	if (ws):
		pass
	


func _data_received(p_id = 1):
	var packet = ws.get_peer(1).get_packet().get_string_from_utf8()

	handleMessage(parse_json(packet))
	
	

	
func sendState():
	ws.poll()
	timer.start()

	if (not loggedIn):
		return

	var player = get_node("./level/playership")
	var state = player.state
	var status = {"action":state}
	var angle = player.angle
	if (state == "idle"):
		status["angle"] = str(angle)
	elif (state == "turning"):
		var targetangle = player.targetAngle
		status["angle"] = str(angle)
		status["targetangle"] = str(targetangle)
	elif (state == "moving"):
		status["x"] = str(player.translation.x)
		status["y"] = str(player.translation.z)


	ws.get_peer(1).put_packet(JSON.print(status).to_utf8())
	
	"""
	if (ws):
		var node = get_node("./level/playership")
		var x = node.translation.x
		var y = node.translation.z
		var state = node.state
		var d = {"x": x, "y":y, "state":state}
		ws.get_peer(1).put_packet(JSON.print(d).to_ascii())
		ws.poll()
	"""


func handleMessage(message):

	if (not loggedIn):
		if ("auth" in message):
			if (message["auth"] == "accepted"):
				print("logged in")
				loggedIn = true
	else:
		if ("data" in message):
			var relevant = message["data"]

			var otherRoot = get_node("./level/OtherPlayers")
			var others = otherRoot.get_children()
			var existingNames = []
			for o in others:
				existingNames.append(o.name)

			#add nodes that have connected since last tick
			for person in relevant:
				if (person != username):
					if (not person in existingNames):

						var otherplayer = load("res://assets/otherplayer.tscn")
						var other_instance = otherplayer.instance()
						other_instance.set_name(person)
						otherRoot.add_child(other_instance)
						print("lisätään")
			#remove nodes that have disconnected
			for i in range(others.size() - 1, -1, -1):
				if (not others[i].name in relevant):
					otherRoot.remove_child(others[i])
					print("poistetaan") 
			#update the info on children
			others = otherRoot.get_children()
			#handle stuff regarding other players
			for other in others:
				var name = other.name
				var data = relevant[name]
				#print(name, data)
				other.updateState(data)
			#handle the player themself
			var playerData = relevant[username]
			#print(playerData)
