from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Fisico, Humor, Libido, Secrecao, Intensidade, HumorEnum, TexturaSecrecao
from .serializers import FisicoSerializer, HumorSerializer, LibidoSerializer, SecrecaoSerializer
from ciclos.models import Ciclo


class FisicoViewSet(viewsets.ModelViewSet):
    serializer_class = FisicoSerializer

    def get_queryset(self):
        return Fisico.objects.filter(ciclo__usuario=self.request.user)

    def perform_create(self, serializer):
        ciclo = serializer.validated_data.get('ciclo')
        if ciclo.usuario != self.request.user:
            raise PermissionError('Você só pode adicionar sintomas aos seus próprios ciclos.')
        serializer.save()


class HumorViewSet(viewsets.ModelViewSet):
    serializer_class = HumorSerializer

    def get_queryset(self):
        return Humor.objects.filter(ciclo__usuario=self.request.user)

    def perform_create(self, serializer):
        ciclo = serializer.validated_data.get('ciclo')
        if ciclo.usuario != self.request.user:
            raise PermissionError('Você só pode adicionar sintomas aos seus próprios ciclos.')
        serializer.save()


class LibidoViewSet(viewsets.ModelViewSet):
    serializer_class = LibidoSerializer

    def get_queryset(self):
        return Libido.objects.filter(ciclo__usuario=self.request.user)

    def perform_create(self, serializer):
        ciclo = serializer.validated_data.get('ciclo')
        if ciclo.usuario != self.request.user:
            raise PermissionError('Você só pode adicionar sintomas aos seus próprios ciclos.')
        serializer.save()


class SecrecaoViewSet(viewsets.ModelViewSet):
    serializer_class = SecrecaoSerializer

    def get_queryset(self):
        return Secrecao.objects.filter(ciclo__usuario=self.request.user)

    def perform_create(self, serializer):
        ciclo = serializer.validated_data.get('ciclo')
        if ciclo.usuario != self.request.user:
            raise PermissionError('Você só pode adicionar sintomas aos seus próprios ciclos.')
        serializer.save()


class ChoicesAPIView(APIView):
    def get(self, request):
        return Response({
            "intensidade": [{"key": k, "label": v} for k, v in Intensidade.choices],
            "humor": [{"key": k, "label": v} for k, v in HumorEnum.choices],
            "textura_secrecao": [{"key": k, "label": v} for k, v in TexturaSecrecao.choices],
        })
