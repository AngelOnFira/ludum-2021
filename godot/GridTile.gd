extends TextureRect
onready var base_card = preload("res://Card.tscn")
var filled = false

# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func delete_card():
	if get_node_or_null("Card"):
		var card = get_node("Card")
		remove_child(card)
		card.queue_free()
	filled = false
		
func update_card(card):
	delete_card()
	var new_card = base_card.instance()
	new_card.prepare_card(card)
	add_child(new_card)
	filled = true

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
