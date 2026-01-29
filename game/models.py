import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class MapTile(models.Model):
    class TileType(models.TextChoices):
        EMPTY = "EMPTY", _("Empty Pathway")
        WALL = "WALL", _("Wall")
        EXIT = "EXIT", _("Level Exit")
        CHEST = "CHEST", _("Treasure Chest")

    map = models.ForeignKey("Map", on_delete=models.CASCADE, related_name="tiles")
    x = models.IntegerField()
    y = models.IntegerField()

    type = models.CharField(
        max_length=20, choices=TileType.choices, default=TileType.EMPTY
    )

    class Meta:
        unique_together = ("map", "x", "y")


class Map(models.Model):
    hero = models.ForeignKey("Hero", on_delete=models.CASCADE, related_name="maps")
    width = models.IntegerField(default=10)
    height = models.IntegerField(default=10)
    map_level = models.IntegerField(default=1)

    @classmethod
    def create_map(cls, hero, width, height, map_level):
        new_map = cls.objects.create(
            hero=hero, width=width, height=height, map_level=map_level
        )

        walls = []
        floors = []

        for x in range(width):
            for y in range(height):
                if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                    walls.append((x, y))
                else:
                    floors.append((x, y))

        start_pos, end_pos = random.sample(floors, 2)

        floors.remove(start_pos)
        floors.remove(end_pos)

        tiles_to_create = []

        for x, y in walls:
            tiles_to_create.append(
                MapTile(map=new_map, x=x, y=y, type=MapTile.TileType.WALL)
            )
        for x, y in floors:
            tiles_to_create.append(
                MapTile(map=new_map, x=x, y=y, type=MapTile.TileType.EMPTY)
            )

        tiles_to_create.append(
            MapTile(
                map=new_map, x=start_pos[0], y=start_pos[1], type=MapTile.TileType.EMPTY
            )
        )

        tiles_to_create.append(
            MapTile(map=new_map, x=end_pos[0], y=end_pos[1], type=MapTile.TileType.EXIT)
        )

        MapTile.objects.bulk_create(tiles_to_create)

        new_map.spawn_enemies(floors, map_level)
        new_map.spawn_loot(floors)

        hero.current_map = new_map
        hero.x_pos = start_pos[0]
        hero.y_pos = start_pos[1]
        hero.save()

        return new_map

    def spawn_enemies(self, available_tiles, map_level):
        count = random.randint(3, (5 + map_level))

        count = min(count, len(available_tiles))

        chosen_tiles = random.sample(available_tiles, count)

        enemies_to_create = []
        for x, y in chosen_tiles:
            hp = 20 + 10 * (map_level)
            damage = 2 + (2 * map_level)
            enemies_to_create.append(
                Enemy(map_level=self, name="Gamoń", x=x, y=y, hp=hp, damage=damage)
            )

        Enemy.objects.bulk_create(enemies_to_create)

    def spawn_loot(self, available_tiles):
        if available_tiles and random.random() < 0.2:
            loot_location = random.choice(available_tiles)

            tile = self.tiles.get(x=loot_location[0], y=loot_location[1])  # type: ignore
            tile.type = MapTile.TileType.CHEST
            tile.save()

    def __str__(self):
        return f"Map Level {self.map_level} for {self.hero.name}"


class Enemy(models.Model):
    map_level = models.ForeignKey(Map, on_delete=models.CASCADE, related_name="enemies")
    name = models.CharField(max_length=50)
    hp = models.IntegerField()
    damage = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            return True, "Dead"
        return False, "Alive"

    def __str__(self):
        return f"{self.name} at ({self.x}, {self.y})"


