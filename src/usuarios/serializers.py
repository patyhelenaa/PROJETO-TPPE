from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha', 'data_nascimento', 'gravidez', 'peso']

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        senha = validated_data.pop('senha', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if senha:
            instance.set_password(senha)
        instance.save()
        return instance
