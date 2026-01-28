from django.contrib import admin
from .models import Hero, ItemTemplate, ItemInstance, Map, MapTile, Enemy, GameLog


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'xp', 'level', 'current_hp', 'base_hp', 'base_strength', 'base_defense', 'current_map', 'x_pos', 'y_pos', 'direction')


@admin.register(ItemTemplate)
class  ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'type', 'slot', 'base_strength', 'base_defense', 'base_damage', 'base_hp')


@admin.register(ItemInstance)
class InventorySlotAdmin(admin.ModelAdmin):
    pass
    
@admin.register(GameLog)
class ItemSlotAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    pass

@admin.register(MapTile)
class MapTileAdmin(admin.ModelAdmin):
    pass

@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    pass



