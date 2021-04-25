from rest_framework import serializers
from chat.models import Card, COLORS


class CardSerializer(serializers.ModelSerializer):
    left = serializers.CharField(source="get_left_display")
    right = serializers.CharField(source="get_right_display")
    up = serializers.CharField(source="get_up_display")
    down = serializers.CharField(source="get_down_display")
    main = serializers.CharField(source="get_main_display")

    class Meta:
        model = Card
        fields = ["left", "right", "up", "down", "main", "id"]