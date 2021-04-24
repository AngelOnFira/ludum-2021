from django.db import models

# Create your models here.
class ClickTracker(models.Model):
    click_count = models.IntegerField()

COLORS = (
    (0, 'red'),
    (1, 'greed'),
    (2, 'blue'),
)

class Card(models.Model):
    left = models.IntegerField(default=0, choices=COLORS)