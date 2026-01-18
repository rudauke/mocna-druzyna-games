from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Hero, Item
from .serializers import HeroSerializer, ItemSerializer

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
        # Jeśli ktoś próbuje POST, PUT, PATCH lub DELETE
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        # Jeśli ktoś tylko ogląda (GET)
        return [permissions.AllowAny()]
