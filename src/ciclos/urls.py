from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'ciclos', views.CicloViewSet, basename='ciclo')

urlpatterns = [
    path('', include(router.urls)),
] 