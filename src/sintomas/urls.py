from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FisicoViewSet, HumorViewSet, LibidoViewSet, SecrecaoViewSet, ChoicesAPIView

router = DefaultRouter()
router.register(r'fisico', FisicoViewSet)
router.register(r'humor', HumorViewSet)
router.register(r'libido', LibidoViewSet)
router.register(r'secrecao', SecrecaoViewSet)

urlpatterns = [
    path('choices/', ChoicesAPIView.as_view(), name='choices'),  
    path('', include(router.urls)),                             
]
