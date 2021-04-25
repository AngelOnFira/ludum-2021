from django.db import models


COLORS = (
    (0, "red"),
    (1, "green"),
    (2, "blue"),
)


class Player(models.Model):
    score = models.IntegerField(default=0)
    # slot_1 = models.OneToOneField(Card, on_delete=models.CASCADE)
    # slot_2 = models.OneToOneField(Card, on_delete=models.CASCADE)
    # slot_3 = models.OneToOneField(Card, on_delete=models.CASCADE)
    # slot_4 = models.OneToOneField(Card, on_delete=models.CASCADE)
    # slot_5 = models.OneToOneField(Card, on_delete=models.CASCADE)
    # slot_6 = models.OneToOneField(Card, on_delete=models.CASCADE)
    # slot_7 = models.OneToOneField(Card, on_delete=models.CASCADE)
    # slot_8 = models.OneToOneField(Card, on_delete=models.CASCADE)
    # slot_9 = models.OneToOneField(Card, on_delete=models.CASCADE)


class Card(models.Model):
    left = models.IntegerField(default=0, choices=COLORS)
    right = models.IntegerField(default=0, choices=COLORS)
    up = models.IntegerField(default=0, choices=COLORS)
    down = models.IntegerField(default=0, choices=COLORS)
    main = models.IntegerField(default=0, choices=COLORS)

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    slot = models.IntegerField(default=30)