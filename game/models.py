from django.contrib.auth.models import User
from django.db import models


class Hero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)

    # progression
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    # core stats
    hp = models.IntegerField(default=100)
    max_hp = models.IntegerField(default=100)
    strenght = models.IntegerField(default=10)
    stats = models.JSONField

    # position & navigation - prawie jak google maps wariacie
    current_map = models
    x_pos = models.IntegerField(default=0)
    y_pos = models.IntegerField(default=0)

    # direction - w ktr strone jestes skierowany
    direction = models.IntegerField(
        default=0, choices=[(0, "North"), (1, "East"), (2, "South"), (3, "West")]
    )

    def move_forward(self):
        # logika
        pass

    def turn(self, direction):
        # logika
        pass

    def __str__(self):
        return f"{self.name} (Lvl {self.level})"


class Item(models.Model):
    RARITY_OPTIONS = [
        ("COMMON", "Common"),
        ("RARE", "Rare"),
        ("EPIC", "Epic"),
        ("LEGENDARY", "Legendary"),
    ]

    ITEM_TYPE = [("WEAPON", "Weapon"), ("ARMOR", "Armor"), ("CONSUMABLE", "Consumable")]

    ITEM_SLOT = [("HEAD", "Head"), ("CHEST", "Chest"), ("HAND", "Hand")]

    name = models.CharField(max_length=100)

    rarity = models.CharField(max_length=20, choices=RARITY_OPTIONS, default="COMMON")
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE)
    item_slot = models.CharField(
        max_length=20, choices=ITEM_SLOT, null=True, blank=True
    )

    stat_bonus = models  # do przekminienia

    def __str__(self):
        return self.name


# na przyszłość:
# dodaj jeszcze jakis validator do dmg żeby nie dało się wpisać nwm -500
# i poczytaj trochę o textchoices dla rarity - przede wszystkim: czy wgl warto to tutaj stosować?


class ItemInInventory(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name="inventory")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.hero.name}: {self.item.name}"


class ItemSlot(models.Model):
    SLOT_CHOICES = [
        ("HEAD", "Head"),
        ("CHEST", "Chest"),
        ("MAIN_HAND", "Main Hand"),
        ("OFF_HAND", "Off Hand"),
    ]
    hero = models.ForeignKey(Hero, related_name="item_slot", on_delete=models.CASCADE)
    slot_name = models.CharField(max_length=20, choices=SLOT_CHOICES)

    item = models.OneToOneField(
        ItemInInventory, related_name="item_slot", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("hero", "slot_name")


# do dodania:
# ograniczenie, że da się trzymać tylko 1 broń na raz
# (aka jak coś wybierzesz - to co już masz wraca do inv)
# rodzaje przedmiotów? nwm może to jakoś ułatwi to wyżej
# "unikalność" przedmiotu - żeby 2 epickie widelce można było od siebie odróżnić


class Map(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name="maps")
    map_level = models.IntegerField()
    width = models.IntegerField(default=10)
    height = models.IntegerField(default=10)

    def __str__(self):
        return f"Map Level {self.map_level} for {self.hero.name}"


class MapTile(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()

    TILE_TYPES = [
        ("EMPTY", "Empty Pathway"),
        ("WALL", "Wall"),
        ("ENEMY", "Enemy Spawn"),
        ("CHEST", "Treasure Chest"),
    ]
    tile_type = models.CharField(max_length=20, choices=TILE_TYPES)
    
    class Meta:
            unique_together = ('map', 'x', 'y')


class Enemy(models.Model):
    map_level = models.ForeignKey(Map, on_delete=models.CASCADE, related_name="enemies")
    type = models.CharField(max_length=50)
    hp = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    verbose_name_plural = "Enemies"

    def __str__(self):
        return f"{self.type} at ({self.x}, {self.y})"
