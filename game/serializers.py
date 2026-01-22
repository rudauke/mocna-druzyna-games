from rest_framework import serializers
from .models import Hero, Item, InventorySlot, Map, Enemy

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

class InventorySlotSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    
    class Meta:
        model = InventorySlot
        fields = ['id', 'item', 'is_equipped']

class EnemySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enemy
        fields = ['id', 'type', 'hp', 'x', 'y']

class MapSerializer(serializers.ModelSerializer):
    enemies = EnemySerializer(many=True, read_only=True)
    
    class Meta:
        model = Map
        fields = ['level_number', 'layout_data', 'enemies']

class MoveActionSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=["NORTH", "SOUTH", "EAST", "WEST"])

class ShopBuySerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
