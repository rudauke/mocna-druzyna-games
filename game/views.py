from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Hero, Item, InventorySlot
from .serializers import HeroSerializer, ItemSerializer, InventorySlotSerializer

class HeroViewSet(viewsets.ModelViewSet):
    serializer_class = HeroSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Hero.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if Hero.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError({"ERROR": "You already have a hero!"})
        
        serializer.save(user=self.request.user)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventorySlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not hasattr(self.request.user, 'hero'):
            return InventorySlot.objects.none()
        return InventorySlot.objects.filter(hero=self.request.user.hero)

    @action(detail=True, methods=['patch'])
    def equip(self, request, pk=None):
        slot = self.get_object()
        slot.is_equipped = True
        slot.save()
        
        return Response({"status": "equipped", "item": slot.item.name})
