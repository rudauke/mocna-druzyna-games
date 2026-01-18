from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('game.urls')), # z tego co rozumiem gadamy z game
    path('api-auth/', include('rest_framework.urls')),
]