from rest_framework import serializers

from .models import Hero, ItemTemplate, ItemInstance, Map, MapTile, Enemy, GameLog


class HeroSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Hero
        fields = [
            "id",
            "username",
            "name",
            "hp",
            "max_hp",
            "xp",
            "level",
            "x_pos",
            "y_pos",
        ]
        read_only_fields = ["hp", "max_hp", "xp", "level", "x_pos", "y_pos"]


class ItemTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTemplate


class ItemInstanceSerializer(serializers.ModelSerializer):
    item = ItemTemplateSerializer(read_only=True)

    class Meta:
        model = ItemInstance
        fields = ["id", "item", "quantity"]


class EnemySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enemy
        fields = ["id", "name", "hp", "x", "y"]
        

class MapTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapTile


class MapSerializer(serializers.ModelSerializer):
    enemies = EnemySerializer(many=True, read_only=True)

    class Meta:
        model = Map
        fields = ["level_number", "layout_data", "enemies"]


class GameLogSerializer(serializers.Serializer):
    class Meta:
        model = GameLog


