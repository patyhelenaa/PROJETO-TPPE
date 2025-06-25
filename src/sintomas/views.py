from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    Fisico, Humor, Libido, Secrecao, Intensidade, HumorEnum, TexturaSecrecao
)
from .serializers import (
    FisicoSerializer, HumorSerializer, LibidoSerializer, SecrecaoSerializer
)
from ciclos.models import Ciclo
from rest_framework.exceptions import ValidationError


class FisicoViewSet(viewsets.ModelViewSet):
    serializer_class = FisicoSerializer

    def get_queryset(self):
        user = self.request.user
        return Fisico.objects.filter(
            ciclo__usuario_id=getattr(user, 'id', None)
        )

    def perform_create(self, serializer):
        user = self.request.user
        data_sintoma = serializer.validated_data.get('data')
        # Busca o ciclo correspondente à data
        ciclo = Ciclo.objects.filter(
            usuario=user,
            data__lte=data_sintoma
        ).order_by('-data').first()
        if not ciclo:
            raise ValidationError('Não há ciclo correspondente para a data do sintoma.')
        serializer.save(ciclo=ciclo)


class HumorViewSet(viewsets.ModelViewSet):
    serializer_class = HumorSerializer

    def get_queryset(self):
        user = self.request.user
        return Humor.objects.filter(
            ciclo__usuario_id=getattr(user, 'id', None)
        )

    def perform_create(self, serializer):
        user = self.request.user
        data_sintoma = serializer.validated_data.get('data')
        # Busca o ciclo correspondente à data
        ciclo = Ciclo.objects.filter(
            usuario=user,
            data__lte=data_sintoma
        ).order_by('-data').first()
        if not ciclo:
            raise ValidationError('Não há ciclo correspondente para a data do sintoma.')
        serializer.save(ciclo=ciclo)


class LibidoViewSet(viewsets.ModelViewSet):
    serializer_class = LibidoSerializer

    def get_queryset(self):
        user = self.request.user
        return Libido.objects.filter(
            ciclo__usuario_id=getattr(user, 'id', None)
        )

    def perform_create(self, serializer):
        user = self.request.user
        data_sintoma = serializer.validated_data.get('data')
        # Busca o ciclo correspondente à data
        ciclo = Ciclo.objects.filter(
            usuario=user,
            data__lte=data_sintoma
        ).order_by('-data').first()
        if not ciclo:
            raise ValidationError('Não há ciclo correspondente para a data do sintoma.')
        serializer.save(ciclo=ciclo)


class SecrecaoViewSet(viewsets.ModelViewSet):
    serializer_class = SecrecaoSerializer

    def get_queryset(self):
        user = self.request.user
        return Secrecao.objects.filter(
            ciclo__usuario_id=getattr(user, 'id', None)
        )

    def perform_create(self, serializer):
        user = self.request.user
        data_sintoma = serializer.validated_data.get('data')
        # Busca o ciclo correspondente à data
        ciclo = Ciclo.objects.filter(
            usuario=user,
            data__lte=data_sintoma
        ).order_by('-data').first()
        if not ciclo:
            raise ValidationError('Não há ciclo correspondente para a data do sintoma.')
        serializer.save(ciclo=ciclo)


@swagger_auto_schema(
    operation_description=(
        "Obter opções disponíveis para intensidade, humor e textura de "
        "secreção"
    ),
    responses={
        200: openapi.Response(
            description="Opções disponíveis",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'intensidade': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT)
                    ),
                    'humor': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT)
                    ),
                    'textura_secrecao': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT)
                    ),
                }
            )
        )
    }
)
class ChoicesAPIView(APIView):
    def get(self, request):
        return Response({
            "intensidade": [
                {"key": k, "label": v}
                for k, v in Intensidade.choices
            ],
            "humor": [
                {"key": k, "label": v}
                for k, v in HumorEnum.choices
            ],
            "textura_secrecao": [
                {"key": k, "label": v}
                for k, v in TexturaSecrecao.choices
            ],
        })
