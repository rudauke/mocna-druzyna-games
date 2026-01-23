from django.db import models
from django.contrib.auth.models import User

class Hero(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hp = models.IntegerField(default=100)
    max_hp = models.IntegerField(default=100)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    x_pos = models.IntegerField(default=0)
    y_pos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Lvl {self.level})"
    
class Item(models.Model):
    RARITY_OPTIONS = [
        ('COMMON', 'Common'),
        ('RARE', 'Rare'),
        ('EPIC', 'Epic'),
        ('LEGENDARY', 'Legendary'),
    ]

    name = models.CharField(max_length=100)
    damage = models.IntegerField(default=1)
    rarity = models.CharField(max_length=20, choices=RARITY_OPTIONS, default='COMMON')

    def __str__(self):
        return f"{self.name} ({self.get_rarity_display().upper()}) - DMG: {self.damage}" # overkill?

# na przyszłość:
# dodaj jeszcze jakis validator do dmg żeby nie dało się wpisać nwm -500
# i poczytaj trochę o textchoices dla rarity - przede wszystkim: czy wgl warto to tutaj stosować?

class InventorySlot(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_equipped = models.BooleanField(default=False)

    def __str__(self):
        status = "[Equipped]" if self.is_equipped else ""
        return f"{self.hero.name}: {self.item.name} {status}"

# do dodania:
# ograniczenie, że da się trzymać tylko 1 broń na raz
# (aka jak coś wybierzesz - to co już masz wraca do inv)
# rodzaje przedmiotów? nwm może to jakoś ułatwi to wyżej
# "unikalność" przedmiotu - żeby 2 epickie widelce można było od siebie odróżnić
<<<<<<< Updated upstream
=======

class Map(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name='maps')
    level_number = models.IntegerField()
    layout_data = models.JSONField(default=dict, help_text="JSON struktura granic mapy")

    def __str__(self):
        return f"Map Level {self.level_number} for {self.hero.name}"

class Enemy(models.Model):
    map_level = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='enemies')
    type = models.CharField(max_length=50)
    hp = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    verbose_name_plural = "Enemies"

    def __str__(self):
        return f"{self.type} at ({self.x}, {self.y})"

>>>>>>> Stashed changes
