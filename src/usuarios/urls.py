from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from ciclos.views import CicloViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuario')
router.register(r'ciclos', CicloViewSet, basename='ciclo')

urlpatterns = [
    path('', include(router.urls)),
]
