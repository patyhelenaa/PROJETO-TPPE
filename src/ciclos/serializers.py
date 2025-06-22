from rest_framework import serializers
from .models import Ciclo


class CicloSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ciclo
        fields = [
            'id', 'usuario', 'data', 'dia_menstruada',
            'duracao_ciclo', 'duracao_menstruacao', 'fluxo_menstrual'
        ]
