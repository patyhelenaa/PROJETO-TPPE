from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    senha = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    gravidez = models.BooleanField(default=False)
    peso = models.FloatField()

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)

    def __str__(self):
        return self.nome

    def calcular_duracao_media_ciclos(self):
        # O acesso self.ciclos.all() funciona pois Ciclo tem related_name='ciclos'
        ciclos = self.ciclos.all()  # type: ignore
        if not ciclos:
            return 0
        total = sum(c.duracao_ciclo for c in ciclos)
        return total / len(ciclos)

    def prever_proximo_ciclo(self):
        # O acesso self.ciclos.order_by('-data') funciona pois Ciclo tem related_name='ciclos'
        ciclos = self.ciclos.order_by('-data')  # type: ignore
        if not ciclos:
            return None
        ultimo_ciclo = ciclos.first()
        media = self.calcular_duracao_media_ciclos()
        if not media:
            return None
        return ultimo_ciclo.data + timedelta(days=int(media))

    class Meta:
        db_table = 'usuario'
