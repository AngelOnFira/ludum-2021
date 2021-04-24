extends Control
onready var websocket_client = get_node("/root/WebsocketClient")

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var card = preload("res://Card.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	websocket_client.connect("new_hand", self, "update_hand")
#	hand = websocket_client.hand
	var new_card = card.instance()
	$V/InventoryGrid/GridContainer/Inv1.add_child(new_card)


func update_hand(hand):
	var hand_slots = [
		$V/InventoryGrid/GridContainer/Inv1,
		$V/InventoryGrid/GridContainer/Inv2,
		$V/InventoryGrid/GridContainer/Inv3,
	]

	for i in range(len(hand)):
		hand_slots[i].update_card(hand[i])
