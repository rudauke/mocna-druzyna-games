from django.contrib import admin
from .models import Hero, Item, InventorySlot, Map, Enemy

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'level', 'hp')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rarity', 'damage')
    list_filter = ('rarity',) # overkill??
    search_fields = ('name',)

@admin.register(InventorySlot)
class InventorySlotAdmin(admin.ModelAdmin):
    list_display = ('hero', 'item', 'is_equipped')

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('hero', 'level_number')

@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    list_display = ('type', 'hp', 'map_level')