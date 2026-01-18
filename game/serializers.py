from rest_framework import serializers
from .models import Hero, Item

class HeroSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Hero
        fields = ['id', 'username', 'name', 'hp', 'max_hp', 'xp', 'level', 'x_pos', 'y_pos']
        read_only_fields = ['hp', 'max_hp', 'xp', 'level', 'x_pos', 'y_pos']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'damage', 'rarity']