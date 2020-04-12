extends Panel

const MAXSLOTS = 20
const ItemSlot = preload("res://scripts/itemslot.gd");


const itemIcons = {
	"uranium": preload("res://assets/itemicons/uranium.png")
}


var itemSlots = []

# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	
	var ItemGrid = get_node("./Grid")
	var offset = 8
	for i in range(MAXSLOTS):
		var slot = ItemSlot.new()
		ItemGrid.add_child(slot)
		itemSlots.push_back(slot)
		

		slot.setItem("uranium", itemIcons["uranium"])



func setItems(items):
	
	for i in itemSlots:
		i.clearItem()
	for i in range (0, len(items)):
		if (i < MAXSLOTS):
			itemSlots[i].setItem(items[i], itemIcons[items[i]])



# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
