from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _  


class ItemTemplate(models.Model):
    
    class Rarity(models.TextChoices):
        COMMON = 'COMMON', _('Common')
        RARE = 'RARE', _('Rare')
        EPIC = 'EPIC', _('Epic')
        LEGENDARY = 'LEGENDARY', _('Legendary')
            
    class Type(models.TextChoices):
        WEAPON = 'WEAPON', _('Weapon')
        ARMOR = 'ARMOR', _('Armor')
        CONSUMABLE = 'CONSUMABLE', _('Consumable')
    
    
    class Slot(models.TextChoices):
        HEAD = 'HEAD', _('Head')
        CHEST = 'CHEST', _('Chest')
        MAIN_HAND = 'MAIN_HAND', _('Main Hand')
        OFF_HAND = 'OFF_HAND', _('Off Hand')

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    rarity = models.CharField(max_length=20, choices=Rarity.choices, default=Rarity.COMMON)
    type = models.CharField(max_length=20, choices=Type.choices)
    slot = models.CharField(max_length=20, choices=Slot.choices, null=True, blank=True)

    base_strength = models.IntegerField(default=0)
    base_armor = models.IntegerField(default=0)
    base_damage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.get_rarity_display()})" # type: ignore


class ItemInstance(models.Model):
    template = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)
    hero = models.ForeignKey('Hero', on_delete=models.CASCADE, related_name='inventory')
    
    is_equipped = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def equip(self):
        if not self.template.slot:
            return False
         
        current_equiped = ItemInstance.objects.filter(
            hero = self.hero,
            is_equipped = True,
            template__slot = self.template.slot
        ).exclude(id = self.id) #type: ignore
        
        for item in current_equiped:
            item.is_equipped = False
            item.save()

        self.is_equipped = True
        self.save()
        return True
        
    def __str__(self):
        state = "[E]" if self.is_equipped else ""
        return f"{state} {self.template.name}"
        

class Hero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)

    # progression
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    # base stats
    current_hp = models.IntegerField(default=100)
    base_hp = models.IntegerField(default=100)
    base_strength = models.IntegerField(default=10)

    class Direction(models.IntegerChoices):
        NORTH = 0, _('North')
        EAST = 1, _('East')
        SOUTH = 2, _('South')
        WEST = 3, _('West')
    
    # position & navigation - prawie jak google maps wariacie
    current_map = models.ForeignKey('Map', on_delete=models.SET_NULL, null=True)
    x_pos = models.IntegerField(default=0)
    y_pos = models.IntegerField(default=0)
    # direction - w ktr strone jestes skierowany
    direction = models.IntegerField(choices=Direction.choices, default=Direction.NORTH)
    
    def log(self, message):
        GameLog.objects.create(hero=self, message=message)
    
    # ruchy ruchy skrenty
    def turn(self, side):
        # side: 'left' = -1, 'right' = +1
        self.direction = (self.direction + side) % 4
        self.save()

    def move_forward(self):
        dx, dy = 0, 0
        if self.direction == self.Direction.NORTH:
            dy = -1
        elif self.direction == self.Direction.EAST:
            dx = 1
        elif self.direction == self.Direction.SOUTH:
            dy = 1
        elif self.direction == self.Direction.WEST:
            dx = -1
        tx = self.x_pos + dx
        ty = self.y_pos + dy
        
        enemy = Enemy.objects.filter(map_level=self, x=tx, y=ty).first()
        if enemy:
            self.handle_combat(enemy)
            return
        
        tile = self.current_map.tiles.filter(x=tx, y=ty).first()
        if not tile or tile.type == MapTile.TileType.WALL:
            self.log("You can't move forward.")
            return

        if tile.type == MapTile.TileType.CHEST:
            self.handle_loot(tile)
            return
            
        if tile.type == MapTile.TileType.EXIT:
            self.handle_map_level_up() 
            return

        self.x_pos = tx
        self.y_pos = ty
        self.save()
        self.log("You move forward.")

    def handle_combat(self, enemy):
        
        return
        
    def handle_loot(self, tile):
    
        return
        
    def gain_xp(self, amount):

        return

    @property
    def total_strength(self):
        equipment_bonus = self.inventory.filter(is_equipped = True).aggregate(total = models.Sum('template__base_strength'))['total' or 0] # type: ignore
        return self.base_strength + equipment_bonus
        
    def __str__(self):
        return f"{self.name} (Lvl {self.level})"


class Map(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name="maps")
    width = models.IntegerField(default=10)
    height = models.IntegerField(default=10)
    map_level = models.IntegerField()

    def is_valid_position(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        tile = self.tiles.filter(x=x, y=y).first() # type: ignore
        if tile and tile.type == MapTile.TileType.WALL:
            return False
        return False
        
    def __str__(self):
        return f"Map Level {self.map_level} for {self.hero.name}"


class MapTile(models.Model):
    class TileType(models.TextChoices):
        EMPTY = 'EMPTY', _('Empty Pathway')
        WALL = 'WALL', _('Wall')
        EXIT = 'EXIT', _('Level Exit')
        CHEST = 'CHEST', _('Treasure Chest')
        
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name="tiles")
    x = models.IntegerField()
    y = models.IntegerField()

    type = models.CharField(max_length=20, choices=TileType.choices, default=TileType.EMPTY)

    class Meta:
        unique_together = ("map", "x", "y")


class GameLog(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name="logs")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        

class Enemy(models.Model):
    map_level = models.ForeignKey(Map, on_delete=models.CASCADE, related_name="enemies")
    name = models.CharField(max_length=50)
    hp = models.IntegerField()
    damage = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()

    def take_damage(self, amount):
        self.hp -=amount
        if self.hp <= 0:
            return True, "Dead"
        return False, "Alive"
        
    def __str__(self):
        return f"{self.name} at ({self.x}, {self.y})"
