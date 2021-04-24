extends Control


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

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

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
