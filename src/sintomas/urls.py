from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FisicoViewSet, HumorViewSet, LibidoViewSet, SecrecaoViewSet, ChoicesAPIView
)


router = DefaultRouter()
router.register(r'fisico', FisicoViewSet, basename='fisico')
router.register(r'humor', HumorViewSet, basename='humor')
router.register(r'libido', LibidoViewSet, basename='libido')
router.register(r'secrecao', SecrecaoViewSet, basename='secrecao')

urlpatterns = [
    path('choices/', ChoicesAPIView.as_view(), name='choices'),
    path('', include(router.urls)),
]
