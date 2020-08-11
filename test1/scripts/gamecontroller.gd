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

	# PLAYER STATE
	var player = get_node("./level/playership")
	
	#figure out state of movement
	var state = player.state
	var status = {"action":state}
	var angle = player.angle
	if (state == "idle"):
		status["angle"] = str(angle)
		status["x"] = str(player.translation.x)
		status["y"] = str(player.translation.z)
	elif (state == "turning"):
		var targetangle = player.targetAngle
		status["angle"] = str(angle)
		status["targetangle"] = str(targetangle)
	elif (state == "moving"):
		status["angle"] = str(player.angle)
		status["x"] = str(player.translation.x)
		status["y"] = str(player.translation.z)
		status["targetx"] = str(player.target.x)
		status["targety"] = str(player.target.y)

	#figure out state of acting?

	if (player.nextAction()):
		#print(player.actionTarget)
		status["acttarget"] = player.nextActionTarget
		status["actobject"] = player.nextActionObjectType
		status["acttype"] = player.nextActionType
	
	
	ws.get_peer(1).put_packet(JSON.print(status).to_utf8())
	
	# MESSAGE THAT THE PLAYER HAS SENT
	var msgNode = get_node("./level/HUD/SendButton")
	var msg = msgNode.message
	msgNode.message = ""
	if (msg != ""):
		var messageStatus = {"action":"message", "data":msg}
		ws.get_peer(1).put_packet(JSON.print(messageStatus).to_utf8())

	

func handleMessage(message):

	if (not loggedIn):
		if ("auth" in message):
			if (message["auth"] == "accepted"):
				print("logged in")
				loggedIn = true
	else:
		if ("type" in message):
			if (message["type"] == "game"):
				if ("data" in message):
					if ("playerdata" in message["data"]):
						var relevant = message["data"]["playerdata"]
			
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
						#remove disconnected nodes
						for i in others:
							if (not i.name in relevant):
								otherRoot.remove_child(i)
								i.free()
						#update the info on children
						others = otherRoot.get_children()
						#handle stuff regarding other players
						for other in others:
							var name = other.name
							var data = relevant[name]
							#print(name, data)
							other.updateState(data)
						
						
						#handle the player themself
						var player = get_node("./level/playership")
						var inventory = get_node("./level/HUD/Inventory")
						var playerData = relevant[username]
						if ("actobject" in playerData and "acttype" in playerData and "acttarget" in playerData):
							player.clearNextAction()
							player.setCurrentAction(playerData["actobject"], playerData["acttype"], playerData["acttarget"])
						else:
							player.clearCurrentAction()
						if ("inv" in playerData):
							inventory.setItems(playerData["inv"])
						if ("override" in playerData):
							print("stopped action")
							player.forceState(playerData["state"], playerData["x"], playerData["y"])
						if ("hp" in playerData):
							var hpDict = playerData["hp"]
							if ("hp" in hpDict and "maxhp" in hpDict):
								player.setHp(hpDict["hp"], hpDict["maxhp"])

					
					#handle npc's etc
					if ("dynamicdata" in message["data"]):
						var relevant = parse_json(message["data"]["dynamicdata"])
						var dynamicRoot = get_node("./level/DynamicMap")
						var dynamics = dynamicRoot.get_children()
						var existingNames = []
						for o in dynamics:
							existingNames.append(o.name)
						for object in relevant.keys():
							#add objects that don't yet exist
							if (not object in existingNames):
								var dynamicobject = load("res://assets/dynamicobjects/pirate1.tscn")
								var object_instance = dynamicobject.instance()
								object_instance.set_name(object)
								dynamicRoot.add_child(object_instance)
								object_instance.setPosition(relevant[object]["x"], relevant[object]["y"])
								object_instance.setSpeed(relevant[object]["speed"])
								object_instance.setAction(relevant[object]["action"])
								object_instance.setRadius(relevant[object]["radius"])
						#remove disappeared objects
						for i in dynamics:
							if (not i.name in relevant.keys()):
								dynamicRoot.remove_child(i)
								i.free()
						#update all still remaining nodes
						for dynamicobj in dynamicRoot.get_children():
							dynamicobj.updatePosition(relevant[dynamicobj.name]["x"], relevant[dynamicobj.name]["y"])
							if ("hp" in relevant[dynamicobj.name] and "mhp" in relevant[dynamicobj.name]):
								dynamicobj.setHp(relevant[dynamicobj.name]["hp"], relevant[dynamicobj.name]["mhp"])
					if (not "dynamicdata" in message["data"]):
						print("NO OBJECTS")


			#handle chat
			elif (message["type"] == "message"):
				var messageBox = get_node("./level/HUD/MessageBox")
				messageBox.addMessageBatch(message["data"])
			elif (message["type"] == "map"):
				var mapRoot = get_node("./level/StaticMap")
				var mapObjects = mapRoot.get_children()
				for n in mapObjects:
					mapRoot.remove_child(n)
					n.free()
					
					
				var objects = parse_json(message["data"])
				for o in objects:
					var type = objects[o]["type"]
					var x = objects[o]["x"]
					var y = objects[o]["y"]
					var action = objects[o]["action"]
					var radius = objects[o]["radius"]
					var mapObject = load("res://assets/mapobjects/"+type+".tscn")
					var objectInstance = mapObject.instance()
					objectInstance.set_name(o)
					objectInstance.setPos(x, y)
					objectInstance.setAction(action)
					objectInstance.setRadius(radius)
					
					mapRoot.add_child(objectInstance)
					


