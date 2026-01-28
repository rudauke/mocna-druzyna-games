from rest_framework import serializers

from .models import Hero, ItemTemplate, ItemInstance, Map, MapTile, Enemy, GameLog


class ItemTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTemplate
        fields = ["name", "description", "rarity", "type", "slot", 
                  "base_strenght", "base_defense", "base_hp"]


class ItemInstanceSerializer(serializers.ModelSerializer):
    item = ItemTemplateSerializer(read_only=True)
    class Meta:
        model = ItemInstance
        fields = ["id", "item", "quantity", "is_equipped"]


class EnemySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enemy
        fields = ["id", "name", "hp", "damage", "x", "y"]

#serializator do herosów - czyli staty położenie itp (znaczy jak wymyślę to moze bedzie wiecej <3
class HeroInfoSerializer(serializers.ModelSerializer):
    total_strength = serializers.IntegerField(read_only=True) #przywołuje property co są na koncu modeli do wyliczania do herosa
    total_defense = serializers.IntegerField(read_only=True) #przywoływanie sumy, która jest obliczana na bieżąco
    max_hp = serializers.IntegerField(read_only=True) #czyli zapisywane jakby na chwile, zeby potem mi sie ladnie w jasonie wyswietliło
    current_map_level = serializers.IntegerField(source='current_map.map_level', read_only=True) #model hero -> model map -> map lvl
    class Meta:
        model = HeroSerializer
        fields = ["user", "name", "level", "xp", 
                  "current_hp", "max_hp" ,"total_strength", "total_defense", 
                  "current_map", "x_pos", "y_pos", "direction"]
        

# class MapSerializer(serializers.ModelSerializer):
#     enemies = EnemySerializer(many=True, read_only=True)

#     class Meta:
#         model = Map
#         fields = ["map_level"]


class GameLogSerializer(serializers.Serializer):
    class Meta:
        model = GameLog
        fields = ["hero", "message", "created_at"]

class GameStateSerializer(serializers.Serializer):
    hero_info = HeroInfoSerializer(read_only=True)
    inventory = ItemInstanceSerializer(read_only=True)



#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA