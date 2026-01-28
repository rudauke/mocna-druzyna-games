from django.contrib import admin
from .models import Hero, ItemTemplate, ItemInstance, Map, MapTile, Enemy, GameLog

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    pass

@admin.register(ItemTemplate)
class ItemAdmin(admin.ModelAdmin):
    pass

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
