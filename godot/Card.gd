extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var selected = false
var last_mouse = Vector2()
var new_mouse = Vector2()

var colors = {
	"red": Color(1,0,0),
	"green": Color(0,1,0),
	"blue": Color(0,0,1)
}

# Called when the node enters the scene tree for the first time.
func _ready():
	return
	prepare_card({
		"left": "red",
		"right": "green",
		"up": "blue",
		"down": "green",
		"card": "blue"
	})

func prepare_card(input):
	$Panel/Arrows/ArrowLeft.modulate = colors[input["left"]]
	$Panel/Arrows/ArrowRight.modulate = colors[input["right"]]
	$Panel/Arrows/ArrowUp.modulate = colors[input["up"]]
	$Panel/Arrows/ArrowDown.modulate = colors[input["down"]]
	
	$Panel/CardColor.color = colors[input["card"]]
	
func _process(_delta):
	if selected:
		new_mouse = get_viewport().get_mouse_position()
		position -= (last_mouse - new_mouse)
		last_mouse = new_mouse

func _on_CardArea_input_event(_viewport, event, _shape_idx):
	if event is InputEventMouseButton:
		if event.is_pressed():
			print("tset")
			selected = true
			last_mouse = get_viewport().get_mouse_position()
			z_index = 10
		else:
			z_index = 0
			selected = false
			var collisions = $CardArea.get_overlapping_areas()
			if collisions.size():
				var distance_dict = {}
				print(collisions)
				var current_position = get_parent().get_node("CardPlaceArea").global_position
				for collision in collisions:
					var new_parent = collision.get_parent()
					if new_parent is TextureRect and !new_parent.filled:
						var second_position = new_parent.get_node("CardPlaceArea").global_position
						print(current_position, "", second_position)
						distance_dict[current_position.distance_squared_to(second_position)] = new_parent
				
				print(distance_dict)
				if distance_dict.keys().size():
					var new_parent = distance_dict[distance_dict.keys().max()]
					get_parent().filled = false
					get_parent().remove_child(self)
					new_parent.add_child(self)
					new_parent.filled = true
				
			print(get_parent())
			set_position(get_parent().get_node("CardPlaceArea").position + Vector2(5, 5))
			print("real ", get_parent().get_node("CardPlaceArea").position)

