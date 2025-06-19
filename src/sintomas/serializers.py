from rest_framework import serializers
from .models import Fisico, Humor, Libido, Secrecao

class FisicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fisico
        fields = '__all__'

class HumorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Humor
        fields = '__all__'

class LibidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libido
        fields = '__all__'

class SecrecaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secrecao
        fields = '__all__'
