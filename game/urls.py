from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, HeroViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename = 'item'),
router.register(r'heros', HeroViewSet, basename = 'hero')

urlpatterns = [
    path('', include(router.urls)),
]