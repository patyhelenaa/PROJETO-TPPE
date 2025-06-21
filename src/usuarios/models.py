from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    peso = models.FloatField()

    def __str__(self):
        return self.nome
