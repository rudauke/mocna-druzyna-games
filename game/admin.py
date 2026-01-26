from django.contrib import admin
from .models import Hero, Item, ItemInInventory, ItemSlot, Map, MapTile, Enemy

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'level', 'hp')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rarity')
    list_filter = ('rarity',) # overkill??
    search_fields = ('name',)

@admin.register(ItemInInventory)
class InventorySlotAdmin(admin.ModelAdmin):
    list_display = ('hero', 'item')
    
@admin.register(ItemSlot)
class ItemSlotAdmin(admin.ModelAdmin):
    list_display = ('hero', 'slot_name', 'item')
    
@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('hero', 'map_level', 'width', 'height')

@admin.register(MapTile)
class MapTileAdmin(admin.ModelAdmin):
    list_display = ('map', 'x', 'y')

@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    list_display = ('type', 'hp', 'map_level')