class ItemTemplate(models.Model):
    class Rarity(models.TextChoices):
        COMMON = "COMMON", _("Common")
        RARE = "RARE", _("Rare")
        EPIC = "EPIC", _("Epic")
        LEGENDARY = "LEGENDARY", _("Legendary")

    class Type(models.TextChoices):
        WEAPON = "WEAPON", _("Weapon")
        ARMOR = "ARMOR", _("Armor")
        CONSUMABLE = "CONSUMABLE", _("Consumable")

    class Slot(models.TextChoices):
        HEAD = "HEAD", _("Head")
        CHEST = "CHEST", _("Chest")
        MAIN_HAND = "MAIN_HAND", _("Main Hand")
        OFF_HAND = "OFF_HAND", _("Off Hand")

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    rarity = models.CharField(
        max_length=20, choices=Rarity.choices, default=Rarity.COMMON
    )
    type = models.CharField(max_length=20, choices=Type.choices)
    slot = models.CharField(max_length=20, choices=Slot.choices, null=True, blank=True)

    base_strength = models.IntegerField(default=0)
    base_defense = models.IntegerField(default=0)
    base_damage = models.PositiveIntegerField(default=0)
    base_hp = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.get_rarity_display()})"  # type: ignore


class ItemInstance(models.Model):
    hero = models.ForeignKey("Hero", on_delete=models.CASCADE, related_name="inventory")
    template = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)

    is_equipped = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def equip(self):
        if not self.template.slot:
            return False

        current_equipped = ItemInstance.objects.filter(
            hero=self.hero, is_equipped=True, template__slot=self.template.slot
        ).exclude(id=self.id)  # type: ignore

        for item in current_equipped:
            item.is_equipped = False
            item.save()

        self.is_equipped = True
        self.save()
        return True

    def __str__(self):
        state = "[E]" if self.is_equipped else ""
        return f"{state} {self.template.name}"


