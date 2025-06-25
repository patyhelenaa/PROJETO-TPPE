from rest_framework import serializers
from .models import Fisico, Humor, Libido, Secrecao
from ciclos.models import Ciclo


class FisicoSerializer(serializers.ModelSerializer):
    ciclo = serializers.PrimaryKeyRelatedField(queryset=Ciclo.objects.all(), required=False)
    class Meta:
        model = Fisico
        fields = '__all__'


class HumorSerializer(serializers.ModelSerializer):
    ciclo = serializers.PrimaryKeyRelatedField(queryset=Ciclo.objects.all(), required=False)
    class Meta:
        model = Humor
        fields = '__all__'


class LibidoSerializer(serializers.ModelSerializer):
    ciclo = serializers.PrimaryKeyRelatedField(queryset=Ciclo.objects.all(), required=False)
    class Meta:
        model = Libido
        fields = '__all__'


class SecrecaoSerializer(serializers.ModelSerializer):
    ciclo = serializers.PrimaryKeyRelatedField(queryset=Ciclo.objects.all(), required=False)
    class Meta:
        model = Secrecao
        fields = '__all__'
