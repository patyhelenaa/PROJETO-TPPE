from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet
from ciclos.views import CicloViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')



urlpatterns = [
    path('', include(router.urls)),
]
