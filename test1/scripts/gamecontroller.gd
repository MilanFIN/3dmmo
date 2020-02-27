extends Node

var address = 0
var port = 0
var ws
var timer

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
	timer.connect("timeout",self,"_on_timer_timeout") 
	timer.set_wait_time(0.5)
	
	#timeout is what says in docs, in signals
	#self is who respond to the callback
	#_on_timer_timeout is the callback, can have any name
	add_child(timer) #to process
	timer.start() #to start



func _connection_established(protocol):
	print("Connection established with protocol: ", protocol)
	var d = {"action":"login","username":"1", "password":"1"}
	ws.get_peer(1).put_packet(JSON.print(d).to_ascii())
func _connection_closed():
	print("Connection closed")

func _connection_error():
	print("Connection error")

func _physics_process(delta):
	pass
	if (ws):
		pass

func _data_received(p_id = 1):
	var packet = ws.get_peer(1).get_packet().get_string_from_utf8()
	#print(str(peer_id))
	print("got message")
	print(parse_json(packet))

	
func _on_timer_timeout():
	
	timer.start()
	if (ws):
		var node = get_node("./level/playership")
		var x = node.translation.x
		var y = node.translation.z
		var state = node.state
		var d = {"x": x, "y":y, "state":state}
		ws.get_peer(1).put_packet(JSON.print(d).to_ascii())
		ws.poll()
