from django.db import models
from django.contrib.auth.models import User


class Ciclo(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ciclos'
    )
    data = models.DateField()
    dia_menstruada = models.BooleanField()
    duracao_ciclo = models.PositiveIntegerField()
    duracao_menstruacao = models.PositiveIntegerField()
    fluxo_menstrual = models.CharField(
        max_length=20,
        choices=[
            ('LEVE', 'Leve'),
            ('MODERADO', 'Moderado'),
            ('INTENSO', 'Intenso'),
            ('MUITO_INTENSO', 'Muito Intenso'),
        ]
    )

    def __str__(self):
        user = self.usuario
        user_display = (
            getattr(user, 'username', None)
            or getattr(user, 'email', None)
            or str(user.pk)
        )
        return f"Ciclo do usuário {user_display} em {self.data}"

    class Meta:
        db_table = 'ciclo'