class GameLog(models.Model):
    hero = models.ForeignKey("Hero", on_delete=models.CASCADE, related_name="logs")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


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
    base_defense = models.IntegerField(default=10)

    # position & navigation - prawie jak google maps wariacie
    # direction - w ktr strone jestes skierowany
    class Direction(models.IntegerChoices):
        NORTH = 0, _("North")
        EAST = 1, _("East")
        SOUTH = 2, _("South")
        WEST = 3, _("West")

    current_map = models.ForeignKey(
        Map,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="heroes_on_map",
    )
    x_pos = models.IntegerField(default=0)
    y_pos = models.IntegerField(default=0)
    direction = models.IntegerField(choices=Direction.choices, default=Direction.NORTH)

    def log(self, message):
        GameLog.objects.create(hero=self, message=message)

    # ruchy ruchy skrenty
    def turn(self, side):
        # left = -1, right = +1
        self.direction = (self.direction + side) % 4
        self.save()

    # logika ruchu - rozsyla w odpowiednie miejsca w zaleznosci co przed tb
    # oblicza target tile - pozycja x, y klocka przed tb
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

        # sprawdza czy jest tam do ubicia chlop jakis
        enemy = Enemy.objects.filter(map_level=self.current_map, x=tx, y=ty).first()
        if enemy:
            self.handle_combat(enemy)
            return

        # sprawdza jakiego typu jest klocek
        tile = self.current_map.tiles.filter(x=tx, y=ty).first()
        if not tile or tile.type == MapTile.TileType.WALL:
            self.log("You can't move forward.")
            return

        if tile.type == MapTile.TileType.CHEST:
            self.handle_loot(tile)
            return

        if tile.type == MapTile.TileType.EXIT:
            self.handle_map_next_level()
            return

        # pusty klocek - idziesz w przod
        self.x_pos = tx
        self.y_pos = ty
        self.save()
        self.log("You move forward.")

    def handle_combat(self, enemy):
        dmg_dealt = max(1, self.total_strength)
        is_dead, status = enemy.take_damage(dmg_dealt)

        # is_dead = T
        if is_dead:
            # enemy uwalony + exp
            enemy.delete()
            xp_gain = 20 * self.current_map.map_level  # balance - exp gain logic
            self.gain_xp(xp_gain)
            self.log(f"You defeated {enemy.name}!")

        # is_dead = F
        else:
            enemy.save()
            self.log(f"You dealt {dmg_dealt} damage to the enemy.")

            dmg_taken = max(0, enemy.damage - self.total_defense)
            self.current_hp -= dmg_taken
            self.save()
            self.log(f"You took {dmg_taken} damage.")

            if self.current_hp <= 0:
                self.log("YOU DIED")
                # game restart logic / self.handle_player_death()

        return

    def handle_loot(self, tile):
        templates = ItemTemplate.objects.all()
        if templates.exists():
            found_item = random.choice(templates)
            ItemInstance.objects.create(hero=self, template=found_item)
            self.log(f"You found {found_item.name}!")
        else:
            self.log("No items to loot.")
        tile.type = MapTile.TileType.EMPTY
        tile.save()

    def handle_map_next_level(self):
        self.log("You have found an exit...")

        next_map_level = self.current_map.map_level + 1

        new_map = Map.create_map(
            self,
            self.current_map.width,
            self.current_map.height,
            map_level=next_map_level,
        )

        self.log(f"You entered Map Level {next_map_level}.")

    def gain_xp(self, amount):
        self.xp += amount

        threshold = self.level * 100
        if self.xp >= threshold:
            self.level += 1
            self.xp -= threshold
            self.base_hp += 10
            self.current_hp = self.max_hp
            self.base_strength += 2
        return

    @property
    def total_strength(self):
        equipment_bonus = self.inventory.filter(is_equipped=True).aggregate(  # type: ignore
            total=models.Sum("template__base_strength")
        )  # type: ignore
        return self.base_strength + (equipment_bonus["total"] or 0)

    @property
    def total_defense(self):
        equipment_bonus = self.inventory.filter(is_equipped=True).aggregate(  # type: ignore
            total=models.Sum("template__base_defense")
        )  # type: ignore
        return self.base_defense + (equipment_bonus["total"] or 0)

    @property
    def max_hp(self):
        equipment_bonus = self.inventory.filter(is_equipped=True).aggregate(  # type: ignore
            total=models.Sum("template__base_hp")
        )  # type: ignore
        return self.base_hp + (equipment_bonus["total"] or 0)

    # funkcja pomocnicza do get_visible_tiles, get_nearby_enemies
    def get_view_coords(self):
        x, y = self.x_pos, self.y_pos

        if self.direction == self.Direction.NORTH:
            return {
                "current": (x, y),
                "front": (x, y - 1),
                "left": (x - 1, y),
                "right": (x + 1, y),
            }
        elif self.direction == self.Direction.EAST:
            return {
                "current": (x, y),
                "front": (x + 1, y),
                "left": (x, y - 1),
                "right": (x, y + 1),
            }
        elif self.direction == self.Direction.SOUTH:
            return {
                "current": (x, y),
                "front": (x, y + 1),
                "left": (x + 1, y),
                "right": (x - 1, y),
            }
        elif self.direction == self.Direction.WEST:
            return {
                "current": (x, y),
                "front": (x - 1, y),
                "left": (x, y + 1),
                "right": (x, y - 1),
            }
        return {}

    def get_visible_tiles(self):
        if not self.current_map:
            return {}

        view_coords = self.get_view_coords()

        visible_tiles = {}

        for view, (vx, vy) in view_coords.items():
            tile = self.current_map.tiles.filter(x=vx, y=vy).first()
            visible_tiles[view] = tile.type

        return visible_tiles

    def get_nearby_enemies(self):
        view_coords = self.get_view_coords()
        view_locations = list(view_coords.values())
        all_enemies = self.current_map.enemies.all()
        visible_enemies = []

        for enemy in all_enemies:
            if (enemy.x, enemy.y) in view_locations:
                visible_enemies.append(enemy)

        return visible_enemies

    def get_recent_logs(self, limit=10):
        return self.logs.all()[:limit]  # type: ignore
        

    def __str__(self):
        return f"{self.name} (Lvl {self.level})"
