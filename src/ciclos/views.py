from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Ciclo
from .serializers import CicloSerializer
from .utils import (
    calcular_duracao_media_ciclos, prever_proximo_ciclo,
    calcular_duracao_media_menstruacao
)


class CicloViewSet(viewsets.ModelViewSet):
    serializer_class = CicloSerializer

    def get_queryset(self):
        user = self.request.user
        return Ciclo.objects.filter(usuario_id=getattr(user, 'id', None))

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @swagger_auto_schema(
        method='get',
        operation_description="Obter o último ciclo registrado",
        responses={200: CicloSerializer()}
    )
    @action(detail=False, methods=['get'])
    def ultimo(self, request):
        ultimo_ciclo = self.get_queryset().order_by('-data').first()
        if ultimo_ciclo:
            serializer = self.get_serializer(ultimo_ciclo)
            return Response(serializer.data)
        return Response({'message': 'Nenhum ciclo encontrado'}, status=404)

    @swagger_auto_schema(
        method='get',
        operation_description="Obter previsão do próximo ciclo",
        responses={
            200: openapi.Response(
                description="Previsão calculada",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data_previsao': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format='date'
                        ),
                        'duracao_media': openapi.Schema(
                            type=openapi.TYPE_NUMBER
                        ),
                    }
                )
            ),
            404: openapi.Response(
                description="Dados insuficientes para previsão"
            )
        }
    )
    @action(detail=False, methods=['get'])
    def previsao(self, request):
        usuario = request.user
        previsao = prever_proximo_ciclo(usuario)
        if previsao:
            duracao_media = calcular_duracao_media_ciclos(usuario)
            return Response({
                'data_previsao': previsao.strftime('%Y-%m-%d'),
                'duracao_media': (
                    round(duracao_media)
                    if duracao_media is not None
                    else None
                )
            })
        return Response(
            {'message': 'Dados insuficientes para calcular previsão'},
            status=404
        )

    @swagger_auto_schema(
        method='get',
        operation_description="Obter duração média dos ciclos",
        responses={
            200: openapi.Response(
                description="Duração média calculada",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'duracao_media': openapi.Schema(
                            type=openapi.TYPE_NUMBER
                        ),
                        'total_ciclos': openapi.Schema(
                            type=openapi.TYPE_INTEGER
                        ),
                    }
                )
            )
        }
    )
    @action(detail=False, methods=['get'])
    def duracao_media(self, request):
        usuario = request.user
        ciclos = Ciclo.objects.filter(usuario=usuario)
        duracao_media = calcular_duracao_media_ciclos(usuario)
        duracao_media_menstruacao = calcular_duracao_media_menstruacao(usuario)
        return Response({
            'duracao_media': (
                round(duracao_media)
                if duracao_media is not None
                else None
            ),
            'duracao_media_menstruacao': (
                round(duracao_media_menstruacao)
                if duracao_media_menstruacao is not None
                else None
            ),
            'total_ciclos': ciclos.count()
        })
