extends Node

var address = 0
var port = 0
var ws

func _ready():
	address = global.address
	port = global.port
	
	ws = WebSocketClient.new()
	ws.connect("connection_established", self, "_connection_established")
	ws.connect("connection_closed", self, "_connection_closed")
	ws.connect("connection_error", self, "_connection_error")

	var url = "ws://"+address+":"+port
	print("Connecting to " + url)
	ws.connect_to_url(url)


func _connection_established(protocol):
	print("Connection established with protocol: ", protocol)

func _connection_closed():
	print("Connection closed")

func _connection_error():
	print("Connection error")

func _physics_process(delta):
	pass
	if (ws):
		ws.poll()
