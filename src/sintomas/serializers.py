from rest_framework import serializers
from .models import Fisico, Humor, Libido, Secrecao
from ciclos.models import Ciclo


class FisicoSerializer(serializers.ModelSerializer):
    ciclo = serializers.PrimaryKeyRelatedField(
        queryset=Ciclo.objects.all(),
        required=False
    )
    ciclo_data = serializers.SerializerMethodField()

    class Meta:
        model = Fisico
        fields = '__all__'

    def get_ciclo_data(self, obj):
        return obj.ciclo.data if obj.ciclo else None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['ciclo_data'] = self.get_ciclo_data(instance)
        return rep


class HumorSerializer(serializers.ModelSerializer):
    ciclo = serializers.PrimaryKeyRelatedField(
        queryset=Ciclo.objects.all(),
        required=False
    )
    ciclo_data = serializers.SerializerMethodField()

    class Meta:
        model = Humor
        fields = '__all__'

    def get_ciclo_data(self, obj):
        return obj.ciclo.data if obj.ciclo else None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['ciclo_data'] = self.get_ciclo_data(instance)
        return rep


class LibidoSerializer(serializers.ModelSerializer):
    ciclo = serializers.PrimaryKeyRelatedField(
        queryset=Ciclo.objects.all(),
        required=False
    )
    ciclo_data = serializers.SerializerMethodField()

    class Meta:
        model = Libido
        fields = '__all__'

    def get_ciclo_data(self, obj):
        return obj.ciclo.data if obj.ciclo else None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['ciclo_data'] = self.get_ciclo_data(instance)
        return rep


class SecrecaoSerializer(serializers.ModelSerializer):
    ciclo = serializers.PrimaryKeyRelatedField(
        queryset=Ciclo.objects.all(),
        required=False
    )
    ciclo_data = serializers.SerializerMethodField()

    class Meta:
        model = Secrecao
        fields = '__all__'

    def get_ciclo_data(self, obj):
        return obj.ciclo.data if obj.ciclo else None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['ciclo_data'] = self.get_ciclo_data(instance)
        return rep
