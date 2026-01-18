from django.contrib import admin
from .models import Hero, Item

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'level', 'hp')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rarity', 'damage')
    list_filter = ('rarity',) # overkill??
    search_fields = ('name',)
