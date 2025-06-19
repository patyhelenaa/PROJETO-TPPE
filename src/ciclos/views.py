from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ciclo
from .serializers import CicloSerializer
from usuarios.models import Usuario

class CicloViewSet(viewsets.ModelViewSet):
    serializer_class = CicloSerializer

    def get_queryset(self):
        return Ciclo.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def ultimo(self, request):
        ciclo = self.get_queryset().order_by('-data').first()
        if ciclo:
            return Response(CicloSerializer(ciclo).data)
        return Response({'detail': 'Nenhum ciclo encontrado.'}, status=404)

    @action(detail=False, methods=['get'])
    def previsao(self, request):
        usuario = self.request.user
        data = usuario.prever_proximo_ciclo()
        if data:
            return Response({'previsao_proximo_ciclo': data})
        return Response({'detail': 'Não há dados suficientes para previsão.'}, status=404)

    @action(detail=False, methods=['get'])
    def duracao_media(self, request):
        usuario = self.request.user
        media = usuario.calcular_duracao_media_ciclos()
        return Response({'duracao_media_ciclos': media})
