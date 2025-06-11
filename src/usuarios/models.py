from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    gravidez = models.BooleanField(default=False)
    peso = models.FloatField()


    class Meta:
        db_table = 'Usuario'

    def __str__(self):
        return self.nome

