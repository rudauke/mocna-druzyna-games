# import random

# from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Hero, Item # InventorySlot, Enemy
from .serializers import (
    HeroSerializer,
    ItemSerializer,
    #InventorySlotSerializer,
    #MoveActionSerializer,
    
)

# teraz nie wiem jakie importy już są nieistotne
# sprawdźmy to potem, teraz nie mam siły

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def hero_list(request): # po prostu obiekt hero (patrz niżej)
    
    if request.method == 'GET':
        hero = Hero.objects.get(user=request.user)
        serializer = HeroSerializer(hero) # bo mamy tylko jeden obiekt jaki może być zwrócony -> lista nie pasuje
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = HeroSerializer(data=request.data)
        
        if Hero.objects.filter(user=request.user).exists():
             raise serializers.ValidationError({"ERROR": "You already have a hero!"}) # jeden gracz -> jeden hero
        
        elif serializer.is_valid(): # kuba sprawdź czy elif tu na pewno pasuje bo ja już nie myślę T^T
            serializer.save(user=request.user) # tu się przypisuje id
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# to-do: usuwanie bohaterów i update??? o ile chcemy dać taką opcję

@api_view(['GET']) # lista wszystkich itemów
@permission_classes([permissions.IsAuthenticated])
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def item_detail(request, pk): # wyświetla jeden konkretny item
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({"ERROR": "No such item."}, status=status.HTTP_404_NOT_FOUND) # jak nie ma itemu

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

# to-do:
# lista, usuwanie, update;
# permissions -> token?
# i nie wiem co jeszcze ale to pewnie nie koniec

# class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = InventorySlotSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         if not hasattr(self.request.user, 'hero'):
#             return InventorySlot.objects.none()
#         return InventorySlot.objects.filter(hero=self.request.user.hero)

#     @action(detail=True, methods=['patch'])
#     def equip(self, request, pk=None):
#         slot = self.get_object()
#         slot.is_equipped = True
#         slot.save()
#
#         return Response({"status": "equipped", "item": slot.item.name})
        
        
