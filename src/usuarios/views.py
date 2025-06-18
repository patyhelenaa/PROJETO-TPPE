from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Usuario.objects.filter(id=user.id)  # type: ignore
        return Usuario.objects.none()  # type: ignore

    @action(detail=False, methods=['get', 'put', 'patch', 'delete'])
    def me(self, request):
        usuario = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(usuario)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(usuario, data=request.data, partial=(request.method=='PATCH'))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            usuario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

