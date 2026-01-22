from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, HeroViewSet, InventoryViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename = 'item'),
router.register(r'heros', HeroViewSet, basename = 'hero'),
router.register(r'inventory', InventoryViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]